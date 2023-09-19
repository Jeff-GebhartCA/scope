from m5stack import *
from m5stack_ui import *
from uiflow import *
from libs.m5_espnow import M5ESPNOW
import time


screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xff0000)


track_magic_number = None
ra_west_track = None
data = None
ra_button_speed = None
dec_button_speed = None
ra_track_speed = None
ra_enable_status = None
dec_enable_status = None
center_speed = None
slew_speed = None
ludicrous_speed = None
magic_number_change_factor = None

now = M5ESPNOW(1, 1)

rst_button = M5Btn(text='RST', x=130, y=1, w=70, h=30, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_14, parent=None)
ra_en = M5Btn(text='RA EN', x=8, y=25, w=70, h=30, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_14, parent=None)
ra_speed_track = M5Btn(text='Track', x=0, y=64, w=70, h=30, bg_c=0x33cc00, text_c=0x000000, font=FONT_MONT_14, parent=None)
ra_speed_center = M5Btn(text='Center', x=0, y=99, w=70, h=30, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_14, parent=None)
ra_speed_slew = M5Btn(text='Slew', x=0, y=136, w=70, h=30, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_14, parent=None)
ra_speed_ludicrous = M5Btn(text='Ludicrous', x=0, y=173, w=70, h=30, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_14, parent=None)
btn_save_magic_number = M5Btn(text='Save', x=128, y=210, w=70, h=30, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_14, parent=None)
dec_enable = M5Btn(text='DEC EN', x=250, y=25, w=70, h=30, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_14, parent=None)
dec_speed_track = M5Btn(text='Track', x=250, y=64, w=70, h=30, bg_c=0x33cc00, text_c=0x000000, font=FONT_MONT_14, parent=None)
dec_speed_center = M5Btn(text='Center', x=250, y=99, w=70, h=30, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_14, parent=None)
dec_speed_slew = M5Btn(text='Slew', x=250, y=136, w=70, h=30, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_14, parent=None)
dec_speed_ludicrous = M5Btn(text='Ludicrous', x=250, y=173, w=70, h=30, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_14, parent=None)
btn_North = M5Btn(text='N', x=140, y=54, w=40, h=40, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_14, parent=None)
btn_West = M5Btn(text='W', x=99, y=100, w=40, h=40, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_14, parent=None)
btn_East = M5Btn(text='E', x=176, y=100, w=40, h=40, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_14, parent=None)
btn_South = M5Btn(text='S', x=140, y=156, w=40, h=40, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_14, parent=None)
magic = M5Label('MagicNumber', x=13, y=215, color=0xffffff, font=FONT_MONT_14, parent=None)
magic_number_change = M5Label('Factor', x=231, y=215, color=0xffffff, font=FONT_MONT_14, parent=None)

from numbers import Number


# Describe this function...
def setState():
  global track_magic_number, ra_west_track, data, ra_button_speed, dec_button_speed, ra_track_speed, ra_enable_status, dec_enable_status, center_speed, slew_speed, ludicrous_speed, magic_number_change_factor
  magic.set_text(str(track_magic_number))
  magic_number_change.set_text(str(magic_number_change_factor))
  ra_track_speed = track_magic_number
  ra_west_track = track_magic_number * 2
  ra_button_speed = ra_track_speed
  dec_button_speed = track_magic_number
  center_speed = int((track_magic_number / 4))
  slew_speed = int((center_speed / 4))
  ludicrous_speed = 200
  now.espnow_add_peer('b0a732f34870', 1, 0, False)
  now.espnow_send_data(1, 'ra dis')
  now.espnow_send_data(1, ((str('ra speed ') + str(int(ra_track_speed)))))
  now.espnow_send_data(1, 'ra fwd')
  now.espnow_send_data(1, 'dec dis')
  now.espnow_send_data(1, ((str('dec speed ') + str(int(dec_button_speed)))))
  now.espnow_send_data(1, 'dec fwd')
  ra_enable_status = False
  rgb.setBrightness(10)
  rgb.setColorFrom(6, 10, 0x00ff00)
  rgb.setColorFrom(1, 5, 0x00ff00)
  ra_en.set_bg_color(0xffffff)
  ra_speed_track.set_bg_color(0x33ff33)
  ra_speed_center.set_bg_color(0xffffff)
  ra_speed_slew.set_bg_color(0xffffff)
  ra_speed_ludicrous.set_bg_color(0xffffff)
  dec_enable.set_bg_color(0xffffff)
  dec_speed_track.set_bg_color(0x33ff33)
  dec_speed_center.set_bg_color(0xffffff)
  dec_speed_slew.set_bg_color(0xffffff)
  dec_speed_ludicrous.set_bg_color(0xffffff)
  speaker.playTone(262, 2, volume=5)

# Describe this function...
def sendData(data):
  global track_magic_number, ra_west_track, ra_button_speed, dec_button_speed, ra_track_speed, ra_enable_status, dec_enable_status, center_speed, slew_speed, ludicrous_speed, magic_number_change_factor
  for count in range(5):
    now.espnow_send_data(1, data)
    wait_ms(10)


def rst_button_pressed():
  global track_magic_number, ra_west_track, ra_button_speed, dec_button_speed, ra_track_speed, ra_enable_status, dec_enable_status, center_speed, slew_speed, ludicrous_speed, magic_number_change_factor, data
  setState()
  pass
rst_button.pressed(rst_button_pressed)

def ra_en_pressed():
  global track_magic_number, ra_west_track, ra_button_speed, dec_button_speed, ra_track_speed, ra_enable_status, dec_enable_status, center_speed, slew_speed, ludicrous_speed, magic_number_change_factor, data
  if ra_enable_status:
    ra_enable_status = False
    ra_en.set_bg_color(0xffffff)
    rgb.setColorFrom(6, 10, 0x00ff00)
    sendData('ra dis')
  else:
    ra_enable_status = True
    ra_en.set_bg_color(0x33ff33)
    rgb.setColorFrom(6, 10, 0xff0000)
    sendData((str('ra speed ') + str(int(ra_track_speed))))
    sendData('ra en')
  pass
ra_en.pressed(ra_en_pressed)

def ra_speed_track_pressed():
  global track_magic_number, ra_west_track, ra_button_speed, dec_button_speed, ra_track_speed, ra_enable_status, dec_enable_status, center_speed, slew_speed, ludicrous_speed, magic_number_change_factor, data
  ra_button_speed = ra_track_speed
  ra_speed_track.set_bg_color(0x33ff33)
  ra_speed_center.set_bg_color(0xffffff)
  ra_speed_slew.set_bg_color(0xffffff)
  ra_speed_ludicrous.set_bg_color(0xffffff)
  pass
ra_speed_track.pressed(ra_speed_track_pressed)

def btn_save_magic_number_pressed():
  global track_magic_number, ra_west_track, ra_button_speed, dec_button_speed, ra_track_speed, ra_enable_status, dec_enable_status, center_speed, slew_speed, ludicrous_speed, magic_number_change_factor, data
  pass
btn_save_magic_number.pressed(btn_save_magic_number_pressed)

def btn_North_pressed():
  global track_magic_number, ra_west_track, ra_button_speed, dec_button_speed, ra_track_speed, ra_enable_status, dec_enable_status, center_speed, slew_speed, ludicrous_speed, magic_number_change_factor, data
  sendData((str('dec speed ') + str(int(dec_button_speed))))
  sendData('dec fwd')
  sendData('dec en')
  pass
btn_North.pressed(btn_North_pressed)

def btn_North_released():
  global track_magic_number, ra_west_track, ra_button_speed, dec_button_speed, ra_track_speed, ra_enable_status, dec_enable_status, center_speed, slew_speed, ludicrous_speed, magic_number_change_factor, data
  sendData('dec fwd')
  sendData('dec stop')
  pass
btn_North.released(btn_North_released)

def dec_enable_pressed():
  global track_magic_number, ra_west_track, ra_button_speed, dec_button_speed, ra_track_speed, ra_enable_status, dec_enable_status, center_speed, slew_speed, ludicrous_speed, magic_number_change_factor, data
  if dec_enable_status:
    dec_enable_status = False
    dec_enable.set_bg_color(0xffffff)
    rgb.setColorFrom(1, 5, 0x00ff00)
    sendData('dec dis')
  else:
    dec_enable_status = True
    dec_enable.set_bg_color(0x33ff33)
    rgb.setColorFrom(1, 5, 0xff0000)
    sendData('dec stop')
    sendData('dec en')
  pass
dec_enable.pressed(dec_enable_pressed)

def ra_speed_center_pressed():
  global track_magic_number, ra_west_track, ra_button_speed, dec_button_speed, ra_track_speed, ra_enable_status, dec_enable_status, center_speed, slew_speed, ludicrous_speed, magic_number_change_factor, data
  ra_button_speed = center_speed
  ra_speed_center.set_bg_color(0x33ff33)
  ra_speed_track.set_bg_color(0xffffff)
  ra_speed_slew.set_bg_color(0xffffff)
  ra_speed_ludicrous.set_bg_color(0xffffff)
  pass
ra_speed_center.pressed(ra_speed_center_pressed)

def ra_speed_slew_pressed():
  global track_magic_number, ra_west_track, ra_button_speed, dec_button_speed, ra_track_speed, ra_enable_status, dec_enable_status, center_speed, slew_speed, ludicrous_speed, magic_number_change_factor, data
  ra_button_speed = slew_speed
  ra_speed_slew.set_bg_color(0x33ff33)
  ra_speed_track.set_bg_color(0xffffff)
  ra_speed_center.set_bg_color(0xffffff)
  ra_speed_ludicrous.set_bg_color(0xffffff)
  pass
ra_speed_slew.pressed(ra_speed_slew_pressed)

def ra_speed_ludicrous_pressed():
  global track_magic_number, ra_west_track, ra_button_speed, dec_button_speed, ra_track_speed, ra_enable_status, dec_enable_status, center_speed, slew_speed, ludicrous_speed, magic_number_change_factor, data
  ra_button_speed = ludicrous_speed
  ra_speed_ludicrous.set_bg_color(0x33ff33)
  ra_speed_track.set_bg_color(0xffffff)
  ra_speed_center.set_bg_color(0xffffff)
  ra_speed_slew.set_bg_color(0xffffff)
  pass
ra_speed_ludicrous.pressed(ra_speed_ludicrous_pressed)

def dec_speed_track_pressed():
  global track_magic_number, ra_west_track, ra_button_speed, dec_button_speed, ra_track_speed, ra_enable_status, dec_enable_status, center_speed, slew_speed, ludicrous_speed, magic_number_change_factor, data
  dec_button_speed = ra_track_speed
  dec_speed_track.set_bg_color(0x33ff33)
  dec_speed_center.set_bg_color(0xffffff)
  dec_speed_slew.set_bg_color(0xffffff)
  dec_speed_ludicrous.set_bg_color(0xffffff)
  pass
dec_speed_track.pressed(dec_speed_track_pressed)

def dec_speed_center_pressed():
  global track_magic_number, ra_west_track, ra_button_speed, dec_button_speed, ra_track_speed, ra_enable_status, dec_enable_status, center_speed, slew_speed, ludicrous_speed, magic_number_change_factor, data
  dec_button_speed = center_speed
  dec_speed_center.set_bg_color(0x33ff33)
  dec_speed_track.set_bg_color(0xffffff)
  dec_speed_slew.set_bg_color(0xffffff)
  dec_speed_ludicrous.set_bg_color(0xffffff)
  pass
dec_speed_center.pressed(dec_speed_center_pressed)

def dec_speed_slew_pressed():
  global track_magic_number, ra_west_track, ra_button_speed, dec_button_speed, ra_track_speed, ra_enable_status, dec_enable_status, center_speed, slew_speed, ludicrous_speed, magic_number_change_factor, data
  dec_button_speed = slew_speed
  dec_speed_slew.set_bg_color(0x33ff33)
  dec_speed_center.set_bg_color(0xffffff)
  dec_speed_track.set_bg_color(0xffffff)
  dec_speed_ludicrous.set_bg_color(0xffffff)
  pass
dec_speed_slew.pressed(dec_speed_slew_pressed)

def dec_speed_ludicrous_pressed():
  global track_magic_number, ra_west_track, ra_button_speed, dec_button_speed, ra_track_speed, ra_enable_status, dec_enable_status, center_speed, slew_speed, ludicrous_speed, magic_number_change_factor, data
  dec_button_speed = ludicrous_speed
  dec_speed_ludicrous.set_bg_color(0x33ff33)
  dec_speed_center.set_bg_color(0xffffff)
  dec_speed_slew.set_bg_color(0xffffff)
  dec_speed_track.set_bg_color(0xffffff)
  pass
dec_speed_ludicrous.pressed(dec_speed_ludicrous_pressed)

def btn_South_pressed():
  global track_magic_number, ra_west_track, ra_button_speed, dec_button_speed, ra_track_speed, ra_enable_status, dec_enable_status, center_speed, slew_speed, ludicrous_speed, magic_number_change_factor, data
  sendData((str('dec speed ') + str(int(dec_button_speed))))
  sendData('dec back')
  sendData('dec en')
  pass
btn_South.pressed(btn_South_pressed)

def btn_South_released():
  global track_magic_number, ra_west_track, ra_button_speed, dec_button_speed, ra_track_speed, ra_enable_status, dec_enable_status, center_speed, slew_speed, ludicrous_speed, magic_number_change_factor, data
  sendData('dec fwd')
  sendData('dec stop')
  pass
btn_South.released(btn_South_released)

def btn_East_pressed():
  global track_magic_number, ra_west_track, ra_button_speed, dec_button_speed, ra_track_speed, ra_enable_status, dec_enable_status, center_speed, slew_speed, ludicrous_speed, magic_number_change_factor, data
  sendData((str('ra speed ') + str(int(ra_button_speed))))
  sendData('ra back')
  sendData('ra en')
  pass
btn_East.pressed(btn_East_pressed)

def btn_East_released():
  global track_magic_number, ra_west_track, ra_button_speed, dec_button_speed, ra_track_speed, ra_enable_status, dec_enable_status, center_speed, slew_speed, ludicrous_speed, magic_number_change_factor, data
  sendData((str('ra speed ') + str(int(ra_track_speed))))
  sendData('ra fwd')
  pass
btn_East.released(btn_East_released)

def btn_West_pressed():
  global track_magic_number, ra_west_track, ra_button_speed, dec_button_speed, ra_track_speed, ra_enable_status, dec_enable_status, center_speed, slew_speed, ludicrous_speed, magic_number_change_factor, data
  if ra_button_speed == ra_track_speed:
    sendData((str('ra speed ') + str(int(ra_west_track))))
  else:
    sendData((str('ra speed ') + str(int(ra_button_speed))))
  sendData('ra fwd')
  sendData('ra en')
  pass
btn_West.pressed(btn_West_pressed)

def btn_West_released():
  global track_magic_number, ra_west_track, ra_button_speed, dec_button_speed, ra_track_speed, ra_enable_status, dec_enable_status, center_speed, slew_speed, ludicrous_speed, magic_number_change_factor, data
  sendData((str('ra speed ') + str(int(ra_track_speed))))
  sendData('ra fwd')
  pass
btn_West.released(btn_West_released)

def buttonA_wasPressed():
  global track_magic_number, ra_west_track, ra_button_speed, dec_button_speed, ra_track_speed, ra_enable_status, dec_enable_status, center_speed, slew_speed, ludicrous_speed, magic_number_change_factor, data
  track_magic_number = (track_magic_number if isinstance(track_magic_number, Number) else 0) + magic_number_change_factor * -1
  magic.set_text(str(track_magic_number))
  pass
btnA.wasPressed(buttonA_wasPressed)

def buttonB_wasPressed():
  global track_magic_number, ra_west_track, ra_button_speed, dec_button_speed, ra_track_speed, ra_enable_status, dec_enable_status, center_speed, slew_speed, ludicrous_speed, magic_number_change_factor, data
  if magic_number_change_factor < 1001:
    magic_number_change_factor = magic_number_change_factor * 10
  else:
    magic_number_change_factor = 1
  magic_number_change.set_text(str(magic_number_change_factor))
  pass
btnB.wasPressed(buttonB_wasPressed)

def buttonC_wasPressed():
  global track_magic_number, ra_west_track, ra_button_speed, dec_button_speed, ra_track_speed, ra_enable_status, dec_enable_status, center_speed, slew_speed, ludicrous_speed, magic_number_change_factor, data
  track_magic_number = (track_magic_number if isinstance(track_magic_number, Number) else 0) + magic_number_change_factor * 1
  magic.set_text(str(track_magic_number))
  pass
btnC.wasPressed(buttonC_wasPressed)


track_magic_number = 50000
magic_number_change_factor = 1
setState()

