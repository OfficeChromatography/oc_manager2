# coding=utf-8
from picamera import PiCamera
import time
from fractions import Fraction

pixel = 2464

path = "/home/pi/Test/"
my_image = 'preview_'
my_image = path + my_image

camera = PiCamera()
camera.resolution = (pixel, pixel)
camera.framerate = Fraction(10, 1)
z = int(1 / camera.framerate * 1000000)
camera.shutter_speed = z
f = float(camera.framerate)
fr = round(f, 2)
dg = float(camera.digital_gain)
dgr = round(dg, 2)
ag = float(camera.analog_gain)
agr = round(ag, 2)

#camera.awb_mode = 'incandescent'
    ##set brightness between 0 and 100
#camera.brightness = 0
#camera.sensor_mode = 0
    ##set sharpness between -100 and 100
#camera.sharpness = -100
    ##set saturation between -100 and 100
#camera.saturation = -100
#camera.awb_mode = 'fluorescent'
#camera.image_effect = 'denoise' # or 'saturation'
    ##set contrast between -100 and 100
#camera.contrast = -100
#camera.iso = 800

y1 = 100 #plate height
x1 = 100 #plate width
c = 0 # mm cropping
y = y1-c
x = x1-c
w = int(pixel/(100/x))
h = int(pixel/(100/y))
camera.zoom = (c/100, (100-y)/100, (x-c)/100, (100-2*c)/100)
print('Please wait for 30 s.')
time.sleep(30)
camera.exposure_mode='off'
camera.start_preview(alpha=200)
time.sleep(5)
t0 = time.time()
camera.capture(my_image + str(fr) + '.jpg', quality=100, resize = (w, h))
t1 = time.time()
t = t1 - t0
camera.stop_preview()

print('framerate=', camera.framerate)
print('shutter-speed=', camera.shutter_speed)
print('anal-gain=', camera.analog_gain)
print('digi-gain=', camera.digital_gain)
print('exposure time=', round(t, 2), 's')

time.sleep(5)
camera.close()

