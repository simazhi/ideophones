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
library(DT)
library(shinythemes)

# Here is the data and stuff

ideodata <- read_xlsx("www/data.xlsx") %>%
    filter(morph != "NOTIDEOPHONE") %>%
    select(pinyinnone,
           traditional,
           simplified,
           pinyintone,
           MC,
           OC,
           zdic,
           Kroll,
           morph,
           radsup,
           variant)



## SERVER
# Load the ggplot2 package which provides
# the 'mpg' dataset.

server <- 
function(input, output) {
    checkGroup <- reactive(c(input$checkGroupForm,
                             input$checkGroupMeaning,
                             input$checkGroupFormation))
    #input$checkGroup <- c(input$checkGroupForm,input$checkGroupMeaning)
    # Filter data based on selections
    output$table <- DT::renderDataTable(DT::datatable({
        data <- ideodata
        # if (input$py != "All") {
        #     data <- data[data$pinyintone == input$py,]
        # }
        data[, checkGroup(), drop = FALSE]
        #data[, which(input$checkGroup | input$checkGroup2), drop = FALSE]
        #data %>% select(input$checkGroup)
        #data %>% filter(input$checkGroupMeaning)
    }))
    
}



## UI

ui <-
fluidPage(theme = shinytheme("flatly"),
    titlePanel("Chinese ideophones — a database"),
    
    sidebarLayout(position = "left",
                  fluid = TRUE,
                  sidebarPanel(
                       # h4("test"),
                       # br(),
                       #checkboxes
                       checkboxGroupInput("checkGroupForm", 
                                          label = h3("Phonology"), 
                                          choices = c("Pinyin without tones" = "pinyinnone", 
                                                      "Pinyin with tones" = "pinyintone",
                                                      "Traditional Chinese" = "traditional",
                                                      "Simplified Chinese" = "simplified",
                                                      "Middle Chinese" = "MC", 
                                                      "Old Chinese" = "OC"),
                                          selected = c("traditional", "pinyinnone")
                                          ),
                       #end of checkboxes
                       br(),
                       # checkboxes two
                       checkboxGroupInput("checkGroupMeaning", 
                                          label = h3("Meaning"), 
                                          choices = c("Handian 漢典 (zdic)" = "zdic",
                                                      "Kroll (2015)" = "Kroll"),
                                          selected = "Kroll"
                                          ),
                       #end of checkboxes
                       br(),
                       # checkboxes three
                       checkboxGroupInput("checkGroupFormation", 
                                          label = h3("Formation"), 
                                          choices = c("Base and Reduplicant" = "morph",
                                                      "Radical support" = "radsup",
                                                      "variants" = "variant")
                                          )
                       #end of checkboxes
                ) # end of sidepanel
    ,
    mainPanel(
    # # Create a new Row in the UI for selectInputs
    # fluidRow(
    #     column(12,
    #            selectInput("py",
    #                        "Hanyu pinyin:",
    #                        c("All",
    #                          unique(as.character(ideodata$pinyintone)
    #                                 )
    #                          )
    #                        )
    #      )
    #  ),
    # h2("test"),
    # Create a new row for the table.
    DT::dataTableOutput("table")
) #main panel
    ) #sidebar layout
) #fluidpage





# Run the application 
shinyApp(ui = ui, server = server)
