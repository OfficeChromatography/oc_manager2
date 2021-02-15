import unittest
import sys
import logging
import OCDriver


def get_Documentation_Driver():
    oc_driver = OCDriver.OCDriver()
    return oc_driver.get_documentation_driver()


def update_pictures(docu_driver):
    pictures_list_to_change = docu_driver.create_picture_list(1)
    pictures_list_to_change[0]['UVC'] = 0
    docu_driver.update_pictures(pictures_list_to_change)


def get_LED_gcode(docu_driver):
    pictures_list = docu_driver.pictures.config
    return pictures_list[0].to_LEDs_gcode()


class TestApplication(unittest.TestCase):
    def test_load_Docu(self):
        get_Documentation_Driver()

    def test_initalize_Docu(self):
        docu_driver = get_Documentation_Driver()
        pictures_list = docu_driver.create_picture_list(1)
        correct_pictures_list = [{
            'blue': 255,
            'label': 'Picture',
            'green': 255,
            'UVA': 255,
            'white': 255,
            'UVC': 255,
            'red': 255
        }]
        self.assertEqual(pictures_list, correct_pictures_list)

    def test_update_pictures_list_Docu(self):
        docu_driver = get_Documentation_Driver()
        update_pictures(docu_driver)
        new_pictures_list = docu_driver.get_picture_list()
        expected_pictures_list = [{
            'blue': 255,
            'label': 'Picture',
            'green': 255,
            'UVA': 255,
            'white': 255,
            'UVC': 0,
            'red': 255
        }]
        self.assertEqual(new_pictures_list, expected_pictures_list)

    def test_gcode_LEDs(self):
        docu_driver = get_Documentation_Driver()
        new_LED_gcode = get_LED_gcode(docu_driver)
        expected_LED_gcode = "M150 W255 R255 U255 B255\nM42 P47 S255\nM42 P45 S255"
        self.assertEqual(new_LED_gcode, expected_LED_gcode)

    def test_update_LEDs(self):
        docu_driver = get_Documentation_Driver()
        update_pictures(docu_driver)
        new_LED_gcode = get_LED_gcode(docu_driver)
        expected_LED_gcode = "M150 W255 R255 U255 B255\nM42 P47 S255\nM42 P45 S0"
        self.assertEqual(new_LED_gcode, expected_LED_gcode)


if __name__ == "__main__":
    unittest.main()
