# RespberryPi

# LCD1602a采用I2c，所以接线按照对应位置（SDA,SCL,以及vcc，gnd）
# 在alarm.py以及distance.py中，
HC-SR04超声波模块的接线位置：
trig端接GPIO11(即#23)
echo端接GPIO13(即#33)
vcc选5v，gnd任选
# time-ip.py配合wifi.sh以及lcd1602_startup.sh可以实现在开机时在屏幕上显示当前时间和IP地址（基于树莓派本地）
使用nmcli device wifi list命令可以列举wifi（要先开启NetworkManager服务，命令为sudo service NetworkManager start，在wifi.sh中已配置好）
使用 nmcli device wifi connect ******** password ********来连接wifi
开机会自启动time-ip.py，会影响之后程序运行，可以通过ps -ef | grep py来找到该进程，再通过sudo kill <PID>来结束运行

如果有不周到的地方请大家及时指正！
