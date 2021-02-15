# This is the user-interface definition of a Shiny web application.
# You can find out more about building applications with Shiny here:
#
# http://shiny.rstudio.com
#

library(shiny)
library(shinydashboard)
library(shinyBS)
library(shinyalert)

dbHeader <- dashboardHeader(title = "OC Manager2")

dashboardPage(
  dbHeader,
  dashboardSidebar(width=125,
    sidebarMenu(style = "position: fixed; overflow: visible;",
                menuItem("Connection", tabName = "Connect",icon=icon("home")),
                menuItem("Fine control", tabName = "Fine_Control", icon=icon("wrench")),
                menuItem("Method", tabName = "Method",icon=icon("tasks"))
    )
  ),

  dashboardBody(
    tags$script(HTML("$('body').addClass('sidebar-mini');")),
    fluidRow(
    tabItems(
      tabItem(
        tags$head(tags$style(type="text/css", "tfoot {display: table-header-group}")),
        tags$head(tags$style(type="text/css", "tfoot {display: table-header-group}")),
        tags$head(tags$style(HTML(".shiny-output-error-validation {color: red;font-size: 24px}"))),
        tags$head(tags$style(type="text/css", ".shiny-progress .progress {position: absolute;width: 100%;top: 100px;height: 10px;margin: 0px;}")),
        tags$head(tags$style(type="text/css", ".shiny-progress .progress-text {position: absolute;border-style: solid;
                                     border-width: 2px;right: 10px;height: 36px;width: 50%;background-color: #EEF8FF;margin: 0px;padding: 2px 3px;opacity: 1;}"))
      ),
      # First tab content
      tabItem(tabName = "Connect",
              uiOutput("server_connection")
       ),
      # First tab content
      tabItem(tabName = "Fine_Control",
              uiOutput("server_Fine_control")
      ),
      tabItem(tabName = "Method",
              uiOutput("server_method")

      )
    )
  )
  )
)



