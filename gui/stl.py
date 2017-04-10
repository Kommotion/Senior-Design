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
    print("dbg111: start building the 3D part")

    my_tmp_doc = FreeCAD.newDocument("doc_blabla")  # you can create implicitly the document "doc_blabla" by using it!
    importSVG.insert(input_file, "doc_blabla")

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
    print("output stl file: %s" % output_file)
    print("dbg999: end of script")


def stl_scaling(input_file, output_file):
    """ Scales the stl file to the given dimensions """
    import Mesh
    mesh = Mesh.Mesh("{}".format(input_file))
    print(mesh.BoundBox.XLength, mesh.BoundBox.YLength, mesh.BoundBox.ZLength)

    while any(length > 25.4 for length in (mesh.BoundBox.XLength, mesh.BoundBox.YLength, mesh.BoundBox.ZLength)):
        if mesh.BoundBox.XLength > 25.4 or mesh.BoundBox.YLength > 25.4:
            x_y_scale = .75
        else:
            x_y_scale = 1

        if mesh.BoundBox.ZLength > 25.4:
            z_scale = .75
        else:
            z_scale = 1

        matrix = FreeCAD.Matrix()
        matrix.scale(x_y_scale, x_y_scale, z_scale)
        mesh.transform(matrix)

    print(mesh.BoundBox.XLength, mesh.BoundBox.YLength, mesh.BoundBox.ZLength)
    mesh.write(input_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="STL Conversion")
    parser.add_argument('-i', '--input', help='The input file (Required)', required=True)
    parser.add_argument('-o', '--output', help='The output file (Required)', required=True)
    parser.add_argument('-e', '--extrusion', help='The distance for extrusion (Required)', required=False)
    parser.add_argument('-s', '--scale', help='True or False for scaling STL to fit platform. Default False', default=0)
    # parser.add_argument('-x', help='The max X of etching')
    # parser.add_argument('-y', help='The max Y of etching')
    # parser.add_argument('-z', help='The max Z of etching')

    # There is no argument validation done, we assume the user put in correct args
    results = parser.parse_args()
    input_file = results.input
    output_file = results.output
    extrusion = results.extrusion
    scale = int(results.scale)

    # Scale argument
    if scale == 1:
        stl_scaling(input_file, output_file)
    else:
        main_conversion(input_file, output_file, float(extrusion))
