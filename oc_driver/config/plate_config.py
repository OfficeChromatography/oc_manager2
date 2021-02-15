class Plate:
    def __init__(self, plate_config, calibration_x, calibration_y):
        """

        This class represents the configuration of the OC-plate

        plate_config: dict {
        'gap': number,
        'band_length': number,
        'relative_band_distance_y': number,
        'relative_band_distance_x': number,
        """
        ## x direction of the axis = y direction  of the plate
        ## y direction of the axis = x direction  of the plate
        self.calibration_x = calibration_y
        self.calibration_y = calibration_x
        self.gap = float(plate_config.get('gap'))
        self.relative_band_distance_x = float(plate_config.get('relative_band_distance_x'))
        self.relative_band_distance_y = float(plate_config.get('relative_band_distance_y'))
        self.band_length = float(plate_config.get('band_length'))
        self.band_height = float(plate_config.get('band_height'))
        self.print_bothways = int(plate_config.get('print_bothways'))
	self.heating_temperature = plate_config.get('heating_temperature')


    def get_band_offset_x(self):
        'band offset from the plate in x direction'
        return self.calibration_x + \
            self.relative_band_distance_x

    def get_band_offset_y(self):
        'band offset from the plate in y direction'
        return self.calibration_y + \
            self.relative_band_distance_y
    
    def get_heating_temperature(self):
        return self.heating_temperature
