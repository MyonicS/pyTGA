Usage
=====

Basic usage:
--------
.. code-block:: python

   import pyTGA as tga
   
   # Parse TGA data file
   my_exp = tga.parse_TGA('data.txt', exp_type='general')
   
   # Quick visualization
   my_exp.quickplot()

   # Access individual stages as pandas DataFrames
   my_exp.stages['stage1']

Parsing:
--------
Formats of different manufacturers have different features.
For example, PerkinElmer ASCII files contain method information and split the experiment into stages.
Mettler Toledo files on the other hand do not have this feature. For splitting into stages an additonal file needs to be provided.

Below is a notebook with detailed examples for parsing TGA data from different manufacturers:

.. toctree::
   :maxdepth: 2

   notebooks_test/parsing.ipynb