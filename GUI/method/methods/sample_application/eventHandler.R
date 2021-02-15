setApplicationConf  <- function(printer_head_config, plate_config, band_config, step, estimated_time){
    Method$control[[step]] = list(type="Sample Application",
                                  printer_head_config=printer_head_config,
                                  plate_config = plate_config,
                                  band_config = band_config,
                                  estimated_time = estimated_time)


}

toPythonTableHeadFormat  <- function(tableHeadConf) {
    return (settingsTabletoPythonDict(tableHeadConf, head_conf_pythonKeys, head_conf_labels))
}

toPythonTablePlateFormat  <- function(tablePlateConf) {
    return (settingsTabletoPythonDict(tablePlateConf, plate_conf_pythonKeys, plate_conf_labels))
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

getEstimatedTime <- function(){
    step = getSelectedStep()
    return (Method$control[[step]]$estimated_time)
}

step_add  <- function(){
    step = length(Method$control) + 1
    headConf = sample_application_driver$get_default_printer_head_config()
    plateConf = sample_application_driver$get_default_plate_config()
    bandConf = sample_application_driver$update_settings(plateConf, headConf, number_of_bands=5)
    estimated_time = sample_application_driver$get_print_time()
    
    setApplicationConf(headConf, plateConf, bandConf, step, estimated_time)

    showInfo("Please configure your sample application process")
}


step_start <- function(){
    estimated_time = getEstimatedTime()
    withProgress(message = paste0('Applying the sample, please wait it takes:',estimated_time), value =0, {
        sample_application_driver$start_application()
       })
    
}


observeEvent(input$sample_application_settings_update,{
    step = getSelectedStep()
    pyPlate = getPlateConfigFromTable()
    pyHead = getHeadConfigFromTable()
    band_list = getBandConfigFromTable()
    
    numberOfBands = as.numeric(input$number_of_bands)
    bandList = sample_application_driver$update_settings(plate_config=pyPlate,
                                                         head_config=pyHead,
                                                         band_config=band_list,
                                                         number_of_bands=numberOfBands)

    estimated_time = sample_application_driver$get_print_time()
    setApplicationConf(pyHead, pyPlate, bandList, step, estimated_time)
})

