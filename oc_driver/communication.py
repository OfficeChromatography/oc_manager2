from vendor.printrun import printcore, gcoder, utils
from vendor.printrun.eventhandler import PrinterEventHandler
from time import sleep
from datetime import datetime

import sys


class Communication:
    def __init__(self, connection_string, baud_rate):
        self.connection_string = connection_string
        self.baud_rate = baud_rate
        self.printcore = printcore.printcore()
        self.printcore.loud = True

    def pause(self):
        self.printcore.pause()

    def stop(self):
        self.printcore.stop()

    def resume(self):
        self.printcore.resume()

    def connect(self):
        self.printcore.connect(self.connection_string, self.baud_rate)
        self.printcore.listen_until_online()

    def is_connected(self):
        return self.printcore.online

    def disconnect(self):
        self.printcore.disconnect()

    def get_gcode_from_file(self, path):
        gcode = [code_line.strip() for code_line in open(path)]
        return gcode

    def send(self, gcode):
        light_gcode = gcoder.LightGCode(gcode)
        self.printcore.startprint(light_gcode)
        while self.printcore.printing:
            sleep(1)

    def setup_log_file(self, file_path):
        utils.setup_logging(None, filepath=file_path)

    def write_gcode_file(self, gcode_list):
        with open("./gcode_file.gcode", 'w') as file:
            for line in gcode_list:
                file.write("%s\n" % line)

    def send_from_file(self,
                       path="./gcode_file.gcode",
                       generated_gcode=["", ""]):
        if path == "./gcode_file.gcode":
            self.write_gcode_file(generated_gcode)
        gcode = self.get_gcode_from_file(path)
        self.send(gcode)
