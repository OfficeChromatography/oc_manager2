import drivers.gcodes as GCODES
import numpy as np
import datetime
import logging


class Band:
    def __init__(self, start, end, number_of_repetition, drop_volume, \
                 label, volume_set, nozzle_id, volume_real):
        self.volume_real = volume_real
        self.nozzle_id = nozzle_id
        self.volume_set = volume_set
        self.start = start
        self.end = end
        self.number_of_repetition = number_of_repetition
        self.label = label
        self.drop_volume = drop_volume

    def to_dict(self):
        return {'start': self.start, 'end': self.end, 'drop_volume': self.drop_volume,                         'label' : self.label, 'nozzle_id': self.nozzle_id, \
                'volume_set': self.volume_set, 'volume_real': self.volume_real}


class BandConfig:
    def __init__(self, create_config, printer_head, plate):
        """

        represents which band should use which nozzle in order to apply a given ammount
        of a discrete liquid

        band_config_dict :  [{
          nozzle_id: integer,
          label: str,
          volume_set: float
        }, ....]
        """
        self.printer_head = printer_head
        self.plate = plate
        band_list = self.create_conf_to_band_list(create_config)
        self.build_bands_from_band_list(band_list)
        self.estimate_time = 0

    def calculate_array_repetition(self):
        if self.plate.print_bothways == 1:
            return self.plate.band_height / self.printer_head.step_range // 2 + 1
        else:
            return self.plate.band_height // self.printer_head.step_range + 1

    def update_plate_and_head_configs_to_bands(self, plate, printer_head):
        self.plate = plate
        self.printer_head = printer_head

    def create_conf_to_band_list(self, create_config):
        "Transforms the create_config into a list list"
        bands = []
        number_of_bands = int(create_config['number_of_bands'])
        drop_volume = float(create_config['drop_volume'])
        for i in range(number_of_bands):
            bands.append({
                'nozzle_id':
                create_config['default_nozzle_id'],
                'label':
                create_config['default_label'],
                'drop_volume':
                drop_volume,
                'volume_set':
                round(self.volume_per_band(drop_volume), 3)
            })
        return bands

    def volume_per_band(self, drop_volume):
        "how much volume should be applied on a single band"
        return self.plate.band_length / \
                  self.printer_head.step_range  * \
                  self.printer_head.number_of_fire * \
                  drop_volume  / 1000

    def calculate_band_end_from_start(self, start):
        "aux function to calculate the next 3d printer end pos"
        return start + self.plate.band_length

    def calculate_number_of_reps(self, volume_set, volume_per_band):
        "Calculates the number of application per band by a given volume"
        if self.plate.print_bothways == 1:
            return round(float(volume_set) / volume_per_band /2.)
        else:
            return round(float(volume_set) / volume_per_band)

    def calculate_volume_real(self, number_of_repetitions, volume_per_band):
        "Calculates the applied volume depending on volume_per_band"
        if self.plate.print_bothways == 1:
            return round(number_of_repetitions * volume_per_band * 2., 3)
        else:
            return round(number_of_repetitions * volume_per_band, 3)

    def calculate_start_positions(self, number_of_bands):
        start = self.plate.get_band_offset_x()
        plate = self.plate
        start_pos_list = [start]
        for i in range(number_of_bands):
            start += plate.band_length + plate.gap
            start_pos_list.append(start)
        return start_pos_list

    def build_bands_from_band_list(self, band_list):
        "initializes all bands given by a band configuration"
        if len(band_list) <= 0:
            return
        bands = []
        band_start_list = self.calculate_start_positions(len(band_list))
        fire_rate = self.printer_head.number_of_fire
        estimate_time = 0
        number_of_repetition_for_array = self.calculate_array_repetition()
        for idx, band_config in enumerate(band_list):
            # get values
            nozzle_id = band_config.get('nozzle_id')
            shift = self.printer_head.get_shift_for_nozzle(nozzle_id)
            band_start = band_start_list[idx] - shift
            band_end = self.calculate_band_end_from_start(band_start)
            volume_set = float(band_config.get('volume_set'))
            drop_volume = float(band_config.get('drop_volume'))
            volume_per_band_for_one_nozzle = self.volume_per_band(drop_volume)
            volume_per_band =  volume_per_band_for_one_nozzle * \
                               self.printer_head.get_number_of_working_nozzles(nozzle_id)
            number_of_repetition = self.calculate_number_of_reps(
                volume_set, volume_per_band)
            if number_of_repetition_for_array > 0:
                factor_repetition = number_of_repetition // number_of_repetition_for_array + 1
                number_of_repetition = factor_repetition * number_of_repetition_for_array

            volume_real = self.calculate_volume_real(number_of_repetition,
                                                     volume_per_band)
            label = str(band_config.get('label'))

            # estimate time
            estimate_time += self.printer_head.calculate_time_per_band(
                self.plate.band_length, number_of_repetition)

            # add new band
            bands.append(Band(band_start, band_end, number_of_repetition, drop_volume, \
                              label, volume_set, nozzle_id, volume_real))
        self.bands = bands
        self.estimate_time = int(estimate_time)

    def to_band_list(self):
        band_list = []
        for band in self.bands:
            band_list.append(band.to_dict())
        return band_list

    def get_print_time(self):
        time_str = str(datetime.timedelta(seconds=self.estimate_time))
        return time_str

    def to_gcode(self):
        "generates the gcode containing commands for applying bands of liquid on a plate"
        step_range = self.printer_head.step_range
        speed_in_RPM = self.printer_head.speed
        waiting_time = self.printer_head.waiting_time
        gcode_all_bands = []
        for idx, band in enumerate(self.bands):
            gcode_one_way_band = []
            drops = np.arange(band.start, band.end + step_range, step_range)

            if self.plate.print_bothways == 1:
                drops = np.append(drops,drops[::-1])

            address = self.printer_head.get_address_for_nozzle(band.nozzle_id)
            for drop_position in drops:
                drop_position_round = round(drop_position, 3)
                gcode_one_way_band.append(
                    GCODES.goYPlus(drop_position_round) +
                    GCODES.go_speed(speed_in_RPM))
                gcode_one_way_band.append(
                    self.printer_head.fire_nozzle(address))

            if float(waiting_time) > 0:
                gcode_one_way_band.append(GCODES.DISABLE_STEPPER_MOTORS)
                gcode_one_way_band.append(GCODES.wait(waiting_time))

            if self.plate.band_height > 0:
                gcode_all_bands = self.gcode_for_array_application(
                    band, gcode_all_bands, gcode_one_way_band)
            else:
                for rep in range(1, int(band.number_of_repetition) + 1):
                    gcode_all_bands.append(
                        GCODES.new_lines(gcode_one_way_band))

        return GCODES.new_lines(gcode_all_bands)

    def gcode_for_array_application(self, band, gcode_all_bands,
                                    gcode_one_way_band):
        x_position = self.plate.get_band_offset_y()
        band_array_rep = self.calculate_array_repetition()
        logger_array = []
        for rep in range(1, int(band.number_of_repetition) + 1):
            if rep % band_array_rep != 0:
                x_position += self.printer_head.step_range
            else:
                x_position = self.plate.get_band_offset_y()

            gcode_all_bands.append(GCODES.new_lines(gcode_one_way_band))
            gcode_all_bands.append(GCODES.goXPlus(x_position))
            gcode_all_bands.append(GCODES.DISABLE_STEPPER_MOTORS)

        del gcode_all_bands[-1]
        return gcode_all_bands
