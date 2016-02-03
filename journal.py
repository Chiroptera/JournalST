import sublime, sublime_plugin, time
import os.path
from config import *


# def plugin_loaded():
#     '''called directly from sublime on plugin load
#     '''

#     global JOURNAL_DIR 


#     settings = sublime.load_settings('Journal.sublime-settings')
#     JOURNAL_FOLDER = settings.get('journal_dir')

#      if JOURNAL_FOLDER is None or JOURNAL_FOLDER == '' or not os.path.isfile(JOURNAL_FOLDER):
#         sublime.status_message('WARNING: No journal directory path configured for Journal.')

#     refresh_caches()

# def plugin_loaded():
#     """Called directly from sublime on plugin load
#     """
#     global JOURNAL_PATH
#     global EVERNOTE

#     settings = sublime.load_settings('Citer.sublime-settings')
#     JOURNAL_PATH = settings.get('journal_path')
#     if not os.path.exist(JOURNAL_PATH):
#         raise Exception("Path not found: {}".format(JOURNAL_PATH))
#     EVERNOTE = settings.get('use_evernote')

#     refresh_caches()

class InsertDateCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sel = self.view.sel();
        for s in sel:
            self.view.replace(edit, s, time.strftime('%d-%m-%Y'))

class InsertTimeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sel = self.view.sel()
        for s in sel:
            self.view.replace(edit, s, time.strftime('%Hh%M'))

class PromptJournalEntryCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.meta = dict()
        self.asktag()

    def asktag(self):
        self.window.show_input_panel('tag (comma separated):', '', self.asktag_done, None, None)

    def asktag_done(self, tag):
        try:
            self.meta['tag'] = tag
        except ValueError:
            pass

        self.askloc()

    def askloc(self):
        self.window.show_input_panel('location:', '', self.askloc_done, None, None)

    def askloc_done(self, loc):
        try:
            self.meta['loc'] = loc        
        except ValueError:
            pass

        self.on_exit()

    def on_exit(self):
        try:
            if self.window.active_view():
                self.window.active_view().run_command('insert_journal_entry', self.meta )
        except ValueError:
            pass 

class InsertJournalEntryCommand(sublime_plugin.TextCommand):

    def run(self, edit, **meta):
        entryString = '---\n'
        entryString += 'date: {}\n'.format(time.strftime('%d-%m-%Y'))
        entryString += 'time: \n'.format(time.strftime('%H-%M'))
        entryString += 'tag: {}\n'.format(meta['tag'])
        #entryString += 'location: {}\n'.format(loc)
        entryString += '---\n'

        pos = self.view.sel()[0].begin()

        self.view.insert(edit, pos, entryString)
        pass


class PromptJournalFilenameCommand(sublime_plugin.WindowCommand):
    def run(self):
        filename = '{}.md'.format(time.strftime('%d-%m-%Y'))
        self.window.show_input_panel('filename:', filename, self.on_done, None, None)
        pass

    def on_done(self, filename):
        if not os.path.isfile(FOLDER+filename):
            # save file
            newFile = open(FOLDER + filename, 'w')
            newFile.close()
            
        self.window.open_file(FOLDER + filename)
