from machine import I2C, Pin
from sen5x.sen5x import SEN5x

ID = 0
SCL_PIN_NUM = 7
SDA_PIN_NUM = 6
FREQ = 50000  # see https://github.com/micropython/micropython/issues/7772
ADDRESS = 0x69

i2c = I2C(ID,
          scl=Pin(SCL_PIN_NUM, pull=Pin.PULL_UP),
          sda=Pin(SDA_PIN_NUM, pull=Pin.PULL_UP),
          freq=FREQ
          )
sen = SEN5x(i2c, address=ADDRESS)


def test_str_repr():
    print(repr(sen))
    print(str(sen))


def test_product_name():
    product_name = sen.product_name
    print('product_name:', product_name)
    assert product_name in ['SEN50', 'SEN54', 'SEN55']


def test_serial_number():
    serial_number = sen.serial_number
    print('serial_number:', serial_number)
    assert type(serial_number) == str
    assert len(serial_number) > 0


def test_firmware_version():
    firmware_version = sen.firmware_version
    print('firmware_version:', firmware_version)
    assert firmware_version == 1


def test_data_ready(ready: bool = True):
    """ asserts data_ready == ready arg """
    data_ready = sen.data_ready
    print('data_ready:', data_ready)
    assert data_ready is ready


def test_temperature_compensation_params():
    product_name = sen.product_name
    if product_name in ('SEN54', 'SEN55'):
        offset, slope, time_const = sen.temperature_compensation_params
        print('offset:', offset, 'slope:', slope, 'time_const:', time_const)
        for param in (offset, slope):
            assert type(param) is float
            assert param >= 0.0
        assert type(time_const) is int
        assert time_const >= 0
    else:
        print('temperature_compensation_params not supported')


def test_warm_start_param():
    param = sen.warm_start_param
    print('warm_start:', param)
    assert type(param) is int
    assert param >= 0


def test_voc_algorithm_tuning_params():
    product_name = sen.product_name
    if product_name in ('SEN54', 'SEN55'):
        params = sen.voc_algorithm_tuning_params
        _test_read_tuning_params(params)
    else:
        print('voc_algorithm_tuning_params not supported')


def test_nox_algorithm_tuning_params():
    product_name = sen.product_name
    if product_name == 'SEN55':
        params = sen.nox_algorithm_tuning_params
        _test_read_tuning_params(params)
    else:
        print('nox_algorithm_tuning_params not supported')


def _test_read_tuning_params(params):
    """ requires idle mode """
    index_offset, time_offset, time_gain, max_duration, std_initial, gain_factor = params
    print('index_offset:', index_offset,
          'time_offset:', time_offset,
          'time_gain:', time_gain)
    print('max_duration:', max_duration,
          'std_initial:', std_initial,
          'gain_factor:', gain_factor)
    for param in (index_offset, time_offset, time_gain,
                  max_duration, std_initial, gain_factor):
        assert type(param) is int
        assert param >= 0


def test_rht_acceleration_mode():
    mode = sen.rht_acceleration_mode
    print('mode:', mode)
    assert type(mode) is int
    assert mode in (0, 1, 2)


def test_voc_algorithm_state():
    product_name = sen.product_name
    if product_name in ('SEN54', 'SEN55'):
        state = sen.voc_algorithm_state
        print('state', state)
        assert type(state) is bytes
    else:
        print('voc_algorithm_state not supported')


def test_auto_cleaning_interval():
    interval = sen.auto_cleaning_interval
    print('interval', interval)
    assert type(interval) is int
    assert interval >= 0


def test_status():
    status = sen.status
    print('status:', status)
    assert type(status) is int


def test_fan_cleaning_active(active: bool = False):
    fan_cleaning_active = sen.fan_cleaning_active
    print('fan_cleaning_active', fan_cleaning_active)
    assert fan_cleaning_active is active


def test_check_i2c():
    print('checking i2c')
    sen.check_i2c()


def test_check_for_errors():
    print('checking for errors')
    sen.check_for_errors()


def test_reset():
    print('resetting')
    sen.reset()
    assert sen.data_ready is False


def test_start_measurement_no_checks():
    from time import sleep
    print('start measurement no checks')
    ready = sen.start_measurement(num_checks=0)
    assert ready is False
    sleep(1)  # give it a chance to start (takes ~800 ms)


def test_start_measurement():
    print('start measurement')
    ready = sen.start_measurement(num_checks=99)
    assert ready is True


def test_start_measurement_rht_gas_only():
    print('start measurement rht gas only')
    ready = sen.start_measurement_rht_gas_only_mode(num_checks=99)
    assert ready is True


def test_stop_measurement():
    print('stop measurement')
    sen.stop_measurement()


# noinspection DuplicatedCode
def test_measured_values_raw():
    ppm1_0, ppm2_5, ppm4_0, ppm10_0, rh, t, voc, nox = sen.measured_values_raw
    _print_measured_values(ppm1_0, ppm2_5, ppm4_0, ppm10_0, rh, t, voc, nox)

    for value in (ppm1_0, ppm2_5, ppm4_0, ppm10_0):
        assert type(value) is float

    product_name = sen.product_name
    if product_name == 'SEN50':
        for value in (rh, t, voc, nox):
            assert value is None
    elif product_name == 'SEN54':
        for value in (rh, t, voc):
            assert type(value) is float
        assert nox is None
    elif product_name == 'SEN55':
        for value in (rh, t, voc, nox):
            assert type(value) is float
    else:
        raise Exception('Invalid product name')


def test_measured_values_not_started():
    ppm1_0, ppm2_5, ppm4_0, ppm10_0, rh, t, voc, nox = sen.measured_values
    _print_measured_values(ppm1_0, ppm2_5, ppm4_0, ppm10_0, rh, t, voc, nox)
    for value in (ppm1_0, ppm2_5, ppm4_0, ppm10_0, rh, t, voc, nox):
        assert value is None


# noinspection DuplicatedCode
def test_measured_values():
    ppm1_0, ppm2_5, ppm4_0, ppm10_0, rh, t, voc, nox = sen.measured_values
    _print_measured_values(ppm1_0, ppm2_5, ppm4_0, ppm10_0, rh, t, voc, nox)

    for value in (ppm1_0, ppm2_5, ppm4_0, ppm10_0):
        assert type(value) is int

    product_name = sen.product_name
    if product_name == 'SEN50':
        for value in (rh, t, voc, nox):
            assert value is None
    elif product_name == 'SEN54':
        for value in (rh, voc):
            assert type(value) is int
        for value in (t,):
            assert type(value) is float
        for value in (nox,):
            assert value is None
    elif product_name == 'SEN55':
        for value in (rh, voc, nox):
            assert type(value) is int
        for value in (t,):
            assert type(value) is float
    else:
        raise Exception('Invalid product name')


# noinspection DuplicatedCode
def test_measured_values_imperial():
    ppm1_0, ppm2_5, ppm4_0, ppm10_0, rh, t, voc, nox = sen.measured_values_imperial
    _print_measured_values(ppm1_0, ppm2_5, ppm4_0, ppm10_0, rh, t, voc, nox)

    for value in (ppm1_0, ppm2_5, ppm4_0, ppm10_0):
        assert type(value) is int

    product_name = sen.product_name
    if product_name == 'SEN50':
        for value in (rh, t, voc, nox):
            assert value is None
    elif product_name == 'SEN54':
        for value in (rh, t, voc):
            assert type(value) is int
        for value in (nox,):
            assert value is None
    elif product_name == 'SEN55':
        for value in (rh, t, voc, nox):
            assert type(value) is int
    else:
        raise Exception('Invalid product name')


def _print_measured_values(ppm1_0, ppm2_5, ppm4_0, ppm10_0, rh, t, voc, nox):
    print('ppm1_0:', ppm1_0,
          'ppm2_5:', ppm2_5,
          'ppm4_0:', ppm4_0,
          'ppm10_0:', ppm10_0)
    print('rh:', rh,
          't:', t,
          'voc:', voc,
          'nox:', nox)


def test_start_fan_cleaning():
    """ requires measurement mode """
    from time import sleep
    print('start fan cleaning')
    assert sen.fan_cleaning_active is False
    sen.start_fan_cleaning()
    assert sen.fan_cleaning_active is True
    sleep(14)  # fan cleans for 10 seconds per datasheet, needs 14 here
    assert sen.fan_cleaning_active is False


def test_clear_status():
    print('clear status')
    sen.clear_status()


def test_set_temperature_compensation_params():
    set_offset = 10.0
    set_slope = 0.002
    set_time_const = 30
    print(f'set temp compensation params to {set_offset} {set_slope} {set_time_const}')
    sen.temperature_compensation_params = (set_offset, set_slope, set_time_const)
    new_offset, new_slope, new_time_const = sen.temperature_compensation_params
    assert new_offset == set_offset
    assert new_slope == set_slope
    assert new_time_const == set_time_const


def test_set_warm_start_param():
    set_param = 50000
    print(f'set warm start param to {set_param}')
    sen.warm_start_param = set_param
    new_param = sen.warm_start_param
    assert new_param == set_param


# noinspection DuplicatedCode
def test_set_voc_algorithm_tuning_params():
    """ requires idle mode """
    product_name = sen.product_name
    if product_name in ('SEN54', 'SEN55'):
        set_index_offset: int = 50
        set_time_offset: int = 24
        set_time_gain: int = 24
        set_max_duration: int = 200
        set_std_initial: int = 100
        set_gain_factor: int = 260
        print(f'set voc alog params to {set_index_offset}, {set_time_offset}, {set_time_gain}')
        print(f'and to {set_max_duration}, {set_std_initial}, {set_gain_factor}')
        sen.voc_algorithm_tuning_params = (
            set_index_offset,
            set_time_offset,
            set_time_gain,
            set_max_duration,
            set_std_initial,
            set_gain_factor
        )
        new_index_offset, new_time_offset, new_time_gain, new_max_duration, new_std_initial, new_gain_factor = sen.voc_algorithm_tuning_params

        assert new_index_offset == set_index_offset
        assert new_time_offset == set_time_offset
        assert new_time_gain == set_time_gain
        assert new_max_duration == set_max_duration
        assert new_std_initial == set_std_initial
        assert new_gain_factor == set_gain_factor
    else:
        print('voc_algorithm_tuning_params not supported')


# noinspection DuplicatedCode
def test_set_nox_algorithm_tuning_params():
    """ requires idle mode """
    product_name = sen.product_name
    if product_name == 'SEN55':
        set_index_offset: int = 50
        set_time_offset: int = 24
        set_time_gain: int = 12  # cannot change
        set_max_duration: int = 1000
        set_std_initial: int = 50  # cannot change
        set_gain_factor: int = 250
        print(f'set nox alog params to {set_index_offset}, {set_time_offset}, {set_time_gain}')
        print(f'and to {set_max_duration}, {set_std_initial}, {set_gain_factor}')
        sen.voc_algorithm_tuning_params = (
            set_index_offset,
            set_time_offset,
            set_time_gain,
            set_max_duration,
            set_std_initial,
            set_gain_factor
        )
        new_index_offset, new_time_offset, new_time_gain, new_max_duration, new_std_initial, new_gain_factor = sen.voc_algorithm_tuning_params

        assert new_index_offset == set_index_offset
        assert new_time_offset == set_time_offset
        assert new_time_gain == set_time_gain
        assert new_max_duration == set_max_duration
        assert new_std_initial == set_std_initial
        assert new_gain_factor == set_gain_factor
    else:
        print('nox_algorithm_tuning_params not supported')


def test_set_rht_acceleration_mode():
    product_name = sen.product_name
    if product_name in ('SEN54', 'SEN55'):
        set_mode = 1
        print(f'set rht accel param to {set_mode}')
        sen.rht_acceleration_mode = set_mode
        new_mode = sen.rht_acceleration_mode
        assert set_mode == new_mode
    else:
        print('rht_acceleration_mode not supported')


def test_set_voc_algorithm_state():
    product_name = sen.product_name
    if product_name in ('SEN54', 'SEN55'):
        set_state = b'\x00\x00\x00\x00\x003\x00\x00'
        print(f'set voc alog state to {set_state}')
        sen.voc_algorithm_state = set_state
        new_state = sen.voc_algorithm_state
        assert set_state == new_state
    else:
        print('voc_algorithm_state not supported')


def test_set_auto_cleaning_interval():
    set_interval = 604800 * 2  # 2 weeks
    print(f'set auto cleaning interval to {set_interval}')
    sen.auto_cleaning_interval = set_interval
    new_interval = sen.auto_cleaning_interval
    assert new_interval == set_interval


def test_backup_restore_voc_algorithm_state():
    product_name = sen.product_name
    if product_name in ('SEN54', 'SEN55'):
        sen.purge_backup_voc_algorithm_state()
        try:
            sen.restore_voc_algorithm_state()
        except OSError:
            pass
        save_state = b'\x00\x00\x00\x00\x004\x00\x00'
        print(f'saving voc_algorithm_state {save_state}')
        sen.voc_algorithm_state = save_state
        sen.backup_voc_algorithm_state()
        temp_state = b'\x00\x00\x00\x00\x005\x00\x00'
        sen.voc_algorithm_state = temp_state
        assert sen.voc_algorithm_state == temp_state
        sen.restore_voc_algorithm_state()
        assert sen.voc_algorithm_state == save_state
    else:
        print('voc_algorithm_state not supported')


def test_with():
    print('start with')
    with SEN5x(i2c, address=ADDRESS) as sen5x:
        assert sen5x.data_ready
    assert sen5x.data_ready is False


# noinspection PyStatementEffect
def test_invalid_mode():
    print('invalid mode test')
    sen.reset()
    try:
        sen.start_fan_cleaning()
    except SEN5x.InvalidMode:
        pass
    sen.start_measurement()
    try:
        sen.voc_algorithm_tuning_params
    except SEN5x.InvalidMode:
        pass
    try:
        sen.nox_algorithm_tuning_params
    except SEN5x.InvalidMode:
        pass
    test_stop_measurement()


# noinspection PyUnusedLocal
def test_value_error():
    print('value error test')
    try:
        sen.temperature_compensation_params = (0, -5, 0)
    except ValueError:
        pass
    try:
        sen.warm_start_param = -1
    except ValueError:
        pass
    try:
        sen.voc_algorithm_tuning_params = (0, 0, 0, 0, 0, 0)
    except ValueError:
        pass
    try:
        sen.nox_algorithm_tuning_params = (0, 0, 0, 0, 0, 0)
    except ValueError:
        pass
    try:
        sen.rht_acceleration_mode = 3
    except ValueError:
        pass
    try:
        sen.voc_algorithm_state = bytes(9)
    except ValueError:
        pass


def run_read_tests():
    test_reset()
    test_check_i2c()
    test_check_for_errors()
    test_product_name()
    test_serial_number()
    test_str_repr()
    test_firmware_version()
    test_temperature_compensation_params()
    test_warm_start_param()
    test_voc_algorithm_tuning_params()
    test_nox_algorithm_tuning_params()
    test_rht_acceleration_mode()
    test_voc_algorithm_state()
    test_auto_cleaning_interval()
    test_status()
    test_fan_cleaning_active(active=False)


def run_start_stop_tests():
    test_reset()
    test_data_ready(ready=False)

    test_start_measurement_rht_gas_only()
    test_data_ready(ready=True)
    test_stop_measurement()

    test_start_measurement_no_checks()
    test_data_ready(ready=True)
    test_stop_measurement()

    test_start_measurement()
    test_data_ready(ready=True)
    test_stop_measurement()
    test_data_ready(ready=False)


def run_measurement_tests():
    test_reset()
    test_data_ready(ready=False)  # used in test_start/stop
    test_measured_values_not_started()

    test_start_measurement()
    test_measured_values()
    test_measured_values_imperial()
    test_measured_values_raw()
    test_stop_measurement()


def run_set_tests():
    test_reset()

    # start not required
    test_clear_status()
    test_set_temperature_compensation_params()
    test_set_warm_start_param()
    test_set_voc_algorithm_tuning_params()
    test_set_nox_algorithm_tuning_params()  # not tested
    test_set_rht_acceleration_mode()
    test_set_voc_algorithm_state()
    test_set_auto_cleaning_interval()
    test_backup_restore_voc_algorithm_state()

    # start required
    test_start_measurement()
    test_start_fan_cleaning()
    test_stop_measurement()


def run_exception_tests():
    test_invalid_mode()
    test_value_error()


def run_all_tests():
    run_read_tests()
    run_start_stop_tests()
    run_measurement_tests()
    run_set_tests()
    run_exception_tests()


def run_forever():
    import gc
    from time import sleep, localtime
    from micropython import mem_info
    sen.start_measurement()
    gc.collect()
    mem_info(1)
    sleep(10)
    while True:
        try:
            print(localtime(), sen.measured_values)
            mem_info()
            print(60 * '-')
            sleep(1.1)
        except KeyboardInterrupt:
            print('Done')
            break
    gc.collect()
    mem_info(1)


def sizeit():  # to check memory
    from micropython import mem_info
    import gc
    gc.collect()
    mem_info(1)
