import drivers.gcodes as GCODES
from config.picture_config import PictureConfig
from picamera import PiCamera
from time import sleep
from fractions import Fraction
import csv 

class DocumentationDriver():
    
      
    PICTURE_CONFIG_DEFAULT = {
        "label": "File name",
        "white": 255,
        "red": 0,
        "green": 0,
        "blue": 0,
        "UVA": 0,
        "UVC": 0,
        "number_of_pictures": 1
    }
    PATH = "./www/pictures/"

    def __init__(self, communication):
        self.communication = communication
        number_of_pictures = int(
            self.PICTURE_CONFIG_DEFAULT['number_of_pictures'])
        self.pictures = PictureConfig(self.PICTURE_CONFIG_DEFAULT,
                                      number_of_pictures)
        self.preview = PictureConfig(self.PICTURE_CONFIG_DEFAULT, 1)
    
    def import_from_csv(self):
        try: 
            with open('/home/pi/OC_manager2/plate.csv') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    return {'height':float(row['a']),'width':float(row['b'])} # value read from the csv file
        except IOError:
            return {'height':100,'width':100}

    def take_a_picture(self, Path, pictureType):
        my_file = open(Path, 'w+')
        camera = PiCamera()
        pixel = 2464
        camera.resolution = (pixel, pixel)
        sizes = self.import_from_csv()
        #print(sizes)
        y1 = sizes['width']
        x1 = sizes['height']
        w = int(pixel/(100/x1))
        h = int(pixel/(100/y1))
        c = float(2) # mm cropping
        y = y1-c #cropped width
        x = x1-c #cropped height
                       
        #The illumination type (UVA,UVC) is passed as string.
        #The illumination type is determined in the function "make_pictures_for_documentation"
        #in DocumentationDriver.py.
                
        if pictureType == 'UVA':
           camera.framerate = Fraction(30, 1)
           z = int(1 / camera.framerate * 1000000)
           camera.shutter_speed = z
           #camera.awb_mode = 'fluorescent'  #or 'incandescent' #can improve the contrast
           #Camera warm-up time
           sleep(30)
           
        elif pictureType == 'UVC':
           camera.framerate = Fraction(30, 1)
           z = int(1 / camera.framerate * 1000000)
           camera.shutter_speed = z
           #Camera warm-up time
           sleep(30)
                   
        else: #visible light
           camera.framerate = Fraction(30, 1)
           z = int(1 / camera.framerate * 1000000)
           camera.shutter_speed = z
           #Camera warm-up time
           sleep(10)
        
        
        #Different camera options can be set with the following lines,
        #to be copied into the "if" sections.
           
            ##set brightness between 0 and 100
        #camera.brightness = 0
        #camera.sensor_mode = 0
            ##set sharpness between -100 and 100
        #camera.sharpness = -100
            ##set saturation between -100 and 100
        #camera.saturation = -100
        #camera.awb_mode = 'fluorescent'
        #camera.image_effect = 'denoise' # or 'saturation'
            ##set contrast between -100 and 100
        #camera.contrast = -100
        #camera.iso = 800
           
        camera.exposure_mode='off'
        camera.zoom = (c/100, (100-y)/100, (x-c)/100, (100-2*c)/100)
        #print(camera.zoom)
        camera.capture(my_file, quality = 100, resize = (w, h))
        my_file.close()
        sleep(5)
        camera.close()

    def LEDs_on(self, LED_gcode):
        self.communication.send(LED_gcode)
        sleep(1)

    def go_in_foto_pos(self):
        self.communication.send([
            GCODES.SET_ABSOLUTE_POS, GCODES.GO_TO_FOTO_POSITION,
            GCODES.CURR_MOVEMENT_FIN
        ])

    def LEDs_off(self):
        self.communication.send(GCODES.LEDs(0, 0, 0, 0, 0, 0))

    def get_Preview_Path(self):
        return "./www/Preview.jpg"

    def get_picture_list(self):
        return self.pictures.to_list()

    def get_preview_list(self):
        return self.preview.to_list()

    def create_picture_list(self, number_of_pictures):
        return self.pictures.create_conf_to_picture_list(
            self.PICTURE_CONFIG_DEFAULT, int(number_of_pictures))

    def update_preview(self, preview_config):
        self.preview.build_pictures_from_picture_list([preview_config])

    def update_pictures(self, pictures_config):
        self.pictures.build_pictures_from_picture_list(pictures_config)

    def update_settings(self, pictures_list, number_of_pictures):
        pictures_list = self.add_or_remove_Pictures(number_of_pictures,
                                                    pictures_list)
        self.update_pictures(pictures_list)
        return pictures_list

    def make_preview(self, preview_list):
        self.update_preview(preview_list)
        LED_gcode = self.preview.config[0].to_LEDs_gcode()
        Path = self.get_Preview_Path()
        self.go_in_foto_pos()
        self.LEDs_on(LED_gcode)
        
        self.take_a_picture(Path,'null')
        
        self.LEDs_off()

    def make_pictures_for_documentation(self, pictures_list):
        self.update_pictures(pictures_list)
        self.go_in_foto_pos()
        for picture in self.pictures.config:
            LED_gcode = picture.to_LEDs_gcode()
            label = picture.label
            Path = self.PATH + label + ".jpg"
            self.LEDs_on(LED_gcode)
            
            pictureType='null'
            if picture.UVA != 0:
                pictureType='UVA'
            elif picture.UVC != 0:
                pictureType='UVC'
            self.take_a_picture(Path,pictureType)
            
        self.LEDs_off()
        self.go_home()

    def add_or_remove_Pictures(self, number_of_pictures, old_picture_config):
        difference = int(int(number_of_pictures) - len(old_picture_config))
        new_picture_config = old_picture_config
        if difference > 0:
            new_picture_config = self.add_Pictures(old_picture_config,
                                                   difference)
        elif difference < 0:
            new_picture_config = self.remove_Pictures(old_picture_config,
                                                      int(number_of_pictures))
        return new_picture_config

    def add_Pictures(self, old_picture_config, number_of_pictures_to_add):
        new_pictures = self.create_picture_list(number_of_pictures_to_add)
        new_picture_config = old_picture_config + new_pictures
        return new_picture_config

    def remove_Pictures(self, old_picture_config, number_of_pictures):
        new_picture_config = old_picture_config[0:number_of_pictures]
        return new_picture_config

    def go_home(self):
        self.communication.send([GCODES.GO_TO_ORIGIN_Y])
