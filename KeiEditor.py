import os, webview

class KeiEditor():
    window = None
    file_name = None

    def on_closing(self):
        self.window.destroy()

    def open_file_dialog(self):
        file_types = ('HTML Files (*.html;*.htm)', 'All files (*.*)')
        file_name = self.window.create_file_dialog(webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types)[0]
        if file_name != None:
            file = open(file_name, "r")
            self.window.evaluate_js('document.getElementById("keieditable").outerHTML = (String.raw`' +
                                    file.read().replace('`', '&#96;') + '`);')

    def save_file(self):
        keieditable = self.window.dom.get_elements('#keieditable')
        file = open(self.file_name, "w") 
        file.write(keieditable[0].node['outerHTML'])

    def save_as_file_dialog(self):
        file_types = ('HTML Files (*.html;*.htm)', 'All files (*.*)')
        self.file_name = self.window.create_file_dialog(webview.SAVE_DIALOG, allow_multiple=False, 
                                                        save_filename='', file_types=file_types)[0]
        if self.file_name != None:
            if os.path.isfile(self.file_name):
                result = self.window.create_confirmation_dialog('Question', 'Overwrite Existing File?')
                if not result:
                    self.file_name = None;
                    return
            self.save_file()

    def save_file_dialog(self):
        if self.file_name != None:
            self.save_file()
        else:
            self.save_as_file_dialog()

    def __init__(self):
        self.window = webview.create_window('Kei HTML Editor', url='./index.html', confirm_close=True)
        self.window.expose(self.on_closing)
        self.window.expose(self.open_file_dialog)
        self.window.expose(self.save_file_dialog)
        self.window.expose(self.save_as_file_dialog)
        webview.start()

keiEditor = KeiEditor()
