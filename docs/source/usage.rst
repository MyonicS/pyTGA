Usage
=====

Basic usage:

.. code-block:: python

   import pyTGA as tga
   
   # Parse TGA data file
   my_exp = tga.parse_txt('data.txt', exp_type='general')
   
   # Quick visualization
   my_exp.quickplot()