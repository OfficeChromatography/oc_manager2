setApplicationConf  <- function(printer_head_config, plate_config, band_config, step){
    Method$control[[step]] = list(type="Development",
                                  printer_head_config=printer_head_config,
                                  plate_config = plate_config,
                                  band_config = band_config)
}

toPythonTableHeadFormat  <- function(tableHeadConf) {
    return (settingsTabletoPythonDict(tableHeadConf, head_conf_pythonKeys, head_conf_labels))
}

toPythonTablePlateFormat  <- function(tablePlateConf) {
    #band_length_value = development_driver$calculate_band_length()
    #labels_to_append = c("Band Length","Gap")
    #units_to_append =  c("mm","mm")
    #append_dataFrame = data.frame(row.names= labels_to_append,
                                #  "values"= c(band_length_value,0), "units" = units_to_append)
    #tablePlateConf_appended = rbind(tablePlateConf),append_dataFrame)
    labels_to_append = c("Gap")
    units_to_append =  c("mm ")
    append_dataFrame = data.frame(row.names= labels_to_append,
                                  "values"= 0, "units" = units_to_append)
    tablePlateConf_appended = rbind(tablePlateConf,append_dataFrame)
    return (settingsTabletoPythonDict(tablePlateConf_appended, plate_conf_pythonKeys,
                                      plate_conf_labels))
}




getBandConfigFromTable <- function(){
    bandlistTable= hot_to_r(input$band_config)
    return (bandConfSettingsTableFormatToPython(bandlistTable))

}

getPlateConfigFromTable <- function (){
    plateTable = hot_to_r(input$plate_config)
    return (toPythonTablePlateFormat(plateTable))
}

getHeadConfigFromTable <- function (){
    headTable = hot_to_r(input$printer_head_config)
    return (toPythonTableHeadFormat(headTable))
}

get_default_plate_config <-function(){
    return (development_driver$get_default_plate_config())
}

get_default_printer_head_config <- function(){
    return (development_driver$get_default_printer_head_config())
}


step_add  <- function(){
    step = length(Method$control) + 1
    headConf = get_default_printer_head_config()
    plateConf = get_default_plate_config()
    bandConf = development_driver$update_settings(plateConf, headConf)

    setApplicationConf(headConf, plateConf, bandConf, step)

    showInfo("Please configure your development process")
}


step_start <- function(){
    bandlistpy =  getBandConfigFromTable()
    development_driver$start_application()
}

observeEvent(input$development_settings_update,{
    step = getSelectedStep()
    pyPlate = getPlateConfigFromTable()
    pyHead = getHeadConfigFromTable()
    band_list = getBandConfigFromTable()
    bandList = development_driver$update_settings(plate_config=pyPlate,
                                                  head_config=pyHead,
                                                  band_config=band_list)
    pyPlate$band_length = development_driver$get_band_length()

    setApplicationConf(pyHead, pyPlate, bandList, step)
})
