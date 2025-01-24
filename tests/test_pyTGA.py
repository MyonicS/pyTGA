import os
import sys
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, parent_dir)

import pyTGA as tga


# Construct the path to the test files
testfiledir = os.path.join(current_dir, '..', 'example_data', 'manufacturers')

def test_infer_manufacturer():
    testfile = os.path.join(testfiledir, 'MettlerToledo_example_file.txt')
    testfile2 = os.path.join(testfiledir, 'PerkinElmer_example_file.txt')
    result = tga.infer_manufacturer(testfile)
    result2 = tga.infer_manufacturer(testfile2)
    assert result == 'Mettler Toledo' 
    assert result2 == 'Perkin Elmer' 

    
def test_manufacturer_attribute():
    tga_exp1 = tga.parse_TGA(os.path.join(testfiledir, 'MettlerToledo_example_file.txt'))
    tga_exp2 = tga.parse_TGA(os.path.join(testfiledir, 'PerkinElmer_example_file.txt'))
    assert tga_exp1.manufacturer == 'Mettler Toledo'
    assert tga_exp2.manufacturer == 'Perkin Elmer'

def test_plastic_cracking_class():
    tga_exp = tga.parse_TGA('example_data/plastic_cracking_example.txt',exp_type='pyro',calculate_DTGA=True)
    tga_exp.Tmax = tga.calc_Tmax(tga_exp.cracking())
    tga_exp.T50 = tga.calc_T50(tga_exp.cracking())
    assert tga_exp.Tmax == 245.0
    assert tga_exp.T50 == 245.0