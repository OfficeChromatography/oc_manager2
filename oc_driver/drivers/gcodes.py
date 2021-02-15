def new_lines(arr):
    return "\n".join(arr)


GO = "G1"

GO_X = GO + " X"
GO_X_MINUS = GO_X + "-"

GO_Y = GO + " Y"
GO_Y_MINUS = GO_Y + "-"

SET_REFERENCE = "G91"

SET_ABSOLUTE_POS = "G90"

DISABLE_STEPPER_MOTORS = "M84"

GO_TO_ORIGIN = "G28"

GO_TO_ORIGIN_X = "G28 X0"

GO_TO_ORIGIN_Y = "G28 Y0"

SET_UNITS_IN_MM = "G21"

CURR_MOVEMENT_FIN = "M400"

FIRE = "M700"

GET_POSITION = "M114"

GO_TO_FOTO_POSITION = "G1 Y164"

TURN_HEATING_OFF = "M190 S0"

END = new_lines([GO_TO_ORIGIN_X, GO_TO_ORIGIN_Y, DISABLE_STEPPER_MOTORS, TURN_HEATING_OFF])


def fire(fire_rate, nozzle_address, puls_delay, fire_delay):
    return FIRE + " P0 " + "I" + str(fire_rate) + " L" + str(
        puls_delay) + " D" + str(fire_delay) + " S" + nozzle_address


def wait(waiting_time_in_ms):
    return "G4 " + "P" + waiting_time_in_ms


def goXMinus(steps="5"):
    return GO_X_MINUS + str(steps)


def goXPlus(steps="5"):
    return GO_X + str(steps)


def goYMinus(steps="5"):
    return GO_Y_MINUS + str(steps)


def goYPlus(steps="5"):
    return GO_Y + str(steps)


def go_speed(speed):
    return " F" + str(speed)


def start(speed, distX, temperature=0):
    return new_lines([
        GO_TO_ORIGIN_X, GO_TO_ORIGIN_Y, SET_UNITS_IN_MM, SET_ABSOLUTE_POS,
        goXPlus(distX) + go_speed(speed), DISABLE_STEPPER_MOTORS,
        Heating(temperature)]) 


def set_PIN_with_number_and_value(pin_number, pin_value):
    return "M42" + " P" + str(pin_number) + " S" + str(pin_value)


def LEDs(white, red, green, blue, UVA, UVC):
    gcode_white_LEDs = "M150" + " W" + str(white) + " R" + str(
        red) + " U" + str(green) + " B" + str(blue)
    gcode_UVA = set_PIN_with_number_and_value(44, UVA)
    gcode_UVC = set_PIN_with_number_and_value(64, UVC)
    return [gcode_white_LEDs, gcode_UVA, gcode_UVC]

def Heating(temperature):
    return  "M190 S" + str(temperature);
    return [gcode_white_LEDs, gcode_UVA, gcode_UVC]
