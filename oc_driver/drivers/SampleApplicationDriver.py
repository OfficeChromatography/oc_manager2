import drivers.gcodes as GCODES
from drivers.abstract_application_driver.AbstractApplicationDriver import AbstractApplicationDriver


class SampleApplicationDriver(AbstractApplicationDriver):

    PLATE_CONFIG_DEFAULT = {
        'gap': 2,
        'band_length': 6,
        'band_height': 0,
        'relative_band_distance_x': 10,
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
        'kind_of_fire': "volume control",
        'waiting_time': 0,
        'number_of_working_nozzles': 7
    }


    def __init__(self, communication,calibration_x, calibration_y,
                 plate_config=PLATE_CONFIG_DEFAULT, \
                 head_config=HEAD_CONFIG_DEFAULT):
        super(SampleApplicationDriver, self) \
            .__init__(communication, plate_config, head_config, calibration_x, calibration_y)

    def update_settings(self,
                        plate_config=PLATE_CONFIG_DEFAULT,
                        head_config=HEAD_CONFIG_DEFAULT,
                        band_config=None,
                        number_of_bands=1):
        if not band_config:
            band_config = self.create_band_list(number_of_bands)

        self.update_plate_and_head_configs_to_driver(plate_config, head_config)
        new_band_list = self.add_or_remove_Bands(number_of_bands, band_config)
        return self.create_bands_from_config(new_band_list)

    def add_or_remove_Bands(self, number_of_bands, old_band_config):
        difference = int(number_of_bands - len(old_band_config))
        new_band_config = old_band_config
        if difference > 0:
            new_band_config = self.add_Bands(old_band_config, difference)
        elif difference < 0:
            new_band_config = self.remove_Bands(old_band_config,
                                                int(number_of_bands))
        return new_band_config

    def add_Bands(self, old_band_config, number_of_bands_to_add):
        new_bands = self.create_band_list(number_of_bands_to_add)
        new_band_config = old_band_config + new_bands
        return new_band_config

    def remove_Bands(self, old_band_config, number_of_bands):
        new_band_config = old_band_config[0:number_of_bands]
        return new_band_config
