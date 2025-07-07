import umath
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.pupdevices import Motor
from pybricks.pupdevices import ColorSensor
from pybricks.tools import wait, StopWatch
from pybricks.hubs import PrimeHub
from pybricks.parameters import Icon
from pybricks.tools import Matrix as _Matrix

from bluepad import BluePad
from consts import GAMEPAD_BTN

hub = PrimeHub()
hub.display.orientation(up=Side.RIGHT)
hub.display.icon(Icon.HAPPY)

right_leg = Motor(Port.A)
left_leg = Motor(Port.C)
neck = Motor(Port.D)
color_sensor = ColorSensor(Port.E)

color_sensor.lights.off()

bp = BluePad(Port.F)


SPEED = 500

last_btn = 0

# DPad control

# while True:
#     btn=bp.gamepad()[5]
#     print(btn)
#     if btn != last_btn:
#         ls = 0
#         rs = 0
#         if btn == UP_BTN:
#             ls = rs = 500
#         if btn == DOWN_BTN:
#             ls = rs = -500
#         if btn == LEFT_BTN:
#             ls = 500
#             rs = -500
#         if btn == RIGHT_BTN:
#             ls = -500
#             rs = 500

#         last_btn=btn
#         right_leg.run(ls)
#         left_leg.run(-rs)

last_d_pad = 0
last_a_btn = 0

is_light_on = False

while True:
    btns = bp.gamepad()

    stick_x = btns[0]
    stick_y = btns[1]
    a_btn = btns[4]
    d_pad = btns[5]
    # print(stick_x, stick_y, d_pad)

    if d_pad != last_d_pad:
        ns = 0
        if d_pad == GAMEPAD_BTN.LEFT:
            ns = 500
        if d_pad == GAMEPAD_BTN.RIGHT:
            ns = -500
        last_d_pad = d_pad
        neck.run(ns)

    if a_btn != last_a_btn:

        if a_btn == GAMEPAD_BTN.X:
            if is_light_on:
                color_sensor.lights.off()
            else:
                color_sensor.lights.on()

            is_light_on = not is_light_on
        last_a_btn = a_btn

    # stick x: - <= | => +
    ssx = -(stick_x / 128 if umath.fabs(stick_x) > 10 else 0)
    # stick y: -  v | ^  +
    ssy = stick_y / 128 if umath.fabs(stick_y) > 10 else 0

    lls = SPEED * (ssy - (0 if ssx <= 0 else ssx))
    rls = SPEED * (ssy - (0 if ssx >= 0 else umath.fabs(ssx)))
    # print(ssy, ssx, lls, rls)

    right_leg.run(-lls)
    left_leg.run(rls)

