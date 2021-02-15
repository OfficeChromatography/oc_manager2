

output$server_method = renderUI({
  tagList(
    fluidPage(
    column(3,box(title = "Methods", width = "25%", height = 350,solidHeader = TRUE,status = "primary",
        fluidRow(
        column(1, actionButton("Method_step_add","",icon=icon("plus"))),
        column(1,offset=1,actionButton("Method_step_delete","",icon = icon("window-close")))),
        fluidRow(column(10,ofsett=1,selectizeInput("Method_step_new","",
                                                   choices = c("Sample Application",
                                                               "Development",
                                                               "Documentation"
                                                               ), width = "100%"))),
        fluidRow(
        sidebarPanel( id = "Steps",style = "overflow-y:scroll; height: 175px; position:relative; ", width = 12,
          uiOutput("Method_control_methods")))
        ),
    box( title = "Save & Load",width = "15%", height = "10%",solidHeader = TRUE,status = "primary",
         fluidRow(
         column(9,textInput("Method_save_name","Saving name","Sandbox", width = "100%")),
             column(1,actionButton("Method_save","",icon=icon("save")))
         ),
         fluidRow(
             column(9,selectizeInput("Method_load_name","Method to load",choices=dir("/home/pi/OC_manager2/GUI/method/method_to_load/"))),
             column(1,actionButton("Method_load","",icon=icon("folder-o")))
        )),
    box(title = "Start", width = "15%", height = "10%",solidHeader = TRUE,status = "primary",
        column(1,actionButton("Method_step_exec","",icon = icon("play")))
        ),
    box( width = "15%",status = "warning",
         uiOutput("Method_feedback"))
    ),
    column(9, uiOutput("methodUI"))
  )
  )
})

#output$methods_ui = renderUI (ui_methods_env$methodsUI)

output$Method_control_methods = renderUI({
  validate(
    need(length(Method$control) > 0 ,"Add a step or load a saved method")
  )
  # input$Method_step_add
  truc = seq(length(Method$control))
  names(truc) = paste0("Step ",truc,": ",lapply(Method$control,function(x){x$type}))
  radioButtons("Method_steps","Steps:",choices = truc,selected = Method$selected)
})


## gcode viewer
output$Method_control_gcode = renderUI({
  validate(
    need(length(Method$control) > 0 ,"Add a step or load a saved method")
  )
  if(!is.null(input$Method_steps)){
    tagList(
        fluidPage(
        fluidRow(downloadButton("Method_gcode_download","Download Gcode"))
      )
    )
  }
})


## feedback
output$Method_feedback = renderText({
  Method_feedback$text
})
