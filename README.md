# pyTGA

<p align="center">
  <img src="https://raw.githubusercontent.com/MyonicS/pyTGA/main/docs/source/_static/logo_v1_bright_2.svg" alt="pyTGA logo" width="200"/>
</p>


## Description
A simple python library for parsing and processing Thermogravimetric analysis (TGA) data. At the moment, .txt files from Perkin Elmer and Mettler Toledo and excel files from TA Instruments are supported. Work in progress, if you have suggestions or requests please submit an issue.

[![Test Status](https://github.com/MyonicS/pyTGA/actions/workflows/test.yml/badge.svg)](https://github.com/MyonicS/pyTGA/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **⚠️ WARNING**: pyTGA is under active development. Please report any issues using the [Issue Tracker](https://github.com/MyonicS/pyTGA/issues).

## Getting started

### New to python and want to use pyTGA?
<details>
<summary><b>Here is a quick guide:</b> (Click to expand)</summary>

#### Install a distribution
The easiest way to get started with Python for scientific computing is with [Anaconda](https://www.anaconda.com/download/):
- Includes Python, package manager, and many scientific libraries
- Provides a user-friendly interface (Anaconda Navigator)
- Comes with Jupyter Notebook for interactive analysis
- Handles most dependencies automatically

#### Install a code editor
To be able to write and run code, you should use a code editor such as
- [VS Code](https://code.visualstudio.com/) - a free, open-source editor with excellent Python support
- [Spyder](https://www.spyder-ide.org/) - a scientific environment designed for Python

#### Learn the basics
There are plenty of online tutorials available. Here are some recommendations:
- [Boot.dev](https://www.boot.dev/)
- [sololearn](https://www.sololearn.com/en/)

#### Learn about the most important libraries
For many applications in science, you won't need much more than these 3 libraries:
- [NumPy](https://numpy.org/) - fundamental package for scientific computing in Python
- [pandas](https://pandas.pydata.org/) - data analysis and manipulation library
- [Matplotlib](https://matplotlib.org/) - comprehensive library for plotting
</details>

### Installation 
Install from PyPI:
```
pip install pyTGA
```

### Development installation
If you want to install the development version:

- Clone the repository:
```
git clone https://github.com/MyonicS/pyTGA
```
- Install the package in development mode with dev dependencies by **navigating to the cloned repository** in your python environment and executing:

```
pip install -e .[dev]
```



## Usage

Import the package 
```python
import pyTGA as tga
```

Parse a TGA file using 
```python
tga_exp = tga.parse_TGA('*path-to-your-file*')
```
Use the .quickplot method to have a first look at your data: 

```python
tga_exp.quickplot()
```
Access individual stages as pandas DataFrame:

```python
tga_exp.stages['stage1']
```
Access the data of the whole experiment:

```python
tga_exp.full
```
To get started, check out the 'Quickstart' notebook [here](https://pytga.readthedocs.io/en/latest/notebooks/example_Notebook.html).

## Documentation

Full documentation of the package, including example use cases is available [here](https://pytga.readthedocs.io/).

You can also download example notebooks from the repository [here](https://github.com/MyonicS/pyTGA/tree/main/docs/source/notebooks) using [example data](https://github.com/MyonicS/pyTGA/tree/main/example_data).


## Roadmap
- support for more manufacturers and file formats
- unified weight/temperature/time parsing
- more common processing features (please make suggestions with detailed explanations)

## Contributing
Contributions are more than welcome!
The easiest way to contribute is to suggest new features as an issue.
If you want to contribute code or add to the documentation, fork the repository, implement your changes and submit a pull request.
If you have a question, get in touch.

## Authors
Sebastian Rejman, Utrecht University


