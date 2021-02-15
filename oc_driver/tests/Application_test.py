import unittest
import sys
import logging
import OCDriver

PLATE_CONFIG_CHANGE = {
    'gap': 2,
    'band_length': 10,
    'band_height': 1,
    'relative_band_distance_x': 10,
    'relative_band_distance_y': 10
}

HEAD_CONFIG_CHANGE = {
    'speed': 3000,
    'number_of_fire': 10,
    'pulse_delay': 5,
    'fire_delay': 800,
    'printer_head_resolution': 0.265,
    'step_range': 0.265,
    'kind_of_fire': "volumne control",
    'waiting_time': 0
}


def get_Sample_Application_driver():
    oc_driver = OCDriver.OCDriver()
    return oc_driver.get_sample_application_driver()


def load_test_gcode():
    gcode_file = open("./tests/right_gcode.gcode", 'r')
    return gcode_file.read().replace('\r', '')


def write_gcode_file(fN, code):
    f = open("./tests/" + fN, "w")
    f.write(code)


class TestApplication(unittest.TestCase):
    def test_load_SA(self):
        get_Sample_Application_driver()

    def test_band_config_init_works(self):
        app_driver = get_Sample_Application_driver()
        band_list = app_driver.band_config.to_band_list()
        self.assertEquals(len(band_list), 1)
        expected_band_list = [{
            'drop_volume': 0.15,
            'end': 25.915,
            'volume_set': 0.034,
            'label': 'Band',
            'start': 19.915,
            'volume_real': 0.034,
            'nozzle_id': '1'
        }]
        self.assertEqual(band_list, expected_band_list)

    def test_band_config_update_works(self):
        app_driver = get_Sample_Application_driver()
        band_list_to_change = app_driver.band_config.to_band_list()
        band_list_to_change[0]['nozzle_id'] = '5'
        new_band_list = app_driver.create_bands_from_config(
            band_list_to_change)
        expected_band_list = [{
            'drop_volume': 0.15,
            'end': 24.855,
            'volume_set': 0.034,
            'label': 'Band',
            'start': 18.855,
            'volume_real': 0.034,
            'nozzle_id': '5'
        }]
        self.assertEqual(new_band_list, expected_band_list)

    def test_update_configs(self):
        app_driver = get_Sample_Application_driver()
        new_band_list = app_driver.update_settings(PLATE_CONFIG_CHANGE,
                                                   HEAD_CONFIG_CHANGE)
        expected_band_list = [{
            'drop_volume': 0.15,
            'end': 29.915,
            'volume_set': 0.034,
            'label': 'Band',
            'start': 19.915,
            'volume_real': 0.057,
            'nozzle_id': '1'
        }]
        self.assertEqual(new_band_list, expected_band_list)

    def test_finecontrol_load(self):
        driver = OCDriver.OCDriver()
        return driver.get_fine_control_driver()

    def test_development_load(self):
        driver = OCDriver.OCDriver()
        return driver.get_development_driver()

    def test_get_estimate_time(self):
        app_driver = get_Sample_Application_driver()
        logging.info(app_driver.get_print_time)

    def test_calcualated_number_of_rept(self):
        app_driver = get_Sample_Application_driver()
        new_band_list = app_driver.update_settings(PLATE_CONFIG_CHANGE,
                                                   HEAD_CONFIG_CHANGE)
        step_range_change = HEAD_CONFIG_CHANGE.get('step_range')
        band_height_change = PLATE_CONFIG_CHANGE.get('band_height')
        number_of_rep_for_array = band_height_change // step_range_change + 1
        BandConf = app_driver.band_config
        volume_set = 0.1
        # Update Volume set
        band_list_to_change = BandConf.to_band_list()
        band_list_to_change[0]['volume_set'] = str(volume_set)
        new_band_list = app_driver.create_bands_from_config(
            band_list_to_change)

        volume_per_band = BandConf.volume_per_band(
            new_band_list[0]['drop_volume'])

        number_of_reptition = new_band_list[0]['volume_real'] / volume_per_band

        logging.info(new_band_list)
        logging.info([
            "number_of_repition", number_of_reptition,
            "number_of_rep_for_array", number_of_rep_for_array
        ])
        self.assertEqual(number_of_reptition % number_of_rep_for_array, 0)

    def test_gcode_for_array(self):
        app_driver = get_Sample_Application_driver()
        new_band_list = app_driver.update_settings(PLATE_CONFIG_CHANGE,
                                                   HEAD_CONFIG_CHANGE)
        BandConf = app_driver.band_config
        # Update Volume set
        volume_set = 0.1
        band_list_to_change = BandConf.to_band_list()
        band_list_to_change[0]['volume_set'] = str(volume_set)
        new_band_list = app_driver.create_bands_from_config(
            band_list_to_change)
        gcode_for_bands = BandConf.to_gcode()
        gcode_for_bands_right = load_test_gcode()

        self.assertEqual(gcode_for_bands, gcode_for_bands_right)


if __name__ == "__main__":
    unittest.main()
