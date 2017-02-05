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
from conversion import ConversionOptions
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from utils import constants
from utils import parsers


class Main(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.file_path = os.path.dirname(os.path.realpath(__file__))
        self.file = None
        self.conversion_image = None
        self.root = parent
        self.init_gui()

    def _quit(self):
        """ Terminates the program """
        quit()

    def show_copyrights(self):
        """ Shows copyright dialogues for all software included """
        # TODO
        # Show all the copyrights and credits for software used
        pass

    def enable_widgets(self, filetype):
        """ Enables the widgets based on the filetype given

        A regular raster image will enable the next step in 2D-3D conversion
        A STL file will skip the 2D-3D conversion and enable the slicing widget

        :param filetype: The file extension from the openfile menu
        :return:
        """
        # TODO
        # Parse filetype and determine which widgets
        # to enable

    def disable_widgets(self):
        """ Disables all the widgets except the primary open file ones """
        # TODO
        # Disable all the widgets

    def choose_file(self):
        """ Handles the open file button and the given file

        This method tests to make sure that the given file is a 2D raster image,
        however it will not test that the given STL file is valid. It will be
        assumed that the given STL file is valid, otherwise unknown consequences
        will occur on the user - program failure
        """
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
            messagebox.showerror('Error', 'Wrong Filetype!\n\nAcceptable types: stl, jpg, png')
            self.disable_widgets()

        self.enable_widgets(file_type)

    def convert_to_bitmap(self):
        """ Converts the image to bitmap image """

    def bit_conversion_options(self):
        """ Brings up the conversion options menu for bitmap tracing

        Parses the results and readies for potrace conversion subprocess call
        """
        con_opts = ConversionOptions(self.root, self.conversion_map_type)
        self.wait_window(con_opts.top)
        options = con_opts.get()
        if not options['changed']:
            return

        self.conversion_map_type = parsers.conversion(options, 'filetype')
        self.custom_potrace = parsers.conversion(options, 'potrace')
        print(self.conversion_map_type)
        print(self.custom_potrace)

    def init_gui(self):
        """ Initializes the GUI and all the widgets

        Tkinter's Grid geometry manager is used instead of pack
        """
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
        self.menu_help.add_command(label='Copyrights', command=self.show_copyrights)

        self.menubar.add_cascade(menu=self.menu_file, label='File')
        self.menubar.add_cascade(menu=self.menu_edit, label='Edit')
        self.menubar.add_cascade(menu=self.menu_help, label='Help')

        self.root.config(menu=self.menubar)
        # ------------------------- #

        # --- Open file widgets --- #
        select_file = 'Select File (Image file or STL file)'
        self.step_1_label = ttk.Label(text='Step 1:', anchor=tkinter.W)
        self.step_1_label.grid(padx=5, sticky=tkinter.W)

        self.open_file_label = ttk.Label(text=select_file, anchor=tkinter.W)
        self.open_file_label.grid(row=1, sticky=tkinter.W, pady=5, padx=5)

        self.open_file_button = ttk.Button(text='Browse', command=self.choose_file)
        self.open_file_button.grid(row=2, column=2, padx=5)

        self.file_label = tkinter.StringVar()
        self.open_file_entry = ttk.Entry(textvariable=self.file_label, width=50, justify='left', state='readonly')
        self.open_file_entry.grid(row=2, column=0, sticky=tkinter.W, padx=5)
        # ------------------------- #

        self.separator_1 = ttk.Separator(orient=tkinter.HORIZONTAL, )
        self.separator_1.grid(row=3, padx=5, pady=15, sticky='we', columnspan=5)

        # ---- 2D to 3D conversion widgets ---- #
        self.step_2_label = ttk.Label(text='Step 2:', anchor=tkinter.W)
        self.step_2_label.grid(row=4, padx=5, sticky=tkinter.W)

        self.conversion_label = ttk.Label(text='Bitmap Tracing', anchor=tkinter.W)
        self.conversion_label.grid(padx=5, pady=5, sticky=tkinter.W)

        self.conversion_options_button = ttk.Button(text='Options', command=self.bit_conversion_options)
        self.conversion_options_button.grid(padx=5, pady=5, sticky=tkinter.W)
        self.conversion_map_type = '.bmp'

        #self.conversion_radios = dict()

        # for text, mode in constants.CONVERSION_MODES:
        #     button = ttk.Radiobutton(text=text, variable=self.conversion_map_type, value=mode)
        #     button.grid(sticky=tkinter.W, padx=5)
        #     self.conversion_radios[text] = button

        for child in self.winfo_children():
            child.grid_configure()


if __name__ == '__main__':
    root = tkinter.Tk()
    Main(root)
    root.mainloop()
