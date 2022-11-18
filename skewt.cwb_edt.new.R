#!/usr/bin/Rscript

skewt.cwb_edt.new <- function(strDate,site) {
## R script to plot the skew-T from a CSU sonde

#source("plotskew.R")
#source("calc.hodo.R")
#library("RadioSonde")
library("RadioSonde.RSS")
library("gdata")
library("filesstrings")
#library("tidyverse")
#library("dplyr")

if (site == "46692") {
  lat <- "24.998"
  lon <- "121.442"
} else if (site == "46695") {
  lat <- "25.628"
  lon <- "122.080"
} else if (site == "46699") {
  lat <- "23.975"
  lon <- "121.613"
} else if (site == "46708") {
  lat <- "24.764"
  lon <- "121.756"
} else if (site == "46757") {
  lat <- "24.828"
  lon <- "121.014"
}

rawDir <- paste("/home/disk/monsoon/precip/raw/soundings/",strDate,sep="")
pngDir <- paste("/home/disk/monsoon/precip/skewt/",strDate,sep="")
if (file.exists(pngDir)) {
} else {
  dir.create(pngDir)
}
SHARPpyDir <- paste("/home/disk/monsoon/precip/SHARPpy/",strDate,sep="")
if (file.exists(SHARPpyDir)) {
} else {
  dir.create(SHARPpyDir)
}
binDir <- "/home/disk/monsoon/precip/bin"

filesWild <- paste(site,"-*.edt*txt",sep="")
filenames <- Sys.glob(file.path(rawDir,filesWild))
print(filenames)

# Get latest file
#filename <- filenames[length(filenames)]

for (filename in filenames) {

   skewtExists <- FALSE
   manualLaunch <- FALSE

   # Make sure this is not a Yonaguni file
   file <- basename(filename)
   if (grepl("yonaguni",file) == FALSE) {
      print(file)

      if (grepl("csu",file) == FALSE) {

      	 # Get info from filename
      	 base <- strsplit(file,"[.]")[[1]][1]
      	 datetime <-strsplit(base,"-")[[1]][2]
      	 yymmdd <- substr(datetime,1,8)
      	 gemdate <- substr(datetime,3,8)
      	 hhmm <- paste(substr(datetime,9,10),"00",sep="")
      	 year <- substr(datetime,1,4)
      	 month <- substr(datetime,5,6)
      	 day <- substr(datetime,7,8)
      	 date <- paste(year,'/',month,'/',day,sep='')
      	 skewtFile <- paste(pngDir,"/research.SkewT.",datetime,"00.",site,"_CWB.png",sep="")
      	 title <- paste("CWB-",site," radiosonde for PRECIP -- preliminary data",sep="")
      	 sharppyFile <- paste(SHARPpyDir,"/",yymmdd,hhmm,".",site,"_CWB_PRECIP",sep="")
      	 print(skewtFile)

      	 # If skewt file already exists, do nothing
      	 if (file.exists(skewtFile) == TRUE) {
	    skewtExists <- TRUE
      	    print("skewT already exists")
      	 } else {

       	    ## run this sed command to remove commas from file
       	    ## sed 's/,/ /g' <infile> > <outfile>
       	    filename_out <- paste(filename,".mod",sep="")
     	    cmd <- paste("sed 's/,/ /g' ",filename," > ",filename_out,sep="")
     	    system(cmd)

	    ## read in the EDT file
     	    data <- read.table(filename_out, skip=3, stringsAsFactors=FALSE)
     	    colnames(data) <- c("time","alt","press","temp","rhum","wspd","dir","ascent")

     	    ## get rid of missing data
     	    data[data=="////////"] <- NA

     	    ## convert any character columns to numeric
     	    charcols <- sapply(data,is.character)
     	    charcols <- which(charcols=="TRUE") ## the column numbers that are character
     	    data[,charcols] <- sapply(data[,charcols],as.numeric)

     	    ## make height AGL instead of MSL 
     	    elev <- data$alt[1]
     	    data$alt <- data$alt - elev

     	    ## convert wind speed from m/s to knots
     	    data$wspd <- data$wspd*1.943844

     	    ## add new column for dewpoint
     	    data$dewpt <- 0
     	    data$dewpt <- data$temp - ((100 - data$rhum)/5.)

     	    ## eliminate all rows past minimum pressure val
     	    minPress <- min(data$press, na.rm = TRUE)
     	    ##minPress <- min(data[!data$press %in% exclude,]$press)
     	    minPressRows <- which (data$press == minPress)
     	    lastGoodRow <- minPressRows[1]
     	    dataSub <- data[1:lastGoodRow,]
	    data <- dataSub

      	 }

      } else {

      	 manualLaunch <- TRUE
   
	 # Get info from filename
      	 base <- strsplit(file,"[.]")[[1]][1]
      	 datetime <-strsplit(base,"-")[[1]][2]
      	 yymmdd <- substr(datetime,1,8)
      	 gemdate <- substr(datetime,3,8)
      	 hhmm <- paste(substr(datetime,9,10),"00",sep="")
      	 year <- substr(datetime,1,4)
      	 month <- substr(datetime,5,6)
      	 day <- substr(datetime,7,8)
      	 date <- paste(year,'/',month,'/',day,sep='')
      	 skewtFile <- paste(pngDir,"/research.SkewT.",datetime,"00.",site,"_CSU.png",sep="")
      	 title <- paste("CSU-",site," radiosonde for PRECIP -- preliminary data",sep="")
      	 sharppyFile <- paste(SHARPpyDir,"/",yymmdd,hhmm,".",site,"_CSU_PRECIP",sep="")
      	 print(skewtFile)

      	 # If skewt file already exists, do nothing
      	 if (file.exists(skewtFile) == TRUE) {
	    skewtExists <- TRUE
       	    print("skewT already exists")
      	 } else {

            ## read in the EDT file
    	    data <- read.table(filename, skip=32, stringsAsFactors=FALSE)
    	    colnames(data) <- c("time","alt","press","temp","dewpt","rhum","wspd","dir","ascent","lat","lon")

     	    ## get rid of missing data
            data[data=="/////"] <- NA

     	    ## convert any character columns to numeric
     	    charcols <- sapply(data,is.character)
     	    charcols <- which(charcols=="TRUE") ## the column numbers that are character
     	    data[,charcols] <- sapply(data[,charcols],as.numeric)

     	    ## make height AGL instead of MSL 
     	    elev <- data$alt[1]
     	    data$alt <- data$alt - elev

     	    ## convert wind speed from m/s to knots
     	    data$wspd <- data$wspd*1.943844

     	    ## get date from the file
    	    #dum1 <- readLines(filename,n=6)[6] # date is 6th line
    	    #dum2 <- strsplit(dum1,"\t")[[1]][2]  # get rid of space
    	    #date <- strsplit(dum2,"T")[[1]][1]

     	    ## and similarly the lat/lon
    	    #dum1 <-  readLines(filename,n=7)[7] ## lat is 7th line
    	    #lat <- strsplit(dum1,"\t")[[1]][2]

	    #dum1 <-  readLines(filename,n=8)[8] ## lon is 8th line
    	    #lon <- strsplit(dum1,"\t")[[1]][2]

      	 }
	
      }

      # if skewt does not exist, continue
      if (skewtExists == FALSE) {

      	 ## now calculate hodograph
      	 hodo <- calc.hodo(data)
      	 hodo <- hodo[complete.cases(hodo),]

      	 ## for PRECIP change file naming convention for skewt
      	 #png(paste(pngDir,"/research.SkewT.",yymmdd,hhmm,".",site,"_CWB.png",sep=""),height=9,width=9,unit="in",res=100)
      	 png(skewtFile,height=9,width=9,unit="in",res=100)
      	 #plotskew(dataSub, hodo, parcel=3, thinwind=40, title=paste("CWB-",site," radiosonde for PRECIP -- preliminary data",sep=""), date=paste("Lat:",lat,"Lon:",lon,"  ",hhmm,"UTC ",date))
      	 plotskew(data, hodo, parcel=3, thinwind=40, title=title, date=paste("Lat:",lat,"Lon:",lon,"  ",hhmm,"UTC ",date))

      	 dev.off()

      	 ### now, write out a SHARPpy-format file too:
      	 ## SHARPpy will choke if the height of the sonde descends anywhere.  Remove any places where this happens:
      	 data[which(data$alt[2:length(data$alt)]-data$alt[1:length(data$alt)-1]<=0)+1,] <- NA  ## (looking for places where the height above is less than height below)

      	 ## now, remove rows that are all NAs:
      	 data <- data[rowSums(is.na(data)) != ncol(data),]
      	 ## set any remaining NA's to -9999.00
      	 data[is.na(data)] <- -9999.00

      	 ## now, create data frame with just the needed columns:
      	 data_sub <- data.frame(data$press,data$alt,data$temp,data$dewpt,data$dir,data$wspd)
      	 ## and we need to thin this out, since the high resolution sounding data is a bit too much for SHARPpy:
      	 data_sub <- data_sub[seq(1,length(data_sub$data.press),40),]   ## the number in here is to pull every Nth row 

      	 ## first, the header info:
      	 #outfile <- paste(SHARPpyDir,"/",yymmdd,hhmm,".",site,"_CWB_PRECIP",sep="")
      	 outfile <- sharppyFile
      	 fileConn <- file(outfile)
      	 writeLines(c("%TITLE%",paste(" CSU-PRECIP  ",gemdate,"/",hhmm,sep="")," ","   LEVEL       HGHT       TEMP       DWPT       WDIR       WSPD","-------------------------------------------------------------------","%RAW%"),fileConn)
      	 close(fileConn)

      	 ## and now write the data
      	 write.fwf(format(data_sub,width=9,nsmall=2), file=outfile, sep=",", justify="right",colnames=FALSE, append=TRUE)

      	 ## and the "END" statement:
      	 cat("%END%",file=outfile, append=TRUE)

      	 # Move edt file to DONE subdir
      	 #outDir <- paste(rawDir,"/DONE",sep="")
      	 #move_files(filename,outDir, overwrite = FALSE)
      	 if (file.exists(filename_out) == TRUE) {
      	    unlink(filename_out)
      	 }

      	 # if manual launch from Hsinchu, ftp file to catalog
      	 if (manualLaunch == TRUE) {
      	    cmd <- paste(binDir,Hsinchu_skewt_to_FC.sh,sep="")
	    cmd = paste(cmd,skewtFile)
	    system(cmd)
      	 }

      }  # if skewtExists == FALSE

   }  # if not Yonaguni file

}  # for filename in filenames

}  # end of function
