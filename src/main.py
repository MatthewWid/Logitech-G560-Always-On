import subprocess
import time
import win32gui
import pyautogui

subprocess.run(["C:\\Program Files\\LGHUB\\lghub.exe"])

time.sleep(1)

hwnd = win32gui.FindWindow(None, 'LGHUB')
rect = win32gui.GetWindowRect(hwnd)
winX = rect[0]
winY = rect[1]
winW = rect[2] - winX
winH = rect[3] - winY

prevMouseX, prevMouseY = pyautogui.position()

closeButtonX, closeButtonY = winX + winW - 15, winY + 15

pyautogui.moveTo(closeButtonX, closeButtonY)

pyautogui.click(closeButtonX, closeButtonY)

pyautogui.moveTo(prevMouseX, prevMouseY)
