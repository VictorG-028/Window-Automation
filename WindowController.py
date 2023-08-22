import win32gui, win32ui, win32con
import cv2
import numpy as np
import pyautogui as autogui
from time import sleep

from base.Point import Point

""" Links úteis:
Fast Window Capture
    https://learncodebygaming.com/blog/fast-window-capture
    https://www.youtube.com/watch?v=WymCpVUPWQ4
Documentação da função cDC.BitBlt
    http://www.icodeguru.com/vc&mfc/mfcreference/html/_mfc_cdc.3a3a.bitblt.htm
Print Out Live mouse coordinates
    https://stackoverflow.com/questions/7142342/get-window-position-size-with-python
Get Window/Client coordinates and size
    https://www.programcreek.com/python/example/89832/win32gui.GetClientRect
Bring Window to Front
    https://mail.python.org/pipermail/python-win32/2006-February/004261.html
Template Matching
    ???
"""

class WindowController:
    w = 0
    h = 0
    hwnd = None # Window Handle
    top_left: Point = None
    bottom_right: Point = None
    folder_name = None

    def __init__(self, window_name: str, folder_name: str):
        self.folder_name = folder_name
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception(f'Window with name {window_name} not found')

        self.update_window_position()
    
    @staticmethod
    def clean_before_exit():
        cv2.destroyAllWindows()


    def update_window_position(self) -> None:
        # window_rect = win32gui.GetWindowRect(self.hwnd)

        _left, _top, _right, _bottom = win32gui.GetClientRect(self.hwnd)
        left, top = win32gui.ClientToScreen(self.hwnd, (_left, _top))
        right, bottom = win32gui.ClientToScreen(self.hwnd, (_right, _bottom))

        self.w = right - left
        self.h = bottom - top

        self.top_left = Point(left, top)
        self.bottom_right = Point(right, bottom)


    def take_screenshot(self, top_left: Point = Point(0,0), bottom_right: Point = None, trim: bool = False) -> np.ndarray:
        
        # Avoid NameError: name 'self' is not defined by making bottom_right default value equal Point(self.w, self.h)
        bottom_right = bottom_right or Point(self.w, self.h)

        # Get width and height of a rectangle inside the window
        w, h = bottom_right.x - top_left.x, bottom_right.y - top_left.y

        # get the window image data
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt(top_left.as_tuple(), (w, h), dcObj, top_left.as_tuple(), win32con.SRCCOPY)

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

        # Remove black space around the rectangle screenshot
        if trim:
           img = img[top_left.y:bottom_right.y , top_left.x:bottom_right.x] 

        return img


    def show_screenshot_continuously(self, scan_quadrant = 'full-window') -> None:
        scan_quadrants = {
            'full-window': (Point(0,0), Point(self.w, self.h)),
            'only-right':  (Point(self.w//2, 0), Point(self.w, self.h)),
            'only-left':   (Point(0,0), Point(self.w//2, self.h)),
            'only-up':     (Point(0,0), Point(self.w, self.h//2)),
            'only-bottom': (Point(0, self.h//2), Point(self.w, self.h)),
            'up-left':     (Point(0,0), Point(self.w//2, self.h//2)),
            'up-right':    (Point(self.w//2, 0), Point(self.w, self.h//2)),
            'down-left':   (Point(0, self.h//2), Point(self.w//2, self.h)),
            'down-right':  (Point(self.w//2, self.h//2), Point(self.w, self.h)),
        }
        search_rect = scan_quadrants.get(scan_quadrant)
        while True:
            screenshot = self.take_screenshot(*search_rect)
            cv2.imshow("Screenshot", screenshot)

            if cv2.waitKey(1) == ord('q'):
                break


    def maximize(self) -> None:
        win32gui.ShowWindow(self.hwnd, win32con.SW_MAXIMIZE)


    def to_front(self, focus = False) -> None:
        win32gui.SetForegroundWindow(self.hwnd)
        win32gui.BringWindowToTop(self.hwnd)

        if focus:
            self.move_to(Point(10, 10), {'width': 0, 'height': 0})
            WindowController.click()

        sleep(1)


    def find_button(self, button_img_name: str, scan_quadrant = 'full-window') -> tuple[Point, dict[str, int]]:
        
        scan_quadrants = {
            'full-window': (Point(0,0), None), # Point(self.w, self.h)
            'only-right':  (Point(self.w//2, 0), Point(self.w, self.h)),
            'only-left':   (Point(0,0), Point(self.w//2, self.h)),
            'only-up':     (Point(0,0), Point(self.w, self.h//2)),
            'only-bottom': (Point(0, self.h//2), Point(self.w, self.h)),
            'up-left':     (Point(0,0), Point(self.w//2, self.h//2)),
            'up-right':    (Point(self.w//2, 0), Point(self.w, self.h//2)),
            'down-left':   (Point(0, self.h//2), Point(self.w//2, self.h)),
            'down-right':  (Point(self.w//2, self.h//2), Point(self.w, self.h)),
        }
        search_rect = scan_quadrants.get(scan_quadrant)

        img = self.take_screenshot(*search_rect)
        template = cv2.imread(f"images/{self.folder_name}/{button_img_name}.png")

        # All the 6 methods for comparison in a list
        methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR', 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
 
        res = cv2.matchTemplate(img, template, eval(methods[1]))
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # print(f"{min_val}, {max_val}, {min_loc}, {max_loc}")

        return Point(*max_loc), {'width': template.shape[0], 'height': template.shape[1]}


    def move_to(self, screen_point: Point, rectangle_shape: None | dict[str, int], duration: float = 0.2) -> None:
        relative_to_sreen_coordinate = self.top_left + screen_point
        destination_point = relative_to_sreen_coordinate
        if rectangle_shape is not None:
            certer_button_point = (
                relative_to_sreen_coordinate.x + rectangle_shape['width']//2,
                relative_to_sreen_coordinate.y + rectangle_shape['height']//2,
            )
            destination_point = certer_button_point

        autogui.moveTo(*destination_point)
        sleep(duration)

    
    @staticmethod
    def click(mouse = True, mouse_button = 'left', keyboard_button = 'space', hold = 0.2, duration = 0.2) -> None:
        
        if mouse:
            # autogui.click(button='left', duration=1.0)
            autogui.mouseDown(button=mouse_button)
            sleep(hold)
            autogui.mouseUp(button=mouse_button)
            sleep(duration)
        else: 
            raise Exception("Click with keyboard not implemented")

    @property
    def resolution(self) -> str:
        resolution = self.bottom_right - self.top_left
        return f"{resolution.x} X {resolution.y}"
