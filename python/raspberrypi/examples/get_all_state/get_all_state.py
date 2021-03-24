# -*- coding:utf-8 -*-
"""
  @file get_all_state.py
  @brief ��ȡ��������״̬������
  @n ʵ���������õ�״̬��ӡ���ն�
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
    ��ȡ�¶ȴ������ķֱ��� ,��ͬ�ķֱ��ʣ���ȡ���¶ȵľ��Ȳ�ͬ
    resolution
            RESOLUTION_0_5     // ��ȡ�¶ȵ�С������Ϊ0.5�ı���     ��0.5�� ��1.0�桢1.5��
            RESOLUTION_0_25    // ��ȡ�¶ȵ�С������Ϊ0.25�ı���    ��0.25�桢0.50�桢0.75��
            RESOLUTION_0_125   // ��ȡ�¶ȵ�С������Ϊ0.125�ı���   ��0.125�桢0.250�桢0.375��
            RESOLUTION_0_0625  // ��ȡ�¶ȵ�С������Ϊ0.0625�ı���  ��0.0625�桢0.1250�桢0.1875��
  '''
  resolution = tmp.get_resolution()
  if resolution == RESOLUTION_0_5:
    print "resolution = 0.5 .C"
  elif resolution == RESOLUTION_0_25:
    print "resolution = 0.25 .C"
  elif resolution == RESOLUTION_0_125:
    print "resolution = 0.125 .C"
  else:
    print "resolution = 0.0625 .C"

  '''
    ��ȡ��Դ������ģʽ���ϵ�ģʽ����ģʽ�£������������ʼĴ������ܹ��õ��������¶ȣ�
                                �͹���ģʽ���¶Ȳ���ֹͣ�����Զ�ȡ��д��Ĵ������������߻��ʹ�ĵ�����
      POWER_UP_MODE         // �ϵ�ģʽ
      LOW_POWER_MODE        // �͹���ģʽ
  '''
  state = tmp.get_power_mode()
  if state == POWER_UP_MODE:
    print "Power on mode"
  else:
    print "low power mode"

  '''
    ��ȡ���������ģʽ
      COMPARATOR_OUTPUT_MODE           // �Ƚ������ģʽ
      INTERRPUT_OUTPUT_MODE            // �ж����ģʽ
  '''
  state = tmp.get_alert_output_mode()
  if state == COMPARATOR_OUTPUT_MODE:
    print "Comparator output mode"
  else:
    print "Interrupt output mode"

  '''
      ��ȡALE���ŵļ���״̬�����ż���Ϊ�ߣ�ALE���Ÿߵ�ƽΪ���ƽ��Ĭ��Ϊ�͵�ƽ������������ALEΪ�ߵ�ƽ
                             ���ż���Ϊ�ͣ�ALE���ŵͼ���Ϊ���ƽ��Ĭ��Ϊ�ߵ�ƽ������������ALEΪ�͵�ƽ
      POLARITY_HIGH         // ���ż���Ϊ��
      POLARITY_LOW          // ���ż���Ϊ��
  '''
  state = tmp.get_polarity_state()
  if state == POLARITY_HIGH:
    print "Pin polarity is high"
  else:
    print "Pin polarity is low"

  '''
    ��ȡ��Ӧģʽ����Ӧ�������޺��ٽ�ֵ������ֻ��Ӧ�ٽ�ֵ��
      UPPER_LOWER_CRIT_RESPONSE         // ����/���ߺ��ٽ�ֵ ����Ӧ
      ONLY_CRIT_RESPONSE                // ��ֹ����������Ӧ��ֻ���ٽ�ֵ��Ӧ
  '''
  state = tmp.get_alert_response_mode()
  if state == UPPER_LOWER_CRIT_RESPONSE:
    print "Both upper/lower and crti values respond"
  else:
    print "Critical response"


  '''
    ���ñ����¶��ͺ�ķ�Χ�����������޺��ٽ�ֵ����ֵ������һ����Χ,�ͺ��ܽ������ڽ��£��������䣩,
    Ҳ����˵���޼�ȥ�ͺ��¶ȣ�ALE��ƽ�Żָ�
    ����:�¶�����Ϊ30.0�ȣ��ͺ��¶�Ϊ+1.5�ȣ���ǰ��35��ALE�Ѿ�������ƽ��ת��
         Ҫ��ALE�ָ���ƽ������ﵽ30-1.5��28.5���ȣ�ALE���Ų��ָܻ���ƽ
      HYSTERESIS_0_0        // û���ͺ󣬾��ǵ���ָ���¶Ⱦ���Ӧ
      HYSTERESIS_1_5        // ��������Ҫ�ͺ�1.5��
      HYSTERESIS_3_0        // ��������Ҫ�ͺ�3.0��
      HYSTERESIS_6_0        // ��������Ҫ�ͺ�6.0��
  '''
  state = tmp.get_alert_hysteresis()
  if state == HYSTERESIS_0_0:
    print "The temperature lag range is 0 degrees"
  elif state == HYSTERESIS_1_5:
    print "The temperature lag range is 1.5 degrees"
  elif state == HYSTERESIS_3_0:
    print "The temperature lag range is 3.0 degrees"
  else:
    print "The temperature lag range is 6.0 degrees"
  
  
  '''
    ��ȡ����ģʽ״̬���õ�ʱ����ģʽ���߷Ǳ���ģʽ
      ENABLE_ALERT           // ����ģʽ
      DISABLE_ALERT          // �Ǳ���ģʽ
  '''
  state = tmp.get_alert_enable_state()
  if state == ENABLE_ALERT:
    print "Alarm mode"
  else:
    print "No alarm mode"

  '''
    ��ȡ������״̬�����ж��Ƿ�����޸��������޺��ٽ�ֵ����ֵ
      CRIT_LOCK       // �����ٽ�ֵ���ٽ�ֵ����ֵ�������޸�
      WIN_LOCK        // �����������ޣ��������޵���ֵ�������޸�
      CRIT_WIN_LOCK   // �����ٽ�ֵ���������ޣ��������޺��ٽ�ֵ�����ݶ��������޸�
      NO_LOCK         // �����������޺��ٽ�ֵ������֮�����������ٽ�ֵ����ֵ���Ա��޸�
  '''
  state = tmp.get_lock_state()
  if state == CRIT_LOCK:
    print "The crit is locked"
  elif state == WIN_LOCK:
    print "The upper and lower limits are locked"
  elif state == CRIT_WIN_LOCK:
    print "The upper and lower limits and crit are locked"
  else:
    print "no locked"

def loop():
  time.sleep(0.1)
  exit()

if __name__ == "__main__":
  setup()
  while True:
    loop()