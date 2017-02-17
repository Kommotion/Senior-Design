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
import executors
from conversion import ConversionOptions
from tracing import TracingOptions
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from utils import constants
from utils import parsers
from utils import calculators


class Main(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.file_path = os.path.dirname(os.path.realpath(__file__))
        self.root = parent

        self.file = None
        self.conversion_image = None
        self.conversion_map_type = None
        self.custom_imagemagick = None
        self.custom_potrace = None

        self.objects_path = os.path.join(self.file_path, 'objects')
        if not os.path.exists(self.objects_path):
            os.makedirs(self.objects_path)

        self.init_gui()

    def _soft_restart(self):
        """ Soft restart of the program

        This is done by setting the variables to None and disabling widgets
        """
        self.file = None
        self.conversion_image = None
        self.conversion_map_type = '.bmp'
        self.custom_imagemagick = None
        self.custom_potrace = None

        self.tracing_options_button.config(state='disabled')
        self.blender_options_button.config(state='disabled')
        self.conversion_options_button.config(state='disabled')

        self.tracing_start.config(state='disabled')
        self.conversion_start.config(state='disabled')
        self.blender_start.config(state='disabled')

        self.conversion_result_var.set('NOT RUN')
        self.tracing_result_var.set('NOT RUN')
        self.blender_result_var.set('NOT RUN')

        self.conversion_result_label.config(foreground='gray5')
        self.tracing_result_label.config(foreground='gray5')
        self.blender_result_label.config(foreground='gray5')

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
        """ Disables all the start buttons except the primary open file ones """
        self.conversion_options_button.config(state='disabled')
        self.conversion_start.config(state='disabled')
        self.tracing_options_button.config(state='disabled')
        self.tracing_start.config(state='disabled')


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

        self._soft_restart()
        file = os.path.normpath(file)
        self.file = file
        self.file_label.set(file)
        file_type = imghdr.what(self.file)

        if not file_type:
            file_type = self.file.split('.')
            file_type = file_type[len(file_type)-1]

        if file_type not in constants.ACCEPTABLE_FILETYPES:
            messagebox.showerror('Error', 'Wrong Filetype!\n\nAcceptable types: stl, jpg, png')
            self._soft_restart()
            return

        # Enable the next step
        self.conversion_options_button.config(state='normal')
        self.conversion_start.config(state='normal')

    def convert_to_bitmap(self):
        """ Converts the image to bitmap image """
        options = dict()
        options['line'] = self.custom_imagemagick
        options['filetype'] = self.conversion_map_type
        options['filename'] = self.file
        options['filepath'] = self.objects_path
        file_out, result = executors.exec_imagemagick(**options)

        if not result:
            messagebox.showerror('Error', 'There was an error in conversion process!')
            self.conversion_result_var.set('FAILED')
            self.conversion_result_label.config(foreground='red2')
            return

        self.file = file_out
        self.tracing_options_button.config(state='normal')
        self.tracing_start.config(state='normal')

        self.conversion_result_var.set('PASSED')
        self.conversion_result_label.config(foreground='green4')

    def potrace_trace(self):
        """ Uses potrace to trace the bitmap and output to SVG file """
        options = dict()
        options['line'] = self.custom_potrace
        options['filename'] = self.file
        options['filepath'] = self.objects_path
        file_out, result = executors.exec_potrace(**options)

        if not result:
            messagebox.showerror('Error', 'There was an error in tracing process!')
            self.tracing_result_var.set('FAILED')
            self.tracing_result_label.config('red2')
            return

        self.file = file_out
        self.blender_options_button.config(state='normal')
        self.blender_start.config(state='normal')

        self.tracing_result_var.set('PASSED')
        self.tracing_result_label.config(foreground='green4')

    def bit_conversion_options(self):
        """ Brings up the conversion options menu for bitmap tracing

        Parses the results and readies for imagemagick conversion subprocess call
        """
        con_opts = ConversionOptions(self.root, self.conversion_map_type)
        self.wait_window(con_opts.top)
        options = con_opts.get()
        if not options['changed']:
            return

        self.conversion_map_type = parsers.conversion(options, 'filetype')
        self.custom_imagemagick = parsers.conversion(options, 'imagemagick')

    def tracing_options(self):
        """ Brings up the tracing menu for tracing

        Parses the results and readies for potrace output
        """
        tracing_opts = TracingOptions(self.root)
        self.wait_window(tracing_opts.top)
        options = tracing_opts.get()
        if not options['changed']:
            return

        self.custom_potrace = parsers.conversion(options, 'potrace')

    def blender_options(self):
        """ Brings up the blender menu options for STL conversion

        Parses the results and readies for blender conversion
        """
        pass

    def init_gui(self):
        """ Initializes the GUI and all the widgets

        Tkinter's Grid geometry manager is used instead of pack
        """
        geo = calculators.center(self.root, 800, 500)
        self.root.geometry(geo)
        self.root.title('3D Laser Etcher')
        self.root.wm_iconbitmap(self.file_path + r'\ucf.ico')
        self.root.option_add('*tearOff', 'FALSE')

        # layout all of the main containers
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

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
        self.open_file_frame = ttk.Frame(self.root, width=200, height=10)
        self.open_file_frame.grid(row=0, column=0, sticky='NW')

        select_file = 'Select File (Image file or STL file)'
        self.step_1_label = ttk.Label(self.open_file_frame, text='Step 1:', anchor=tkinter.W)
        self.step_1_label.grid(padx=5, sticky=tkinter.W)

        self.open_file_label = ttk.Label(self.open_file_frame, text=select_file, anchor=tkinter.W)
        self.open_file_label.grid(row=1, sticky=tkinter.W, pady=5, padx=5)

        self.open_file_button = ttk.Button(self.open_file_frame, text='Browse', command=self.choose_file)
        self.open_file_button.grid(row=2, column=2, padx=5)

        self.file_label = tkinter.StringVar()
        self.open_file_entry = ttk.Entry(self.open_file_frame, textvariable=self.file_label, width=50, justify='left', state='readonly')
        self.open_file_entry.grid(row=2, column=0, sticky=tkinter.W, padx=5)

        self.separator_1 = ttk.Separator(self.open_file_frame, orient=tkinter.HORIZONTAL)
        self.separator_1.grid(row=3, padx=5, pady=15, sticky='we', columnspan=5)
        # ------------------------- #

        # ---- 2D to 3D conversion widgets ---- #

        # Bitmap Conversion
        self.conversion_frame = ttk.Frame(self.root, width=200, height=50)
        self.conversion_frame.grid(row=1, column=0, sticky='NW')

        self.step_2_label = ttk.Label(self.conversion_frame, text='Step 2:', anchor=tkinter.W)
        self.step_2_label.grid(row=0, padx=5, sticky=tkinter.W)

        self.conversion_label = ttk.Label(self.conversion_frame, text='Bitmap Conversion', anchor=tkinter.W)
        self.conversion_label.grid(row=1, padx=5, pady=5, sticky=tkinter.W, columnspan=2)

        self.conversion_options_button = ttk.Button(self.conversion_frame, text='Options',
                                                    command=self.bit_conversion_options, state=tkinter.DISABLED)
        self.conversion_options_button.grid(row=2, padx=5, pady=5, sticky=tkinter.W)
        self.conversion_map_type = '.bmp'

        self.conversion_start = ttk.Button(self.conversion_frame, text='Start', command=self.convert_to_bitmap,
                                           state=tkinter.DISABLED)
        self.conversion_start.grid(row=2, column=1, padx=5, pady=5)

        # Tracing
        self.tracing_label = ttk.Label(self.conversion_frame, text='Bitmap Tracing', anchor=tkinter.W)
        self.tracing_label.grid(row=3, padx=5, pady=5, sticky=tkinter.W, columnspan=2)

        self.tracing_options_button = ttk.Button(self.conversion_frame, text='Options', command=self.tracing_options,
                                                 state=tkinter.DISABLED)
        self.tracing_options_button.grid(row=4, padx=5, pady=5, sticky=tkinter.W)

        self.tracing_start = ttk.Button(self.conversion_frame, text='Start', command=self.potrace_trace,
                                        state=tkinter.DISABLED)
        self.tracing_start.grid(row=4, column=1, padx=5, pady=5)

        # STL conversion
        self.blender_label = ttk.Label(self.conversion_frame, text='STL conversion', anchor=tkinter.W)
        self.blender_label.grid(row=5, padx=5, pady=5, sticky=tkinter.W, columnspan=2)

        self.blender_options_button = ttk.Button(self.conversion_frame, text='Options', command=self.tracing_options,
                                                  state=tkinter.DISABLED)
        self.blender_options_button.grid(row=6, padx=5, pady=5, sticky=tkinter.W)

        self.blender_start = ttk.Button(self.conversion_frame, text='Start', command=self.potrace_trace,
                                         state=tkinter.DISABLED)
        self.blender_start.grid(row=6, column=1, padx=5, pady=5)

        self.separator_1 = ttk.Separator(self.conversion_frame, orient=tkinter.HORIZONTAL)
        self.separator_1.grid(row=7, padx=5, pady=15, sticky='we', columnspan=10)

        self.conversion_frame.grid_columnconfigure(5, minsize=30)
        self.conversion_frame.grid_columnconfigure(2, minsize=65)

        # Conversion result widgets
        results_widgets = list()

        self.conversion_result_var = tkinter.StringVar()
        self.conversion_result_label = ttk.Label(self.conversion_frame, textvariable=self.conversion_result_var, anchor=tkinter.CENTER,
                                                 background='gray60', width=20)
        results_widgets.append(self.conversion_result_label)
        self.conversion_result_var.set('NOT RUN')

        self.tracing_result_var = tkinter.StringVar()
        self.tracing_result_label = ttk.Label(self.conversion_frame, textvariable=self.tracing_result_var, anchor=tkinter.CENTER,
                                              background='gray60', width=20)
        results_widgets.append(self.tracing_result_label)
        self.tracing_result_var.set('NOT RUN')

        self.blender_result_var = tkinter.StringVar()
        self.blender_result_label = ttk.Label(self.conversion_frame, textvariable=self.blender_result_var, anchor=tkinter.CENTER,
                                              background='gray60', width=20)
        results_widgets.append(self.blender_result_label)
        self.blender_result_var.set('NOT RUN')

        row = 2
        for label in results_widgets:
            label.grid(row=row, column=3, padx=5, pady=5)
            row += 2

        for child in self.winfo_children():
            child.grid_configure()


if __name__ == '__main__':
    root = tkinter.Tk()
    Main(root)
    root.mainloop()
