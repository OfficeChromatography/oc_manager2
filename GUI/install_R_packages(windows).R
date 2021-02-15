## install R : https://cran.r-project.org/bin/windows/base/
## install Rtools : https://cran.r-project.org/bin/windows/Rtools/
## run File with: "Rscript install_R-packages(windows).R"  in cmd window as admin
install.packages(c(
    'devtools', 
    'httpuv',
    'shiny',
    'serial', 
    'reticulate', 
    'DT',
    'shinyBS',
    'shinyalert',
    'shinydashboard',
    'rhandsontable'),
 repos='http://cran.rstudio.com/')
