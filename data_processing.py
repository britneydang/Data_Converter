import pandas as pd
from source_file import load_data
from output_file import export_data

## Load data from the selected input file:
def select_input_file(input_path):
    df = load_data(input_path)
    return df

## Convert the specified file format and save to specified file location:
def convert_file_and_save(df, output_path, file_format):
    export_data(df, output_path, file_format)
    return "File is successfully converted and saved."