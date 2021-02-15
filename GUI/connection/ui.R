output$server_connection = renderUI({
    column(4, h4("Board"),
          actionButton("Serial_port_refresh","Refresh serial port",icon=icon("refresh")),
          uiOutput("Serial_portUI"), # show the /dev directory
          uiOutput("Serial_port_connectUI") # show an actionButton only if connect$login is TRUE and set connect$board to TRUE
          )
})

output$Serial_portUI = renderUI({
    input$Serial_port_refresh
    #selectizeInput("Serial_port","Select serial port",choices = listPorts()) # or windows
    selectizeInput("Serial_port","Select serial port",choices = dir("/dev/",pattern = "ACM",full.names = T))
  })

output$Serial_port_connectUI = renderUI({
    if(!board$connected){
      actionButton("Serial_port_connect","Connect the board")
    }else{
      actionButton("Serial_port_disconnect","Disconnect the board")
    }
  })
