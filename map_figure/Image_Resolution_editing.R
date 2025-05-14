# making R images high resolution

setwd("~/Downloads")

#general format: Don't forget to change the .jpg image name to match
jpeg(
  filename="apiglike.jpg",
  width=8,
  height=8,
  units="in",
  res=1000)

#insert code here


dev.off()

