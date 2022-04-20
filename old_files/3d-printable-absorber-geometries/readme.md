# 3D-printable broadband millimeter wave absorber geometries

Contained are scripts for generating 3D-printable millimeter wave absorber
geometries based on space-filling curves and the resulting CAD files.

This work serves as a supplement to the paper entitled
_A 3D-printed broadband millimeter wave absorber_.


## Scripts

The `generate_hilbert_curve.py` and `generate_gosper_curve.py` scripts generate
absorber geometries based on geometric approximations of Hilbert curves and
Gosper 37a-1 curves, respectively. The primary input argument is the curve
order / number of L-system iterations; it is not recommended to use orders >6
for the Hilbert script and orders >2 for the Gosper script, due to the
computation time involved.

The Python 2 scripts require [CadQuery](https://github.com/dcowden/cadquery).
They were tested with CadQuery 1.2.0 and FreeCAD 0.17. Python 3 was not used
due to compatibility issues encountered with CadQuery when the scripts
were written.


## CAD files

The `cad-files` directory contains pre-generated STEP files for Hilbert curve
orders [1, 7] and Gosper curve orders [1, 2], using the default parameters of
the above scripts. The `for-sims` subdirectory contains the STEP files used for
geometry comparison simulations in the accompanying paper; these files were
generated using the `--use_square_ends` option for the Hilbert curve script and
then hand-edited to match various manufacturable geometry variants.


## Production files

The `production-files` directory contains the STL file and G-code used for
producing the Hilbert curve absorber prototype measured in the accompanying
paper. It is a fifth order curve with a 5mm pitch, a 1mm base thickness, and a
15mm height before tip truncation; the tip is truncated to have a 0.5mm width.

The G-code was generated using Cura 2.6.1. It is intended for use with a
LulzBot TAZ 6 printer using a filament made from Modern Dispersions, Inc.'s
PS-715 conductive HIPS (or a similar HIPS-based lossy dielectric).


## License

This work is placed into the public domain via the
[CC0 1.0 public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
See the `COPYING` file for details.


## Credits

This work was produced by Matthew Petroff
([ORCID:0000-0002-4436-4215](https://orcid.org/0000-0002-4436-4215)) and was
supported by a Space@Hopkins seed grant.
