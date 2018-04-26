# install.packages('rgdal')
# install.packages('sp')
# install.packages('spatialEco')
# install.packages('raster')
# install.packages('PythonInR')
# install.packages('plyr')
# install.packages('dplyr')
# install.packages('tidyr')
#library(rgdal)
#library(sp)
#library(spatialEco)
#library(raster)
library(PythonInR)
library(plyr)
library(dplyr)
library(tidyr)
autodetectPython("C:/Python27/python.exe") #path to Python (MAKE SURE TO USE / AND NOT \ for all file paths)
pyConnect("C:/Python27/python.exe") #path to Python
pyIsConnected()

# User Input ------------------------------------------------------------------


# File path of the station .csv
stationPath <- "C:/workspace/SiletzWS.csv"

# insert output path here (don't end with "/")
outPath <- "C:/workspace"


# Set Up ------------------------------------------------------------------


stns <- read.csv(stationPath)

long <- grep("lon", colnames(stns), ignore.case = TRUE)
lat <- grep("lat", colnames(stns), ignore.case = TRUE)
ID <- grep("ID", colnames(stns), ignore.case = TRUE)

stnList <- stns[,ID]

# Start Loop Here ---------------------------------------------------------

for(i in stnList){
  
  outName <- paste0(outPath, "/", i, "_Watershed")
  
  stn <- stns[stns[,ID] == i,]
  
  stnx <- as.character(stn[,long])
  stny <- as.character(stn[,lat])
  stnID <- as.character(stn[,ID])
  
  pySet("outPath", outPath)
  pySet("outName", outName)
  pySet("stnx", stnx)
  pySet("stny", stny)
  pySet("stnID", stnID)
  pyTest <- tryCatch(
    pyExecfile("//deqhq1/WQ-Share/ColinD/Watershed Delineation/NavigationDelineationServices.py"),
    error = function(e) e,
    finally = print("Delineation Finished")
  )
  pyTest
}

pyExit()
#Your Watersheds can be found in: 
outPath
