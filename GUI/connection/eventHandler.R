board <<- reactiveValues(connected = FALSE)

Connect_with_the_board  <<- function(){
    ocDriver$connect()
    board$connected <<- TRUE
    if (!ocDriver$is_connected()){
        shinyalert("Oops!", "Can't connect the Board please try again", type = "error")
        board$connected <<- FALSE
   }
}


observeEvent(input$Serial_port_connect,{
     if(nchar(input$Serial_port) == 0){
         shinyalert("Oops!", "No board selected", type = "error")
     }else{
         Connect_with_the_board()
     }
  })

observeEvent(input$Serial_port_disconnect,{
    ocDriver$disconnect()
    if (!ocDriver$is_connected()){
        board$connected <<- FALSE
        }
    })

#auto connect
Connect_with_the_board()

