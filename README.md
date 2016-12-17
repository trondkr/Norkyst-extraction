# Norkyst-extraction

These scripts calculate the diurnal variability during the month of June for range of years and writes the results to NetCDF files. You need to 
1. Compile the Fortran file using the command: 
    
    f2py --verbose  -c -m iso iso.f90
    
2. Edit the path to the HIS ROMS files in the file `norkyst-extraction.py` and then run the script
3. Edit the options in the `calculateDiurnalAnomalies.py` and run the script
4. The result is a NetCDF file containing the diurnal anomalies and a set of figures (one for each hour 1-24)
