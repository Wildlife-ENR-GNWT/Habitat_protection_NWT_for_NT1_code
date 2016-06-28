"""
The purpose of this script is to calculate the total area of undisturbed habitat
for BWC that is in different protected zones.
The inputs are:
    - range file (single file)
    - regions file (single file)
    - "protected" areas file (single feature class that may contain multiple features)
        - Overlap is not accounted for if you are looking for cumulative coverage numbers.
    - undisturbed habitat file
"""
# Imports
import arcpy
import os
import csv

### env
##arcpy.env.overwriteOutput = True # Enable this if you want to overwrite outputs. Use at your own risk!

# inputs (THIS IS WHAT YOU WANT TO MESS AROUND WITH JAMES)
range_NT1 = r"H:\GIS\BWC_base_files\BWC_base_files.gdb\boundaries\NT1"
# ENABLE ONE OF THESE

regions_name_field = "REGION"
# ENABLE ONE OF THESE
areas = r"H:\Boreal_Caribou_Range_Plan\GIS\Habitat_protection_NWT_for_NT1\analyzed_data\redo_protected_areas\main.gdb\scratch\scratch_current_protected"
## Original run files
##areas = r"H:\Boreal_Caribou_Range_Plan\GIS\Habitat_protection_NWT_for_NT1\analyzed_data\areas_2.gdb\protected_areas_CAM"
##areas = r"H:\Boreal_Caribou_Range_Plan\GIS\Habitat_protection_NWT_for_NT1\analyzed_data\areas_2.gdb\conservation_areas_CAM_union"
##areas = r"H:\Boreal_Caribou_Range_Plan\GIS\Habitat_protection_NWT_for_NT1\analyzed_data\areas_2.gdb\combo_areas_CAM" # Not really a useful one, but here anyway because I ran it.
##areas = r"H:\Boreal_Caribou_Range_Plan\GIS\Habitat_protection_NWT_for_NT1\analyzed_data\areas_3.gdb\DC_SS_current_withdrawals" # Probably less useful version. Use the one below.
## Dissolved areas files
##areas = r"H:\Boreal_Caribou_Range_Plan\GIS\Habitat_protection_NWT_for_NT1\analyzed_data\reworked_runs.gdb\protected_areas_CAM_diss"
##areas = r"H:\Boreal_Caribou_Range_Plan\GIS\Habitat_protection_NWT_for_NT1\analyzed_data\reworked_runs.gdb\conservation_areas_CAM_diss"
##areas = r"H:\Boreal_Caribou_Range_Plan\GIS\Habitat_protection_NWT_for_NT1\analyzed_data\reworked_runs.gdb\combo_areas_CAM_diss"
##areas = r"H:\Boreal_Caribou_Range_Plan\GIS\Habitat_protection_NWT_for_NT1\analyzed_data\reworked_runs.gdb\DC_SS_current_withdrawals"
areas_field = "unique_area_name" # Names of the specific areas.
carry_over_fields = ["additional_notes", "Protection_duration","protection_level"] # You can input any number of fields that are in the original "areas" file. They will be added to the output. ONLY WORKS IF NO DUPLICATE UNIQUE AREA NAMES.
undist = r"H:\GIS\BWC_base_files\BWC_base_files.gdb\undisturbed\NT1_undisturbed_2015"
# SET AN OUTPUT LOCATION AS A FOLDER SOMEWHERE.
output_location = r"H:\Boreal_Caribou_Range_Plan\GIS\Habitat_protection_NWT_for_NT1\analyzed_data" # Script creates an output file geodatabase here.
# GIVE THE OUTPUT A NAME (no spaces)
run_name = "June23_run2_ENRITI_withWater_current_protected"
out_csv_name = run_name.replace(" ", "_") + ".csv"

# defaults
sr = arcpy.SpatialReference(102001) # Canada Albers Equal Area Conic

# Create output file geodatabase
################################
arcpy.CreateFileGDB_management(output_location, run_name)
# assign as the workspace
wksp = os.path.join(output_location, run_name + ".gdb")
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
        arcpy.CreateFeatureDataset_management(wksp, region, sr)
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
        out_fc = "/{0}/{1}".format(region, region + "_undisturbed")
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
##                region + "_area_" + row[0].replace(" ", "_").replace("'", "").replace("(", "").replace(")", "") + "_undist")
                # MIGHT HAVE FIXED THE ERRORNEOUS NAMING GOING ON IN NAMING IN ONE PLACE GOD ONLY KNOWS
                region + "_" + row[0].replace(" ", "_").replace("'", "").replace("(", "").replace(")", "") + "_undist")
                arcpy.Clip_analysis(undist, row[1], out_fc)
        ## Add the extra fields data to the output. Pull from region/areas file.
        for field in carry_over_fields:
            arcpy.AddField_management("/{0}/{1}".format(region, area), field, "TEXT", "", "", 200)
        ## Then calculate them based on the respective fields in the areas file.
        """
        ADDING THE EXTRA FIELDS TO THE UNDIST INTERMEDIARY FILES, THEN PULLING THEM FROM THERE
        TO THE FINAL OUTPUT WHEN NEEDED (LATER IN THE SCRIPT)
        """

# Create output csv with desired areas
################################
# Area of each region
region_area = []
for region in arcpy.ListDatasets():
    region_area.append([region])
    area = 0
    SQL = """ {0} = '{1}' """.format(regions_name_field, region)
    with arcpy.da.SearchCursor(regions, ("Shape_Area", regions_name_field), SQL) as cursor:
        for row in cursor:
            area += (row[0] * 0.0001) # Gets area in hectares. Should only get 1 row as a return.
            region_area[-1].append(area)
## Output list for above
regions_area_output = region_area # This still changes the original...fine details on object assignment that elude me right now. It doesn't affect the script.
for i in range(len(regions_area_output)):
    regions_area_output[i].insert(1, regions_area_output[i][0])
    regions_area_output[i].insert(2,"full")
# Area of undisturbed in each region
regions_undist_area = []
for region in arcpy.ListDatasets():
    regions_undist_area.append([region])
    for fc in arcpy.ListFeatureClasses("*_undisturbed", "", region): # Should only grab one fc.
        area = 0
        with arcpy.da.SearchCursor(fc, ("Shape_Area")) as cursor:
            for row in cursor:
                area += (row[0] * 0.0001)
                regions_undist_area[-1].append(area)
## Output list for above
regions_undist_area_output = regions_undist_area # This still changes the original...fine details on object assignment that elude me right now. It doesn't affect the script.
for i in range(len(regions_undist_area_output)):
    regions_undist_area_output[i].insert(1, regions_undist_area_output[i][0])
    regions_undist_area_output[i].insert(2,"undisturbed")
# Area of protection (for each unique protection) in each region
areas_area = []
for region in arcpy.ListDatasets():
    areas_area.append([region])
    for fc in arcpy.ListFeatureClasses("*_areas", "", region):
        with arcpy.da.SearchCursor(fc, ("Shape_Area", areas_field)) as cursor:
            for row in cursor:
                area = (row[0] * 0.0001)
                areas_area[-1].append([row[1], area])
## Output list for above
areas_area_output = []
for item in areas_area:
    if len(item) > 1:
        subitem = item[1:len(item)]
        for i in range(len(subitem)):
            Region = item[0]
            Area_Name = subitem[i][0]
            Type = "full"
            Area_Hectares = subitem[i][1]
            entry = [Region, Area_Name, Type, Area_Hectares]
            areas_area_output.append(entry)
            ## add in the extra data from the original file
            SQL = """ {0} = '{1}' """.format(areas_field, Area_Name)
            initial_fields = [areas_field]
            fields = initial_fields + carry_over_fields
            fields = tuple(fields)
            temp_list = []
            with arcpy.da.SearchCursor(areas, fields, SQL) as cursor:
                for row in cursor:
                    temp_list = row[len(initial_fields):]
            areas_area_output[-1] += temp_list
# Area of undisturbed in each protection in each region
areas_undist_area = []
for region in arcpy.ListDatasets():
    areas_undist_area.append([region])
    for fc in arcpy.ListFeatureClasses("*_undist", "", region):
        with arcpy.da.SearchCursor(fc, ("Shape_Area",)) as cursor:
            for row in cursor:
                area = (row[0] * 0.0001)
                area_name = fc.split("_", 1)[1].rstrip("_undist")
                areas_undist_area[-1].append([area_name, area])
## Output list for above
areas_undist_area_output = []
for item in areas_undist_area:
    if len(item) > 1:
        subitem = item[1:len(item)]
        for i in range(len(subitem)):
            Region = item[0]
            Area_Name = subitem[i][0]
            Type = "undisturbed"
            Area_Hectares = subitem[i][1]
            entry = [Region, Area_Name, Type, Area_Hectares]
            areas_undist_area_output.append(entry)
            ## add in the extra data from the original file
            SQL = """ {0} = '{1}' """.format(areas_field, Area_Name)
            initial_fields = [areas_field]
            fields = initial_fields + carry_over_fields
            fields = tuple(fields)
            temp_list = []
            with arcpy.da.SearchCursor(areas, fields, SQL) as cursor:
                for row in cursor:
                    temp_list = row[len(initial_fields):]
            areas_undist_area_output[-1] += temp_list
# Make output csv
header_list = ["Region", "Area_Name", "Type", "Area_Hectates"] + carry_over_fields
out_csv = os.path.join(output_location, out_csv_name)
with open(out_csv, "wb") as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    # Write headers first
    wr.writerow(header_list)
    # Now write data
    for item in regions_area_output:
        wr.writerow(item)
    for item in regions_undist_area_output:
        wr.writerow(item)
    for item in areas_area_output:
        wr.writerow(item)
    for item in areas_undist_area_output:
        wr.writerow(item)