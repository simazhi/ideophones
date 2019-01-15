#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

#global.R
library(shiny)
library(tidyverse)
library(readxl)

# Here is the data and stuff

ideodata <- read_xlsx("data.xlsx") %>%
    filter(morph != "NOTIDEOPHONE") %>%
    select(pinyinnone,
           traditional,
           pinyintone,
           MC,
           OC,
           zdic)

# #memoise for caching
# get_ideo_tc <- memoise(function(searchterm){
#     data %>%
#         filter(str_detect(pinyinnum, searchterm))
# })



## SERVER
# Load the ggplot2 package which provides
# the 'mpg' dataset.
library(ggplot2)

server <- 
function(input, output) {
    
    # Filter data based on selections
    output$table <- DT::renderDataTable(DT::datatable({
        data <- ideodata
        if (input$py != "All") {
            data <- data[data$pinyintone == input$py,]
        }
        # if (input$cyl != "All") {
        #     data <- data[data$cyl == input$cyl,]
        # }
        # if (input$trans != "All") {
        #     data <- data[data$trans == input$trans,]
        # }
        data
    }))
    
}



## UI
# Load the ggplot2 package which provides
# the 'mpg' dataset.
library(ggplot2)

ui <-
fluidPage(
    titlePanel("Chinese ideophones — marked words (form)"),
    
    # Create a new Row in the UI for selectInputs
    fluidRow(
        column(12,
               selectInput("py",
                           "Hanyu pinyin:",
                           c("All",
                             unique(as.character(ideodata$pinyintone))))
         )
        #,
        # column(4,
        #        selectInput("trans",
        #                    "Transmission:",
        #                    c("All",
        #                      unique(as.character(mpg$trans))))
        # ),
        # column(4,
        #        selectInput("cyl",
        #                    "Cylinders:",
        #                    c("All",
        #                      unique(as.character(mpg$cyl))))
        # )
    ),
    # Create a new row for the table.
    DT::dataTableOutput("table")

)





# Run the application 
shinyApp(ui = ui, server = server)
