import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from data_processing import select_input_file, convert_file_and_save

## Create the main application window and set title for main window:
app = tk.Tk()                                                                       
app.title("Data Format Converter")                                                        
app.geometry("400x300")                                   # set size

## Create label with vertical padding of 10 pixels:
tk.Label(app, text="Select desired data format to export to:").pack(pady=10) 
        
## Create a variable to hold the selected output format and set default format as csv:
output_format = tk.StringVar(value='csv')                                                          
        
## List of formats: 
formats = ['csv', 'excel', 'json', 'parquet', 'feather', 'orc', 'hdf5', 'netcdf', 'avro']
        
## Create combobox for format selection. Combobox will be placed inside app container:     
format_dropdown = ttk.Combobox(app, textvariable=output_format, values=formats)
format_dropdown.pack(pady=10)                                                                     
        
## Function to open file dialog:
def select_file_dialog():
    input_path = filedialog.askopenfilename(      
        title="Select Input File", 
        filetypes=[("All Files", "*.*")])                  # askopenfilename to browse file system and select a file, returns the file path of the selected file as a string
    df = select_input_file(input_path)                     # call function from data_processing.py
    
    print(f"Selected input path: {input_path}")

    ## Function to open file dialog to specify the output file path:
    output_path = filedialog.asksaveasfilename(   
        title="Save As",
        defaultextension=f".{output_format.get()}",
        filetypes=[
            ("CSV Files", "*.csv"),
            ("Excel Files", "*.xlsx"),
            ("JSON Files", "*.json"),
            ("Parquet Files", "*.parquet"),
            ("Feather Files", "*.feather"),
            ("HDF5 Files", "*.h5"),
            ("ORC Files", "*.orc"),
            ("NetCDF Files", "*.nc"),
            ("AVRO Files", "*.avro")                       # asksaveasfilename to open a dialog where user choose location, type in filename, save 
        ]
    )

    print(f"Selected output path: {output_path}")

    ## Create function to convert and save the file:
    if input_path and output_path:                         # ensure both paths are valid
        file_format = output_format.get()                  # obtain the selected file format from the combobox, this format will be apply to output file
        
        message = convert_file_and_save(df, output_path, file_format) # call function from data_processing.py
        messagebox.showinfo("Success", message)

## Create button to select file and convert, with vertical padding of 20 pixels:
tk.Button(app, text="Select File and Convert", command=select_file_dialog).pack(pady=20)

app.mainloop()




