import drivers.gcodes as GCODES
from drivers.abstract_application_driver.AbstractApplicationDriver import AbstractApplicationDriver


class DevelopmentDriver(AbstractApplicationDriver):

    PLATE_CONFIG_DEFAULT = {
        'gap': 0,
        'band_length': 100,
        'band_height': 0,
        'relative_band_distance_x': 0,
        'relative_band_distance_y': 10,
        'plate_x': 100,
        'plate_y': 100,
        'print_bothways': 0,
	'heating_temperature': 0
    }

    HEAD_CONFIG_DEFAULT = {
        'speed': 3000,
        'number_of_fire': 10,
        'pulse_delay': 5,
        'fire_delay': 800,
        'printer_head_resolution': 0.265,
        'step_range': 0.265,
        'kind_of_fire': "spraying",
        'waiting_time': 0,
        'number_of_working_nozzles': 7
    }


    def __init__(self, communication, calibration_x, calibration_y,
                 plate_config=PLATE_CONFIG_DEFAULT, \
                 head_config=HEAD_CONFIG_DEFAULT):
        super(DevelopmentDriver, self) \
            .__init__(communication, plate_config, head_config, calibration_x, calibration_y)
        self.update_plate_and_head_configs_to_driver(plate_config, head_config)
        self.plate_length = 100

    def calculate_band_length(self):
        #self.plate.band_length = self.plate_length - 2 * self.plate.relative_band_distance_x
        return self.plate.band_length

    def get_band_length(self):
        return self.plate.band_length

    def update_settings(self,
                        plate_config=PLATE_CONFIG_DEFAULT,
                        head_config=HEAD_CONFIG_DEFAULT,
                        band_config=None):
        if not band_config:
            band_config = self.create_band_list(1)
        self.update_plate_and_head_configs_to_driver(plate_config, head_config)
        self.calculate_band_length()
        return self.create_bands_from_config(band_config)
