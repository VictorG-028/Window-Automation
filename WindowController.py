from typing import Tuple
import win32gui, win32ui, win32con
import cv2
import numpy as np
import pyautogui as autogui

from Point import Point

""" Links úteis:
Fast Window Capture
    https://learncodebygaming.com/blog/fast-window-capture
    https://www.youtube.com/watch?v=WymCpVUPWQ4
Print Out Live mouse coordinates
    https://stackoverflow.com/questions/7142342/get-window-position-size-with-python
Get Window/Client coordinates and size
    https://www.programcreek.com/python/example/89832/win32gui.GetClientRect
Bring Window to Front
    https://mail.python.org/pipermail/python-win32/2006-February/004261.html
Template Matching
    
"""

class WindowController:
    w = 0
    h = 0
    hwnd = None # Window Handle
    top_left: Point = None
    bottom_right: Point = None

    def __init__(self, window_name: str):
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception(f'Window with name {window_name} not found')

        self.update_window_size()


    def update_window_size(self) -> None:
        # window_rect = win32gui.GetWindowRect(self.hwnd)

        _left, _top, _right, _bottom = win32gui.GetClientRect(self.hwnd)
        left, top = win32gui.ClientToScreen(self.hwnd, (_left, _top))
        right, bottom = win32gui.ClientToScreen(self.hwnd, (_right, _bottom))

        self.w = right - left
        self.h = bottom - top

        self.top_left = Point(left, top)
        self.bottom_right = Point(right, bottom)




    def take_screenshot(self) -> np.ndarray:

        # get the window image data
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (0, 0), win32con.SRCCOPY)

        # convert the raw data into a format opencv can read
        #dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        # free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        # drop the alpha channel, or cv.matchTemplate() will throw an error like:
        #   error: (-215:Assertion failed) (depth == CV_8U || depth == CV_32F) && type == _templ.type() 
        #   && _img.dims() <= 2 in function 'cv::matchTemplate'
        img = img[...,:3]

        # make image C_CONTIGUOUS to avoid errors that look like:
        #   File ... in draw_rectangles
        #   TypeError: an integer is required (got type tuple)
        # see the discussion here:
        # https://github.com/opencv/opencv/issues/14866#issuecomment-580207109
        img = np.ascontiguousarray(img)

        return img


    def maximize(self) -> None:
        win32gui.ShowWindow(self.hwnd, win32con.SW_MAXIMIZE)


    def to_front(self) -> None:
        win32gui.SetForegroundWindow(self.hwnd)

    def find_button(self, button_img_name: str) -> Point:

        # All the 6 methods for comparison in a list
        methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR', 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

        img = self.take_screenshot()
        template = cv2.imread(f"images/{button_img_name}.png")

        res = cv2.matchTemplate(img, template, eval(methods[1]))
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        print(f"{min_val}, {max_val}, {min_loc}, {max_loc}")

        return Point(*max_loc), template.shape


    def move_to(self, screen_point: Point, rectangle_shape: Tuple[int, int]) -> None:
        relative_to_sreen_coordinate = self.top_left + screen_point
        certer_button_point = (
            relative_to_sreen_coordinate.x + rectangle_shape[0]//2,
            relative_to_sreen_coordinate.y + rectangle_shape[1]//2,
        )
        autogui.moveTo(*certer_button_point)