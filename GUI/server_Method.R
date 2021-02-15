########## METHOD #############################################
# load control variable
Method <<- reactiveValues(control=list(),selected = 1)
Method_feedback <<- reactiveValues(text="No feedback yet")
#load event Handler
source("./GUI/method/eventHandler.R", local=T)
# load UI
source("./GUI/method/ui.R", local=T)
# load driver
sample_application_driver <<- ocDriver$get_sample_application_driver()
development_driver <<- ocDriver$get_development_driver()
documentation_driver <<- ocDriver$get_documentation_driver()



# load configs
## band_config
band_pythonKeys <<- c("label", "nozzle_id","drop_volume","volume_set", "volume_real", "start", "end")
band_labels <<- c("Label", "Nozzle Id","Drop volume [nl]","Volume set [µl]", "Volume real [µl]", "Approx. band start [mm]", "Approx. band end [mm]")

### plate config
plate_conf_pythonKeys <<-  c("relative_band_distance_y", "relative_band_distance_x" ,"band_length", "band_height", "gap","plate_x","plate_y","print_bothways", "heating_temperature")
plate_conf_labels <<- c("Band distance [Y]", "Band distance [X]","Band length","Band height", "Gap","Plate X","Plate Y", "Print both ways", "Heating Temperature")
plate_conf_units <<- c("mm", "mm", "mm", "mm", "mm ", "mm", "mm","", "°C")


### printer head config
head_conf_pythonKeys <<- c("speed", "pulse_delay", "fire_delay" , "number_of_fire" , "step_range", "printer_head_resolution", "kind_of_fire", "waiting_time", "number_of_working_nozzles" )
head_conf_labels <<-  c("Speed", "Pulse delay", "Fire delay", "Number of fire", "Step range", "Printer head resolution","Kind of fire", "Waiting time","Number of working nozzles" )
head_conf_units <<-  c("mm/m", "\U00B5s","\U00B5s", "", "mm", "mm","","ms","")

# documentation
LED_pythonKeys <<- c("label", "white", "red", "green", "blue","UVA","UVC")
LED_labels <<- c("Label", "White","Red", "Green", "Blue","UVA","UVC")
