import sublime, sublime_plugin, time
import os.path

def plugin_loaded():
    """Called directly from sublime on plugin load
    """
    global JOURNAL_PATH

    settings = sublime.load_settings('journal.sublime-settings')

    JOURNAL_PATH = settings.get('journal_path')
    print('journal_path setting: {}'.format(JOURNAL_PATH))
    # sublime.status_message('journal_path setting: {}'.format(JOURNAL_PATH))

    if not os.path.exists(JOURNAL_PATH):
        sublime.status_message('No journal directory path configured for Journal. Use the "Preferences: JournalST - User" command to set it.')
        sublime.error_message('No journal directory path configured for Journal. Use the "Preferences: JournalST - User" command to set it.')

class InsertDateCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sel = self.view.sel();
        for s in sel:
            self.view.replace(edit, s, time.strftime('%d-%m-%Y'))

class InsertTimeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sel = self.view.sel()
        for s in sel:
            self.view.replace(edit, s, time.strftime('%H:%M'))

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
        entryString += 'time: {}\n'.format(time.strftime('%H:%M'))
        if meta['tag'] is not '':
            entryString += 'tag: {}\n'.format(meta['tag'])
        if meta['loc'] is not '':
            entryString += 'location: {}\n'.format(meta['loc'])
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
        if not os.path.exists(JOURNAL_PATH):
            sublime.status_message('Configured journal path does not exist. Use the "Preferences: JournalST - User" command to set a valid path.')
            sublime.error_message('Configured journal path does not exist. Use the "Preferences: JournalST - User" command to set a valid path.')
            return

        file_path = os.path.join(JOURNAL_PATH, filename)
        # create file if it does not exist
        if not os.path.isfile(file_path):
            newFile = open(file_path, 'w')
            newFile.close()
            
        self.window.open_file(file_path)