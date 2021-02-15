#abstract
setDocumentationConf  <- function(pictures_config, preview_config, step){
    Method$control[[step]] = list(type="Documentation",
                                  pictures_config = pictures_config,
                                  preview_config = preview_config)

}


# abstract
step_add  <- function(){
    step = length(Method$control) + 1
    pictures_config = documentation_driver$get_picture_list()
    preview_config = documentation_driver$get_preview_list()[[1]]
    setDocumentationConf(pictures_config, preview_config, step)
                         
    showInfo("Please configure your documentation proccess")
}


step_start <- function(){
    pictures_list = getPicturesConfigFromTable()
    withProgress(message = 'Taking images please wait', value = 0, {
        documentation_driver$make_pictures_for_documentation(pictures_list)
       })
}


getPicturesConfigFromTable  <- function(){
    settingsFormat = hot_to_r(input$pictures_config)
    return (settingsTabletoPythonDict(settingsFormat, LED_pythonKeys, LED_labels))    
}

getPreviewConfigFromTable <- function (){
    settingsFormat = hot_to_r(input$preview_config)
    list = settingsTabletoPythonDict(settingsFormat, LED_pythonKeys, LED_labels, TRUE)
    return (list) 

}

observeEvent(input$documentation_pictures_update,{
    number_of_pictures =  getNumberOfPictures()
    pictures_list = getPicturesConfigFromTable()
    pictures_list = documentation_driver$update_settings(pictures_list, number_of_pictures)
                                                        
    step = getSelectedStep()
    Method$control[[step]]$pictures_config = pictures_list
})


observeEvent(input$take_a_picture,{
    preview_list = getPreviewConfigFromTable()
    documentation_driver$make_preview(preview_list)
    creat_random_image_hash()
})

observeEvent(input$go_home,{
    documentation_driver$go_home()
})


