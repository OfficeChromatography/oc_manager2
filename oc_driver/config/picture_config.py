import drivers.gcodes as GCODES
import numpy as np


class Picture:
    def __init__(self, label, white, red, green,  \
                 blue, UVA, UVC):
        self.label = label
        self.white = white
        self.red = red
        self.green = green
        self.blue = blue
        self.UVA = UVA
        self.UVC = UVC

    def to_dict(self):
        return {'label' : self.label , 'white' : self.white , 'red' : self.red , \
                'green' : self.green , 'blue' : self.blue, 'UVA': self.UVA, 'UVC': self.UVC}

    def to_LEDs_gcode(self):
        return GCODES.LEDs(
            white=self.white,
            red=self.red,
            green=self.green,
            blue=self.blue,
            UVA=self.UVA,
            UVC=self.UVC)


class PictureConfig:
    def __init__(self, PICTURE_CONFIG_DEFAULT, number_of_pictures):
        pictures_list = self.create_conf_to_picture_list(
            PICTURE_CONFIG_DEFAULT, number_of_pictures)
        self.build_pictures_from_picture_list(pictures_list)

    def build_pictures_from_picture_list(self, picture_list):
        "initializes all pictures given by a pictures configuration"
        if len(picture_list) <= 0:
            return
        pictures = []
        for picture_config in picture_list:
            label = picture_config.get('label')
            white = picture_config.get('white')
            red = picture_config.get('red')
            green = picture_config.get('green')
            blue = picture_config.get('blue')
            UVA = picture_config.get('UVA')
            UVC = picture_config.get('UVC')
            # add new picture
            pictures.append(Picture(label, white, red, green,  \
                                    blue, UVA, UVC))
        self.config = pictures

    def create_conf_to_picture_list(self, create_config, number_of_pictures):
        'Transforms the create_config into a pictures list'
        pictures = []
        number_of_pictures = number_of_pictures
        for i in range(number_of_pictures):
            pictures.append({
                'label': create_config['label'],
                'white': create_config['white'],
                'red': create_config['red'],
                'green': create_config['green'],
                'blue': create_config['blue'],
                'UVA': create_config['UVA'],
                'UVC': create_config['UVC']
            })
        return pictures

    def to_list(self):
        picture_list = []
        for picture in self.config:
            picture_list.append(picture.to_dict())
        return picture_list
