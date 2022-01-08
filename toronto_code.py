#Rex Devereux
#V00800847
#Final Project

#Create GDB and import datasets 
#data path (alter this path)
data_path = "Z:\\428_FinalProject\\Data"

#create GDB (alter path)
path = "Z:\\428_FinalProject"
out_name = "TorontoHomicides"
arcpy.management.CreateFileGDB(path, out_name)

gdbpath = path + "\\" + out_name + r".gdb"
arcpy.env.workspace = "gdbpath"
print("GDB Created")

#Import data

#Import neighbourhoods
data_name = "Neighbourhoods"
arcpy.FeatureClassToFeatureClass_conversion(data_path + "\\neighbourhoods_planning_areas_wgs84\\NEIGHBORHOODS_WGS84.shp", gdbpath, data_name)

#Import Homicide
data_name = "Homicides"
arcpy.FeatureClassToFeatureClass_conversion(data_path + "\\Homicide\\Homicide.shp", gdbpath, data_name)

#Import Parks
data_name = "Parks"
arcpy.FeatureClassToFeatureClass_conversion(data_path + "\\city_green_space_wgs84\\CITY_GREEN_SPACE_WGS84.shp", gdbpath, data_name)

#Import Schools
data_name = "Schools"
arcpy.FeatureClassToFeatureClass_conversion(data_path + "\\school_frm_police_wgs84\\SCHOOL_WGS84.shp", gdbpath, data_name)

#Import Bridge_Culverts
data_name = "Bridges_and_Culverts"
arcpy.FeatureClassToFeatureClass_conversion(data_path + "\\BRIDGE_AND_CULVERT_WGS84_Shapefile\\BRIDGE_AND_CULVERT_WGS84.shp", gdbpath, data_name)


#Import census data
arcpy.TableToGeodatabase_conversion(data_path + "\\TO_nhood_censusdata.csv", gdbpath)
print("Data uploaded :)")

#Data from whole city of Toronto based on neighourhoods profile
#City of Toronto	total pop 2016= 2,731,571	total pop 2011 = 2,615,060	pop change = 4.50%	pop density = 4,334	total income avg amount = 52,268  unemployment rate = 8.2%

#Join census data with neighbourhood polygons
in_data = "Neighbourhoods"
in_field = "OBJECTID"
join_table = gdbpath + "\\TO_nhood_censusdata.csv"
join_field = "ID"
arcpy.JoinField_management(in_data, in_field, join_table, join_field) 

#Global Morans I test, spatial autocorrelation
arcpy.SpatialAutocorrelation_stats("Homicides", "ObjectID", "GENERATE_REPORT", "INVERSE_DISTANCE", "EUCLIDEAN_DISTANCE", "NONE") 
arcpy.SpatialAutocorrelation_stats("Homicides", "ObjectID", "GENERATE_REPORT", "INVERSE_DISTANCE", "EUCLIDEAN_DISTANCE", "NONE", 500) 
arcpy.SpatialAutocorrelation_stats("Homicides", "ObjectID", "GENERATE_REPORT", "INVERSE_DISTANCE", "EUCLIDEAN_DISTANCE", "NONE", 200)

#Homicides are clustered at 2300m, 500m, and 200m

#Kernel density 
KDens = arcpy.sa.KernelDensity("Homicides", "ObjectId")
KDens.save()

#Nearest Neighbourhood Distance
nn_output = arcpy.AverageNearestNeighbor_stats("Homicides", "EUCLIDEAN_DISTANCE", "GENERATE_REPORT")
print("The nearest neighbor index is: " + nn_output[0])
print("The z-score of the nearest neighbor index is: " + nn_output[1])
print("The p-value of the nearest neighbor index is: " + nn_output[2])
print("The expected mean distance is: " + nn_output[3])
print("The observed mean distance is: " + nn_output[4])
print("The path of the HTML report: " + nn_output[5])

#Create bar graph of homicides by neighbourhood
#Create GDB
out_folder_path = ('Z:\\428_FinalProject')
out_name = ('HomicideGraph')
arcpy.management.CreateFileGDB(out_folder_path, out_name)

# set workspace
arcpy.env.workspace = 'Z:\\428_FinalProject\\HomicideGraph.gdb'

#Split
in_feature = 'Z:\\428_FinalProject\\Data\\neighbourhoods_planning_areas_wgs84\\NEIGHBORHOODS_WGS84.shp'
splitFeatures = 'Z:\\428_FinalProject\\Data\\neighbourhoods_planning_areas_wgs84\\NEIGHBORHOODS_WGS84.shp'
splitField = 'AREA_NAME'
outWorkspace = 'Z:\\428_FinalProject\\HomicideGraph.gdb'
arcpy.Split_analysis(in_feature, splitFeatures, splitField, outWorkspace)

#Import homicides to the new gdb for graph

arcpy.env.workspace = 'Z:\\428_FinalProject\\HomicideGraph.gdb'
area_list = arcpy.ListFeatureClasses()

#For Loop Creating Homicide by Neighbourhood 
for area in area_list:
	print(area)	
	input = [area, 'Z:\\428_FinalProject\Data\\Homicide\\Homicide.shp']
	output = 'homicides_in_'+area
	arcpy.analysis.Intersect(input, output, "ALL")
#done
	
#Count Crime Frequencies for Each Neighbourhood
for area in area_list:
	print(area)
	in_table = 'homicides_in_'+area
	out_table = 'Z:\\428_FinalProject\\HomicideGraph.gdb\crimes_freq_'+area
	freq_fields = 'Homicide_T'
	arcpy.Frequency_analysis(in_table, out_table, freq_fields)
#done


# Export created table to csv 
for area in area_list:
	in_rows = 'Z:\\428_FinalProject\\HomicideGraph.gdb\\crimes_freq_'+area
	out_path = 'Z:\\428_FinalProject\\Figures&Tables\GraphTables'	
	out_name = area+'_table.csv'
	arcpy.TableToTable_conversion(in_rows, out_path, out_name)
#done

#Search cursor 
#where homicide type = shooting stabbign etc, 
#Get count
	
#Intersect homicides and neighbourhoods
Select where # homicides > 10
	
#Edit this to find average distance of parks to homicides 

###########

with arcpy.da.SearchCursor(FC,(distField),where_clause=expression) as cursor:
	for row in cursor:
		nearestdisthospitals += row[0]
		recordsCounted += 1

averagedist = nearestdisthospitals / recordsCounted
print ("Average distance to hospitals for cities +/- 10% population of Lillooet is " + str(averagedist),"meters ")
#Average distance to hospitals for cities +/- 10% population of Lillooet is 35863.65793476146 meters 
print("Task 6 Complete")


#Edit this to make incomes small, medium, and high

############

#add fields
in_feature = "popPlaces"
field_name = "SmallCities"
field_type = "TEXT"

arcpy.AddField_management(in_feature, field_name, field_type)

field_name = "MedCities"
arcpy.AddField_management(in_feature, field_name, field_type)

field_name = "LargeCities"
arcpy.AddField_management(in_feature, field_name, field_type)
print("Fields Added")

#assign fields to variables
small = "SmallCities"
medium = "MedCities"
large = "LargeCities"

distField = "NEAR_DIST"


#assign classifications	
with arcpy.da.UpdateCursor(FC, (distField, small),'"EST_POP" <= 500') as cursor:
 for row in cursor:
  if row[0] <= 1000:
     row[1] = "VERY CLOSE"
  elif row[0] > 1000 and row[0] <= 10000:
      row[1] = 'CLOSE'
  else:
       row[1] = 'FAR'
  cursor.updateRow(row)
  
with arcpy.da.UpdateCursor(FC, (distField, medium),'"EST_POP" > 500 And "EST_POP" <= 10000') as cursor:
 for row in cursor:
  if row[0] <= 1000:
     row[1] = "VERY CLOSE"
  elif row[0] > 1000 and row[0] <= 10000:
      row[1] = 'CLOSE'
  else:
       row[1] = 'FAR'
  cursor.updateRow(row)

with arcpy.da.UpdateCursor(FC, (distField, large),'"EST_POP" > 10000') as cursor:
 for row in cursor:
  if row[0] <= 1000:
     row[1] = "VERY CLOSE"
  elif row[0] > 1000 and row[0] <= 10000:
      row[1] = 'CLOSE'
  else:
       row[1] = 'FAR'
  cursor.updateRow(row)