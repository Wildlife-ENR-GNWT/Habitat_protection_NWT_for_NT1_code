import arcpy
import numpy
import csv
import os
import datetime

# Timing the script
start_time = datetime.datetime.now()

# Inputs:
## Assumed by naming in script to be NT1. If this is changed - the naming
## throughout the script will need to be changed. The output lists will need to
## be changed as well.
Range = arcpy.GetParameterAsText(0)
#Range = r"H:\GIS\BWC_base_files\BWC_base_files.gdb\boundaries\NT1"
## Assumed to be non-overlapping.
regions = arcpy.GetParameterAsText(1)
#regions = r"H:\GIS\BWC_base_files\BWC_base_files.gdb\boundaries\ENRITI_AdministrativeRegions_incl_Gw_YT"
#regions = r"H:\Boreal_Caribou_Range_Plan\GIS\Habitat_protection_NWT_for_NT1\code\Habitat_protection_NWT_for_NT1_code\base_files_for_script_tool.gdb\NWT_Regions_2015_LCs"
##regions = r"H:\Boreal_Caribou_Range_Plan\GIS\Habitat_protection_NWT_for_NT1\raw_data\data_for_script.gdb\NWT_Regions_2015_LCs"
#regions = r"H:\Boreal_Caribou_Range_Plan\GIS\Habitat_protection_NWT_for_NT1\code\Habitat_protection_NWT_for_NT1_code\base_files_for_script_tool.gdb\ENRITI_AdministrativeRegions_incl_Gw_YT_waterErase"
##regions = r"H:\Boreal_Caribou_Range_Plan\GIS\Habitat_protection_NWT_for_NT1\analyzed_data\areas_3.gdb\ENRITI_AdministrativeRegions_incl_Gw_YT_waterErase"
#regions = r"H:\Boreal_Caribou_Range_Plan\GIS\Habitat_protection_NWT_for_NT1\code\Habitat_protection_NWT_for_NT1_code\base_files_for_script_tool.gdb\NWT_Regions_2015_LCs_waterErase"
##regions = r"H:\Boreal_Caribou_Range_Plan\GIS\Habitat_protection_NWT_for_NT1\analyzed_data\areas_3.gdb\NWT_Regions_2015_LCs_waterErase"
##regions = r"H:\GIS\BWC_base_files\BWC_base_files.gdb\boundaries\NT1"
##regions = r"H:\Boreal_Caribou_Range_Plan\GIS\Habitat_protection_NWT_for_NT1\analyzed_data\redo_protected_areas\scenarioA.gdb\inputs\NT1_er_water"
regions_name_field = arcpy.GetParameterAsText(2)
#regions_name_field = "REGION"
##regions_name_field = "POPULATION"
## Overlapping is okay. However this will preclude post-analysis to get at total
## numbers. If total non-overlapping numbers are wanted then input will need to
## be non-overlapping. Not the role of this script to do this step. If different
## areas have the same unique name (and additional info if additional fields are
## included) they will be dissolved together in the script.
##areas = r"H:\Boreal_Caribou_Range_Plan\GIS\Habitat_protection_NWT_for_NT1\analyzed_data\redo_protected_areas\main.gdb\scratch\scratch_current_protected"
##areas = r"H:\Boreal_Caribou_Range_Plan\GIS\Habitat_protection_NWT_for_NT1\analyzed_data\redo_protected_areas\main.gdb\Protected_current\current_protected_NWT_June27_2016_PROTECTED_diss2"
##areas = r"H:\Boreal_Caribou_Range_Plan\GIS\Habitat_protection_NWT_for_NT1\analyzed_data\redo_protected_areas\main.gdb\Protected_current\prot_and_cons_no_overlap_diss"
##areas = r"H:\Boreal_Caribou_Range_Plan\GIS\Habitat_protection_NWT_for_NT1\analyzed_data\redo_protected_areas\main.gdb\Protected_current\current_protected_NWT_June27_2016"
##areas = r"H:\GIS\BWC_base_files\BWC_base_files.gdb\boundaries\ENRITI_AdministrativeRegions_incl_Gw_YT"
##areas = r"H:\Boreal_Caribou_Range_Plan\GIS\Habitat_protection_NWT_for_NT1\raw_data\data_for_script.gdb\NWT_Regions_2015_LCs"
##areas = r"H:\Boreal_Caribou_Range_Plan\GIS\Habitat_protection_NWT_for_NT1\analyzed_data\areas_3.gdb\ENRITI_AdministrativeRegions_incl_Gw_YT_waterErase"
##areas = r"H:\Boreal_Caribou_Range_Plan\GIS\Habitat_protection_NWT_for_NT1\analyzed_data\areas_3.gdb\NWT_Regions_2015_LCs_waterErase"
##areas = r"H:\Boreal_Caribou_Range_Plan\GIS\Habitat_protection_NWT_for_NT1\analyzed_data\redo_protected_areas\main.gdb\Protected_current\current_all_NWT_July7_2016"
##areas = r"H:\Boreal_Caribou_Range_Plan\GIS\Habitat_protection_NWT_for_NT1\analyzed_data\redo_protected_areas\main.gdb\scratch\conservation_july7_2016_reduced"
##areas = r"H:\Boreal_Caribou_Range_Plan\GIS\Habitat_protection_NWT_for_NT1\analyzed_data\redo_protected_areas\scenarioA.gdb\inputs\scenario_A"
##areas = r"H:\Boreal_Caribou_Range_Plan\GIS\Habitat_protection_NWT_for_NT1\analyzed_data\redo_protected_areas\scenarioA.gdb\inputs\scenario_A_2_diss"#
##areas = r"H:\Boreal_Caribou_Range_Plan\GIS\Habitat_protection_NWT_for_NT1\analyzed_data\redo_protected_areas\scenarioB.gdb\main\scenario_B_diss"
areas = arcpy.GetParameterAsText(3)
#areas = r"H:\Boreal_Caribou_Range_Plan\GIS\Habitat_protection_NWT_for_NT1\analyzed_data\redo_protected_areas\scenarioB.gdb\main\scenario_B_diss_by_scenario_level_3"
##areas = r"H:\Boreal_Caribou_Range_Plan\GIS\Habitat_protection_NWT_for_NT1\analyzed_data\redo_protected_areas\scenarioB.gdb\main\scenario_B_2_diss"#
##areas = r"H:\Boreal_Caribou_Range_Plan\GIS\Habitat_protection_NWT_for_NT1\analyzed_data\redo_protected_areas\scenarioA.gdb\inputs\scenario_A_2_diss_by_level_2"#
##areas_field = "unique_area_name"
areas_field = arcpy.GetParameterAsText(4)
#areas_field = "scenario_level"
##areas_field = "scenario"
##areas_field = "REGION"
## You can input any number of fields that are in the original "areas" file.
## The attributes will be carried through to the output.
##carry_over_fields = ["additional_notes", "Protection_duration", "protection_level"]
carry_over_fields = ""
carry_over_fields = arcpy.GetParameterAsText(5)
carry_over_fields = [x.replace(" ", "") for x in carry_over_fields.split(",")]
if carry_over_fields == [""]:
    carry_over_fields = []
##carry_over_fields = []
undist = arcpy.GetParameterAsText(6)
#undist = r"H:\GIS\BWC_base_files\BWC_base_files.gdb\undisturbed\NT1_undisturbed_2015"
##undist = r"H:\GIS\BWC_base_files\BWC_base_files.gdb\undisturbed\NT1_undisturbed_2010"
##undist = r"H:\GIS\BWC_base_files\BWC_base_files.gdb\undisturbed\NT1_undisturbed_fireOnly_2010"
##undist = r"H:\GIS\BWC_base_files\BWC_base_files.gdb\undisturbed\NT1_undisturbed_anthropogenicOnly_2010"
## Script creates an output file geodatabase here.
##output_location = r"H:\Boreal_Caribou_Range_Plan\GIS\Habitat_protection_NWT_for_NT1\analyzed_data\redo_protected_areas"
output_location = arcpy.GetParameterAsText(7)
#output_location = r"H:\Boreal_Caribou_Range_Plan\GIS\Habitat_protection_NWT_for_NT1\analyzed_data\July12_on"
run_name = arcpy.GetParameterAsText(8)
#run_name = "July13__run9__NT1__withoutWater__Scenario_B_dissolved_by_level"
## Produces resulting area unit. Based on the base unit of the inputs. Base unit
## is commonly 1 metre. 0.0001 produces hectares with 1m base unit.
area_factor = arcpy.GetParameterAsText(9)
#area_factor = 0.0001
area_factor = float(area_factor)

# Derived inputs
out_csv_name = run_name.replace(" ", "_") + ".csv"

# Create output file geodatabase and assign as the workspace
arcpy.CreateFileGDB_management(output_location, run_name)
# assign as the workspace
wksp = os.path.join(output_location, run_name + ".gdb")
arcpy.env.workspace = wksp

# Unique defs
def unique_values(table, field):
    data = arcpy.da.TableToNumPyArray(table, [field])
    unqs = numpy.unique(data[field])
    output = [str(x) for x in unqs]
    return output

# Step one:
# Clip regions with NT1
# Produces regions_NT1
arcpy.Clip_analysis(regions, Range, "regions_NT1")

# Step two:
# Clip regions_NT1 with undist
# Produces regions_NT1_undist
arcpy.Clip_analysis("regions_NT1", undist, "regions_NT1_undist")

# Step three:
# Intersect regions_NT1 with areas.
# Produces areas_regions_NT1
arcpy.Intersect_analysis(["regions_NT1", areas], "areas_regions_NT1")

# Step four:
# Dissolve based on region and unique area name (and also the carry_over_fields,
# which will be carried over if included, but will not affect the resulting
# dissolve).
# Produces areas_regions_NT1_diss
arcpy.Dissolve_management("areas_regions_NT1", "areas_regions_NT1_diss", [regions_name_field, areas_field] + carry_over_fields)

# Step five:
# Clip areas_regions_NT1_diss with undist
# Produces areas_regions_NT1_diss_undist
arcpy.Clip_analysis("areas_regions_NT1_diss", undist, "areas_regions_NT1_diss_undist")

# Step six:
# Clip NT1 with undist
# Produces NT1_undist
arcpy.Clip_analysis(Range, undist, "NT1_undist")

# Output section
# Output Range list
with arcpy.da.SearchCursor(Range, ("Shape_Area",)) as cursor:
    for row in cursor:
        Range_area_hectares = row[0] * area_factor
Range_output = ["NT1", "RANGE", "full", Range_area_hectares]
# Output NT1_undist list
with arcpy.da.SearchCursor("NT1_undist", ("Shape_Area",)) as cursor:
    for row in cursor:
        Range_undist_area_hectares = row[0] * area_factor
Range_undist_output = ["NT1", "RANGE", "undist", Range_undist_area_hectares]
# Output regions_NT1 list of lists
regions_NT1_output = []
with arcpy.da.SearchCursor("regions_NT1", (regions_name_field, "Shape_Area")) as cursor:
    for row in cursor:
        region_NT1_output = [row[0], "REGION", "full", row[1] * area_factor]
        regions_NT1_output.append(region_NT1_output)
# Output regions_NT1_undist list of lists
regions_NT1_undist_output = []
with arcpy.da.SearchCursor("regions_NT1_undist", (regions_name_field, "Shape_Area")) as cursor:
    for row in cursor:
        region_NT1_undist_output = [row[0], "REGION", "undist", row[1] * area_factor]
        regions_NT1_undist_output.append(region_NT1_undist_output)
# Output areas_regions_NT1_diss list of lists
areas_regions_NT1_diss_output = []
fields = tuple([regions_name_field, areas_field, "Shape_Area"] + carry_over_fields)
with arcpy.da.SearchCursor("areas_regions_NT1_diss", fields) as cursor:
    for row in cursor:
        area_regions_NT1_diss_output = [row[0], row[1], "full", row[2] * area_factor]
        for i in range(len(carry_over_fields)):
            area_regions_NT1_diss_output.append(row[i + (len(fields) - len(carry_over_fields))])
        areas_regions_NT1_diss_output.append(area_regions_NT1_diss_output)
# Output areas_regions_NT1_diss_undist list of lists
areas_regions_NT1_diss_undist_output = []
fields = tuple([regions_name_field, areas_field, "Shape_Area"] + carry_over_fields)
with arcpy.da.SearchCursor("areas_regions_NT1_diss_undist", fields) as cursor:
    for row in cursor:
        area_regions_NT1_diss_undist_output = [row[0], row[1], "undist", row[2] * area_factor]
        for i in range(len(carry_over_fields)):
            area_regions_NT1_diss_undist_output.append(row[i + (len(fields) - len(carry_over_fields))])
        areas_regions_NT1_diss_undist_output.append(area_regions_NT1_diss_undist_output)
# Output results to csv
output_fields = ["region", "area_name", "type", "area_hectares"] + carry_over_fields
# Make output csv
out_csv = os.path.join(output_location, out_csv_name)
with open(out_csv, "wb") as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    # Write headers first
    wr.writerow(output_fields)
    # Now write data
    # Range data
    wr.writerow(Range_output)
    wr.writerow(Range_undist_output)
    # Region data
    for item in regions_NT1_output:
        wr.writerow(item)
    for item in regions_NT1_undist_output:
        wr.writerow(item)
    # Areas data
    for item in areas_regions_NT1_diss_output:
        arcpy.AddMessage(item)
        wr.writerow(item)
    for item in areas_regions_NT1_diss_undist_output:
        wr.writerow(item)

# Timing the script
script_duration = datetime.datetime.now() - start_time
print script_duration