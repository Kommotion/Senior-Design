"""
   Copyright 2017 Nicolas Ramirez

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import tkinter
import os
import imghdr
from tkinter import ttk
from tkinter import filedialog
from utils import constants


class Main(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.file_path = os.path.dirname(os.path.realpath(__file__))
        self.file = None
        self.root = parent
        self.init_gui()

    def _quit(self):
        """ Terminates the program """
        quit()

    def _show_copyrights(self):
        """ Shows copyright dialogues for all software included """
        # TODO
        # Show all the copyrights and credits for software used
        pass

    def _choose_file(self):
        """ Handles the open file button """
        file = filedialog.askopenfilename(initialdir=self.file_path, filetypes=constants.FILE_EXTENSIONS)

        if not file:
            return

        self.file_path = file
        self.file = file
        self.file_label.set(file)
        file_type = imghdr.what(self.file)

        if not file_type:
            file_type = self.file.split('.')
            file_type = file_type[len(file_type)-1]

        if file_type not in constants.ACCEPTABLE_FILETYPES:
            print('not in acceptable filetypes')
            # TODO
            # Disable all GUI compomnents
            # Alert user invalid filetype

        # TODO
        # Passes all checks
        # Enable all next step

    def init_gui(self):
        """ Initializes the GUI """
        self.root.geometry('800x500')
        self.root.title('3D Laser Etcher')
        self.root.wm_iconbitmap(self.file_path + r'\ucf.ico')
        self.root.option_add('*tearOff', 'FALSE')

        # ------- menubar ------- #
        self.menubar = tkinter.Menu(self.root)

        self.menu_file = tkinter.Menu(self.menubar)
        self.menu_file.add_command(label='Exit', command=self._quit)

        self.menu_edit = tkinter.Menu(self.menubar)

        self.menu_help = tkinter.Menu(self.menubar)
        self.menu_help.add_command(label='Copyrights', command=self._show_copyrights)

        self.menubar.add_cascade(menu=self.menu_file, label='File')
        self.menubar.add_cascade(menu=self.menu_edit, label='Edit')
        self.menubar.add_cascade(menu=self.menu_help, label='Help')

        self.root.config(menu=self.menubar)
        # ------------------------- #

        # --- Open file widgets --- #
        select_file = 'Select File (Image file or STL file)'
        self.open_file_label = ttk.Label(text=select_file, anchor=tkinter.W)
        self.open_file_label.grid(row=0, column=0, sticky=tkinter.W, pady=5, padx=5)

        self.open_file_button = ttk.Button(text='Browse', command=self._choose_file, width=7)
        self.open_file_button.grid(row=1, column=2, padx=5)

        self.file_label = tkinter.StringVar()
        self.open_file_entry = ttk.Entry(textvariable=self.file_label, width=50, justify='left', state='readonly')
        self.open_file_entry.grid(row=1, column=0, sticky=tkinter.W, padx=5)
        # ------------------------- #

        for child in self.winfo_children():
            child.grid_configure()


if __name__ == '__main__':
    root = tkinter.Tk()
    Main(root)
    root.mainloop()
