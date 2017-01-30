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
from tkinter import ttk
from tkinter import filedialog

file_path = os.path.dirname(os.path.realpath(__file__))


class Main(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
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
        """ Chooses the file and stuff"""
        file = filedialog.askopenfilename(initialdir=file_path)

        self.file = file

    def init_gui(self):
        self.root.geometry('800x500')
        self.root.title('3D Laser Etcher')
        self.root.wm_iconbitmap(file_path + r'\ucf.ico')
        self.root.option_add('*tearOff', 'FALSE')

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

        file = filedialog.askopenfilename(initialdir=file_path)




if __name__ == '__main__':
    root = tkinter.Tk()
    Main(root)
    root.mainloop()
