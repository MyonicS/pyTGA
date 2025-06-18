import os
import sys
import pytest
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, parent_dir)

# Set matplotlib to use non-interactive backend for testing
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend which doesn't require a display

import pyTGA as tga


# Construct the path to the test files
testfiledir = os.path.join(current_dir, '..', 'example_data', 'manufacturers')
testfiledir_examples = os.path.join(current_dir, '..', 'example_data')


def test_infer_manufacturer():
    testfile = os.path.join(testfiledir, 'MettlerToledo_example_file.txt')
    testfile2 = os.path.join(testfiledir, 'PerkinElmer_example_file.txt')
    testfile3 = os.path.join(testfiledir, 'TA_instrument_excel.xls')
    result = tga.infer_manufacturer(testfile)
    result2 = tga.infer_manufacturer(testfile2)
    result3 = tga.infer_manufacturer(testfile3)
    assert result == 'Mettler Toledo' 
    assert result2 == 'Perkin Elmer' 
    assert result3 == 'TA Instruments (Excel)' 

    
def test_manufacturer_attribute():
    tga_exp1 = tga.parse_TGA(os.path.join(testfiledir, 'MettlerToledo_example_file.txt'))
    tga_exp2 = tga.parse_TGA(os.path.join(testfiledir, 'PerkinElmer_example_file.txt'))
    tga_exp3 = tga.parse_TGA(os.path.join(testfiledir, 'TA_instrument_excel.xls'))
    assert tga_exp1.manufacturer == 'Mettler Toledo'
    assert tga_exp2.manufacturer == 'Perkin Elmer'
    assert tga_exp3.manufacturer == 'TA Instruments (Excel)'
    
def test_ANSI_encoding():
    # some files are ANSI encoded
    tga_exp = tga.parse_TGA(os.path.join(testfiledir_examples, 'Methane_Pyrolysis.txt'))
    target = 5.748245
    testweight = tga_exp.get_stage('stage1')['Unsubtracted weight'].min()
    assert testweight == pytest.approx(target, abs=1e-5)

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

def test_date_time_extraction_TA():
    # Test TA Instruments date/time extraction
    ta_exp = tga.parse_TA_excel(os.path.join(testfiledir, 'TA_instrument_excel.xls'))
    assert ta_exp.date is not None
    assert ta_exp.time is not None
    
def test_quickplot():
    # Test with Perkin Elmer data
    tga_exp_pe = tga.parse_TGA(os.path.join(testfiledir, 'PerkinElmer_example_file.txt'))
    fig_pe = tga.quickplot(tga_exp_pe, show=False)
    assert fig_pe is not None
    
    # Test with Mettler Toledo data
    tga_exp_mt = tga.parse_TGA(os.path.join(testfiledir, 'MettlerToledo_example_file.txt'))
    fig_mt = tga.quickplot(tga_exp_mt, show=False)
    assert fig_mt is not None
    
    # Test with TA Instruments data
    tga_exp_ta = tga.parse_TGA(os.path.join(testfiledir, 'TA_instrument_excel.xls'))
    fig_ta = tga.quickplot(tga_exp_ta, show=False)
    assert fig_ta is not None
    
    # Test with a TGA experiment with no full data
    tga_exp_no_full = tga.parse_TGA(os.path.join(testfiledir, 'PerkinElmer_example_file.txt'))
    tga_exp_no_full.full = None
    fig_no_full = tga.quickplot(tga_exp_no_full, show=False)
    assert fig_no_full is not None
    assert 'full' in tga_exp_no_full.stages

def test_parse_TA_excel():
    # Test direct parsing of TA Instruments Excel file
    ta_exp = tga.parse_TA_excel(os.path.join(testfiledir, 'TA_instrument_excel.xls'))
    assert ta_exp.manufacturer == 'TA Instruments (Excel)'
    assert ta_exp.default_temp == 'Temperature (C)'
    assert ta_exp.default_weight == 'Weight (mg)'
    assert ta_exp.default_time == 'Time (min)'
    assert ta_exp.full is not None
    assert len(ta_exp.stage_names()) > 0

def test_TA_stages_and_metadata():
    # Test that stages and metadata are correctly parsed
    ta_exp = tga.parse_TGA(os.path.join(testfiledir, 'TA_instrument_excel.xls'))
    
    # Check metadata
    assert ta_exp.details is not None
    assert ta_exp.date is not None
    assert ta_exp.time is not None
    
    # Check stage data
    for stage_name in ta_exp.stage_names():
        if stage_name != 'full':
            stage = ta_exp.get_stage(stage_name)
            assert stage is not None
            assert ta_exp.default_temp in stage.columns
            assert ta_exp.default_weight in stage.columns
            assert ta_exp.default_time in stage.columns

