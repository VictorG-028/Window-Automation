import numpy as np
import cv2
# import pytesseract as tess
# tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import os
import pyautogui as autogui
from time import sleep
from WindowController import WindowController

clash_emulator_window = WindowController("BlueStacks App Player")


print("INICIO")
sleep(3)
autogui.moveTo(*clash_emulator_window.top_left)
# print(autogui.displayMousePosition())
# button_loc, button_shape = clash_emulator_window.find_button("Upgrade_Info_Button")
button_loc, button_shape = clash_emulator_window.find_button("Elixir_Storage_Info")
clash_emulator_window.move_to(button_loc, button_shape)
sleep(1)
button_loc, button_shape = clash_emulator_window.find_button("Gold_Storage_Info")
clash_emulator_window.move_to(button_loc, button_shape)
sleep(1)
button_loc, button_shape = clash_emulator_window.find_button("Dark_Elixir_Storage_Info")
clash_emulator_window.move_to(button_loc, button_shape)


def clean_before_exit():
    cv2.destroyAllWindows()

print("FIM")
clean_before_exit()
exit()
