import pyautogui
from time import sleep

while(pyautogui.getActiveWindowTitle() != 'VNU Lic'):
    print("Please choose VNU Lic window!")
    sleep(2)

pyautogui.scroll(200)

for numPage in range(1, 5):
    pyautogui.scroll(-95)
    image = pyautogui.screenshot(region=(576, 81, 743, 950))
    image.save(
        'D:\\IMPORTANTS\\CODE\\my_tools\\book_images\\' + str(numPage) + '.jpg')
    pyautogui.scroll(95)
    pyautogui.moveTo(1134, 114, duration=0.25)
    pyautogui.click()
    sleep(1)
