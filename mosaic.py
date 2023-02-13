import arcpy
import os
from glob import glob
import shutil
arcpy.env.verbose = True
def recreate_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
    return path

DATA_DIR = "data/20221220_Sudol"
MOSAIC_DIR = os.path.abspath(f"{DATA_DIR}/mosaic")
recreate_dir(MOSAIC_DIR)
#load rasters from 
GEOTIF_UNCAL_DIR = os.path.abspath(f"{DATA_DIR}/geotif_uncal")
GEOTIF_CAL_DIR = os.path.abspath(f"{DATA_DIR}/geotif_cal")
print("Mosaicking uncalibrated images...")
files = glob(f"{GEOTIF_UNCAL_DIR}/*.tif")
print("MEAN")
arcpy.MosaicToNewRaster_management(files, MOSAIC_DIR, "mosaic_uncal_MEAN.tif", "", "32_BIT_FLOAT", "", 1, "MEAN", "FIRST")
print("LAST")
arcpy.MosaicToNewRaster_management(files, MOSAIC_DIR, "mosaic_uncal_LAST.tif", "", "32_BIT_FLOAT", "", 1, "LAST", "FIRST")
print("Mosaicking calibrated images...")
files = glob(f"{GEOTIF_CAL_DIR}/*.tif")
print("MEAN")
arcpy.MosaicToNewRaster_management(files, MOSAIC_DIR, "mosaic_cal_MEAN.tif", "", "32_BIT_FLOAT", "", 1, "MEAN", "FIRST")
print("LAST")
arcpy.MosaicToNewRaster_management(files, MOSAIC_DIR, "mosaic_cal_LAST.tif", "", "32_BIT_FLOAT", "", 1, "LAST", "FIRST")