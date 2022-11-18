#!/usr/bin/Rscript

skewt.csu <- function() {
## R script to plot the skew-T from a CSU sonde

#source("plotskew.R")
#source("calc.hodo.R")
#library("RadioSonde")
library("RadioSonde.RSS")
library("gdata")
library("filesstrings")

baseDir <- "/home/snowband/brodzik/precip/raw/sounding_csu"
edtDir <- paste(baseDir,"/edt",sep="")
pngDir <- paste(baseDir,"/png",sep="")
SHARPpyDir <- paste(baseDir,"/SHARPpy",sep="")

#filenames <- list.files(edtDir,full.names=TRUE)
filenames <- Sys.glob(file.path(edtDir,"edt_*"))

for (filename in filenames)
{
    #filename <- filenames[length(filenames)]
    file <- basename(filename)
    print(file)
    yymmdd <- strsplit(file,"_")[[1]][2]
    dum <- strsplit(file,"_")[[1]][3]
    hhmm <- substr(dum,1,4)
    gemdate <- substr(yymmdd,3,8)

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
    dum1 <- readLines(filename,n=6)[6] # date is 6th line
    dum2 <- strsplit(dum1,"\t")[[1]][2]  # get rid of space
    date <- strsplit(dum2,"T")[[1]][1]

    ## and similarly the lat/lon
    dum1 <-  readLines(filename,n=7)[7] ## lat is 7th line
    lat <- strsplit(dum1,"\t")[[1]][2]

    dum1 <-  readLines(filename,n=8)[8] ## lon is 8th line
    lon <- strsplit(dum1,"\t")[[1]][2]

    ## now calculate hodograph
    hodo <- calc.hodo(data)
    hodo <- hodo[complete.cases(hodo),]

    ## for PRECIP change file naming convention for skewt
    png(paste(pngDir,"/research.SkewT.",yymmdd,hhmm,".Yonaguni_CSU.png",sep=""),height=9,width=9,unit="in",res=100)
    plotskew(data, hodo, parcel=3, thinwind=40, title="CSU radiosonde for PRECIP -- preliminary data", date=paste("Lat:",lat,"Lon:",lon,"  ",hhmm,"UTC ",date))

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
    outfile <- paste(SHARPpyDir,"/",yymmdd,hhmm,".CSU_PRECIIP",sep="")
    fileConn <- file(outfile)
    writeLines(c("%TITLE%",paste(" CSU-PRECIP  ",gemdate,"/",hhmm,sep="")," ","   LEVEL       HGHT       TEMP       DWPT       WDIR       WSPD","-------------------------------------------------------------------","%RAW%"),fileConn)
    close(fileConn)

    ## and now write the data
    write.fwf(format(data_sub,width=9,nsmall=2), file=outfile, sep=",", justify="right",colnames=FALSE, append=TRUE)

    ## and the "END" statement:
    cat("%END%",file=outfile, append=TRUE)

    # Move edt file to DONE subdir
    outDir <- paste(edtDir,"/DONE",sep="")
    move_files(filename,outDir, overwrite = FALSE)
}

}
