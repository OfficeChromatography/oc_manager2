output$server_Fine_control = renderUI({
  tagList(
  fluidPage(
  column(6,
      fluidRow(
      box(title = "Motor Control", width = "50 %", heigth ="50 %",solidHeader = TRUE,status = "primary",
      fluidRow(
      column(6,
      fluidRow(
          column(2,"X :"),
          column(2,offset=1,actionButton("xleft","",icon=icon("arrow-left"))),
          column(2,actionButton("xhome","",icon=icon("home"))),
          column(2,actionButton("xright","",icon=icon("arrow-right")))
           ),

      fluidRow(
          column(2,"Y :"),
          column(2,offset=1,actionButton("yup","",icon=icon("arrow-up"))),
          column(2,actionButton("yhome","",icon=icon("home"))),
          column(2,actionButton("ydown","",icon=icon("arrow-down")))
           )),

      column(4,
           actionButton("stop","Disable Motors")
           )),
      fluidRow(
        column(8,
           textInput("test_ink_cmd","Command","G1 X10", width = "100%"),
           actionButton("test_ink_cmd_button","Launch GCODE")
          )
        )
      )),
     fluidRow(
     box(title = "GCode upload", width = "50 %", heigth ="50 %", solidHeader = TRUE,status = "primary",
                    fileInput("test_ink_gcode_file","Upload a GCODE file"),
         actionButton("test_ink_gcode_file_action","Launch the GCODE file")

         )
     ),
     fluidRow(
     box(title = "Documentation", width = "50 %", heigth ="50 %", solidHeader = TRUE,status = "primary",
                    actionButton("test_ink_visu_position","Go in position"),
                    actionButton("test_ink_ring_on","RGBW_LEDs on"),
                    actionButton("test_ink_ring_off","RGBW_LEDs off")
       ))

  ),
  column(6,
         box(title = "Inkjet", width = "50 %", heigth ="50 %", solidHeader = TRUE,status = "primary",
           rHandsontableOutput("application_settings"),
           textInput("Noozle_test_start_y","Starting Position Y [mm]","10", width = "100%"),
           checkboxGroupInput("test_ink_selected_nozzles","Nozzles to fire",
                              choices = fineControlDriver$get_Nozzles_Ids(),
                              inline = T,selected = 1),
           actionButton("test_ink_fire_selected_nozzles",label = "Fire selected nozzles"),
           actionButton("test_ink_nozzle_test",label = "Nozzle testing process")
    )
  )
  )
  )
})
