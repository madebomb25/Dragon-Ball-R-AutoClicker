import time
import pydirectinput
import PySimpleGUI as sg

'''
He usado 'pydirectinput' en lugar de otras bibliotecas para simular pulsaciones de teclas o clicks en ratones
debido a que los juegos suelen requerir de inputs de un tipo concreto. Roblox usa DirectInput, y casualmente
'pydirectinput' simula el teclado/raton de esa forma.
'''

pydirectinput.FAILSAFE = False # Evito que una rutina pare si se cambia de pestaña. Al volver al juego se seguirá ejecutando.

'''
Cooldown que tienen las funciones de pygameinput. La pulsación de una tecla durará 0.01. Esto es conveniente
para hacer que la pulsación de una tecla sea de solo 0.01 segundos. Esto permite pulsar una tecla lo más rápido posible.
Bajar este valor por debajo de 0.01 no tiene efectos notables. Subirla hará que el autoclicker sea más lento.
'''
pydirectinput.PAUSE = 0.01

#Ancho y alto de la interfaz gráfica (UI).
winWidth = 100
winHeight = 50


'''
En Dragon Ball Rage se entrena la defensa o el Ki manteniendo la tecla Q (entrenar KI) o R (entrenar Defensa)
pulsada, consumiendo una barra de Ki en el proceso. Si la barra llega a 0, se debe recargar pulsando la tecla
C durante 6 segundos.

En esta función, recojo:

    - El tiempo que el jugador quiere entrenar (en segundos).
    - Durante cuanto tiempo (en segundos) se quiere mantener la tecla de entrenamiento (Q o R) antes de recargar el Ki.

No pido el tiempo de recarga o la tecla al usuario, la UI se encargará de pasar ambas cosas como argumentos dependiendo
del tipo de entrenamiento seleccionado.
'''
def trainKiDef(trainDuration, timeToKiRecharge, key):
    rechargeTime = 6 # tiempo de recarga de la barra de Ki.

    '''
    Calculo el tiempo que dura un ciclo de entrenamiento. Desde que se comienza a entrenar hasta que se acaba la barra de Ki y se termina de recargar.
    '''
    cycleDuration = timeToKiRecharge + rechargeTime # Duración de un cíclo: [ COMIENZO_A_ENTRENAR + RECARGO EL KI ]

    '''
    Calculo la cantidad de ciclos que se pueden realizar en el tiempo dado por el usuario y uso un for loop para repetir
    el mismo ciclo de entrenamiento tantas veces como se pueda en el tiempo dado. El calculo es sencillo, dividir la cantidad
    de segundos dados por la ya calculada duración de un ciclo de entrenamiento.
    '''
    for x in range(int(trainDuration/cycleDuration)+1): #Convierto el valor a entero porque range() no acepta float.

        '''
        Se mantiene pulsada la tecla de entrenamiento durante el tiempo dado.
        '''
        pydirectinput.keyDown(key)
        time.sleep(timeToKiRecharge)

        '''
        Deja de pulsar la tecla y se espera 0.5 segundos para pulsar la tecla de recarga de Ki.
        Esto para evitar que no se pulsen a la vez.
        '''
        pydirectinput.keyUp(key)
        time.sleep(0.5)

        '''
        Recarga de Ki durante 6 segundos.
        '''
        pydirectinput.keyDown('c')
        time.sleep(rechargeTime)

        '''
        Deja de pulsar la tecla de recarga de Ki para comenzar el siguiente ciclo de entrenamiento.
        '''
        pydirectinput.keyUp('c')


'''
Para entrenar el ataque no se permite mantener la tecla pulsada, hay que pulsar repetidamente la tecla 'E'.
'''
def trainAttack(trainDuration):
    timeBetweenPress = 0.2 # Defino el tiempo entre pulsaciones

    '''
    Calculo la cantidad de veces que se debe repetir el ciclo de entrenamiento de la misma forma que en
    trainKiDef().
    '''
    for x in range(int(trainDuration / timeBetweenPress + 1)): #Convierto el valor a entero porque range() no acepta float.

        '''
        El método .press() es la fusion de keyDown() y keyUp(). En resumen, simula que haces una única pulsación en el tiempo
        especificado en pydirectinput.PAUSE.
        '''
        pydirectinput.press('e')
        time.sleep(timeBetweenPress)


# Distribución de los elementos de la interfaz gráfica.
layout = [
    [sg.Text('Train Duration  '), sg.Input(key='trainDuration', do_not_clear=True, size=(5, 1))],
    [sg.Text('Time to Ki Recharge '), sg.Input(key='timeToKiRecharge', do_not_clear=True, size=(5, 1))],
    [sg.Text(' ')],
    [sg.Button(key='KiTrain',button_text='Train Ki')],
    [sg.Button(key='AttackTrain',button_text='Train Attack')],
    [sg.Button(key='DefTrain',button_text='Def Train')]
]

# Genero una ventana usando el layout y el tamaño definidos anteriormente.
window = sg.Window("DB:Rage AutoClicker by MadeBomb", layout, margins=(winWidth,winHeight))

'''
Bucle principal del programa. Cada 'evento' corresponde a hacer click en un botón de la interfaz gráfica.
Dependiendo del botón seleccionado se ejecuta una rutina de entrenamiento diferente.

Espero 5 segundos después de ejecutar alguna rutina para dar tiempo a ir a Roblox.

La síntaxis values['ALGO'] hace referencia al valor que el usuario ha puesto en algún cuadro de texto. Lo que
se pone entre comillas simples es el identificador del cuadro (revisa el parámetro 'key' en los botones).
'''
while True:
    event, values = window.read();
    if event == sg.WIN_CLOSED:
        break
    elif event == 'KiTrain':
        time.sleep(5)
        trainKiDef(float(values['trainDuration']), float(values['timeToKiRecharge']), 'q')
    elif event == 'AttackTrain':
        time.sleep(5)
        trainAttack(float(values['trainDuration']))
    elif event == 'DefTrain':
        time.sleep(5)
        trainKiDef(float(values['trainDuration']), float(values['timeToKiRecharge']), 'r')
window.close()



