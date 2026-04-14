import pigpio
import time
import sys
import termios
import tty

SERVO_PIN = 12

# Inicializar pigpio
pi = pigpio.pi()
if not pi.connected:
    print("Error: pigpio no está corriendo")
    exit()

# Función para convertir ángulo a ancho de pulso (µs)
def angle_to_pulse(angle):
    # 0° -> 500us, 180° -> 2500us (ajustable según servo)
    return 500 + (angle / 180.0) * 2000

# Leer una tecla sin enter
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

# Ángulo inicial
angle = 90
pi.set_servo_pulsewidth(SERVO_PIN, angle_to_pulse(angle))
print(f"Ángulo inicial: {angle}°")

print("\nControles:")
print("  a → -1 grado")
print("  d → +1 grado")
print("  q → salir\n")

try:
    while True:
        key = getch()

        if key == 'a':
            angle = max(0, angle - 1)
        elif key == 'd':
            angle = min(180, angle + 1)
        elif key == 'q':
            break

        pi.set_servo_pulsewidth(SERVO_PIN, angle_to_pulse(angle))
        print(f"\rÁngulo actual: {angle}°   ", end="")

except KeyboardInterrupt:
    pass

# Apagar servo
pi.set_servo_pulsewidth(SERVO_PIN, 0)
pi.stop()
print("\nPrograma terminado")