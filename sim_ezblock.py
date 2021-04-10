import time
import math

timer = [
    {
        "arr": 0
    }
] * 4

class Servo():
    MAX_PW = 2500
    MIN_PW = 500
    _freq = 50
    def __init__(self, pwm):
        pass
#        super().__init__()
#        self.pwm = pwm
#        self.pwm.period(4095)
#        prescaler = int(float(self.pwm.CLOCK) /self.pwm._freq/self.pwm.period())
#        self.pwm.prescaler(prescaler)
        # self.angle(90)

    # angle ranges -90 to 90 degrees
    def angle(self, angle):
        pass
#        if not (isinstance(angle, int) or isinstance(angle, float)):
#            raise ValueError("Angle value should be int or float value, not %s"%type(angle))
#        if angle < -90:
#            angle = -90
#        if angle > 90:
#            angle = 90
#        High_level_time = self.map(angle, -90, 90, self.MIN_PW, self.MAX_PW)
#        self._debug("High_level_time: %f" % High_level_time)
#        pwr =  High_level_time / 20000
#        self._debug("pulse width rate: %f" % pwr)
#        value = int(pwr*self.pwm.period())
#        self._debug("pulse width value: %d" % value)
#        self.pwm.pulse_width(value)

class PWM():
    REG_CHN = 0x20
    REG_FRE = 0x30
    REG_PSC = 0x40
    REG_ARR = 0x44

    ADDR = 0x14

    CLOCK = 72000000

    def __init__(self, channel, debug="critical"):
        if isinstance(channel, str):
            if channel.startswith("P"):
                channel = int(channel[1:])
            else:
                raise ValueError("PWM channel should be between [P1, P14], not {0}".format(channel))

        self.channel = channel
        self.timer = int(channel/4)
        pass

    def i2c_write(self, reg, value):
        pass

    def freq(self, *freq):
        if len(freq) == 0:
            return 50
        else:
            pass

    def prescaler(self, *prescaler):
        if len(prescaler) == 0:
            return 0
        else:
            pass

    def period(self, *arr):
        global timer
        if len(arr) == 0:
            return timer[self.timer]["arr"]
        else:
            pass

    def pulse_width(self, *pulse_width):
        if len(pulse_width) == 0:
            return 0
        else:
            pass

    def pulse_width_percent(self, *pulse_width_percent):
        global timer
        if len(pulse_width_percent) == 0:
            return 0
        else:
            pass

class Pin():

    _dict = {
        "BOARD_TYPE": 12,
    }

    _dict_1 = {
        "D0":  17,
        "D1":  18,
        "D2":  27,
        "D3":  22,
        "D4":  23,
        "D5":  24,
        "D6":  25,
        "D7":  4,
        "D8":  5,
        "D9":  6,
        "D10": 12,
        "D11": 13,
        "D12": 19,
        "D13": 16,
        "D14": 26,
        "D15": 20,
        "D16": 21,
        "SW":  19,
        "LED": 26,
        "BOARD_TYPE": 12,
        "RST": 16,
        "BLEINT": 13,
        "BLERST": 20,
        "MCURST": 21,
    }

    _dict_2 = {
        "D0":  17,
        "D1":   4, # Changed
        "D2":  27,
        "D3":  22,
        "D4":  23,
        "D5":  24,
        "D6":  25, # Removed
        "D7":   4, # Removed
        "D8":   5, # Removed
        "D9":   6,
        "D10": 12,
        "D11": 13,
        "D12": 19,
        "D13": 16,
        "D14": 26,
        "D15": 20,
        "D16": 21,
        "SW":  25, # Changed
        "LED": 26,
        "BOARD_TYPE": 12,
        "RST": 16,
        "BLEINT": 13,
        "BLERST": 20,
        "MCURST":  5, # Changed
    }

    def __init__(self, *value):
        pass
        
    def check_board_type(self):
        pass

    def init(self, mode, pull=None):
        pass

    def dict(self, *_dict):
        if len(_dict) == 0:
            return self._dict
        else:
            pass

    def __call__(self, value):
        return self.value(value)

    def value(self, *value):
        if len(value) == 0:
            return 'done'
        else:
            return value

    def on(self):
        return self.value(1)

    def off(self):
        return self.value(0)

    def high(self):
        return self.on()

    def low(self):
        return self.off()

    def mode(self, *value):
        if len(value) == 0:
            return (self._mode, self._pull)
        else:
            pass

    def pull(self, *value):
        return self._pull

    def irq(self, handler=None, trigger=None, bouncetime=200):
        pass
    def name(self):
        return "GPIO"

    def names(self):
        return ['0', '1']

    class cpu(object):
        GPIO17 = 17
        GPIO18 = 18
        GPIO27 = 27
        GPIO22 = 22
        GPIO23 = 23
        GPIO24 = 24
        GPIO25 = 25
        GPIO26 = 26
        GPIO4  = 4
        GPIO5  = 5
        GPIO6  = 6
        GPIO12 = 12
        GPIO13 = 13
        GPIO19 = 19
        GPIO16 = 16
        GPIO26 = 26
        GPIO20 = 20
        GPIO21 = 21

        def __init__(self):
            pass

class ADC():
    ADDR=0x14                   # 扩展板的地址为0x14

    def __init__(self, chn):
        if isinstance(chn, str):
            if chn.startswith("A"):     # 判断穿境来的参数是否为A开头，如果是，取A后面的数字出来
                chn = int(chn[1:])
            else:
                raise ValueError("ADC channel should be between [A0, A7], not {0}".format(chn))
        if chn < 0 or chn > 7:          # 判断取出来的数字是否在0~7的范围内
            self._error('Incorrect channel range')
        chn = 7 - chn
        self.chn = chn | 0x10           # 给从机地址
        self.reg = 0x40 + self.chn
        # self.bus = smbus.SMBus(1)
        
    def read(self):
        return 0

    def read_voltage(self):                             # 将读取的数据转化为电压值（0~3.3V）
        return 0*3.3/4095

