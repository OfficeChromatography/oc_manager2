import unittest
import sys
import logging
from config.print_head_config import PrinterHead
import OCDriver

logger = logging.getLogger()
logger.level = logging.DEBUG


def log(message):
    stream_handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(stream_handler)
    try:
        logging.getLogger().info(message)
    finally:
        logger.removeHandler(stream_handler)


CREATE_BAND_CONFIG = {
    "default_nozzle_id": "1",
    'default_label': "Band",
    "number_of_bands": 3
}

HEAD_CONFIG_DEFAULT = {
    'speed': 3000,
    'number_of_fire': 10,
    'pulse_delay': 5,
    'fire_delay': 800,
    'printer_head_resolution': 0.265,
    'step_range': 0.265,
    'kind_of_fire': "spraying"
}


class TestNozzleId(unittest.TestCase):
    def test_finecontrol_load(self):
        driver = OCDriver.OCDriver()
        return driver.get_fine_control_driver()

    def test_development_load(self):
        driver = OCDriver.OCDriver()
        return driver.get_development_driver()

    def test_calculate_nozzle_address(self):
        driver = self.test_finecontrol_load()
        result = driver.calculate_nozzle_address_for_gcode(['all'])
        exspected = "3087"
        self.assertEquals(result, exspected)

    def test_kind_of_fire_in_printer_head(self):
        driver = self.test_development_load()
        address = "1"
        gcode = driver.printer_head.fire_nozzle(address)
        log(gcode)

    def test_kind_of_fire_in_band_config(self):
        driver = self.test_development_load()
        gcode = driver.band_config.to_gcode()
        log(gcode)


if __name__ == "__main__":
    unittest.main()
