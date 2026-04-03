import smbus2
import time

# Dirección del MPU6050
MPU_ADDR = 0x68

# Registros importantes
PWR_MGMT_1 = 0x6B
ACCEL_XOUT = 0x3B
GYRO_XOUT = 0x43

# Inicializar I2C
bus = smbus2.SMBus(1)

# Despertar el MPU6050
bus.write_byte_data(MPU_ADDR, PWR_MGMT_1, 0)

# Leer 2 bytes y convertir a entero con signo
def read_word(reg):
    high = bus.read_byte_data(MPU_ADDR, reg)
    low = bus.read_byte_data(MPU_ADDR, reg + 1)
    value = (high << 8) + low
    if value >= 0x8000:
        value = -((65535 - value) + 1)
    return value

# Leer acelerómetro
def read_accel():
    ax = read_word(ACCEL_XOUT)
    ay = read_word(ACCEL_XOUT + 2)
    az = read_word(ACCEL_XOUT + 4)
    return ax, ay, az

# Leer giroscopio
def read_gyro():
    gx = read_word(GYRO_XOUT)
    gy = read_word(GYRO_XOUT + 2)
    gz = read_word(GYRO_XOUT + 4)
    return gx, gy, gz

# Loop principal
while True:
    ax, ay, az = read_accel()
    gx, gy, gz = read_gyro()

    # Convertir a unidades reales
    ax_g = ax / 16384.0
    ay_g = ay / 16384.0
    az_g = az / 16384.0

    gx_dps = gx / 131.0
    gy_dps = gy / 131.0
    gz_dps = gz / 131.0

    print("Aceleración (g): X={:.2f} Y={:.2f} Z={:.2f}".format(ax_g, ay_g, az_g))
    print("Giroscopio (°/s): X={:.2f} Y={:.2f} Z={:.2f}".format(gx_dps, gy_dps, gz_dps))
    print("------")

    time.sleep(0.5)