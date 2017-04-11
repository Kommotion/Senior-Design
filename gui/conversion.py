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
from tkinter import messagebox
from utils import constants
from utils import calculators


class ConversionOptions:
    """ Class for the Bitmap conversion options """

    def __init__(self, parent, conversion_type, negate):
        self.top = tkinter.Toplevel(parent)
        self._file_path = os.path.dirname(os.path.realpath(__file__))
        self._conversion_map_type = tkinter.StringVar()
        self._conversion_map_type.set(conversion_type)
        self._conversion_radios = dict()
        self._options = dict()
        self._options['changed'] = False
        self._custom_imagemagick = tkinter.StringVar()
        self._negate = tkinter.BooleanVar()
        self._negate.set(negate)
        self._init_gui()

    def get(self):
        """ Returns the options """
        return self._options

    def _save_options(self):
        """ Sets all the options and saves into a dict """
        self._options['changed'] = True
        self._options['filetype'] = self._conversion_map_type
        self._options['imagemagick'] = self._custom_imagemagick
        self._options['negate'] = self._negate
        self._quit()

    def _quit(self):
        """ Destroys this Toplevel widget """
        self.top.destroy()

    def _init_gui(self):
        """ Initializes all the widgets """
        self.top.grab_set()
        geo = calculators.center(self.top.master, 425, 175)
        self.top.geometry(geo)
        self.top.title('Conversion Options')
        self.top.resizable(height=False, width=False)
        self.top.wm_iconbitmap(self._file_path + r'\ucf.ico')
        self.top.grid_columnconfigure(1, weight=1)

        label = 'Bitmap filetype:\t   Custom command line:'
        self.output_label = ttk.Label(self.top, text=label, anchor=tkinter.W)
        self.output_label.grid(padx=5, pady=5, columnspan=10, sticky=tkinter.W)

        row = 0
        for text, mode in constants.CONVERSION_MODES:
            row += 1
            button = ttk.Radiobutton(self.top, text=text, variable=self._conversion_map_type, value=mode)
            button.grid(row=row, sticky=tkinter.W, padx=5)
            self._conversion_radios[text] = button

        self.save_button = ttk.Button(self.top, text='Save', command=self._save_options)
        self.save_button.grid(row=6, padx=5, pady=5, sticky=tkinter.W)

        self.cancel_button = ttk.Button(self.top, text='Cancel', command=self._quit)
        self.cancel_button.grid(row=6, column=1, padx=5, pady=5, sticky=tkinter.E)

        self.custom_entry = ttk.Entry(self.top, textvariable=self._custom_imagemagick, width=50)
        self.custom_entry.grid(row=1, column=1, columnspan=15, padx=5, sticky=tkinter.E)

        self.negate_box = ttk.Checkbutton(self.top, text='Invert Image', variable=self._negate)
        self.negate_box.grid(row=5, padx=5, pady=5, sticky=tkinter.W)

        label = 'Warning: Only change the command line option ' \
                'if you know what you\'re doing. This adds on ' \
                'to end of the convert command so there is no ' \
                'need to specify input and output files.'
        self.warning_label = ttk.Label(self.top, text=label, wraplength=300, justify='left')
        self.warning_label.grid(row=2, column=1, rowspan=3)


class StlOptions:
    """ Class for STL conversion options """

    def __init__(self, parent, extrusion_depth):
        self.top = tkinter.Toplevel(parent)
        self._file_path = os.path.dirname(os.path.realpath(__file__))
        self._options = dict()
        self._options['changed'] = False
        self.extrusion_depth = tkinter.StringVar()
        self.extrusion_depth.set(extrusion_depth)
        self._init_gui()

    def get(self):
        """ Returns the options """
        return self._options

    def _check_boundaries(self):
        """ Checks to make sure that the given extrusion depth is within the boundaries

        The current boundaries at 1 and 10
        """
        depth = self.extrusion_depth.get()

        try:
            depth = float(depth)
        except ValueError:
            return False

        return True if 1 <= depth <= 10 else False

    def _save_options(self):
        """ Sets all the options and saves into a dict """
        if not self._check_boundaries():
            messagebox.showerror('Error', 'Extrusion must be a number between 1 and 10')
            return

        self._options['changed'] = True
        self._options['extrusion'] = self.extrusion_depth
        self._quit()

    def _quit(self):
        """ Destroys this Toplevel widget """
        self.top.destroy()

    def _init_gui(self):
        """ Initializes all the widgets """
        self.top.grab_set()
        geo = calculators.center(self.top.master, 200, 100)
        self.top.geometry(geo)
        self.top.title('STL')
        self.top.resizable(height=False, width=False)
        self.top.wm_iconbitmap(self._file_path + r'\ucf.ico')
        self.top.grid_columnconfigure(1, weight=1)

        label = 'Extrusion Depth:'
        self.output_label = ttk.Label(self.top, text=label, anchor=tkinter.W)
        self.output_label.grid(padx=5, pady=5, sticky=tkinter.W, columnspan=2)

        self.custom_entry = ttk.Entry(self.top, textvariable=self.extrusion_depth, width=30)
        self.custom_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tkinter.W)

        self.save_button = ttk.Button(self.top, text='Save', width=15, command=self._save_options)
        self.save_button.grid(row=2, padx=5, pady=5, sticky=tkinter.W)

        self.cancel_button = ttk.Button(self.top, text='Cancel', width=15, command=self._quit)
        self.cancel_button.grid(row=2, column=1, padx=5, pady=5, sticky=tkinter.W)

