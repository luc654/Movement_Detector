import gpiod
from gpiozero import DistanceSensor
import time
from gpiozero import Button
button = Button(2)



max = input("Max centimeters.Default 400: ")
barsize = input("Barsize. Default 36: ")


if len(barsize) < 1:
        barsize = 36

if len(max) < 1:
        max = 400

maxMeters = int(max) / 100

ultrasonic = DistanceSensor(echo=17, trigger=4, max_distance=maxMeters)
margin = 9


def genBasis():
    counter = 100
    index = 0
    total = 0
    while index < counter:
        distance = ultrasonic.distance
        rounded = str(round(distance, 3))
        total += float(rounded)
        index += 1
    average = total / counter * 100
    return float(str(round(average, 3)))


# For printing the bar
fillBlock = "██"
emptBlock = "▒▒"
targetBlock = "▞▞"
def printBar(max, curr, barsize, target):

        curr= round(float(curr))
        fillAmount = round(int(barsize) / int(max) * int(curr))
        targetPlacement = round(int(barsize) / int(max) * int(target) -1 )
        fillBar =  [fillBlock] * int(fillAmount)
        emptBar = [emptBlock] * (int(barsize)-int(fillAmount))
        bar = fillBar+emptBar
        bar[targetPlacement] = targetBlock

        barString = "".join(bar)
        print(barString)





chip = gpiod.Chip('gpiochip4')
led_line = chip.get_line(26)
led_line.request(consumer='LED', type=gpiod.LINE_REQ_DIR_OUT)



button.wait_for_press()


basis = genBasis()
print("basis: " + str(basis))
out = False

while True:
    # Handle if button is pressed
    if button.is_pressed:
        basis = genBasis()

    time.sleep(0.05)
    distance = ultrasonic.distance
    rounded = str(round(distance * 100, 2))

    printBar(max, rounded, barsize, basis)

    top = basis + margin
    bottom = basis - margin

    if float(rounded) > float(top) or float(rounded) < float(bottom):
        led_line.set_value(1)
        if out is False:
            out = True
    else:
        led_line.set_value(0)
        if out is True:
            out = False
