#install script for OC_manager2
#!/bin/bash
echo ""
echo "***********************************************************"
echo ""
echo "You are going to install OC_manager2 on your Raspberry Pi."
echo ""
echo "Don't worry, this will take some time!"
echo ""
echo "Are you ready to start? (y/n)"
read userinput
if [ "$userinput" == "y" ]
then
  echo "Installing r-base"
  yes | sudo apt-get install r-base
  echo ""
  echo "Installing libraries"
  yes | sudo apt-get install libssl-dev libcurl4-openssl-dev r-cran-rgl libtiff5-dev
  echo ""
  echo "Installing more libraries"
  echo ""
  yes | sudo apt-get install libssh2-1-dev libboost-atomic-dev libxml2-dev libgit2-dev
  echo ""
  echo "Removing packages not used anymore"
  yes | sudo apt autoremove
  echo ""
  echo "Installing virtualenv"
  echo ""
  yes | sudo apt-get install python-virtualenv
  echo ""
  yes | virtualenv --python=python2.7 --system-site-packages ./OC_manager2/oc_driver/py_virtual_env
  echo ""
  echo "... Done!"
  echo ""
  echo "Installing R packages"
  echo ""
  yes | sudo su - -c "R -e \"install.packages('devtools', repos='http://cran.rstudio.com/')\""
  yes | sudo su - -c "R -e \"devtools::install_github('rstudio/shiny')\""
  yes | sudo su - -c "R -e \"devtools::install_github('rstudio/shinydashboard')\""
  yes | sudo su - -c "R -e \"devtools::install_version('serial', version = '3.0', repos='http://cran.rstudio.com/')\""
  yes | sudo su - -c "R -e \"devtools::install_version('reticulate', version = '1.16', repos = 'http://cran.rstudio.com')\""
  yes | sudo su - -c "R -e \"install.packages('shinyBS', repos='http://cran.rstudio.com/')\""
  yes | sudo su - -c "R -e \"install.packages('shinyalert', repos='http://cran.rstudio.com/')\""
  yes | sudo su - -c "R -e \"devtools::install_github('jrowen/rhandsontable')\""
  echo ""
  echo "Installing Neopixel libraries"
  echo ""
  sudo apt-get update
  yes | sudo apt-get install scons swig
  git clone https://github.com/jgarff/rpi_ws281x.git
  cd rpi_ws281x
  scons
  cd python
  yes | sudo python setup.py install
  echo ""
  echo "Performing reboot"
  sudo reboot
else
  echo "The installation was skipped"
fi
