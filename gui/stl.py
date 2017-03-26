"""
# a generic script that extrudes all paths of a svg file
# created by charlyoleg on 2013/05/08

 Modifications by Nicolas Ramirez on 3/22/2017

 Cleaned up and added argeparsing capabilities where user can pass
 in arguments

 Required Arguments for script:
    -i --input          The input SVG file
    -o --output         The output STL file
    -e --extrusion      The extrusion depth for the paths

 Example script call:
 python2 stl.py -i "C:\user\blah\Desktop\ayy.svg" -o "C:\user\blah\Desktop\boo.stl -e 45

 Requirements:
 Freecad bin folder should be in your PYTHONPATH

# license: CC BY SA 3.0
"""
import argparse
import sys
import FreeCAD
import Part
import importSVG
from FreeCAD import Base


def main_conversion(input_file, output_file, extrusion):
    """ The main function to run Freecad and carry out the STL conversion process

        input_file  : The input file that should be SVG
        output_file : The output file that should be STL
        extrusion   : The depth that the object will be extruded to

        The function opens the SVG file in Freecad, extrudes all paths, and exports as an SVG file
    """
    # FREECADPATH='/usr/lib/freecad/lib' # adapt this path to your system

    # # choose your favorite test to check if you are running with FreeCAD GUI or traditional Python
    # freecad_gui = True
    # #if not(FREECADPATH in sys.path): # test based on PYTHONPATH
    # if not("FreeCAD" in dir()):       # test based on loaded module
    #     freecad_gui = False
    # print("dbg102: freecad_gui:", freecad_gui)
    #
    # if not(freecad_gui):
    #     print("dbg101: add FREECADPATH to sys.path")
    #     sys.path.append(FREECADPATH)
    #     import FreeCAD
    #
    # print("FreeCAD.Version:", FreeCAD.Version())
    # #FreeCAD.Console.PrintMessage("Hello from PrintMessage!\n") # avoid using this method because it is not printed in the FreeCAD GUI
    #
    # import Part
    # from FreeCAD import Base

    print("dbg111: start building the 3D part")

    my_tmp_doc = FreeCAD.newDocument("doc_blabla") # you can create implicitly the document "doc_blabla" by using it!
    #import importSVG
    importSVG.insert(input_file,"doc_blabla")

    # Extrusion of paths
    my_solids = []
    for obj in my_tmp_doc.Objects:
        my_svg_shape = obj.Shape
        my_svg_wire = Part.Wire(my_svg_shape.Edges)
        my_svg_face = Part.Face(my_svg_wire)
        my_solids.append(my_svg_face.extrude(Base.Vector(0, 0, extrusion)))  # straight linear extrusion

    my_compound = Part.makeCompound(my_solids)

    # Exporting STL file
    # Part.show(my_compound) # works only with FreeCAD GUI, ignore otherwise
    my_compound.exportStl(output_file)
    print("output stl file: %s"%(output_file))
    print("dbg999: end of script")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="STL Conversion")
    parser.add_argument('-i', '--input', help='The input file (Required)', required=True)
    parser.add_argument('-o', '--output', help='The output file (Required)', required=True)
    parser.add_argument('-e', '--extrusion', help='The distance for extrusion (Required)', required=True)

    # There is no argument validation done, we assume the user put in correct args
    results = parser.parse_args()
    input_file = results.input
    output_file = results.output
    extrusion = results.extrusion

    main_conversion(input_file, output_file, float(extrusion))
