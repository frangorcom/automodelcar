import time
import board
import busio
import adafruit_vl53l0x

# Inicializar I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Crear objeto sensor
vl53 = adafruit_vl53l0x.VL53L0X(i2c)

print("Sensor listo")

while True:
    distancia = vl53.range  # en mm
    print(f"Distancia: {distancia} mm")
    time.sleep(0.5)