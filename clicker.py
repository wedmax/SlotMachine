import serial
import time
import sys

# Автоматический поиск порта Arduino
def find_arduino_port():
    import serial.tools.list_ports
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        # Ищем по ключевым словам в описании устройства
        if "CH340" in p.description or "Arduino" in p.description or "USB-SERIAL" in p.description:
            return p.device
    # Если автопоиск не сработал, берем первый попавшийся COM-порт
    if ports:
        return ports[0].device
    return None

# Динамический импорт библиотеки для кликов в зависимости от ОС
try:
    import keyboard
    mode = "keyboard"
except ImportError:
    # На Mac Mini без прав администратора keyboard может не встать, используем pynput как запасной
    try:
        from pynput.keyboard import Key, Controller
        keyboard_controller = Controller()
        mode = "pynput"
    except ImportError:
        print("Ошибка: Установите библиотеку клавиатуры командой: pip install keyboard pynput")
        sys.exit(1)

port = find_arduino_port()
if not port:
    print("Ошибка: Arduino не найдена! Проверьте USB-кабель.")
    sys.exit(1)

print(f"Подключаемся к Arduino на порту: {port}...")
BAUD_RATE = 9600

try:
    ser = serial.Serial(port, BAUD_RATE, timeout=0.1)
    print("Готово! Скрипт активен. Нажмите физическую кнопку для отправки Пробела.")
    
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if "HIT" in line:
                print("Физическое нажатие! Эмулируем Пробел...")
                if mode == "keyboard":
                    keyboard.press_and_release('space')
                else:
                    keyboard_controller.press(Key.space)
                    keyboard_controller.release(Key.space)
        time.sleep(0.01)

except serial.SerialException:
    print("Связь с платой потеряна.")
except KeyboardInterrupt:
    print("\nСкрипт остановлен.")