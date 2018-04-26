#Test Delineation Tool#
import json
import urllib2
from urllib2 import Request
import os
import shapefile
import time

startTime = time.time()
#==============================================================================
#
# This code will take an input lat/long and return the upstream watershed from
# the closest downhill point on an NHD line. The output will be a shapefile
# located in the given output location.
# 
#==============================================================================

#-------------------------------------------------------------------------------
#USER INPUT (from R)
#initial lat/long
lonPt1 = stnx
latPt1 = stny
SetDistance = 100
gisUser=1
print "Station " + str(stnID)

#-------------------------------------------------------------------------------
#build the point indexing URL (substitute for pour point, note the RAINDROP method
#uses downhill path to find comid vs closest NHD feature)
PtServiceUrl = "http://ofmpub.epa.gov/waters10/PointIndexing.Service?" \
+ "pGeometry=POINT(%s+%s)"%(lonPt1, latPt1) \
+ "&pResolution=3" \
+ "&pPointIndexingMethod=RAINDROP" \
+ "&pPointIndexingMaxDist=25" \
+ "&pOutputPathFlag=FALSE"

#load response into JSON object
response = json.loads(urllib2.urlopen(PtServiceUrl).read())

#check the status message from the response to see if it worked
status_message = response['status']['status_message']
##if status_message == "No Results Returned.":
##    raise Exception('Point service did not find an NHD feature within 560 km of '
##                    + \a. 'lat=%s, lon=%s. Please double check your coordinates.'%(latPt1, lonPt1))
##extract comid
comid = response['output']['ary_flowlines'][0]['comid']
measure = response['output']['ary_flowlines'][0]['fmeasure']
indexDist = response['output']['path_distance']
pointTravel = "Point moved: " + str(indexDist) + " km"
print pointTravel

"""
Uses the EPA Waters Navigation Delineation Services to draw the upstream watershed from a given lat/long
Parameters:
comid1 - start location on the river
Returns:
JSON of watershed
"""
#build the URL to call the Navigation Delineation service tool
DelinServiceUrl = "http://ofmpub.epa.gov/waters10/NavigationDelineation.Service?" \
+ "pNavigationType=UT" \
+ "&pStartComid=%s"%(comid) \
+ "&pStartMeasure=%s"%(measure) \
+ "&pMaxDistance=560" \
+ "&pFeatureType=CATCHMENT" \
+ "&pOutputFlag=FEATURE" \
+ "&pAggregationFlag=TRUE" \
+ "&optOutGeomFormat=GEOJSON" \
+ "&optOutPrettyPrint=0"

#load response into JSON object
response = json.loads(urllib2.urlopen(DelinServiceUrl).read())
outJsonPath = outPath + "/jsonOutput.json"
try:    
    with open(outJsonPath, 'wb') as outfile:
        json.dump(response['output']['shape'], outfile)
except:
    print "Delineation failed to create polygon, may be confused by NHD"

geoJFile = json.load(open(outJsonPath))

#create shapefiles from JSON coordinates
j = 1
for i in geoJFile['coordinates'][0:1]:
    outName = outName + str(j)
    w = shapefile.Writer(shapefile.POLYGON)
    w.poly(parts=[i])
    w.field('F_FLD','C','40')
    w.field('S_FLD','C','40')
    w.record('First','Polygon')
    w.save(outName)
    j += 1

endTime = time.time()
processTime = (endTime - startTime)/60

print "Process time: " + str(processTime) + " minutes"
