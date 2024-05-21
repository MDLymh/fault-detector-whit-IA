import cv2
import time
import numpy as np
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import mss
import win32gui

class BrowserRecorder:
    def __init__(self, url):
        self.url = url
        self.driver = None
        self.recording_thread = None
        self.is_recording = False
        self.browser_handle = None
        self.out = None

    def get_browser_handle(self):
        browser_title = self.driver.title
        def enum_windows(hwnd, result):
            if browser_title in win32gui.GetWindowText(hwnd):
                result.append(hwnd)
        result = []
        win32gui.EnumWindows(enum_windows, result)
        return result[0] if result else None

    def start_browser(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)  # No cerrar el navegador cuando termine el script
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.get(self.url)
        time.sleep(5)  # Ajusta este tiempo según sea necesario
        self.browser_handle = self.get_browser_handle()
        if not self.browser_handle:
            raise Exception("No se pudo encontrar la ventana del navegador.")

    def screen_recorder(self, output_filename):
        sct = mss.mss()
        rect = win32gui.GetWindowRect(self.browser_handle)
        monitor = {'top': rect[1], 'left': rect[0], 'width': rect[2] - rect[0], 'height': rect[3] - rect[1]}
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        self.out = cv2.VideoWriter(output_filename, fourcc, 20.0, (monitor['width'], monitor['height']))

        self.is_recording = True
        try:
            while self.is_recording:
                rect = win32gui.GetWindowRect(self.browser_handle)
                monitor['top'] = rect[1]
                monitor['left'] = rect[0]
                monitor['width'] = rect[2] - rect[0]
                monitor['height'] = rect[3] - rect[1]
                img = sct.grab(monitor)
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                self.out.write(frame)
                time.sleep(0.05)
        finally:
            self.out.release()

    def start_recording(self, output_filename="screen_recording.avi"):
        self.start_browser()
        if self.browser_handle:
            self.recording_thread = threading.Thread(target=self.screen_recorder, args=(output_filename,))
            self.recording_thread.start()
        else:
            raise Exception("El navegador no está iniciado o no se encontró la ventana del navegador.")

    def stop_recording(self):
        self.is_recording = False
        if self.recording_thread:
            self.recording_thread.join()

    def close_browser(self):
        self.stop_recording()
        if self.driver:
            self.driver.quit()
        self.driver = None

