from machine import I2C, Pin
from sen5x.sen5x import SEN5x

"""
    Wiring:
        ESP32 Pin 7 ------- SEN5x SCL (internal or external pull-up to 3V3)
        ESP32 Pin 6 ------- SEN5x SDA (internal or external pull-up to 3V3)
        ESP32 5V    ------- SEN5x 5V
        ESP32 GND   ------- SEN5x GND
        ESP32 GND   ------- SEN5x SEL       
"""
ID = 0
SCL_PIN_NUM = 7
SDA_PIN_NUM = 6
FREQ = 50000  # see https://github.com/micropython/micropython/issues/7772

def main():
    i2c = I2C(ID,
              scl=Pin(SCL_PIN_NUM, pull=Pin.PULL_UP),  # internal pull-up
              sda=Pin(SDA_PIN_NUM, pull=Pin.PULL_UP),  # internal pull-up
              freq=FREQ)

    with SEN5x(i2c) as sen:
        print('Product Name:', sen.product_name)
        print('Serial Number:', sen.serial_number)
        print('Data Ready:', sen.data_ready)
        ppm1_0, ppm2_5, ppm4_0, ppm10_0, rh, t, voc, nox = sen.measured_values
        print('PPM 1.0:', ppm1_0, 'PPM 2.5:', ppm2_5, 'PPM 4.0:', ppm4_0, 'PPM 10.0:', ppm10_0)
        print('Humidity:', rh, 'Temp:', t, 'VOC:', voc, 'NOx:', nox)


if __name__ == '__main__':
    main()
