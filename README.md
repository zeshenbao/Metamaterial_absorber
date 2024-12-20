# Metamaterial_absorber

## Overview

A metamaterial absorber generator and exporter.

A metamaterial absorber generator with different pattern and cross sections to choose from and exports the built absorber or cadquery Workplane object as a stl file to 3D print.

The code generates different wall tiles with cadquery Workplane objects by defined points to later be combined into more complex tiles and in the end added to a complete pattern which can be exported into a stl file.


|<img src="https://github.com/zeshenbao/Metamaterial_absorber/blob/main/im/dog_dots_im.jpg"  width="800"/>|
|:--:| 
| *Figure 1. Example 3D print of generated stl file.* |



| ![](https://github.com/zeshenbao/Metamaterial_absorber/blob/main/im/dog_rows_im.png)  | ![](https://github.com/zeshenbao/Metamaterial_absorber/blob/main/im/triangle_dot_im.png) | ![](https://github.com/zeshenbao/Metamaterial_absorber/blob/main/im/block_hilbert_im.png)|
|:---:|:---:|:---:|
|Figure 2. Dogleg rows absorber| Figure 3. Triangle dots absorber|Figure 4. Block hilbert example|



This repo contains might contain old code by other people and also [my own code](https://github.com/zeshenbao/Metamaterial_absorber/tree/main/current) which I wrote during my summer project.

Check out the [History_log.md](https://github.com/zeshenbao/Metamaterial_absorber/blob/main/History_log.md) and [my presentation](https://github.com/zeshenbao/Metamaterial_absorber/blob/main/Metamaterial_absorber_presentation_Zeshen_Bao.pdf) for an overview of the project.

## Installation
1. Install Python3.
2. Install the latest [Miniconda](https://docs.conda.io/en/latest/miniconda.html).
3. Create a [virtual environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) with conda.
4. Install [Cadquery2](https://cadquery.readthedocs.io/en/latest/installation.html) inside conda venv.
5. Run the [code](https://github.com/zeshenbao/Metamaterial_absorber/blob/main/current/own_code/MeMAb_code/gen_MeMAb_v1.0.1.py) file in the venv.

## Getting started
0. Main code to use is [gen_MeMAb_v1.0.1](https://github.com/zeshenbao/Metamaterial_absorber/blob/main/current/MeMAb_code/gen_MeMAb_v1.0.1.py) and main code directory is [MeMAb_code](https://github.com/zeshenbao/Metamaterial_absorber/tree/main/current/MeMAb_code).
1. Looking at cadquery [examples](https://cadquery.readthedocs.io/en/latest/examples.html) could be useful.
2. Look in cadquery [class summary](https://cadquery.readthedocs.io/en/latest/classreference.html#cadquery.Workplane) for details.
3. Test to make simple geometries and export to stl file.
4. Test run example code in main().
5. Look at [example stl files](https://github.com/zeshenbao/Metamaterial_absorber/tree/main/current/MeMAb_code/example_stl_files).


## Documentation
Read [Documentation.md](https://github.com/zeshenbao/Metamaterial_absorber/blob/main/Documentation.md) for documentation. It is too long to add here.



## Make extensions to the [code](https://github.com/zeshenbao/Metamaterial_absorber/blob/main/current/MeMAb_code/gen_MeMAb_v1.0.1.py)

### New cross sections
1. Add new method for cross section in method _make_new_basic() around line 345 with the groups sides, corners, other.
2. Add method to dictionary in the method set_cross_section() around line 184. 
3. Select and use like other cross patterns.

### New patterns
1. Add new method for pattern generation in method create_new_blueprint() around line 676.
2. Call create_new_blueprint() to generate pattern like other patterns.

### Change dogleg parameters
1. Look at [dogleg_geometry_ derivation.pdf](https://github.com/zeshenbao/Metamaterial_absorber/blob/main/current/MeMAb_code/dogleg_geometry_%20derivation.pdf)
2. Change lists for points (area_left_pts, area_right_pts, pts) in method _make_dogleg_basic().

## Roadmap

* The API of this library is frozen.
* Version numbers adhere to [semantic versioning](http://semver.org/).

The only accepted reason to modify the API of this package
is to handle issues that can't be resolved in any other
reasonable way.

Zeshen Bao – [zeshenbao](https://github.com/zeshenbao)

