import os
import sys
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, parent_dir)

# Set matplotlib to use non-interactive backend for testing
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend which doesn't require a display

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
    assert tga_exp.T50 == 230.89
    assert tga_exp.date == '10/04/2023'
    assert tga_exp.time == '08:20:41'

def test_date_time_extraction_MT():
    # Test Mettler Toledo date/time extraction
    mt_exp = tga.parse_MT(os.path.join(testfiledir, 'MettlerToledo_example_file.txt'))
    assert mt_exp.date == '01.01.2024'
    assert mt_exp.time == '18:00:00'


    
def test_quickplot():
    # Test with Perkin Elmer data
    tga_exp_pe = tga.parse_TGA(os.path.join(testfiledir, 'PerkinElmer_example_file.txt'))
    fig_pe = tga.quickplot(tga_exp_pe, show=False)
    assert fig_pe is not None
    
    # Test with Mettler Toledo data
    tga_exp_mt = tga.parse_TGA(os.path.join(testfiledir, 'MettlerToledo_example_file.txt'))
    fig_mt = tga.quickplot(tga_exp_mt, show=False)
    assert fig_mt is not None
    
    # Test with a TGA experiment with no full data
    tga_exp_no_full = tga.parse_TGA(os.path.join(testfiledir, 'PerkinElmer_example_file.txt'))
    tga_exp_no_full.full = None
    fig_no_full = tga.quickplot(tga_exp_no_full, show=False)
    assert fig_no_full is not None
    assert 'full' in tga_exp_no_full.stages

