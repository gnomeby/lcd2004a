# https://habr.com/ru/articles/522938/

import gpiozero
import time

d4 = gpiozero.LED(17)
d5 = gpiozero.LED(27)
d6 = gpiozero.LED(22)
d7 = gpiozero.LED(10)
rs = gpiozero.LED(9)
en = gpiozero.LED(11)

CLEAR_DISPLAY = 0x1

# 1.52 ms
RETURN_HOME = 0x2

# 37 us
ENTRY_MODE_SET = 0x6  # mode cursor shift right, display non shift
DISPLAY_ON = 0xC  # non cursor, non blinking
DISPLAY_OFF = 0x8  #
CURSOR_SHIFT_LEFT = 0x10
CURSOR_SHIFT_RIGHT = 0x14
DISPLAY_SHIFT_LEFT = 0x18
DISPLAY_SHIFT_RIGHT = 0x1C
DATA_BUS_4BIT_PAGE0 = 0x28
DATA_BUS_4BIT_PAGE1 = 0x2A
DATA_BUS_8BIT_PAGE0 = 0x38
SET_CGRAM_ADDRESS = 0x40  # usage address |= SET_CGRAM_ADDRESS
SET_DDRAM_ADDRESS = 0x80


def delay_ms(n):
    time.sleep(float(n)/1000)

def delay_us(n):
    time.sleep(float(n)/1000000)

def sendByte(char: int, isData: bool = False):
    # обнуляем все пины дисплея
    d4.off()
    d5.off()
    d6.off()
    d7.off()
    rs.off()
    en.off()

    if isData:
        rs.on()
    else:
        rs.off()

	# ставим старшую тетраду на порт
    if char & 0x80:
        d7.on()
    if char & 0x40:
        d6.on()
    if char & 0x20:
        d5.on()
    if char & 0x10:
        d4.on()

    # поднимаем пин E
    en.on()
	# сбрасываем пин Е
    en.off()

	# обнуляем все пины дисплея кроме RS
    d4.off()
    d5.off()
    d6.off()
    d7.off()

	# ставим младшую тетраду на порт
    if char & 0x8:
        d7.on()
    if char & 0x4:
        d6.on()
    if char & 0x2:
        d5.on()
    if char & 0x1:
        d4.on()

    # поднимаем пин E
    en.on()
	# сбрасываем пин Е
    en.off()

    delay_us(40)


def lcdInit():
    delay_ms(15)  # ждем пока стабилизируется питание

    sendByte(0x33)  # шлем в одном байте два 0011
    delay_us(100)

    sendByte(0x32)  # шлем в одном байте  00110010
    delay_us(40)

    sendByte(DATA_BUS_4BIT_PAGE0)  # включаем режим 4 бит
    delay_us(40)
    sendByte(DISPLAY_OFF)  # выключаем дисплей
    delay_us(40)
    sendByte(CLEAR_DISPLAY)  # очищаем дисплей
    delay_ms(2)
    sendByte(ENTRY_MODE_SET)  # ставим режим смещение курсора экран не смещается
    delay_us(40)
    sendByte(DISPLAY_ON)  # включаем дисплей и убираем курсор
    delay_us(40)


def sendStr(string: str, row: int):
    start_address = {1: 0x0, 2: 0x40, 3: 0x14, 4: 0x54}[row]

    # ставим курсор на начало нужной строки в DDRAM
    sendByte(start_address | SET_DDRAM_ADDRESS)

    delay_ms(4)

    for char in string:
        sendByte(ord(char), isData=True)


if __name__ == '__main__':
    lcdInit()

    sendStr("    HELLO, HABR", 1)
    sendStr("     powered by", 2)
    sendStr("Raspberry Pi Zero 2W", 3)
    sendStr("Nibiru", 4)
