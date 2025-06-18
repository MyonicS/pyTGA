import pandas as pd
import numpy as np
import io
import re
from matplotlib import pyplot as plt
import os
import warnings
import chardet

#Experiment_types---------------------------------------------------------------------------------------------------------------- 
class TGA_exp:
    '''
    A class to represent a TGA experiment

    Attributes
    ----------
    stages : dict
        A dictionary containing the stages of the TGA experiment
    method : str
        A string containing the method used for the TGA experiment
    calibration : str
        A string containing the calibration information for the TGA experiment

    manufacturer : str
        A string containing the manufacturer of the TGA machine
    details :
        Additional metadata of the TGA experiment, only read for TA Instruments Excel files.

    default_weight : str
        The default column name for the weight data
    default_temp : str
        The default column name for the temperature data
    default_time : str
        The default column name for the time data
    time_unit : str
        The unit of time used in the TGA experiment, default is 'min'
    weight_unit : str
        The unit of weight used in the TGA experiment, default is 'mg'
    temp_unit : str
        The unit of temperature used in the TGA experiment, default is '°C'

    Methods
    -------
    add_stage(stage_name, data)
        Adds a stage to the TGA experiment
    get_stage(stage)
        Returns the data for a specific stage
    stage_names()
        Returns the names of the stages
    trim_stage(stage, temp_range)
        Trims a stage to a specified temperature range
    add_method(method)
        Adds a method to the TGA experiment
    combine_stages(stage_names, new_stage_name='comb_stage')
        Combines a list of stages in the TGA experiment into a new stage
    quickplot()
        Generates a simple plot of the TGA data with time as x axis and weight and temperature as y axes.
        Uses the full data if available, otherwise combines stages to create it.
    '''
    def __init__(self, stage_files=None):
        self.date = None
        self.time = None
        self.stages = {}
        self.method = None
        self.calibration = None
        self.manufacturer = None
        self.details = None

        self.default_weight: None | str = None
        self.default_temp: None | str = None
        self.default_time: None | str = None

        self.time_unit = 'min'  # Default time unit is minutes
        self.weight_unit = 'mg'  # Default weight unit is milligrams
        self.temp_unit = '°C'  # Default temperature unit is degrees Celsius


        if stage_files is not None:
            for stage, file in stage_files.items():
                data = pd.read_csv(file)
                self.add_stage(stage, data)
        self.full = None

    def add_stage(self, stage_name, data):
        '''
        Adds a stage to the TGA experiment
        ----------
        Args:
            stage (str): The name of the stage
            data (pandas.DataFrame): The data for the stage
        '''
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Data must be a pandas DataFrame")
        self.stages[stage_name] = data

    def get_stage(self, stage):
        '''
        Returns the data for a specific stage
        ----------
        Args:
            stage (str): The name of the stage to return
        '''
        return self.stages.get(stage, None)
    
    def stage_names(self):
        '''
        Returns the names of the stages
        '''
        return list(self.stages.keys())
    
    def trim_stage(self, stage: str, temp_range: list):
        '''
        Trims a stage to a specified temperature range
        ----------
        Args:
            stage (str): The name of the stage to trim
            temp_range (list): A list containing the minimum and maximum temperature e.g. [200,800]
        '''
        # check if the temperature range is valid
        if len(temp_range) != 2:
            raise ValueError("temp_range must contain two values")
        if max(temp_range) > self.stages[stage][self.default_temp].max():
            raise ValueError("upper bound of temp_range is greater than the maximum temperature in the stage. The max temp in the stage is: "+ str(self.stages[stage][self.default_temp].max()))
        if min(temp_range) < self.stages[stage][self.default_temp].min():
            raise ValueError("lower bound of temp_range is less than the minimum temperature in the stage. The min temp in the stage is: " + str(self.stages[stage][self.default_temp].min()))
        self.stages[stage] = self.stages[stage][(self.stages[stage][self.default_temp] >= min(temp_range)) & (self.stages[stage][self.default_temp] <= max(temp_range))].reset_index()
    def add_method(self, method):
        self.method = method

    def combine_stages(self, stage_names, new_stage_name='comb_stage'):
        """
        Combine a list of stages in a TGA_exp object into a new stage.
        Use 'all' to combine all base stages in the experiment including the label 'stage'. # To-do: This needs to be done better
        """
        if stage_names == 'all':
            stage_names = [i for i in self.stage_names() if 'stage' in i]
        else:
            stage_names = stage_names
        new_stage = pd.concat([self.get_stage(stage_name) for stage_name in stage_names])
        self.add_stage(new_stage_name, new_stage)


    def quickplot(self):
        quickplot(self)





class TGA_pyro(TGA_exp):
    """
    Represents a TGA pyrolysis experiment.

    Attributes:
        Tmax (float): The temperature at which the maximum rate of weight loss occurs.
        T50 (float): The temperature at which 50% of the weight has been lost.
        cracking_stage_name (str): The name of the cracking stage, e.g. 'stage4'.
        burnoff_stage_name (str): The name of the burnoff stage, e.g. 'stage8'.

    """

    def __init__(self, stage_files=None):
        super().__init__(stage_files)
        self.Tmax = None
        self.T50 = None
        self.cracking_stage_name = 'stage4'
        self.burnoff_stage_name = 'stage8'

    def cracking(self):
        """
        Returns the cracking stage data.

        Returns:
            pandas.DataFrame: The cracking stage data.
        """
        return self.stages[self.cracking_stage_name]

    def burnoff(self):
        """
        Returns the burnoff stage data.

        Returns:
            pandas.DataFrame: The burnoff stage data.
        """
        return self.stages[self.burnoff_stage_name]

    def m_cat(self):
        """
        Returns the amount of catalyst in mg.

        Returns:
            float: The amount of catalyst in mg.
        """
        return self.burnoff()['Unsubtracted weight'].min()

    def m_poly(self):
        """
        Returns the amount of polymer.

        Returns:
            float: The amount of polymer.
        """
        return self.cracking()['Unsubtracted weight'].max() - self.m_cat()

    def m_coke(self):
        """
        Returns the amount of coke.

        Returns:
            float: The amount of coke in mg.
        """
        return self.cracking()['Unsubtracted weight'].min() - self.m_cat()

    def pct_loss(self):
        """
        Returns the relative loss of polymer.

        Returns:
            float: The loss of polymer as decimal.
        """
        return self.m_poly() / (self.m_poly() + self.m_cat())

    def P_C_ratio(self):
        """
        Returns the polymer-to-catalyst ratio.

        Returns:
            float: The polymer-to-catalyst ratio.
        """
        return self.m_poly() / self.m_cat()

    def coke_yield(self):
        """
        Returns the coke yield.

        Returns:
            float: The coke yield.
        """
        return self.m_coke() / self.m_poly()


class TGA_pyro_iso(TGA_exp):
    def __init__(self, stage_files=None):
        super().__init__(stage_files)
        self.Tmax = None
        self.T50 = None
    def cracking(self):
        return self.stages['stage5']
    def burnoff(self):
        return self.stages['stage7']
    def m_cat(self):# returns the amount of catalyst
        return self.burnoff()['Unsubtracted weight'].min()
    def m_poly(self): # returns the amount of polymer
        return self.cracking()['Unsubtracted weight'].max() - self.m_cat()
    def m_coke(self):
        return self.cracking()['Unsubtracted weight'].min()-self.m_cat()
    def pct_loss(self):
        return self.m_poly()/(self.m_poly()+self.m_cat())
    def P_C_ratio(self):
        return self.m_poly()/self.m_cat()
    def temp(self):
        return np.round(self.cracking()['Sample Temp.'].iloc[-1],0)


###Parsing functions---------------------------------------------------------------------------------------------------------

def infer_manufacturer(filepath):
    '''
    Infers the manufacturer of the TGA file.
    Returns 'Perkin Elmer', 'Mettler Toledo', or 'TA Instruments (Excel)'
    '''
    # Check if file is an Excel file based on extension
    file_extension = os.path.splitext(filepath)[1].lower()
    if file_extension in ['.xlsx', '.xls']:
        return 'TA Instruments (Excel)'
    
    # For text files, check content
    else:
        with open(filepath, 'rb') as file:
            result = chardet.detect(file.read(10000))
    
        with open(filepath, encoding=result['encoding']) as file:
            first_line = file.readline()
            if first_line[0:8] == 'Filename':
                return 'Perkin Elmer'
            elif first_line[0:5] == 'Title':
                return 'Mettler Toledo'
            else:
                raise ValueError('File format not recognized')

def parse_TGA(filepath, manufacturer='infer', **kwargs):
    '''
    Parses a TGA file and returns a TGA_exp object.
    Infers the manufacturer if not specified, if the type is known ideally use the specific parsing function.
    Currently Supported:
    - Perkin Elmer
    - Mettler Toledo
    
    Optional Parameters:
    For PE TGA files:
    - exp_type: str, the type of TGA experiment. Must be 'general', 'pyro' or 'pyro_iso'. Default is 'general'
    - calculate_DTGA: bool, whether to calculate the derivative of the TGA curve. Default is False
    For MT TGA files:
    - exp_type: str, the type of TGA experiment. Must be 'general', 'pyro' or 'pyro_iso'. Default is 'general'
    - rename_columns: bool, whether to rename the columns to the default ones used in this library (as in Perkin Elmer TGA files). Default is True.
    - calculate_DTGA: bool, whether to calculate the derivative of the TGA curve. Default is False
    - stage split: str or dict or None
        Specifies whether or how to split the TGA experiment into stages.
        If a string, it should be the path to a csv file containing the stage split information. File formating:
        stage, start_index, end_index
        stage1, 0, 100
        stage2, 101, 300
        etc.
        If a dictionary, it should be a dictionary with stage names as keys and indices as values.


    Parameters
    ----------
    filepath : str
        The path to the TGA file
    manufacturer : str
        The manufacturer of the TGA machine. Must be 'Perkin Elmer' or 'Mettler Toledo'. Default is 'infer'
    **kwargs
        Additional keyword arguments to pass to the parsing function

    Returns
    -------
    TGA_exp
        The TGA_exp object
    '''
    if manufacturer == 'infer':
        manufacturer = infer_manufacturer(filepath)
    if manufacturer == 'Perkin Elmer':
        return parse_PE(filepath, **kwargs)
    elif manufacturer == 'Mettler Toledo':
        return parse_MT(filepath, **kwargs)
    elif manufacturer == 'TA Instruments (Excel)':
        return parse_TA_excel(filepath, **kwargs)
    else:
        raise ValueError("manufacturer must be 'Perkin Elmer' or 'Mettler Toledo'")
    
# Parsing    
## Perkin Elmer
def parse_txt(filepath,exp_type = 'general',calculate_DTGA = False): # exp_type can be 'general' or 'pyro'
    '''
    Parses a perkin Elmer ASCII TGA file and returns a TGA_exp object

    Parameters
    ----------
    filepath : str
        The path to the TGA file
    exp_type : str
        The type of TGA experiment. Must be 'general', 'pyro' or 'pyro_iso'. Default is 'general'
    calculate_DTGA : bool
        Whether to calculate the derivative of the TGA curve. Default is False

    Returns
    -------
    TGA_exp
        The TGA_exp object
    '''
    if exp_type == 'general':
        tga_exp_instance = TGA_exp()  # Create an instance of TGA_exp
    elif exp_type == 'pyro':
        tga_exp_instance = TGA_pyro()
    elif exp_type == 'pyro_iso':
        tga_exp_instance = TGA_pyro_iso()
    else:
        raise ValueError("type must be 'general','pyro' or pyro_iso'")
    
    # setting the manufacturer
    tga_exp_instance.manufacturer = 'Perkin Elmer'

    # default column names for the TGA data
    tga_exp_instance.default_weight = 'Unsubtracted weight'
    tga_exp_instance.default_temp = 'Sample Temp.'
    tga_exp_instance.default_time = 'Time'

    names = ['Blank', 'Time', 'Unsubtracted weight', 'Baseline weight',
            'Program Temp.', 'Sample Temp.', 'Sample Purge Flow',
            'Balance purge flow']
    


    def read_section(data):
        try:
            frame = pd.read_table(io.StringIO(data), sep='\t', header=None,skiprows=5, names=names, engine='python')
        except UnicodeDecodeError:
            frame = pd.read_table(io.StringIO(data), sep='\t', header=None,skiprows=5, names=names, engine='python',encoding='latin1')

            
        frame.drop(columns=['Blank'], inplace=True)
        frame['Time'] = frame['Time'].astype(float)
        return frame
    
    def read_last_section(data):
        frame = pd.read_table(io.StringIO(data), sep='\t', header=None,skiprows=5,
                        names=names, engine='python',skipfooter=45)
        frame.drop(columns=['Blank'], inplace=True)
        frame['Time'] = frame['Time'].astype(float)
        return frame


    #checking the file encoding
    with open(filepath, 'rb') as file:
        result = chardet.detect(file.read(10000))

    with open(filepath, encoding=result['encoding']) as full:
        text = full.read()
        split = re.split(r'(\d+\) TGA)', text)
        section_numbers = [int(element[0:-5]) for element in split[1::2]]
        sections = split[2::2]
        
        # Extract date and time from the header
        header = split[0]
        date_time_match = re.search(r'Data Collected:\s+(\d+/\d+/\d+)\s+(\d+:\d+:\d+)', header)
        if date_time_match:
            tga_exp_instance.date = date_time_match.group(1)
            tga_exp_instance.time = date_time_match.group(2)
        
        try:
            calib = re.split(r'TEMPERATURE CALIBRATION INPUTS: ',split[-1])[1]
        except:
            calib = None 
        method = re.split(r'Pre-Run Actions',split[0])[1]
        tga_exp_instance.add_method('Method:'+method)
        tga_exp_instance.calibration = ('Calibration:'+calib)
    
    # Add stages to the TGA_exp instance
    for i in range(len(section_numbers)):
        if i == len(section_numbers)-1:
            tga_exp_instance.add_stage('stage'+str(section_numbers[i]), read_last_section(sections[i]))
        else: 
            tga_exp_instance.add_stage('stage'+str(section_numbers[i]), read_section(sections[i]))
    
    #remove the last 45 rows of the last stage as they contain the calibration information
    tga_exp_instance.stages['stage'+str(section_numbers[-1])] = tga_exp_instance.stages['stage'+str(section_numbers[-1])].iloc[:-45]

    # Combine the stages into a full stage
    tga_exp_instance.full = pd.concat([tga_exp_instance.stages[stage_name] for stage_name in tga_exp_instance.stage_names() if 'stage' in stage_name])


    if calculate_DTGA == True:
        if exp_type != 'pyro':
            raise Exception('DTGA calculation only implemented for pyro')
        elif exp_type == 'pyro':
            return calc_DTGA_pyro(tga_exp_instance)
        
    else:
        return tga_exp_instance

# adding alias

parse_PE = parse_txt


# def calc_DTGA_all(tga_exp):
#     with warnings.catch_warnings():
#         warnings.simplefilter("ignore")
#         for stage in [tga_exp.stages[stage_name] for stage_name in tga_exp.stage_names()]:

#             stage.drop(stage.index[stage['Sample Temp.'] == stage['Sample Temp.'].iloc[0]], inplace=True) # removing a couple datapoints to avoid infinities
#             avering_window = 30
            
#             rel_weight_twl = (stage['Unsubtracted weight']/stage['Unsubtracted weight'].max()).to_numpy()
#             rel_weight_pwl = ((stage['Unsubtracted weight']-tga_exp.m_cat())/tga_exp.m_poly()).to_numpy()

#             stage['rel_weight_twl'] = rel_weight_twl
#             stage['rel_weight_pwl'] = rel_weight_pwl

#             temp = stage['Sample Temp.'].to_numpy()

#             stage['DTGA_pwl'] = -np.gradient(rel_weight_pwl,temp)
#             stage['DTGA_pwl']=stage['DTGA_pwl'].rolling(avering_window,win_type='triang').mean()
#             stage['DTGA_twl'] = -np.gradient(rel_weight_twl,temp)
#             stage['DTGA_twl']=stage['DTGA_twl'].rolling(avering_window,win_type='triang').mean()
#     return tga_exp

## # Mettler Toledo
def parse_MT(filepath,exp_type = 'general', rename_columns=True, stage_split= None, calculate_DTGA = False):
    '''
    Parses a Mettler Toldeo TGA file and returns a TGA_exp object

    Parameters
    ----------
    filepath : str
        The path to the TGA file
    exp_type : str
        The type of TGA experiment. Must be 'general', 'pyro' or 'pyro_iso'. Default is 'general'
    rename_columns : bool
        Whether to rename the columns to the default ones used in this library (as in Perkin Elmer TGA files). Default is True.
        When False, the original column names of the Mettler Toledo file are used.
    stage split : str or dict or None
        Specifies whether or how to split the TGA experiment into stages.
        If a string, it should be the path to a csv file containing the stage split information. File formating:
        stage, start_index, end_index
        stage1, 0, 100
        stage2, 101, 300
        etc.
        If a dictionary, it should be a dictionary with stage names as keys and indices as values.
    calculate_DTGA : bool
        Whether to calculate the derivative of the TGA curve. Default is False

    Returns
    -------
    TGA_exp
        The TGA_exp object

    '''

    with open(filepath, 'rb') as file:
        result = chardet.detect(file.read(10000))  # Read only the first 10,000 bytes

    if exp_type == 'general':
        tga_exp_instance = TGA_exp()  # Create an instance of TGA_exp
    elif exp_type == 'pyro':
        tga_exp_instance = TGA_pyro()
    elif exp_type == 'pyro_iso':
        tga_exp_instance = TGA_pyro_iso()
    else:
        raise ValueError("exp_type must be 'general','pyro' or pyro_iso'")
    
    # setting the manufacturer
    tga_exp_instance.manufacturer = 'Mettler Toledo'

    # default column names for the TGA data
    if rename_columns:
        tga_exp_instance.default_weight = 'Weight'
        tga_exp_instance.default_temp = 'Sample Temp.'
        tga_exp_instance.default_time = 'Time(min)'
    else:
        tga_exp_instance.default_weight = 'Value'
        tga_exp_instance.default_temp = 'Ts'
        tga_exp_instance.default_time = 't'


    with open(filepath, encoding=result['encoding']) as full:
        text = full.read()
        
        # Extract date and time from the header
        date_time_match = re.search(r'FileName:[\s\S]*?(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})', text)
        if date_time_match:
            tga_exp_instance.date = date_time_match.group(1)
            tga_exp_instance.time = date_time_match.group(2)
        
        split_text = text.split('Curve:')[1].split('LastKeyWD:')[0]
        original_columns = split_text.split('\n')[1].split()

        # in this case the original colum names are ['Index', 't', 'Ts', 'Tr', 'Value']
        # where t is the time in s, Ts is the sample temperature, Tr is the chamber temperature and Value is the weight in mg
        # for consistence, the columns are renamed by defualt
        if rename_columns:
            column_names = ['Index', 'Time', 'Sample Temp.', 'Reactor Temp.', 'Weight']
        else:
            column_names = original_columns
        frame = pd.read_table(io.StringIO(split_text),delimiter=r'\s+',header=None,skiprows=3,engine='python',names=column_names, index_col='Index')
        
        # for PE TGAs (the daufault) the time is in minutes, not seconds. Adjusting for consistency
        frame['Time(min)'] = frame['Time']/60

        #adding full
        tga_exp_instance.full = frame

        # splitting the stages. Either with a csv file (see example for formatting)
        if type(stage_split) == str:
            split_seperator = pd.read_csv(stage_split, header=0)
            for row in split_seperator.iterrows():
                tga_exp_instance.add_stage(row[1]['stage'], frame.loc[row[1]['start_index']:row[1]['end_index']])
        elif type(stage_split) == dict:
            # stage_split should be a dictionary with stage names as keys and indices as values
            # example: stage_split = {'stage1': {'start_index': 0, 'end_index': 100}, 'stage2': {'start_index': 101, 'end_index': 300}}
            for stage, indices in stage_split.items():
                tga_exp_instance.add_stage(stage, frame.loc[indices['start_index']:indices['end_index']])
        elif stage_split == None:
            tga_exp_instance.add_stage('stage1', frame)

        if calculate_DTGA == True:
            if exp_type != 'pyro':
                raise Exception('DTGA calculation only implemented for pyro')
            elif exp_type == 'pyro':
                return calc_DTGA_pyro(tga_exp_instance)
        else:
            return tga_exp_instance


def parse_TA_excel(filepath,exp_type = 'general',calculate_DTGA = False): # exp_type can be 'general' or 'pyro'
    '''
    Parses a TA Instruments excel TGA file and returns a TGA_exp object

    Parameters
    ----------
    filepath : str
        The path to the TGA file
    exp_type : str
        The type of TGA experiment. Must be 'general', 'pyro' or 'pyro_iso'. Default is 'general'
        Presently only 'general' is supported for this format
    calculate_DTGA : bool
        Whether to calculate the derivative of the TGA curve. Default is False
        Currently not supported for TA Instruments.

    Returns
    -------
    TGA_exp
        The TGA_exp object
    '''
    if exp_type == 'general':
        tga_exp_instance = TGA_exp()  # Create an instance of TGA_exp
    elif exp_type == 'pyro':
        raise NotImplementedError("pyro class not implemented for TA Instruments TGA files")
        #tga_exp_instance = TGA_pyro()
    elif exp_type == 'pyro_iso':
        raise NotImplementedError("pyro_iso class not implemented for TA Instruments TGA files")
        #tga_exp_instance = TGA_pyro_iso()  
    else:
        raise ValueError("only 'general' is supported for TA Instruments TGA files")
    
    # setting the manufacturer
    tga_exp_instance.manufacturer = 'TA Instruments (Excel)'

    # default column names for the TGA data
    tga_exp_instance.default_temp = 'Temperature (C)'
    tga_exp_instance.default_weight = 'Weight (mg)'
    tga_exp_instance.default_time = 'Time (min)'

    # parsing
    excel = pd.ExcelFile(filepath)
    stage_names = excel.sheet_names
    details = pd.read_excel(excel, sheet_name=stage_names[0], header=None, names=['label', 'value'], index_col=0)

    # adding metadata
    tga_exp_instance.details = details
    tga_exp_instance.date = details.loc['rundate']['value'].date()
    tga_exp_instance.time = details.loc['rundate']['value'].time() 

    def read_TA_stage(excel: pd.ExcelFile, stage_name: str) -> pd.DataFrame:
        """Read a stage from the TA instrument excel file."""
        return pd.read_excel(excel, sheet_name=stage_name, skiprows=3, names=['Time (min)', 'Temperature (C)', 'Weight (mg)', 'Weight (%)'])

    for stage in enumerate(stage_names):
        if stage[0] != 0:
            name = 'stage{}_{}'.format(stage[0], stage[1])
            tga_exp_instance.add_stage(stage_name=name,data=read_TA_stage(excel, stage[1]))

    # generating full
    tga_exp_instance.combine_stages('all', 'full')
    tga_exp_instance.full = tga_exp_instance.stages['full']

    if calculate_DTGA == True:
        raise NotImplementedError("DTGA calculation not implemented for TA Instruments TGA files")
        # if exp_type != 'pyro':
        #     raise Exception('DTGA calculation only implemented for pyro')
        # elif exp_type == 'pyro':
        #     return calc_DTGA_pyro(tga_exp_instance)
        
    else:
        return tga_exp_instance













# Functions
def calc_DTGA_pyro(tga_exp):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for stage in [tga_exp.cracking(),tga_exp.burnoff()]:
            stage.drop(stage.index[stage['Sample Temp.'] == stage['Sample Temp.'].iloc[0]], inplace=True) # removing a couple datapoints to avoid infinities
            avering_window = 30
            
            rel_weight_twl = (stage['Unsubtracted weight']/stage['Unsubtracted weight'].max()).to_numpy()
            rel_weight_pwl = ((stage['Unsubtracted weight']-tga_exp.m_cat())/tga_exp.m_poly()).to_numpy()

            stage['rel_weight_twl'] = rel_weight_twl
            stage['rel_weight_pwl'] = rel_weight_pwl

            temp = stage['Sample Temp.'].to_numpy()

            stage['DTGA_pwl'] = -np.gradient(rel_weight_pwl,temp)
            stage['DTGA_pwl']=stage['DTGA_pwl'].rolling(avering_window,win_type='triang').mean()
            stage['DTGA_twl'] = -np.gradient(rel_weight_twl,temp)
            stage['DTGA_twl']=stage['DTGA_twl'].rolling(avering_window,win_type='triang').mean()
    return tga_exp


def calc_DTGA_stage(tga_exp: TGA_exp, stage_name: str,x = 'Temp',y='relative',avering_window: int = 30)->TGA_exp:
    """
    Calculate the derivative the TGA curve for each stage in the TGA_exp object, average over window

    Args:
        tga_exp (TGA_exp): The TGA_exp object
        stage_name (str): The name of the stage to calculate the derivative for
        x (str): The x-axis to use for the derivative calculation. Must be 'Time' or 'Temp'
        y (str): The y-axis to use for the derivative calculation. Must be 'relative' or 'absolute'
        avering_window (int): The window to average the derivative over. Default is 30
    Returns:
        TGA_exp: The TGA_exp object with the derivative added to the stage
    """
    # enabling using 'cracking' or 'burnoff' as stage_name
    if stage_name == 'cracking':
        stage_name = tga_exp.cracking_stage_name
    elif stage_name == 'burnoff':
        stage_name = tga_exp.burnoff_stage_name

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        if stage_name == 'full':
            stage = tga_exp.full
        else:
            stage = tga_exp.get_stage(stage_name)
        if x == 'Time':
            dx = stage[tga_exp.default_time].to_numpy()
        elif x == 'Temp':
            dx = stage[tga_exp.default_temp].to_numpy()
        else:
            raise ValueError("x must be 'Time' or 'Temp'")
        
        if y == 'relative':
            dy = (stage[tga_exp.default_weight]/stage[tga_exp.default_weight].max()).to_numpy()
        elif y == 'absolute':
            dy = stage[tga_exp.default_weight].to_numpy()
        else:
            raise ValueError("y must be 'relative' or 'absolute'")

        stage['DTGA'+'_'+x+'_'+y] = -np.gradient(dy,dx)
        stage['DTGA'+'_'+x+'_'+y] = stage['DTGA'+'_'+x+'_'+y].rolling(avering_window,win_type='triang').mean()
    return tga_exp


def combine_stages(tga_exp: TGA_exp, stage_names, new_stage_name: str)->TGA_exp:
    """
    Combines a list of stages in a TGA_exp object into a new stage

    Parameters
    ----------
    tga_exp : TGA_exp
        The TGA_exp object
    stage_names : list or 'all'
        The names of the stages to combine, e.g. ['stage1', 'stage2']
        Use 'all' to combine all base stages in the experiment including the label 'stage'.
    new_stage_name : str
        The name of the new stage e.g. 'full'
    """
    if stage_names == 'all':
        stage_names = [i for i in tga_exp.stage_names() if 'stage' in i]
    else:
        stage_names = stage_names
    new_stage = pd.concat([tga_exp.get_stage(stage_name) for stage_name in stage_names])
    tga_exp.add_stage(new_stage_name, new_stage)
    return tga_exp

def trim_stage(tga_exp: TGA_exp, stage_name: str, min_temp: float, max_temp: float)->TGA_exp:
    """
    Trim a stage in a TGA_exp object to a specified temperature range
    """
    stage = tga_exp.get_stage(stage_name)
    stage = stage[(stage[tga_exp.default_temp] >= min_temp) & (stage[tga_exp.default_temp] <= max_temp)]
    tga_exp.add_stage(stage_name, stage)
    return tga_exp


def calc_Tmax_exp(tga_exp,stage='cracking'):
    if stage == 'cracking':
        stage_select = tga_exp.cracking()
    elif stage == 'burnoff':
        stage_select = tga_exp.burnoff()
    Tmax = stage_select[tga_exp.default_temp].loc[stage_select['DTGA_twl'].idxmax()]
    return Tmax


def calc_T50_old(tga_exp,stage='cracking'):
    if stage == 'cracking':
        stage_select = tga_exp.cracking()
    elif stage == 'burnoff':
        stage_select = tga_exp.burnoff()
    T50 = stage_select[tga_exp.default_temp].loc[stage_select['rel_weight_pwl'].sub(0.5).abs().idxmin()]
    return T50


def quickplot(tga_exp, show=True):
    '''
    Generates a simple plot of the TGA data with time as x axis and weight and temperature as y axes.
    Uses the full data if available, otherwise combines stages to create it.
    
    Parameters
    ----------
    tga_exp : TGA_experiment
        The TGA experiment object to plot
    show : bool, optional
        Whether to display the plot, default True. Set to False for testing.
    
    Returns
    -------
    fig : matplotlib.figure.Figure
        The figure object containing the plot
    '''
    # If full data doesn't exist yet, create it
    if tga_exp.full is None:
        tga_exp.combine_stages('all', 'full')
        full_data = tga_exp.stages['full']
    else:
        full_data = tga_exp.full
        
    fig, ax = plt.subplots()
    ax2 = ax.twinx()
    ax.plot(full_data[tga_exp.default_time], full_data[tga_exp.default_weight], label='Sample weight', color='tab:blue')
    ax2.plot(full_data[tga_exp.default_time], full_data[tga_exp.default_temp], linestyle='--')
    ax.set_xlabel('Time ({})'.format(tga_exp.time_unit))
    ax2.set_xlabel('Time ({})'.format(tga_exp.time_unit))
    ax.set_ylabel('Sample weight ({})'.format(tga_exp.weight_unit))
    ax2.set_ylabel('Temperature ({})'.format(tga_exp.temp_unit))
    ax.set_xlim(0, full_data[tga_exp.default_time].max())
    if show:
        plt.show()
    return fig



# Functions applying to stages:---------------------------------------------------------------
# Making these functions apply to stages for different file  formats is not ideally implemented. It might be refactored offer more convenience.

def calc_Tmax(stage, temp_col='Sample Temp.'):
    '''
    For a stage in the experiment, returns the temperature at which the derivative of the TGA curve is max.
    '''
    if not isinstance(stage, pd.DataFrame):
        raise ValueError("stage must be a pandas DataFrame")
    if temp_col not in stage.columns:
        raise ValueError(f"temp_col '{temp_col}' not found in stage columns and must be specified manually from {stage.columns}")

    #find which column contaions 'DTGA'
    DTGA_col = [col for col in stage.columns if 'DTGA' in col]
    if len(DTGA_col) == 0:
        raise ValueError("No DTGA column found in stage")
    Tmax = stage[temp_col].loc[stage[DTGA_col[0]].idxmax()]
    return Tmax


def calc_T50(stage: pd.DataFrame)->float:
    '''
    For a stage in the experiment, returns the temperature at which 50% of the weight has been lost.
    '''
    if 'Sample Temp.' not in stage.columns or 'rel_weight_pwl' not in stage.columns:
        raise ValueError("stage must contain 'Sample Temp.' and 'rel_weight_pwl' columns")
    T50 = stage['Sample Temp.'].loc[stage['rel_weight_pwl'].sub(0.5).abs().idxmin()]
    return T50


def get_color(min_rel_weight,cmap='viridis'):
    '''
    Returns a color for the TGA plot based on the minimum relative weight.
    Parameters:
    ----------
    min_rel_weight : float
        The minimum relative weight of the sample
    cmap : str
        The colormap to use. Default is 'viridis'
    Returns:
    -------
    color : tuple
        The color for the TGA plot
    '''
    norm = plt.Normalize(0, 1.07)
    color = plt.get_cmap(cmap)(norm(min_rel_weight))
    return color


def get_coke_content(stage, weight_col='Unsubtracted weight'):
    '''
    For a stage in the experiment, returns the coke content as a fraction of the total weight.
    '''
    if weight_col not in stage.columns:
        raise ValueError(f"weight_col '{weight_col}' not found in stage columns and must be specified manually from {stage.columns}")
    
    catweight = stage[weight_col].min()
    cokeweight = stage[weight_col].max() - catweight
    return cokeweight/(catweight+cokeweight)
