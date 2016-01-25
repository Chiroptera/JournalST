import sublime, sublime_plugin, time
import os.path

"""
TODO:
- prompt for location

"""

JOURNAL_PATH = "/home/chiroptera/Dropbox/journal/"
EVERNOTE = True # enables metadata for using entry as a Evernote note; to be used with Evernote package

# def plugin_loaded():
#     """Called directly from sublime on plugin load
#     """

#     global JOURNAL_DIR 


#     settings = sublime.load_settings('Journal.sublime-settings')
#     JOURNAL_FOLDER = settings.get('journal_dir')

#      if JOURNAL_FOLDER is None or JOURNAL_FOLDER == '' or not os.path.isfile(JOURNAL_FOLDER):
#         sublime.status_message("WARNING: No journal directory path configured for Journal.")

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
            self.view.replace(edit, s, time.strftime("%d-%m-%Y"))

class InsertTimeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sel = self.view.sel()
        for s in sel:
            self.view.replace(edit, s, time.strftime("%Hh%M"))


global ENTRY_TAGS
global ENTRY_NOBTEBOOK
global ENTRY_NAME

class PromptJournalEntryCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel("tags:", "", self.on_done, None, None)
        pass

    def on_done(self, tags):
        try:
            if self.window.active_view():
                self.window.active_view().run_command("insert_journal_entry", {"tags": tags} )
        except ValueError:
            pass

class PromptLocationCommand(sublime_plugin.WindowCommand):
    def run(self,tags):
        self.tags = tags
        self.window.show_input_panel("location:", "", self.on_done, None, None)
        pass

    def on_done(self, loc):
        try:
            if self.window.active_view():
                self.window.active_view().run_command("insert_journal_entry", {"tags": self.tags, "loc": loc} )
        except ValueError:
            pass

class InsertJournalEntryCommand(sublime_plugin.TextCommand):

    def run(self, edit, tags):
        entryString = "---" + '\n'
        if EVERNOTE:
            entryString += "title:" + '\n'
            entryString += "notebook:" + '\n'

        entryString += "date:" + time.strftime("%d-%m-%Y") + '\n'
        entryString += "time:" + '\n'
        entryString += "tag:" + tags + '\n'
        #entryString += "location:" + loc + '\n'
        entryString += "---" + '\n'

        pos = self.view.sel()[0].begin()

        self.view.insert(edit, pos, entryString)
        pass


class PromptJournalFilenameCommand(sublime_plugin.WindowCommand):
    def run(self):
        filename = time.strftime("%d-%m-%Y") + ".md"
        self.window.show_input_panel("filename:", filename, self.on_done, None, None)
        pass

    def on_done(self, filename):
        if not os.path.isfile(FOLDER+filename):
            # save file
            newFile = open(FOLDER + filename, 'w')
            newFile.close()
            
        self.window.open_file(FOLDER + filename)
