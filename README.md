Sensirion SEN5x Micropython Driver
=================================
Provides access from ESP32-C3 to all Sensirion SEN5x capability via I2C.

## Built With
Tested with the following; "should" work with similar setups.
- [ESP32-C3-DevKitM-1](https://docs.espressif.com/projects/esp-idf/en/v4.4.1/esp32c3/hw-reference/esp32c3/user-guide-devkitm-1.html)
- [Sensirion SEN54](https://sensirion.com/products/catalog/SEN54/)
- [Micropython 1.18](https://micropython.org/download/esp32c3/)

## Sample Usage
```python
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
```
### Code Samples

- [examples/main.py](example/main.py)
- [tests/main.py](test/main.py)

## Getting Started

1. [Setup ESP32](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html)
2. Wire ESP32-C3-DevKitM-1 to Sensirion SEN5x following Wiring comment in examples/main.py
3. Configure SCL_PIN_NUM, SDA_PIN_NUM in examples/main.py
4. Copy files to ESP32 root directory
   - examples/main.py -> /pyboard/main.py
   - sen5x/sen5x.py -> /pyboard/lib/sen5x/sen5x.py
   - tools/tools.py -> /pyboard/lib/tools/tools.py
5. Start REPL
6. Boot ESP32

I found [rshell](https://github.com/dhylands/rshell) to be useful. 

## Documentation

Refer to [Sensirion SEN5x Datasheet](https://sensirion.com/products/catalog/SEN54/) for property, method & argument details. 
### SEN5x properties
| Property                        | Has<br/>Setter? | Type(s)                                                                                                                                                                                 |
|---------------------------------|-----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| product_name                    | no              | str                                                                                                                                                                                     |
| serial_number                   | no              | str                                                                                                                                                                                     |
| firmware_version                | no              | int                                                                                                                                                                                     |
| data_ready                      | no              | bool                                                                                                                                                                                    |
| measured_values                 | no              | tuple<br/>- ppm 1.0: int<br>- ppm 2.5: int<br>- ppm 4.0: int<br>- ppm 10.0: int<br>- temperature **°C**: float<br>- humidity: int<br>- voc index: int<br>- nox index: int               |
| measured_values_imperial        | no              | tuple<br/>- ppm 1.0: int<br>- ppm 2.5: int<br>- ppm 4.0: int<br>- ppm 10.0: int<br>- temperature**°F**: int<br>- humidity: int<br>- voc index: int<br>- nox index: int                  |
| measured_values_raw             | no              | tuple<br/>- ppm 1.0: float<br/>- ppm 2.5: float<br/>- ppm 4.0: float<br/>- ppm 10.0: float<br/>- temperature: float<br/>- humidity: float<br/>- voc index: float<br/>- nox index: float |
| temperature_compensation_params | yes             | tuple<br/>- offset: float<br/>- slope: float<br/>- time const: int                                                                                                                      |
| warm_start_param                | yes             | int                                                                                                                                                                                     |
| voc_algorithm_tuning_params     | yes             | tuple<br/>- index offset: int<br/>- time offset: int<br/>- time gain: int<br/>- max duration: int<br/>- std initial: int<br/>- gain factor: int                                         |
| nox_algorithm_tuning_params     | yes             | tuple<br/>- index offset: int<br/>- time offset: int<br/>- time gain: int<br/>- max duration: int<br/>- std initial: int<br/>- gain factor: int                                         |
| rht_acceleration_mode           | yes             | int                                                                                                                                                                                     |
| voc_algorithm_state             | yes             | bytes(8)                                                                                                                                                                                |
| auto_cleaning_interval          | yes             | int                                                                                                                                                                                     |
| status                          | no              | int                                                                                                                                                                                     |                                                                                                                                                                                    |                                                                                                                                                                                    |
| fan_cleaning_active             | no              | bool                                                                                                                                                                                    |

### SEN5x methods
| Method                                | Args                 | Return                              |
|---------------------------------------|----------------------|-------------------------------------|
| start()                               | None                 | None                                |
| stop()                                | None                 | None                                |
| start_measurement()                   | num checks: int = 100 | ready: bool                         |
| start_measurement_rht_gas_only_mode() | num checks: int = 100 | ready: bool                         |
| stop_measurement()                    | None                 | None                                |
| backup_voc_algorithm_state()          | None                 | None                                |
| restore_voc_algorithm_state()         | None                 | None                                |
| purge_backup_voc_algorithm_state()    | None                 | None                                |
| start_fan_cleaning()                  | None                 | None                                |
| check_i2c()                           | None                 | None<br/>Raises SEN5x.NotFoundError |
| check_for_errors()                    | None                 | None<br/>Raises SEN5x.StatusError   |
| clear_status()                        | None                 | None                                |
| reset()                               | None                 | None                                |

##License
This project is released under the MIT License.
