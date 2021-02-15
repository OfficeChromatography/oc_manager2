methodsUI_documentation <- renderUI({
    fluidPage(
    fluidRow(
        box(title = "Image Settings", width = "85%", height = "45%",status = "primary",
           uiOutput("documentation_settings"))
    ),
    fluidRow(
    box(title = "Preview", width = "85%", height = "45%",status = "primary",
        uiOutput("documentation_preview"))
    )
    )
})


## settings
output$documentation_settings = renderUI({
    validate(
    need(length(Method$control) > 0 ,"Add a step or load a saved method")
    )
  if(!is.null(input$Method_steps)){
    tagList(
        fluidPage(
            column(10,box(title = "Images", width = "33%", height = "45%",status = "warning",
                         rHandsontableOutput("pictures_config")
                         )
                   ),
            column(2,box(title = "Number of images", width = "33%", height = "45%",status = "warning",
                         fluidRow(textInput("number_of_pictures", "", getNumberOfPictures(),width="100%")),
                         fluidRow(actionButton("documentation_pictures_update"," Update ",icon=icon("gears"), width="100%"))
                         )
                   )
        )
        )
  }
})


getNumberOfPictures <<- function(){
    numberOfPictures = input$number_of_pictures
    if (is.null ( numberOfPictures )) {
        numberOfPictures = 2

    }
    return (numberOfPictures)
}

get_Image_Path <- function (){
    documentation_driver$get_Preview_Path()
}


pictures_config_to_Table_Format<- function (pictures_config){
    return (toRSettingsTableFormat(pictures_config, LED_pythonKeys, LED_labels))
}

preview_config_to_Table_Format <- function (preview_config){
    settingsTable = toRSettingsTableFormat(preview_config, LED_pythonKeys, LED_labels, TRUE)
    settingsTable$units <- NULL
    return (settingsTable)
}
  

## information
output$documentation_preview = renderUI({
  validate(
    need(length(Method$control) > 0 ,"Add a step or load a saved method")
  )
  if(!is.null(input$Method_steps)){
    tagList(
        column(8,box(title = "Image Preview", width = "33%", height = "45%",status = "warning",
        tags$img(src = paste0("Preview.jpg?",image$hash), height = 400, width = 400))),
        column(4,box(title = "Settings", width = "33%", height = "45%",status = "warning",
                     rHandsontableOutput("preview_config"),
                     actionButton("take_a_picture",label = "Take an image", icon=icon("camera")),
                     fluidRow (actionButton("go_home",label = "Go Home", icon= icon("home")) )
                     )
              )
        )
  }
})


image <- reactiveValues (hash = "")

creat_random_image_hash <<- function(){
    image$hash <- toString(sample(1:100, 1))
}
 
output$Method_step_feedback = renderText({
  validate(
    need(length(Method$control) > 0 ,"add a step or load a saved method")
  )
  Method$control[[as.numeric(input$Method_steps)]]$info
})


output$pictures_config = renderRHandsontable({
    if(!is.null(input$Method_steps)) {
        index = getSelectedStep()
        pictures_list = Method$control[[index]]$pictures_config
        table = pictures_config_to_Table_Format(pictures_list)
        rhandsontable(table, rowHeaders = NULL) %>%
            hot_cols(colWidth = 80) %>%
	    hot_col("Label", width = 90)
    }
})


output$preview_config = renderRHandsontable({
    if(!is.null(input$Method_steps)) {
        index = getSelectedStep()
        preview_list = Method$control[[index]]$preview_config
        table = preview_config_to_Table_Format(preview_list)
        rhandsontable(table, colHeaders = NULL)%>%
            hot_cols(colWidth = 80)
        }
})    

