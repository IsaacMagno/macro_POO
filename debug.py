import pyautogui
from time import sleep

num = [1, 2, 3]

# função auxiliar para desbugar o shift
# durante desenvolvimento

for n in num:
    pyautogui.keyDown('shiftleft')
    pyautogui.keyDown('shiftright')
    pyautogui.keyDown('shift')

    pyautogui.click(1009, 159)
    sleep(1)
    pyautogui.click(996, 239)

    pyautogui.keyUp('shiftleft')
    pyautogui.keyUp('shiftright')
    pyautogui.keyUp('shift')
