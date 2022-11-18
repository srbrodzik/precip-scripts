#!/usr/bin/Rscript

skewt.csu <- function(strDate,site) {
## R script to plot the skew-T from a CSU sonde

#source("plotskew.R")
#source("calc.hodo.R")
#library("RadioSonde")
library("RadioSonde.RSS")
library("gdata")
library("filesstrings")
#library("tidyverse")
#library("dplyr")

## FOR TESTING
strDate = "20220525"
site = "46757"

rawDir <- paste("/home/snowband/brodzik/precip/raw/sounding/",strDate,sep="")
pngDir <- paste("/home/snowband/brodzik/precip/skewt/",strDate,sep="")
if (file.exists(pngDir)) {
} else {
  dir.create(pngDir)
}
SHARPpyDir <- paste("/home/snowband/brodzik/precip/skewt/SHARPpy/",strDate,sep="")
if (file.exists(SHARPpyDir)) {
} else {
  dir.create(SHARPpyDir)
}

filenames <- Sys.glob(file.path(rawDir,"46757-*.edt.txt"))

for (filename in filenames)
{
    file <- basename(filename)
    print(file)
    base <- strsplit(file,"[.]")[[1]][1]
    datetime <-strsplit(base,"-")[[1]][2]
    yymmdd <- substr(datetime,1,8)
    gemdate <- substr(datetime,3,8)
    hhmm <- paste(substr(datetime,9,10),"00",sep="")

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
    minPress <- min(data[!data$press %in% exclude,]$press)
    lastGoodRow <- which (data$press == minPress)
    dataSub <- data[1:lastGoodRow,]

    ## get date from the file
    dum1 <- readLines(filename_out,n=1)[1] # date is in 1st line
    date <- strsplit(dum1, " +")[[1]][3]  # get rid of space

    ## and similarly the lat/lon
    lat <- "24.828"
    lon <- "121.014"

    ## now calculate hodograph
    hodo <- calc.hodo(data)
    hodo <- hodo[complete.cases(hodo),]

    ## for PRECIP change file naming convention for skewt
    png(paste(pngDir,"/research.SkewT.",yymmdd,hhmm,".46757_CWB.png",sep=""),height=9,width=9,unit="in",res=100)
    #plotskew(data, hodo, parcel=3, thinwind=40, title="CWB radiosonde for PRECIP -- preliminary data", date=paste("Lat:",lat,"Lon:",lon,"  ",hhmm,"UTC ",date))
    plotskew(dataSub, hodo, parcel=3, thinwind=40, title=paste("CWB-",site," radiosonde for PRECIP -- preliminary data",sep=""), date=paste("Lat:",lat,"Lon:",lon,"  ",hhmm,"UTC ",date))

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
    outfile <- paste(SHARPpyDir,"/",yymmdd,hhmm,".46757_CWB_PRECIIP",sep="")
    fileConn <- file(outfile)
    writeLines(c("%TITLE%",paste(" CSU-PRECIP  ",gemdate,"/",hhmm,sep="")," ","   LEVEL       HGHT       TEMP       DWPT       WDIR       WSPD","-------------------------------------------------------------------","%RAW%"),fileConn)
    close(fileConn)

    ## and now write the data
    write.fwf(format(data_sub,width=9,nsmall=2), file=outfile, sep=",", justify="right",colnames=FALSE, append=TRUE)

    ## and the "END" statement:
    cat("%END%",file=outfile, append=TRUE)

    # Move edt file to DONE subdir
    outDir <- paste(rawDir,"/DONE",sep="")
    move_files(filename,outDir, overwrite = FALSE)
    unlink(filename_out)
}

}
