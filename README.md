# Metamaterial_absorber

## Overview

A metamaterial absorber generator and exporter.

A metamaterial absorber generator with different pattern and cross sections to choose from and exports the built absorber or cadquery Workplane object as a stl file to 3D print.

This repo contains old code by other people and also [my own code](https://github.com/zeshenbao/Metamaterial_absorber/tree/main/current/own_code) which I wrote during my summer project.

Check out the [History_log.md](https://github.com/zeshenbao/Metamaterial_absorber/blob/main/History_log.md) for an overview of the project.

The most important files that I wrote during this summer:

1. Generate doglegged hilbert geometry
2. Generate doglegged grid geometry
3. Notes for cadquery
4. Work in progress code to extract VNA traces
5. VNA notes
6. Solid work parts for the static reflectometry system

## Installation
1. Install Python3.
2. Install latest [Miniconda](https://docs.conda.io/en/latest/miniconda.html).
3. Install [Cadquery2](https://cadquery.readthedocs.io/en/latest/installation.html) on Miniconda.
4. Create a [virtual enviroment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) with conda.
5. Run the [code](https://github.com/zeshenbao/Metamaterial_absorber/blob/main/current/own_code/MeMAb_code/gen_MeMAb_v1.0.0.py) file in the venv.

## Getting started
0. Main code to use is [gen_MeMAb_v1.0.0](https://github.com/zeshenbao/Metamaterial_absorber/blob/main/current/own_code/MeMAb_code/gen_MeMAb_v1.0.0.py) and main code directory is [MeMAb_code](https://github.com/zeshenbao/Metamaterial_absorber/tree/main/current/own_code/MeMAb_code).
1. Looking at cadquery [examples](https://cadquery.readthedocs.io/en/latest/examples.html) could be useful.
2. Look in cadquery [class summary](https://cadquery.readthedocs.io/en/latest/classreference.html#cadquery.Workplane) for details.
3. Test to make simple geometries and exporting to stl file.
4. Test run example code in main().
5. Look at [example stl files](https://github.com/zeshenbao/Metamaterial_absorber/tree/main/current/own_code/MeMAb_code/example_stl_files).

## Make extensions to the [code](https://github.com/zeshenbao/Metamaterial_absorber/blob/main/current/own_code/MeMAb_code/gen_MeMAb_v1.0.0.py)

### New cross sections
1. Add new method for cross section in method _make_new_basic() around line 345 with the groups sides, corners, other.
2. Add method to dictionary in the method set_cross_section() around line 184. 
3. Select and use like other cross patterns.

### New patterns
1. Add new method for pattern generation in method create_new_blueprint() around line 676.
2. Call create_new_blueprint() to generate pattern like other patterns.


## Roadmap

* The API of this library is frozen.
* Version numbers adhere to [semantic versioning](http://semver.org/).

The only accepted reason to modify the API of this package
is to handle issues that can't be resolved in any other
reasonable way.

Zeshen Bao – [zeshenbao](https://github.com/zeshenbao)

