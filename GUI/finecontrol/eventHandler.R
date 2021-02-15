

observeEvent(input$test_ink_cmd_button,{
    fineControlDriver$customCommand(toupper(input$test_ink_cmd))

})

observeEvent(input$xleft,{
    fineControlDriver$goXLeft()
})
observeEvent(input$xhome,{
    fineControlDriver$goXHome()
})

observeEvent(input$xright,{
    fineControlDriver$goXRight()
})

observeEvent(input$yup,{
    fineControlDriver$goYUp()
})

observeEvent(input$yhome,{
    fineControlDriver$goYHome()
})

observeEvent(input$ydown,{
    fineControlDriver$goYDown()
})

observeEvent(input$stop,{
    fineControlDriver$stop()
})


#---------------------------------------------------------------------------------------
#Inkjet
#-------
                                        # TODO REFACTOR
writeFile  <- function(filePath, input){
    fileConn<-file(filePath)
    writeLines(input, fileConn)
    close(fileConn)
}

toTableApply_settings <- function (pythonHeadConf){
    number_of_fire = pythonHeadConf[["number_of_fire"]]
    pulse_delay = pythonHeadConf[["pulse_delay"]]
    fineControl_printhead_dict = list (number_of_fire = number_of_fire ,
                                       pulse_delay =pulse_delay)
    labels = c("Number of Fire", "Pulse Delay")
    pythonKeys = c("number_of_fire","pulse_delay")
    units = c("","\U00B5s")

    return ( toRSettingsTableFormat(fineControl_printhead_dict, pythonKeys, labels, units) )
}

toPythonTableApply_settings <- function (tableHeadConf, printer_head_config){
    values = tableHeadConf[["values"]]
    printer_head_config[["number_of_fire"]] = values[[1]]
    printer_head_config[["pulse_delay"]] = values [[2]]
    return (printer_head_config)
}


output$application_settings = renderRHandsontable({
  config= fineControlDriver$get_default_printer_head_config()
  table = toTableApply_settings(config)
  rhandsontable(table, rowHeaderWidth = 160) %>%
      hot_cols(colWidth = 100)  %>%
      hot_col("units", readOnly = TRUE)
})

observeEvent(input$test_ink_nozzle_test,{
    selected_nozzles = getUserInputforInkjet()
    fineControlDriver$nozzle_testing_process(selected_nozzles)

})

observeEvent(input$test_ink_fire_selected_nozzles,{
    selected_nozzles = getUserInputforInkjet()
    fineControlDriver$fire_selected_nozzles(selected_nozzles)
})

get_start_position <- function (){
    return (as.numeric (input$Noozle_test_start_y))
    }


getUserInputforInkjet <- function (){
    headTable = hot_to_r(input$application_settings)
    printer_head_config = fineControlDriver$get_default_printer_head_config()
    updated_printer_head_config = toPythonTableApply_settings(headTable, printer_head_config)
    fineControlDriver$set_configs(updated_printer_head_config, get_start_position())
    selected_nozzles = as.list(input$test_ink_selected_nozzles)
}

#----------------------------------------------------------------------------------------
#Gcode
observeEvent(input$test_ink_gcode_file_action,{
    ocDriver$send_from_file(input$test_ink_gcode_file$datapath)
})

observeEvent(input$pause,{
    ocDriver$pause()
})

observeEvent(input$resume,{
    ocDriver$resume()
})



#----------------------------------------------------------------------------------------
#Docu

observeEvent(input$test_ink_visu_position,{
    fineControlDriver$go_to_foto_position()
})
observeEvent(input$test_ink_ring_on,{
    fineControlDriver$LEDs(255,255,255,255)
})
observeEvent(input$test_ink_ring_off,{
    fineControlDriver$LEDs()
})




