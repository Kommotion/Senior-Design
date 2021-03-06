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
import serials
import fileinput
import sys
# from copyrights import CopyrightText
from conversion import ConversionOptions
from conversion import StlOptions
from tracing import TracingOptions
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from utils import constants
from utils import parsers
from utils import calculators
# from tempfile import mkstemp
# from shutil import move
# from os import remove, close
#from utils import point
from PIL import Image, ImageTk


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
        self.image = None
        self.negate = True
        self.extrusion_depth = 2.0

        self.objects_path = os.path.join(self.file_path, 'objects')
        if not os.path.exists(self.objects_path):
            os.makedirs(self.objects_path)

        self.x = tkinter.DoubleVar()
        self.y = tkinter.DoubleVar()
        self.z = tkinter.DoubleVar()
        self.x.set(2.75)
        self.y.set(2.75)
        self.z.set(2.75)

        self.device_path = None

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
        self.negate = True
        self.extrusion_depth = 2.0
        self.device_path = None

        self.canvas.delete(self.image)
        self.image = None
        self.canvas_button.lower(self.canvas)

        self.tracing_options_button.config(state='disabled')
        self.stl_options_button.config(state='disabled')
        self.conversion_options_button.config(state='disabled')
        self.slicing_options_button.config(state='disabled')

        self.tracing_start.config(state='disabled')
        self.conversion_start.config(state='disabled')
        self.stl_start.config(state='disabled')
        self.slicing_start_button.config(state='disabled')

        self.conversion_result_var.set('NOT RUN')
        self.tracing_result_var.set('NOT RUN')
        self.stl_result_var.set('NOT RUN')
        self.slicing_result_var.set('NOT RUN')

        self.conversion_result_label.config(foreground='gray5')
        self.tracing_result_label.config(foreground='gray5')
        self.stl_result_label.config(foreground='gray5')
        self.slicing_result_label.config(foreground='gray5')

        self.current_x_entry.config(state='disabled')
        self.current_y_entry.config(state='disabled')
        self.current_z_entry.config(state='disabled')
        self.test_connections_button.config(state='disabled')
        self.etching_start.config(state='disabled')

        self.current_x_entry.config(state='disabled')
        self.current_y_entry.config(state='disabled')
        self.current_z_entry.config(state='disabled')
        self.x.set(2.75)
        self.y.set(2.75)
        self.z.set(2.75)

    def _quit(self):
        """ Terminates the program """
        quit()

    def _update_image(self):
        """ Displays an image within the canvas """
        try:
            image = Image.open(self.file)
        except Exception as e:
            self.canvas.delete(self.image)
            self.image = None
            self.canvas_button.lift(self.canvas)
            return

        image = image.resize((250, 250), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(image)
        self.canvas.create_image(150, 150, image=self.image)

    def show_copyrights(self):
        """ Shows copyright dialogues for all software included """
        curr_dic = os.path.dirname(os.path.realpath(__file__))[:-3]
        curr_dic = os.path.join(curr_dic, 'COPYRIGHTS.txt')
        os.startfile(curr_dic)

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
        self.file_path = file
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

        # Enable the next step, Slicing if STL file
        if file_type == 'stl':
            #self.slicing_options_button.config(state='normal')
            self.slicing_start_button.config(state='normal')
            self.current_z_entry.config(state='normal')
            self.current_y_entry.config(state='normal')
            self.current_x_entry.config(state='normal')
        elif file_type == 'gcode':
            self.test_connections_button.config(state='normal')
        else:
            self.conversion_options_button.config(state='normal')
            self.conversion_start.config(state='normal')

        self._update_image()

    def convert_to_bitmap(self):
        """ Converts the image to bitmap image """
        options = dict()
        options['line'] = self.custom_imagemagick
        options['filetype'] = self.conversion_map_type
        options['filename'] = self.file
        options['filepath'] = self.objects_path
        options['negate'] = self.negate
        file_out, result = executors.exec_imagemagick(**options)

        if not result:
            messagebox.showerror('Error', 'There was an error in conversion process!')
            self.conversion_result_var.set('FAILED')
            self.conversion_result_label.config(foreground='red2')
            return

        self.file = file_out
        self.tracing_options_button.config(state='normal')
        self.tracing_start.config(state='normal')

        self.conversion_start.config(state='disabled')
        self.conversion_result_var.set('PASSED')
        self.conversion_result_label.config(foreground='green4')

        self._update_image()

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
            self.tracing_result_label.config(foreground='red2')
            return

        self.file = file_out
        self.stl_options_button.config(state='normal')
        self.stl_start.config(state='normal')

        self.tracing_start.config(state='disabled')
        self.tracing_result_var.set('PASSED')
        self.tracing_result_label.config(foreground='green4')

        self._update_image()

    def stl_convert(self):
        """ Launches the SVG to STL conversion process """
        self.stl_result_var.set('RUNNING')
        options = dict()
        options['filename'] = self.file
        options['filepath'] = self.objects_path
        options['extrusion'] = self.extrusion_depth
        file_out, result = executors.stl_conversion(self.root, **options)

        if not result:
            messagebox.showerror('Error', 'There was an error in the STL conversion process!')
            self.stl_result_var.set('FAILED')
            self.stl_result_label.config(foreground='red2')
            return

        self.file = file_out
        # self.slicing_options_button.config(state='normal')
        self.slicing_start_button.config(state='normal')
        self.current_y_entry.config(state='normal')
        self.current_z_entry.config(state='normal')
        self.current_x_entry.config(state='normal')

        self.stl_start.config(state='disabled')
        self.stl_result_var.set('PASSED')
        self.stl_result_label.config(foreground='green4')

        self._update_image()

    def slicing_start(self):
        """ Executes the slicer for the given 3D object

        This prepares and calls the executor from executors module
        """
        self.slicing_result_var.set('RUNNING')

        mod_x = self.x.get() - .375
        mod_y = self.y.get() - .375
        mod_z = self.z.get() - .375
        # Run the scaler before slicing
        executors.execute_scale_stl(self.file, self.objects_path, mod_x, mod_y, mod_z)

        # Edit the Ini to include bed frame dimensions
        config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.ini')
        mod_x = 25.4 * mod_x
        mod_y = 25.4 * mod_y
        mod_z = 25.4 * mod_z
        shape = '0x0,{}x0,{}x{},0x{}'.format(mod_x, mod_x, mod_y, mod_y)

        for line in fileinput.input(config_path, inplace=True):
            if line.strip().startswith('bed_shape = '):
                line = 'bed_shape = {}\n'.format(shape)
            sys.stdout.write(line)

        mod_x = self.x.get() - .375
        mod_y = self.y.get() - .375

        options = dict()
        options['filename'] = self.file
        options['filepath'] = self.objects_path
        file_out, result = executors.execute_slic3r(x=mod_x, y=mod_y, **options)

        if not result:
            messagebox.showerror('Error', 'There was an error in the Slicing process!')
            self.slicing_result_var.set('FAILED')
            self.slicing_result_label.config(foreground='red2')
            return

        self.file = file_out
        self.current_x_entry.config(state='normal')
        self.current_y_entry.config(state='normal')
        self.current_z_entry.config(state='normal')
        self.test_connections_button.config(state='normal')

        self.slicing_start_button.config(state='disabled')
        self.slicing_result_var.set('PASSED')
        self.slicing_result_label.config(foreground='green4')

    def bit_conversion_options(self):
        """ Brings up the conversion options menu for bitmap tracing

        Parses the results and readies for imagemagick conversion subprocess call
        """
        con_opts = ConversionOptions(self.root, self.conversion_map_type, self.negate)
        self.wait_window(con_opts.top)
        options = con_opts.get()
        if not options['changed']:
            return

        self.conversion_map_type = parsers.conversion(options, 'filetype')
        self.custom_imagemagick = parsers.conversion(options, 'imagemagick')
        self.negate = parsers.conversion(options, 'negate')

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

    def stl_options(self):
        """ Brings up the menu options for STL conversion

        Parses the results and readies for STL conversion
        """
        stl_opts = StlOptions(self.root, self.extrusion_depth)
        self.wait_window(stl_opts.top)
        options = stl_opts.get()
        if not options['changed']:
            return

        self.extrusion_depth = float(parsers.conversion(options, 'extrusion'))

    def slicing_options(self):
        """  Brings up options menu for 3D slicing

        Parses the results for when running the Freecad extrusion and STL output script
        """
        # Not needed as of first revision
        pass

    def etching_ready(self):
        """ Calls the etching ready module to prepare for etching

        The module tries to establish connections to both the laser and the MCU. Switches
        the ready state to READY if the connections are correctly established,
        otherwise changes the state to not ready and provides error.
        """
        result = serials.pre_test()

        if result['result'] is False:
            messagebox.showerror(title='Error', message=result['reason'])
            return

        self.device_path = result['device']
        self.etching_start.configure(state='normal')

    def etching_start(self):
        """ Begins the etching process """
        try:
            result, reason = serials.full_test(self.file, self.device_path)
        except:
            serials.stop_laser()
            messagebox.showerror(title='Error', message='There was a critical error')
            return

        if result is False:
            messagebox.showerror(title='Error', message=reason)
            return

        messagebox.showinfo(title='Success', message='Etching process complete!')

    def open_file(self):
        """ Opens the file using default for operating system """
        os.startfile(self.file)

    def init_gui(self):
        """ Initializes the GUI and all the widgets

        Tkinter's Grid geometry manager is used instead of pack
        """
        geo = calculators.center(self.root, 800, 500)
        self.root.geometry(geo)
        self.root.title('3D Laser Plasma Art')
        self.root.wm_iconbitmap(self.file_path + r'\ucf.ico')
        self.root.option_add('*tearOff', 'FALSE')

        # layout all of the main containers
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

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
        self.conversion_frame = ttk.Frame(self.root, width=200, height=10)
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
        self.stl_label = ttk.Label(self.conversion_frame, text='STL conversion', anchor=tkinter.W)
        self.stl_label.grid(row=5, padx=5, pady=5, sticky=tkinter.W, columnspan=2)

        self.stl_options_button = ttk.Button(self.conversion_frame, text='Options', command=self.stl_options,
                                                  state=tkinter.DISABLED)
        self.stl_options_button.grid(row=6, padx=5, pady=5, sticky=tkinter.W)

        self.stl_start = ttk.Button(self.conversion_frame, text='Start', command=self.stl_convert,
                                         state=tkinter.DISABLED)
        self.stl_start.grid(row=6, column=1, padx=5, pady=5)

        self.separator_1 = ttk.Separator(self.conversion_frame, orient=tkinter.HORIZONTAL)
        self.separator_1.grid(row=7, padx=5, pady=5, sticky='we', columnspan=10)

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

        self.stl_result_var = tkinter.StringVar()
        self.stl_result_label = ttk.Label(self.conversion_frame, textvariable=self.stl_result_var, anchor=tkinter.CENTER,
                                              background='gray60', width=20)
        results_widgets.append(self.stl_result_label)
        self.stl_result_var.set('NOT RUN')

        row = 2
        for label in results_widgets:
            label.grid(row=row, column=3, padx=5, pady=5)
            row += 2

        # --- STL Slicing ----
        self.slicing_frame = ttk.Frame(self.root, width=200, height=15)
        self.slicing_frame.grid(row=2, sticky='NW', column=0)

        self.slicing_label = ttk.Label(self.slicing_frame, text='Step 3:')
        self.slicing_label.grid(padx=5, pady=5, sticky=tkinter.NW)

        self.slicing_label_opts = ttk.Label(self.slicing_frame, text='3D Slicing')
        self.slicing_label_opts.grid(padx=5, pady=5, sticky=tkinter.NW, row=1)

        self.slicing_options_button = ttk.Button(self.slicing_frame, text='Options', command=self.slicing_options,
                                                 state=tkinter.DISABLED)
        self.slicing_options_button.grid(row=3,padx=5, pady=5, sticky=tkinter.NW)

        self.slicing_start_button = ttk.Button(self.slicing_frame, text='Start', command=self.slicing_start,
                                               state=tkinter.DISABLED)
        self.slicing_start_button.grid(row=3, column=1, padx=5, pady=5, columnspan=3)

        #self.slicing_frame.grid_columnconfigure(2, minsize=65)

        self.slicing_result_var = tkinter.StringVar()
        self.slicing_result_label = ttk.Label(self.slicing_frame, textvariable=self.slicing_result_var, anchor=tkinter.CENTER,
                                              background='gray60', width=20)
        self.slicing_result_var.set('NOT RUN')
        self.slicing_result_label.grid(row=3, column=4, padx=5, pady=5, columnspan=3)

        self.current_position_label = ttk.Label(self.slicing_frame, text='Glass Dimensions (Inches):')
        self.current_position_label.grid(row=2, padx=5, pady=5)

        self.current_x_label = ttk.Label(self.slicing_frame, text='X:')
        self.current_y_label = ttk.Label(self.slicing_frame, text='Y:')
        self.current_z_label = ttk.Label(self.slicing_frame, text='Z:')

        self.current_x_entry = ttk.Entry(self.slicing_frame, textvariable=self.x, width=4, state=tkinter.DISABLED)
        self.current_y_entry = ttk.Entry(self.slicing_frame, textvariable=self.y, width=4, state=tkinter.DISABLED)
        self.current_z_entry = ttk.Entry(self.slicing_frame, textvariable=self.z, width=4, state=tkinter.DISABLED)

        self.current_x_label.grid(row=2, column=1)
        self.current_x_entry.grid(row=2, column=2)
        self.current_y_label.grid(row=2, column=3)
        self.current_y_entry.grid(row=2, column=4)
        self.current_z_label.grid(row=2, column=5)
        self.current_z_entry.grid(row=2, column=6)

        # --- Etching widgets ----
        self.etching_frame = ttk.Frame(self.root, width=200, height=15)
        self.etching_frame.grid(row=2, column=1, sticky='NW')

        self.etching_label = ttk.Label(self.etching_frame, text='Step 4:')
        self.etching_label.grid(padx=5, pady=5, sticky='W')

        self.etching_label_desc = ttk.Label(self.etching_frame, text='Laser Etching')
        self.etching_label_desc.grid(row=1, padx=5, pady=5, sticky='W', columnspan=5)

        #self.choose_connections_button = ttk.Button(self.etching_frame, text='Choose connections', command=self.choose_connections,
        #                                     state=tkinter.DISABLED, width=20)
        #self.choose_connections_button.grid(row=3, padx=5, pady=5)

        self.test_connections_button = ttk.Button(self.etching_frame, text='Test Connections', command=self.etching_ready,
                                                  state=tkinter.DISABLED, width=20)
        self.test_connections_button.grid(row=4, padx=5, pady=10)

        self.etching_start = ttk.Button(self.etching_frame, text='Start', width=20, command=self.etching_start,
                                        state=tkinter.DISABLED)
        self.etching_start.grid(row=4, column=1, padx=5, pady=10, columnspan=5)

        # --- Image preview ---
        self.image_frame = ttk.Frame(self.root, width=200, height=15)
        self.image_frame.grid(row=0, column=1, sticky='W', rowspan=2)

        self.image_frame.grid_columnconfigure(0, minsize=60)
        self.image_frame.grid_columnconfigure(1, weight=1)

        self.canvas = tkinter.Canvas(self.image_frame, width=300, height=300, borderwidth=2, relief=tkinter.GROOVE)
        self.canvas.grid(padx=5, pady=5, column=1)

        self.canvas_button = ttk.Button(self.image_frame, text='Preview File', command=self.open_file, width=20)
        self.canvas_button.place(x=155, y=150)
        self.canvas_button.lower(self.canvas)

        for child in self.winfo_children():
            child.grid_configure()


if __name__ == '__main__':
    root = tkinter.Tk()
    Main(root)
    root.mainloop()
