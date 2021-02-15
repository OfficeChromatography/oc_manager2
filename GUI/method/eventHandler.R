PATH = "./GUI/method"
PATH_methods = paste0(PATH,"/methods/")
PATH_load = paste0(PATH,"/method_to_load/")

renderMethodsUI <- function (type){
    switch (type,
            "Sample Application" = {
                ## load UI
                source(paste0 (PATH_methods,"sample_application/ui.R"), local=T)
                output$methodUI  <- methodsUI_sample_application
                },
            "Development" = {
                ## load UI
                source(paste0 (PATH_methods,"development/ui.R"), local=T)
                output$methodUI <- methodsUI_development
                },
            "Documentation" = {
                ## load UI
                source(paste0 (PATH_methods,"documentation/ui.R"), local=T)
                output$methodUI <- methodsUI_documentation
                }
            )

}

eventHandlerMethods <- function (type){
    switch (type,
            "Sample Application" = {
                ##load event Handler
                source(paste0 (PATH_methods,"sample_application/eventHandler.R"), local=T)
                },
            "Development" = {
                ##load event Handler
                source(paste0 (PATH_methods,"development/eventHandler.R"), local=T)
                },
            "Documentation" = {
                ##load event Handler
                source(paste0 (PATH_methods,"documentation/eventHandler.R"), local=T)
            }
            )
    # override function for each eventHandler
    step_add_Methods <<- step_add
    step_start_Methods <<- step_start
 }



showInfo  <<- function(msg) {
    Method_feedback$text = msg
}

getSelectedStep  <<- function(){
    return (as.numeric(input$Method_steps))
}

get_Method_type <<- function () {
    index = getSelectedStep()
    return (Method$control[[index]]$type)
}



## methods
observeEvent(input$Method_step_add,{
    type = input$Method_step_new
    renderMethodsUI(type)
    eventHandlerMethods(type)
    step_add_Methods()
    Method$selected = length(Method$control)
})

observeEvent(input$Method_step_delete,{
    index = getSelectedStep()
    if(index > 0) {
        Method$control[[index]] = NULL
    }
    Method$selected = length (Method$control)

})



## start
observeEvent(input$Method_step_exec,{
    step_start_Methods()
})


## save
observeEvent(input$Method_save,{
    filePath = paste0(PATH_load,input$Method_save_name,".Rdata")
    control = Method$control
    save(control,file=filePath)
    Method_feedback$text = paste0("Saved ", filePath)
})

observeEvent(input$Method_load,{
    loadMethod = input$Method_load_name
    if (!is.null(loadMethod)){
        load(paste0(PATH_load,loadMethod))
        Method$control=control
        Method_feedback$text = "Method loaded"
    }
    else{
        Method_feedback$text = "Method can't load, no file selected"
    }
    Method$selected = 0
})


observeEvent(input$Method_steps,{
    type = get_Method_type()
    renderMethodsUI(type)
    Method$selected = getSelectedStep()
 })
