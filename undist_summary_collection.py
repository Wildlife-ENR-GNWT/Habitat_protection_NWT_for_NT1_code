import os
import arcpy
arcpy.env.overwriteOutput = True

Dir = r"H:\Boreal_Caribou_Range_Plan\GIS\Habitat_protection_NWT_for_NT1\analyzed_data\diss_runs"
output_gdb = r"H:\Boreal_Caribou_Range_Plan\GIS\Habitat_protection_NWT_for_NT1\analyzed_data\diss_runs\summary_undist.gdb"

for folder in os.walk(Dir).next()[1]:
    if not folder.endswith(".gdb"):
        wksp_temp = os.path.join(Dir, folder, os.walk(os.path.join(Dir, folder)).next()[1][0])
        arcpy.env.workspace = wksp_temp
        for dataset in arcpy.ListDatasets():
            master_undist = []
            for fc in arcpy.ListFeatureClasses("*_undist", "", dataset):
                master_undist.append(fc)
            output_fc = os.path.join(output_gdb, dataset + "_run_" + folder)
            if len(master_undist) > 0:
                arcpy.Merge_management(master_undist, output_fc)