#!/usr/bin/Rscript

args = commandArgs(trailingOnly=TRUE)

if (length(args) != 2) {
   print("Usage: run.skewt.cwb_edt_allDay.R [YYYYMMDD] [5-digit site ID]")
   quit()
} else {
  strDate = args[1]
  site = args[2]
}

print(strDate)
print(site)

source("/home/disk/monsoon/precip/bin/skewt.cwb_edt_allDay.R")

skewt.cwb_edt_allDay(strDate,site)
