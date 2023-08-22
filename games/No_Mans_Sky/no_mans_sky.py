import numpy as np
import cv2
# import pytesseract as tess
# tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import os
import pyautogui as autogui
import pydirectinput as directinput
from time import sleep
from base.Point import Point
from WindowController import WindowController


nms_emulator_window = WindowController("No Man's Sky", "No_Mans_Sky")


def farm_cloro():
    sleep(2)

    # Coloca em foco janela do jogo
    nms_emulator_window.to_front(focus = True)


    # Abastecer oxigênio
    nms_emulator_window.move_to(150, 351)
    WindowController.click()

    oxygen_item_loc, oxygen_item_shape = nms_emulator_window.find_button("Oxygen")
    nms_emulator_window.move_to(oxygen_item_loc, oxygen_item_shape)
    WindowController.click()

    nms_emulator_window.move_to(150, 351)
    WindowController.click()


    # Abastecer Cloro
    nms_emulator_window.move_to(150, 463)
    WindowController.click()

    chlorine_item_loc, chlorine_item_shape = nms_emulator_window.find_button("Chlorine")
    nms_emulator_window.move_to(chlorine_item_loc, chlorine_item_shape)
    WindowController.click()

    nms_emulator_window.move_to(150, 463)
    WindowController.click()



    # Ligar máquina
    directinput.keyDown('e')
    sleep(1)
    directinput.keyUp('e')

    # Esperar 4 minutos e 5 segundos
    sleep(4*60 + 5)

    # Encontra o cloro de output
    chlorine_item_loc, chlorine_item_shape = nms_emulator_window.find_button("Chlorine", scan_quadrant = 'only-right')
    nms_emulator_window.move_to(chlorine_item_loc, chlorine_item_shape)

    chlorine_item_loc, chlorine_item_shape = nms_emulator_window.find_button("Chlorine", scan_quadrant = 'only-right')
    nms_emulator_window.move_to(chlorine_item_loc, chlorine_item_shape)
    WindowController.click()
    
    # Colocar cloro gerado no iventário
    directinput.press('x')

    
    # Encontra o cloro de input
    chlorine_item_loc, chlorine_item_shape = nms_emulator_window.find_button("Chlorine", scan_quadrant = 'only-left')
    nms_emulator_window.move_to(chlorine_item_loc, chlorine_item_shape)

    chlorine_item_loc, chlorine_item_shape = nms_emulator_window.find_button("Chlorine", scan_quadrant = 'only-left')
    nms_emulator_window.move_to(chlorine_item_loc, chlorine_item_shape)
    WindowController.click()
    
    # Colocar cloro gerado de input no iventário
    directinput.press('x')

    # Reabastecer cloro
    autogui.moveTo(1340, 620)
    sleep(1)
    WindowController.click()

    chlorine_item_loc, chlorine_item_shape = nms_emulator_window.find_button("Chlorine")
    nms_emulator_window.move_to(chlorine_item_loc, chlorine_item_shape)
    WindowController.click()

    autogui.moveTo(1340, 620)
    sleep(1)
    WindowController.click()

    # Encontra o oxigênio de input
    oxygen_item_loc, oxygen_item_shape = nms_emulator_window.find_button("Oxygen", scan_quadrant = 'only-left')
    nms_emulator_window.move_to(oxygen_item_loc, oxygen_item_shape)

    oxygen_item_loc, oxygen_item_shape = nms_emulator_window.find_button("Oxygen", scan_quadrant = 'only-left')
    nms_emulator_window.move_to(oxygen_item_loc, oxygen_item_shape)
    WindowController.click()
    
    # Colocar oxigênio gerado de input no iventário
    directinput.press('x')

    




# WindowController.clean_before_exit()

def test():
    # sleep(2)
    nms_emulator_window.update_window_position()
    print(nms_emulator_window.top_left)
    print(nms_emulator_window.resolution)

    # Coloca em foco janela do jogo
    # nms_emulator_window.to_front(focus = True)

    # test 1
    top_left = Point(1183, 179)
    sample_top = Point(1332, 529)
    sample_bottom = Point(1334, 643)
    r1 = sample_top - top_left
    r2 = sample_bottom - top_left
    print(f"Test 1 response: {r1} {r2}")

    # Test 2
    top_left = Point(152, 151)
    sample_top = Point(300, 502)
    sample_bottom = Point(301, 615)
    r1 = sample_top - top_left
    r2 = sample_bottom - top_left
    print(f"Test 2 response: {r1} {r2}")

    # Test 3
    top_left = Point(655, 397)
    sample_top = Point(803, 752)
    sample_bottom = Point(805, 858)
    r1 = sample_top - top_left
    r2 = sample_bottom - top_left
    print(f"Test 3 response: {r1} {r2}")


    # resultado
    # top = (150, 351) 
    # bottom = (150, 463)

    
