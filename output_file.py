import pandas as pd
import fastavro as fa ## for avro
import pyarrow.parquet as pq
import pyarrow as pa ## for ORC
import pyarrow.orc as orc ## for ORC
import xarray as xr ## for Netcdf

## Select the data type to convert into:

def export_to_csv(df, output_path):                        # csv
    df.to_csv(output_path, index=False)
def export_to_excel(df, output_path):                      # excel
    df.to_excel(output_path, index=False)
def export_to_json(df, output_path):                       # json
    df.to_json(output_path, orient='records', lines=True)
def export_to_parquet(df, output_path):                    # parquet
    pq.to_parquet(output_path)
def export_to_feather(df, output_path):                    # feather
    df.to_feather(output_path)
def export_to_hdf5(df, output_path):                       # hdf5
    df.to_hdf(output_path, key='df', mode='w')

## Special data types ORC, NetCDF, AVRO:

def export_to_orc(df, output_path):                        # orc
    orc_data = pa.Table.from_pandas(df)           # convert df to arrow table
    with open(output_path, 'wb') as orc_file:     # open the file in binary write mode
        orc.write_table(orc_data, orc_file)       # write arrow table to ORC file   

def export_to_netcdf(df, output_path):                     # netcdf
    netcdf_data = xr.Dataset.from_dataframe(df)   # convert df to xarray Dataset
    netcdf_data.to_netcdf(output_path)            # write dataset to NetCDF file

def export_to_avro(df, output_path):                       # avro
    records = df.to_dict(orient='records')        # convert the df to a list of dictionaries (each dic is a record in avro file)
    schema = {                                    # define the Avro schema with all fields as strings (keep all as string for now)
        "type": "record",                         # indicate this is a record type
        "name": "Converted_Record",               # name of the record type                              
        "fields": [{"name": col, "type": "string"} for col in df.columns]
    }
    with open(output_path, 'wb') as avro_file:    # open the file in binary write mode
            fa.writer(avro_file, schema, records) # write records and schema to the Avro file

## This function simplifies exporting data to different formats:
def export_data(df, output_path, file_format):
    file_format_list = {
        'csv': export_to_csv,
        'excel': export_to_excel,
        'json': export_to_json,
        'parquet': export_to_parquet,
        'feather': export_to_feather,
        'orc': export_to_orc,
        'hdf5': export_to_hdf5,
        'netcdf': export_to_netcdf,
        'avro': export_to_avro
    }
    
    if file_format in file_format_list:
        file_format_list[file_format](df, output_path)
    else:
        raise ValueError("Unsupported file format")
