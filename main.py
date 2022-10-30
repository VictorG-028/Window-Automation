import numpy as np
import cv2
# import pytesseract as tess
# tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import os
import pyautogui as autogui
from time import sleep
from PIL import ImageGrab
from WindowController import WindowController


""" Links úteis:
Changing working directory to the folder this script is in.
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

Como pegar o título de uma janela
    https://superuser.com/questions/378790/how-to-get-window-title-in-windows-from-shell
    Lista de processos -> tasklist /v /FO:CSV
    Todos os títulos de janela existentes -> Get-Process | Where-Object {$_.mainWindowTitle} | Format-Table Id, Name, mainWindowtitle -AutoSize
    Título da janela com PID -> (Get-Process -id <PID_AKI> -ErrorAction SilentlyContinue).MainWindowTitle
"""

clash_emulator_window = WindowController("BlueStacks App Player")

while False:
    screenshot = clash_emulator_window.take_screenshot()

    cv2.imshow("Screenshot", screenshot)
    

    if cv2.waitKey(1) == ord('q'):
        break



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
