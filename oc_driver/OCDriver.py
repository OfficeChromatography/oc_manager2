from drivers.FineControlDriver import FineControlDriver
from drivers.SampleApplicationDriver import SampleApplicationDriver
from drivers.DevelopmentDriver import DevelopmentDriver
from drivers.DocumentationDriver import DocumentationDriver

from communication import Communication

# TODO default values!

DEFAULT_CONFIG = {
    'connection_string': "/dev/ttyACM0",
    'baud_rate': 115200,
    'calibration_x': 1,
    'calibration_y': 3,
    'dpi': 96,
    'log_file_path': "./"
}


class OCDriver:
    INCHE = 25.4

    def __init__(self, oc_driver_config=DEFAULT_CONFIG):
        """
        CONNECTION_STRING
        baud_rat
        Drop_vol # in nL, use to calculate volume in Methods
        xlevel
        ylevel
        inche # mm/inche
        dpi # resolution of the Hp cartdrige (datasheet), dpi=number/inch
        # distance of one nozzle to the next one  round(inche/dpi,3)
        visu_roi
        """
        self.communication = Communication(
            oc_driver_config['connection_string'],
            oc_driver_config['baud_rate'])
        self.communication.setup_log_file(oc_driver_config['log_file_path'])
        self.config = oc_driver_config
        self.config['reso'] = round(self.INCHE / self.config['dpi'], 3)

    def get_sample_application_driver(self):
        return SampleApplicationDriver(communication=self.communication, \
                 calibration_x=self.config.get('calibration_x'), \
                 calibration_y=self.config.get('calibration_y'))

    def get_development_driver(self):
        return DevelopmentDriver(communication=self.communication, \
                 calibration_x=self.config.get('calibration_x'), \
                 calibration_y=self.config.get('calibration_y'))

    def get_fine_control_driver(self):
        return FineControlDriver(communication=self.communication, \
                 calibration_x=self.config.get('calibration_x'), \
                 calibration_y=self.config.get('calibration_y'))

    def get_documentation_driver(self):
        return DocumentationDriver(self.communication)

    def connect(self, connection_string=None):
        if isinstance(connection_string, basestring):
            self.communication.connection_string = connection_string
            print(connection_string)
        self.communication.connect()

    def is_connected(self):
        return self.communication.printcore.online

    def disconnect(self):
        self.communication.disconnect()

    def pause(self):
        self.communication.pause()

    def stop(self):
        self.communication.stop()

    def resume(self):
        self.communication.resume()

    def send_from_file(self, file_path):
        self.communication.send_from_file(path=file_path)
