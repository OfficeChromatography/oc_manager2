library(stringi)


use_virtualenv(file.path(getwd() ,"oc_driver", "py_virtual_env"), required=T)
ocdriverPackage <- import_from_path("OCDriver", path='oc_driver', convert = TRUE)
ocDriver <- ocdriverPackage$OCDriver() # use default config


toRSettingsTableFormat <- function(pythonDict,pythonKeys, labels, units = NULL, preview = FALSE){
    values = c()
    if (is.null(units) && !preview){
        for (arr in pythonDict){
            value_array = c()
            for (Key  in pythonKeys ){value_array= c(value_array,arr[[Key]])}
            values = rbind(values,value_array)
        }
        f = data.frame(values, stringsAsFactors = FALSE)
        colnames(f) = labels
        return (f)

    }else {
        for (Key  in pythonKeys ){values= c(values,pythonDict[[Key]])}
        f = data.frame(values, units, stringsAsFactors = FALSE)
        rownames(f) = labels
        return (f)
    }
}


settingsTabletoPythonDict  <- function(settingsTable, pythonKeys, labels, preview = FALSE){
    values = c()
    python_dict = c()
    if ("units" %in% colnames(settingsTable) || preview){
        for (label in labels ){values= c(values,settingsTable[label,"values"])}
        python_dict = c(python_dict,(py_to_r(py_dict(pythonKeys, values))))
    }
    else {
        for (i in 1:nrow(settingsTable)){
            arr = settingsTable[i,]
            values = c()
            for (label in labels ){values= c(values,arr[label])}
            python_dict[[i]] = py_to_r(py_dict(pythonKeys, values))
        }
    }
    return (python_dict)
}


bandConfToRSettingsTableFormat  <- function(bandConf){
   return (toRSettingsTableFormat(bandConf,band_pythonKeys, band_labels))
}


bandConfSettingsTableFormatToPython  <- function(settingsFormat){
   return (settingsTabletoPythonDict(settingsFormat, band_pythonKeys, band_labels))
}
4
