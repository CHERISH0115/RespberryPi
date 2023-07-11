import time
import smbus
import sys
import socket
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
if __name__ == '__main__':
    my1602 = My1602()
    def get_ip_address():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
            s.close()
            return ip_address
        except:
            return "Error: Unable to get IP address"
    while True:
        # 显示当前时间
        current_time = time.strftime("%H:%M:%S")
        my1602.print_lcd(0, 0, "Time: " + current_time)
        # 显示IP地址
        ip_address = get_ip_address()
        my1602.print_lcd(0, 1, "IP: " + ip_address)
        time.sleep(1)
