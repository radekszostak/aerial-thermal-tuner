import arcpy
import os
from glob import glob
import shutil
#arcpy.env.verbose = True
def recreate_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
    return path

DATA_DIR = "data/20211215_kocinka_rybna"
MOSAIC_DIR = os.path.abspath(f"{DATA_DIR}/mosaic")
recreate_dir(MOSAIC_DIR)
#load rasters from
GEOTIF_INIT_DIR = os.path.abspath(f"{DATA_DIR}/geotif_init")
GEOTIF_RAW_DIR = os.path.abspath(f"{DATA_DIR}/geotif_raw")
GEOTIF_DIVIGNETTE_DIR = os.path.abspath(f"{DATA_DIR}/geotif_devignette")
GEOTIF_CAL_DIR = os.path.abspath(f"{DATA_DIR}/geotif_cal")
    # print("Mosaicking initial images...")
    # files = glob(f"{GEOTIF_INIT_DIR}/*.tif")
    # print("MEAN")
    # arcpy.MosaicToNewRaster_management(files, MOSAIC_DIR, "mosaic_init_MEAN.tif", "", "32_BIT_FLOAT", "", 1, "MEAN", "FIRST")
    # print("LAST")
    # arcpy.MosaicToNewRaster_management(files, MOSAIC_DIR, "mosaic_init_LAST.tif", "", "32_BIT_FLOAT", "", 1, "LAST", "FIRST")
print("Mosaicking raw images...")
files = glob(f"{GEOTIF_RAW_DIR}/*.tif")
# print("MEAN")
# arcpy.MosaicToNewRaster_management(files, MOSAIC_DIR, "mosaic_raw_MEAN.tif", "", "32_BIT_FLOAT", "", 1, "MEAN", "FIRST")
print("LAST")
arcpy.MosaicToNewRaster_management(files, MOSAIC_DIR, "mosaic_raw_LAST.tif", "", "32_BIT_FLOAT", "", 1, "LAST", "FIRST")
# print("Mosaicking devignetted images...")
# files = glob(f"{GEOTIF_DIVIGNETTE_DIR}/*.tif")
# print("MEAN")
# arcpy.MosaicToNewRaster_management(files, MOSAIC_DIR, "mosaic_devignette_MEAN.tif", "", "32_BIT_FLOAT", "", 1, "MEAN", "FIRST")
# print("LAST")
# arcpy.MosaicToNewRaster_management(files, MOSAIC_DIR, "mosaic_devignette_LAST.tif", "", "32_BIT_FLOAT", "", 1, "LAST", "FIRST")
print("Mosaicking calibrated images...")
files = glob(f"{GEOTIF_CAL_DIR}/*.tif")
# # print("MEAN")
# # arcpy.MosaicToNewRaster_management(files, MOSAIC_DIR, "mosaic_cal_MEAN.tif", "", "32_BIT_FLOAT", "", 1, "MEAN", "FIRST")
print("LAST")
arcpy.MosaicToNewRaster_management(files, MOSAIC_DIR, "mosaic_cal_LAST.tif", "", "32_BIT_FLOAT", "", 1, "LAST", "FIRST")