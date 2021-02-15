from abc import ABCMeta, abstractmethod
import drivers.gcodes as GCODES
from config.band_config import BandConfig
from config.plate_config import Plate
from config.print_head_config import PrinterHead


class AbstractApplicationDriver:
    __metaclass__ = ABCMeta

    CREATE_BAND_CONFIG = {
        "default_nozzle_id": "1",
        'default_label': "Band",
        "number_of_bands": 1,
        "drop_volume": 0.15
    }

    def __init__(self, communication, plate_config, head_config, calibration_x,
                 calibration_y):
        self.calibration_x = calibration_x
        self.calibration_y = calibration_y
        self.update_plate_and_head_configs_to_driver(plate_config, head_config)
        self.communication = communication
        self.band_config = BandConfig(self.CREATE_BAND_CONFIG,
                                      self.printer_head, self.plate)

    def update_plate_and_head_configs_to_driver(self,
                                                plate_config=None,
                                                head_config=None):
        if plate_config:
            self.plate = Plate(plate_config, self.calibration_x,
                               self.calibration_y)
        if head_config:
            self.printer_head = PrinterHead(head_config)

    def create_band_list(
            self, number_of_bands=CREATE_BAND_CONFIG['number_of_bands']):
        create_conf = self.CREATE_BAND_CONFIG
        create_conf['number_of_bands'] = int(number_of_bands)
        return self.band_config.create_conf_to_band_list(create_conf)

    def create_bands_from_config(self, band_config):
        self.band_config.update_plate_and_head_configs_to_bands(
            self.plate, self.printer_head)
        self.band_config.build_bands_from_band_list(band_config)
        return (self.band_config.to_band_list())

    def generate_gcode_and_send(self):
        gcode_list = self.generate_gcode()
        self.communication.send_from_file(generated_gcode=gcode_list)

    def get_print_time(self):
        return self.band_config.get_print_time()

    def set_band_config(self, band_list):
        self.band_config.build_bands_from_band_list(band_list)

    def start_application(self):
        self.generate_gcode_and_send()

    def generate_gcode(self):
        gcode_start = GCODES.start(self.printer_head.speed,
                                   self.plate.get_band_offset_y(),
				   self.plate.get_heating_temperature())
        gcode_for_bands = self.band_config.to_gcode()
        gcode_end = GCODES.END
        return [gcode_start, gcode_for_bands, gcode_end]

    def get_Nozzles_Ids(self):
        "which nozzles are used from the printer head"
        keys = sorted(list(self.printer_head.NOZZLE_CHANNEL.keys()))
        #array_sort_direction = [0, 4, 5, 6, 7, 8, 9, 10, 11, 1, 2, 3, 12] #12 nozzles HP cartridge
        array_sort_direction = [0, 3, 4, 5, 6, 1, 2, 7] #7 nozzles spring contacts
        sorted_keys = sort_algorithmn(keys, array_sort_direction)
        return sorted_keys

    def get_default_printer_head_config(self):
        return self.HEAD_CONFIG_DEFAULT

    def get_default_plate_config(self):
        return self.PLATE_CONFIG_DEFAULT

    def get_options_of_kind_of_fire(self):
        return self.printer_head.get_options_of_kind_of_fire()


def sort_algorithmn(array_to_sort, array_sort_direction):
    sorted_array = []
    for idx, pos in enumerate(array_sort_direction):
        sorted_array.append(array_to_sort[pos])
    return sorted_array
