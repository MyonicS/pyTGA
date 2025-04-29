from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyTGA",
    version="0.1.0",
    description="A simple python library for parsing and processing Thermogravimetric analysis (TGA) data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Sebastian Rejman",
    author_email="s.rejman@uu.nl",
    url="https://github.com/MyonicS/pyTGA",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "matplotlib",
        "chardet"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Chemistry"
    ],
    python_requires=">=3.7",
)