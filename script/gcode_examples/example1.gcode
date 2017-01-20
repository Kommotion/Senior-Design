; Example pulled from Gcode simulator
; https://nraynaud.github.io/webgcode/
G0 Y10 Z-5
G1 Z-10
G1 Y20
G02 X10 Y30 R10
G1 X30
G2 X40 Y20 R10
G1 Y10
G2 X30 Y0 R10
G1 X10
G2 X0 Y10 Z-15 R10 (yeah spiral !)
G3 X-10 Y20 R-10 (yeah, long arc !)
G3 X0 Y10 I10 (center)
G91 G1 X10 Z10
G3 Y10 R5 Z3 (circle in incremental)
Y10 R5 Z3 (again, testing modal state)
G20 G0 X1 (one inch to the right)
G3 X-1 R1 (radius in inches)
G3 X1 Z0.3 I0.5 J0.5 (I,J in inches)
G21 (back to mm)
G80 X10 (do nothing)
G90
G0 X30 Y30 Z30
G18 (X-Z plane)
G3 Z40 I0 K5
G19 (Y-Z plane)
G3 Z50 J0 K5
G17 (back to X-Y plane)
