"""
The purpose of this script is to calculate the total area of undisturbed habitat
for BWC that is in different protected zones.
The inputs are:
    - regions file (single file)
    - "protected" areas file (changes on different runs, may loop through a set)
    - undisturbed habitat file
"""

# Imports
import arcpy
import os

# env
arcpy.env.overwriteOutput = True

# inputs
range_NT1 = r""
regions = r"" # Admin or land claims. Can overlap. Shouldn't.
regions_name_field = ""
areas = r"" # Such as "protected" and "conservation" areas. Could also iterate through several individual protected areas.
areas_field = "" # Names of the specific areas.
undist = r""
output_location = r"" # Script creates an output file geodatabase here.
run_name = "TEST1"

# defaults
sr = arcpy.SpatialReference(102001) # Canada Albers Equal Area Conic

# Create output file geodatabase
################################
arcpy.CreateFileGDB_management(output_location, run_name)
# assign as the workspace
wksp = os.path.join(output_location, run_name)
arcpy.env.workspace = wksp

# Clip the regions to NT1
################################
# Clip
regions_NT1 = "regions_clipped_to_range"
arcpy.Clip_analysis(regions, range_NT1, regions_NT1)
# reassign "regions"
regions = regions_NT1

# Create region-specific output feature datasets
################################
region_list = []
with arcpy.da.SearchCursor(regions, (regions_name_field,)) as cursor:
    for row in cursor:
        region = row[0].replace(" ", "_")
        arcpy.CreateFeatureDataset_management(wksp, row[0], sr)
        region_list.append(region) # for easier dataset access later

# Iterate through the regions and create the region-specific "areas" AND create
# the region-specific undist patches
################################
# region iteration
with arcpy.da.SearchCursor(regions,(regions_name_field, "SHAPE@")) as cursor:
    for row in cursor:
        region = row[0].replace(" ", "_")
        # Clip the "areas" to the regions
        out_fc = "/{0}/{1}".format(region, region + "_areas")
        arcpy.Clip_analysis(areas, row[1], out_fc)
        # Clip the undist to the regions
        out_fc = "/{0}/{1}".format(region, region + "_undist")
        arcpy.Clip_analysis(undist, row[1], out_fc)

# Iterate through the regions-specific areas and clip undist to them
################################
# iterate through region datasets
for region in arcpy.ListDatasets():
    # grab region-specific areas file
    for area in arcpy.ListFeatureClasses("*_areas", "", region):
        # iterate through areas and clip undist to them
        with arcpy.da.SearchCursor(area, (areas_field, "SHAPE@")) as cursor:
            for row in cursor:
                out_fc = "/{0}/{1}".format(region,
                region + row[0].replace(" ", "_") + "_undist")
                arcpy.Clip_analysis(undist, row[1], out_fc)

# Create output csv with desired areas
################################
# To be done