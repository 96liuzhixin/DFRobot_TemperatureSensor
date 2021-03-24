# -*- coding:utf-8 -*-
"""
  @file get_temperature.py
  @brief ��ͨ��ȡ�¶ȵ�����
  @n ʵ�������¶��ڴ�����ʾ�������¶��滷���¶ȸı���ı�
  @n i2c ��ַѡ��Ĭ��i2c��ַΪ0x1F��A2��A1��A0����Ϊ�ߵ�ƽ��
  @n ��8�����Ϊ,1����ߵ�ƽ��0����͵�ƽ
                | A2 | A1 | A0 |
                | 0  | 0  | 0  |    0x18
                | 0  | 0  | 1  |    0x19
                | 0  | 1  | 0  |    0x1A
                | 0  | 1  | 1  |    0x1B
                | 1  | 0  | 0  |    0x1D
                | 1  | 0  | 1  |    0x1D
                | 1  | 1  | 0  |    0x1E
                | 1  | 1  | 1  |    0x1F   default i2c address
                
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @licence     The MIT License (MIT)
  @author      [ZhixinLiu](zhixin.liu@dfrobot.com)
  @version  V0.1
  @date  2021-03-23
  @get from https://www.dfrobot.com
  @url https://github.com/DFRobot/DFRobot_TemperatureSensor
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from DFRobot_TemperatureSensor import *

I2C_1       = 0x01               # I2C_1 ʹ��i2c1�ӿ������������� ���Ե���Ϊi2c0������Ҫ������ݮ�ɵ��ļ�
I2C_ADDRESS = 0x1F               # I2C �豸�ĵ�ַ�����Ը���A2��A1��A0��������ַ��Ĭ�ϵ�ַΪ0x1F
tmp = DFRobot_TemperatureSensor_I2C(I2C_1 ,I2C_ADDRESS)

def setup():
  while ERROR == tmp.sensor_init():
    print "sensor init error ,please check connect or device id or manufacturer id error"
  print "sensor init success"
  '''
    �����¶ȴ������ķֱ��ʣ���ͬ�ķֱ��ʣ���ȡ���¶ȵľ��Ȳ�ͬ
    resolution
            RESOLUTION_0_5     // ��ȡ�¶ȵ�С������Ϊ0.5�ı���     ��0.5�� ��1.0�桢1.5��
            RESOLUTION_0_25    // ��ȡ�¶ȵ�С������Ϊ0.25�ı���    ��0.25�桢0.50�桢0.75��
            RESOLUTION_0_125   // ��ȡ�¶ȵ�С������Ϊ0.125�ı���   ��0.125�桢0.250�桢0.375��
            RESOLUTION_0_0625  // ��ȡ�¶ȵ�С������Ϊ0.0625�ı���  ��0.0625�桢0.1250�桢0.1875��
  '''
  if 0 == tmp.set_resolution(RESOLUTION_0_25):
    print "Resolution set successfully"
  else:
    print "parameter error"

  '''
    ���õ�Դģʽ���ϵ�ģʽ����ģʽ�£������������ʼĴ������ܹ��õ��������¶ȣ�
                  �͹���ģʽ���¶Ȳ���ֹͣ�����Զ�ȡ��д��Ĵ������������߻��ʹ�ĵ�����
      POWER_UP_MODE         // �ϵ�ģʽ
      LOW_POWER_MODE        // �͹���ģʽ
  '''
  if 0 == tmp.set_power_mode(POWER_UP_MODE):
    print "Power mode was set successfully"
  else:
    print "Register lock"
  
def loop():
  temperature = tmp.get_temperature()
  print "temperature = %.2f .C"%temperature
  print ""
  time.sleep(1)

if __name__ == "__main__":
  setup()
  while True:
    loop()