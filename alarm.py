import time
import RPi.GPIO as GPIO
import smbus
class My1602(object):
    BUS = smbus.SMBus(1)
    LCD_ADDR = 0x27
    BLEN = 1
    
    def turn_light(self, key):
        self.BLEN = key
        if key == 1:
            self.BUS.write_byte(self.LCD_ADDR, 0x08)
        else:
            self.BUS.write_byte(self.LCD_ADDR, 0x00)
    
    def write_word(self, addr, data):
        temp = data
        if self.BLEN == 1:
            temp |= 0x08
        else:
            temp &= 0xF7
        self.BUS.write_byte(addr, temp)
    
    def send_command(self, comm):
        buf = comm & 0xF0
        buf |= 0x04
        self.write_word(self.LCD_ADDR, buf)
        time.sleep(0.002)
        buf &= 0xFB
        self.write_word(self.LCD_ADDR, buf)
        buf = (comm & 0x0F) << 4
        buf |= 0x04
        self.write_word(self.LCD_ADDR, buf)
        time.sleep(0.002)
        buf &= 0xFB
        self.write_word(self.LCD_ADDR, buf)
    
    def send_data(self, data):
        buf = data & 0xF0
        buf |= 0x05
        self.write_word(self.LCD_ADDR, buf)
        time.sleep(0.002)
        buf &= 0xFB
        self.write_word(self.LCD_ADDR, buf)
        buf = (data & 0x0F) << 4
        buf |= 0x05
        self.write_word(self.LCD_ADDR, buf)
        time.sleep(0.002)
        buf &= 0xFB
        self.write_word(self.LCD_ADDR, buf)
    
    def __init__(self):
        try:
            self.send_command(0x33)
            time.sleep(0.005)
            self.send_command(0x32)
            time.sleep(0.005)
            self.send_command(0x28)
            time.sleep(0.005)
            self.send_command(0x0C)
            time.sleep(0.005)
            self.send_command(0x01)
            self.BUS.write_byte(self.LCD_ADDR, 0x08)
        except:
            return None
        else:
            return None
    
    def clear_lcd(self):
        self.send_command(0x01)
    
    def print_lcd(self, x, y, str):
        if x < 0:
            x = 0
        if x > 15:
            x = 15
        if y < 0:
            y = 0
        if y > 1:
            y = 1
        addr = 0x80 + 0x40 * y + x
        self.send_command(addr)
        for chr in str:
            self.send_data(ord(chr))
class HC_SR04(object):
    def __init__(self, trig_pin, echo_pin):
        self.TRIG_PIN = trig_pin
        self.ECHO_PIN = echo_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.TRIG_PIN, GPIO.OUT)
        GPIO.setup(self.ECHO_PIN, GPIO.IN)
    
    def measure_distance(self):
        GPIO.output(self.TRIG_PIN, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.TRIG_PIN, GPIO.LOW)
        while GPIO.input(self.ECHO_PIN) == GPIO.LOW:
            pass
        start_time = time.time()
        while GPIO.input(self.ECHO_PIN) == GPIO.HIGH:
            pass
        end_time = time.time()
        distance = (end_time - start_time) * 34300 / 2
        return distance
class Buzzer(object):
    def __init__(self, pin):
        self.PIN = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PIN, GPIO.OUT)
    
    def buzz(self, duration):
        GPIO.output(self.PIN, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(self.PIN, GPIO.LOW)
if __name__ == '__main__':
    try:
        lcd = My1602()
        hc_sr04 = HC_SR04(11, 13)
        buzzer = Buzzer(16)  # 设置蜂鸣器的GPIO引脚
        
        # 设置阈值
        threshold = float(input("请输入距离阈值（单位：cm）："))
        
        while True:
            distance = hc_sr04.measure_distance()
            lcd.clear_lcd()
            lcd.print_lcd(0, 0, 'Distance:')
            lcd.print_lcd(0, 1, '{:.2f} cm'.format(distance))
            
            # 在命令行终端上打印距离结果
            print('Distance: {:.2f} cm'.format(distance))
            
            # 判断距离是否小于阈值，如果是则使蜂鸣器响
            if distance < threshold:
                buzzer.buzz(0.1)  # 蜂鸣器响0.5秒
            
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        lcd.clear_lcd()
        lcd.print_lcd(0, 0, 'Program Stopped')
        GPIO.cleanup()
