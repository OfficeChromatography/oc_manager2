#!/usr/bin/env Rscript



## app_exec for OC_manager on the pi, to be call with crontab, from the pi, to allow access on the local network to the instrument



shiny::runApp("/home/pi/OC_manager2/",host="0.0.0.0",port=80)



# shiny::runApp("/home/clau/Documents/Dropbox_true/Dropbox/OC/Software/OC_manager/",host="0.0.0.0",port=5579,launch.browser = T)