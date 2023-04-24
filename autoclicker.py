import time
from pynput.mouse import Controller, Button
import pydirectinput
import PySimpleGUI as sg

pydirectinput.FAILSAFE = False
pydirectinput.PAUSE = 0.01

winWidth = 200
winHeight = 200

mouse = Controller()

# ciclo = attack_duration + rechargeTime + PAUSE
def trainKiDef(trainDuration, timeToKiRecharge, rechargeTime, key):
    timeBetweenPress = 0.2
    attacksPerCycle = timeToKiRecharge / timeBetweenPress

    attackDuration = timeToKiRecharge + rechargeTime

    for x in range(int(trainDuration/attackDuration)+1):

        for y in range(int(attacksPerCycle+1)):
            pydirectinput.keyDown(key)
            time.sleep(timeBetweenPress)
    
        pydirectinput.keyUp(key)
        time.sleep(0.1)
        pydirectinput.keyDown('c')

        time.sleep(rechargeTime)

        pydirectinput.keyUp('c')

def trainAttack(trainDuration):
    timeBetweenPress = 0.2
    for x in range(int(trainDuration / (timeBetweenPress+pydirectinput.PAUSE))+1):
        pydirectinput.press('e')
        time.sleep(timeBetweenPress) # total = 0.21

#KAKAROTO, ERES LA CURA DE ESTE AMOOOOR!

layout = [
    [sg.Text('Train Duration  '), sg.Input(key='trainDuration', do_not_clear=True, size=(5, 1))],
    [sg.Text('Ki Recharge Time '), sg.Input(key='rechargeTime', do_not_clear=True, size=(5, 1))],
    [sg.Text('Time to Ki Recharge '), sg.Input(key='timeToKiRecharge', do_not_clear=True, size=(5, 1))],
    [sg.Text(' ')],
    [sg.Button(key='KiTrain',button_text='Train Ki')],
    [sg.Button(key='AttackTrain',button_text='Train Attack')]
]

window = sg.Window("Basic AutoClicker by MadeBomb", layout, margins=(winWidth,winHeight))

while True:
    event, values = window.read();
    if event == sg.WIN_CLOSED:
        break
    elif event == 'KiTrain':
        time.sleep(5)
        trainKiDef(float(values['trainDuration']), float(values['timeToKiRecharge']), float(values['rechargeTime']), 'q')
    elif event == 'AttackTrain':
        time.sleep(5)
        trainAttack(float(values['trainDuration']))
window.close()



