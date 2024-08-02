import pandas as pd
import fastavro as fa ## avro
import pyarrow.parquet as pq ## Parquet - columnar format
import pyarrow.orc as orc ## ORC - optimized row columnar
import pyarrow.feather as fe ## feather
import xarray as xr ## NetCDF - network common data form


## Select the file with data format that need data type conversion:

def load_data(input_path):
    if input_path.endswith('.csv'):                                   # csv
        return pd.read_csv(input_path)
    elif input_path.endswith('.xlsx') or input_path.endswith('.xls'): # excel
        return pd.read_excel(input_path)          
    elif input_path.endswith('.json'):                                # json
        return pd.read_json(input_path)
    elif input_path.endswith('.parquet'):                             # parquet
        return pd.read_parquet(input_path)
    elif input_path.endswith('.feather'):                             # feather
        return fe.feather.read_table(input_path).to_pandas()
    elif input_path.endswith('.h5') or input_path.endswith('.hdf5'):  # hdf5
        return pd.read_hdf(input_path)
    
    ## Special data types ORC, NetCDF, AVRO require more steps:

    elif input_path.endswith('.orc'):                                 # orc
        orc_data = orc.read_table(input_path)            # read the ORC file into a pyarrow table
        orc_df = orc_data.to_pandas()                    # convert the pyarrow Table to a pandas df
        return orc_df
    
    elif input_path.endswith('.nc'):                                  #netcdf
        netcdf_data = xr.open_dataset(input_path)        # Open the NetCDF file into an xarray dataset
        netcdf_df = netcdf_data.to_dataframe()           # Convert the xarray dataset to a pandas df
        return netcdf_df
    
    elif input_path.endswith('.avro'):                                #avro
        with open(input_path, 'rb') as avro_file:        # open the file in binary read mode
            avro_data = fa.reader(avro_file)
            avro_df = [record for record in avro_data]   # read all records from the file
        return pd.DataFrame(avro_df)                     # convert Avro records to a df
    else:
        raise ValueError("Unsupported file type")