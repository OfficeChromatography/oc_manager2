from math import pi as pi
import drivers.gcodes as GCODES


class Nozzle:
    " represents a printer head's nozzle "

    def __init__(self, nozzle_id, address):
        self.nozzle_id = nozzle_id
        self.address = address

    def get_shift(self, printer_head_resolution):
        "calculates the nozzle's shift (relative offset to next nozzle), returns float"
        if self.check_if_only_one_nozzles_selected():
		return float(
                round((int(self.nozzle_id)- 1) * printer_head_resolution,
                      3))
        else:
            return 0

    def check_if_only_one_nozzles_selected(self):
        return unicode(self.nozzle_id, 'utf-8').isnumeric()


class PrinterHead:

    "represents a configuration for a oc - printer head, contains its nozzle configuration"

    # setup the nozzle channels as wanted. Checkout the binary signal documentation for your print head
    NOZZLE_CHANNEL = {
        "1": "4",  # channel :3
        "3": "8",  # channel: 4
        "5": "16",  # channel: 5
        "6": "2",  # channel: 2
        "8": "1",  # channel: 1
        "10": "2048",  # channel: 12
        "12": "1024",  # channel: 11
        "all": "3103"  # all channels
        
        #12 nozzles with HP cartridge
        #"1": "1",
        #"2": "2",
        #"3": "4",
        #"4": "8",
        #"5": "16",
        #"6": "32",
        #"7": "64",
        #"8": "128",
        #"9": "256",
        #"10": "512",
        #"11": "1024",
        #"12": "2048",
        #"all": "4095"

    }

    def __init__(self, head_config):
        """ head_config: dict {
        'speed': number,
        'number_of_fire': number,
        'pulse_delay': number,
        'printer_head_resolution: float '
        'step_range'
        } """
        self.speed = int(head_config.get('speed'))
        self.number_of_fire = int(head_config.get('number_of_fire'))
        self.pulse_delay = int(head_config.get('pulse_delay'))
        self.step_range = float(head_config.get('step_range'))
        self.printer_head_resolution = float(
            head_config.get('printer_head_resolution'))
        self.init_with_default_settings()
        self.kind_of_fire = head_config.get('kind_of_fire')
        self.waiting_time = head_config.get('waiting_time')
        self.number_of_working_nozzles = int(
            head_config.get('number_of_working_nozzles'))
        self.fire_delay = int(head_config.get('fire_delay'))

    def init_with_default_settings(self):
        "sets nozzles internally using the NOZZLE_CHANNEL config (see above)"
        nozzles = {}
        for nozzle_id, address in self.NOZZLE_CHANNEL.items():
            nozzles[nozzle_id] = Nozzle(nozzle_id, address)
        self.nozzles = nozzles

    def get_number_of_working_nozzles(self, nozzle_id):
        "defines how many nozzle are considered for volume calculation"
        return 1 if self.nozzles.get(nozzle_id) \
                           .check_if_only_one_nozzles_selected() \
                           else self.number_of_working_nozzles

    def get_shift_for_nozzle(self, nozzle_id):
        "defines a relative offset for each nozzle specified by the printer head geometry"
        return self.nozzles.get(nozzle_id) \
                           .get_shift(self.printer_head_resolution)

    def get_address_for_nozzle(self, nozzle_id):
        "calculate nozzle address and returns a string"
        address = self.nozzles.get(nozzle_id).address
        return address

    def calculate_speed_in_mms(self, speed_in_RPM):
        "calcualtes the speed in mm/s"
        speed_in_mms = round(speed_in_RPM / 60, 3)
        return speed_in_mms

    def calculate_nozzle_fire_time(self):
        max_delay = 800
        return (self.pulse_delay + max_delay) * 10**(-6) * self.number_of_fire

    def calculate_time_per_band(self, band_length, number_of_repetition):
        fire_rate_per_band = band_length / self.step_range
        time_for_fire = fire_rate_per_band * self.calculate_nozzle_fire_time()
        speed_for_accerlerated_moves = self.calculate_speed_in_mms(400)
        moving_time = 2 * band_length / speed_for_accerlerated_moves
        return (time_for_fire + moving_time) * number_of_repetition

    def fire_nozzle(self, address):
        if self.kind_of_fire == "spraying":
            return GCODES.fire(self.number_of_fire, address, self.pulse_delay,
                               self.fire_delay)
        elif self.kind_of_fire == "volume control":
            return GCODES.new_lines([
                GCODES.CURR_MOVEMENT_FIN,
                GCODES.fire(self.number_of_fire, address, self.pulse_delay,
                            self.fire_delay), GCODES.CURR_MOVEMENT_FIN
            ])

    def get_options_of_kind_of_fire(self):
        return list(["spraying", "volume control"])
