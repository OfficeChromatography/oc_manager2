# This is the server logic for a Shiny web application.
# You can find out more about building applications with Shiny here:
#
# http://shiny.rstudio.com

library(shiny)
# library(rPython)
library(reticulate)
#library(DLC)
library(serial)#for port detection in windows
library(rhandsontable)
library(parallel)
library(shinyBS)
library(shinyalert)


shinyServer(function(input, output,session) {
  source("./OCDriverLoader.R", local = T)
  source("GUI/server_Connection.R", local = T)
  source("GUI/server_Fine_control.R", local = T)
  source("GUI/server_Method.R", local = T)
   
  session$onSessionEnded(function() {
      ocDriver$disconnect()
      stopApp()
  })

})


