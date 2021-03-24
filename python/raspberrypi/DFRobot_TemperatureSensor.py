# -*- coding: utf-8 -*
""" 
  @file DFRobot_TemperatureSensor.py
  @note DFRobot_TemperatureSensor Class infrastructure, implementation of underlying methods
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @licence     The MIT License (MIT)
  @author      [ZhixinLiu](zhixin.liu@dfrobot.com)
  version  V0.1
  date  2021-03-24
  @get from https://www.dfrobot.com
  @url https://github.com/DFRobot/DFRobot_TemperatureSensor
"""
import serial
import time
import smbus
import spidev
import os
import RPi.GPIO as GPIO

#GPIO.setwarnings(False)

I2C_MODE                       = 1
SPI_MODE                       = 2
ERROR                          = -1
I2C_ADDRESS_REGISTER           = (0x00)
I2C_BUFF_LEN                   = (0x20)
NONE                           = (0x00)

FRU_REGISTER                   = (0x00 & 0x0F)
CONFIG_REGISTER                = (0x01 & 0x0F)
T_UPPER_REGISTER               = (0x02 & 0x0F)
T_LOWER_REGISTER               = (0x03 & 0x0F)
T_CRIT_REGISTER                = (0x04 & 0x0F)
TEMPERATURE_REGISTER           = (0x05 & 0x0F)
MANUFACTURER_REGISTER          = (0x06 & 0x0F)
DEVICE_REGISTER                = (0x07 & 0x0F)
RESOLUTION_REGISTER            = (0x08 & 0x0F)

MANUFACTURER_ID                = (0x54)
DEVICE_ID                      = (0x04)

CRIT_0_UPPER_0_LOWER_0         = (0x00 << 5)
CRIT_0_UPPER_0_LOWER_1         = (0x01 << 5)
CRIT_0_UPPER_1_LOWER_0         = (0x02 << 5)
CRIT_0_UPPER_1_LOWER_1         = (0x03 << 5)
CRIT_1_UPPER_0_LOWER_0         = (0x04 << 5)
CRIT_1_UPPER_0_LOWER_1         = (0x05 << 5)
CRIT_1_UPPER_1_LOWER_0         = (0x06 << 5)
CRIT_1_UPPER_1_LOWER_1         = (0x07 << 5)

RESOLUTION_0_5                 = (0x00 & 0x03)
RESOLUTION_0_25                = (0x01 & 0x03)
RESOLUTION_0_125               = (0x02 & 0x03)
RESOLUTION_0_0625              = (0x03 & 0x03)      # default resolutivn

COMPARATOR_OUTPUT_MODE         = 0x00               # default comparator mode
INTERRPUT_OUTPUT_MODE          = 0x01

CRIT_LOCK                      = 0x80
WIN_LOCK                       = 0x40
CRIT_WIN_LOCK                  = 0xC0
NO_LOCK                        = 0x00               # default no lock
POWER_UP_MODE                  = 0x00               # dafault power up
LOW_POWER_MODE                 = 0x01

HYSTERESIS_0_0                 = 0x00               # default hysteresis
HYSTERESIS_1_5                 = 0x02
HYSTERESIS_3_0                 = 0x04
HYSTERESIS_6_0                 = 0x06

POLARITY_HIGH                  = 0x02
POLARITY_LOW                   = 0x00               # default active low

ENABLE_ALERT                   = 0x08
DISABLE_ALERT                  = 0x00               # default disable

ONLY_CRIT_RESPONSE             = 0x40
UPPER_LOWER_CRIT_RESPONSE      = 0x00               # dafault output mode

class DFRobot_TemperatureSensor(object):
  def __init__(self ,bus):
    if bus != 0:
      self.i2cbus = smbus.SMBus(bus)
      self.__i2c_spi = I2C_MODE;
    else:
      self.__i2c_spi = SPI_MODE;

  '''
    @brief ��ʼ�����������Աȴ�������оƬid �� ���� id
    @return 0  is init success
            -1 оƬid ���߳���id��������
  '''
  def sensor_init(self):
    device_id = self.get_device_id()
    manufaturer_id = self.get_manufacturer_id()
    if device_id == DEVICE_ID and manufaturer_id == MANUFACTURER_ID:
      return 0
    else:
      return -1

  '''
    @brief get device id
    @return device id
                DEVICE_ID          // device id is 0x04
  '''
  def get_device_id(self):
    rslt = self.read_reg(DEVICE_REGISTER ,2)
    return rslt[0]

  '''
    @brief get manufacturer id
    @return manufacturer id
                MANUFACTURER_ID    // manufacturer id is 0x54
  '''
  def get_manufacturer_id(self):
    rslt = self.read_reg(MANUFACTURER_REGISTER ,2)
    return rslt[1]

  '''
    @brief �����¶ȴ������ķֱ��ʣ���ͬ�ķֱ��ʣ���ȡ���¶ȵľ��Ȳ�ͬ
    @param resolution
                RESOLUTION_0_5     // ��ȡ�¶ȵ�С������Ϊ0.5�ı���     ��0.5�� ��1.0�桢1.5��
                RESOLUTION_0_25    // ��ȡ�¶ȵ�С������Ϊ0.25�ı���    ��0.25�桢0.50�桢0.75��
                RESOLUTION_0_125   // ��ȡ�¶ȵ�С������Ϊ0.125�ı���   ��0.125�桢0.250�桢0.375��
                RESOLUTION_0_0625  // ��ȡ�¶ȵ�С������Ϊ0.0625�ı���  ��0.0625�桢0.1250�桢0.1875��
    @return state
                0    is set successfully
                -1   ���õķֱ��ʴ�������ֱ��ʲ���
  '''
  def set_resolution(self ,resolution):
    txbuf = [0]
    if resolution == RESOLUTION_0_5 or resolution == RESOLUTION_0_25 or resolution == RESOLUTION_0_125 or resolution == RESOLUTION_0_0625:
      txbuf[0] = resolution
      self.write_reg(RESOLUTION_REGISTER ,txbuf)
      return 0
    else:
      return -1

  '''
    @brief ��ȡ�¶ȴ������ķֱ��� ,��ͬ�ķֱ��ʣ���ȡ���¶ȵľ��Ȳ�ͬ
    @return resolution
                RESOLUTION_0_5     // ��ȡ�¶ȵ�С������Ϊ0.5�ı���     ��0.5�� ��1.0�桢1.5��
                RESOLUTION_0_25    // ��ȡ�¶ȵ�С������Ϊ0.25�ı���    ��0.25�桢0.50�桢0.75��
                RESOLUTION_0_125   // ��ȡ�¶ȵ�С������Ϊ0.125�ı���   ��0.125�桢0.250�桢0.375��
                RESOLUTION_0_0625  // ��ȡ�¶ȵ�С������Ϊ0.0625�ı���  ��0.0625�桢0.1250�桢0.1875��
  '''
  def get_resolution(self):
    rslt = self.read_reg(RESOLUTION_REGISTER ,1)
    return rslt[0]&0x03

  '''
    @brief ��ȡ��ǰ�Ļ����¶ȣ�ע�����ò�ͬ�ֱ����ܹ��õ����¶Ⱦ��Ȳ�ͬ
    @return �¶�ֵΪ��������
  '''
  def get_temperature(self):
    rslt = self.read_reg(TEMPERATURE_REGISTER ,2)
    rslt[0] &= 0x1F
    if rslt[0]&0x10 == 0x10:
      rslt[0] &= 0x0F
      return 256.0-(float(rslt[0]*16.0) + float(rslt[1]/16.0))
    else:
      return float(rslt[0]*16.0) + float(rslt[1]/16.0)

  '''
    @brief ��ȡ��ǰ�Ƚ�����״̬��ֻ���ڱȽ���ģʽ����Ч
           �Ƚ���ģʽ�ǱȽϵ�ǰ�¶���������ֵ��������ֵ�����ٽ�ֵ�Ĺ�ϵ��ģʽ
    @return state
                TA ����ǰ�¶ȣ�TCRIT�����ٽ��¶ȣ�TUPPER���������¶ȣ�TLOWER���������¶�
                CRIT_0_UPPER_0_LOWER_0    // TA < TCRIT��TA �� TUPPER��TA �� TLOWER
                CRIT_0_UPPER_0_LOWER_1    // TA < TCRIT��TA �� TUPPER��TA < TLOWER
                CRIT_0_UPPER_1_LOWER_0    // TA < TCRIT��TA > TUPPER��TA �� TLOWER
                CRIT_0_UPPER_1_LOWER_1    // TA < TCRIT��TA > TUPPER��TA < TLOWER
                CRIT_1_UPPER_0_LOWER_0    // TA �� TCRIT��TA �� TUPPER��TA �� TLOWER
                CRIT_1_UPPER_0_LOWER_1    // TA �� TCRIT��TA �� TUPPER��TA < TLOWER
                CRIT_1_UPPER_1_LOWER_0    // TA �� TCRIT��TA > TUPPER��TA �� TLOWER
                CRIT_1_UPPER_1_LOWER_1    // TA �� TCRIT��TA > TUPPER��TA < TLOWER
  '''
  def get_comparator_state(self):
    rslt = self.read_reg(TEMPERATURE_REGISTER ,2) 
    return (rslt[0]&0xE0)

  '''
    @brief ���õ�Դģʽ���ϵ�ģʽ����ģʽ�£������������ʼĴ������ܹ��õ��������¶ȣ�
                         �͹���ģʽ���¶Ȳ���ֹͣ�����Զ�ȡ��д��Ĵ������������߻��ʹ�ĵ�����
    @param mode
                POWER_UP_MODE         // �ϵ�ģʽ
                LOW_POWER_MODE        // �͹���ģʽ
    @return 0x00 is set success
            -1   ����ʧ�ܣ��Ĵ����Ѿ����������Ƚ����Ĵ���
  '''
  def set_power_mode(self ,mode):
    if self.get_lock_state() != 0:
      return -1
    rslt = self.read_reg(CONFIG_REGISTER ,2)
    rslt[0] &= 0x06
    rslt[0] |= (mode&0x01);
    self.write_reg(CONFIG_REGISTER ,rslt)
    return 0

  '''
    @brief ��ȡ��Դ������ģʽ���ϵ�ģʽ����ģʽ�£������������ʼĴ������ܹ��õ��������¶ȣ�
                                �͹���ģʽ���¶Ȳ���ֹͣ�����Զ�ȡ��д��Ĵ������������߻��ʹ�ĵ�����
    @return mode
                POWER_UP_MODE         // �ϵ�ģʽ
                LOW_POWER_MODE        // �͹���ģʽ
  '''
  def get_power_mode(self):
    rslt = self.read_reg(CONFIG_REGISTER ,2) 
    return (rslt[0]&0x01)

  '''
    @brief ��������ģʽ���������ֹ��������������ޡ����ޡ��ٽ�ֵ�Ĵ�С
    @param lock
                CRIT_LOCK       // �����ٽ�ֵ���ٽ�ֵ����ֵ�������޸�
                WIN_LOCK        // �����������ޣ��������޵���ֵ�������޸�
                CRIT_WIN_LOCK   // �����ٽ�ֵ���������ޣ��������޺��ٽ�ֵ�����ݶ��������޸�
                NO_LOCK         // �����������޺��ٽ�ֵ������֮�����������ٽ�ֵ����ֵ���Ա��޸�
     @return state
                0x00 is set successfully
                0xFE ���õ�ģʽ����
  '''
  def set_lock_state(self ,lock):
    rslt = self.read_reg(CONFIG_REGISTER ,2)
    if lock == CRIT_LOCK or lock == WIN_LOCK or lock == CRIT_WIN_LOCK or lock == NO_LOCK:
      rslt[1] &= 0x3F
      rslt[1] |= lock
      self.write_reg(CONFIG_REGISTER ,rslt)
      return 0
    else:
      return 0xfe

  '''
    @brief ��ȡ������״̬�����ж��Ƿ�����޸��������޺��ٽ�ֵ����ֵ
    @return state
                CRIT_LOCK       // �ٽ�ֵ�������ٽ�ֵ����ֵ�������޸�
                WIN_LOCK        // ���������������������޵���ֵ�������޸�
                CRIT_WIN_LOCK   // �ٽ�ֵ�ʹ���ͬʱ�������������޺��ٽ�ֵ�����ݶ��������޸�
                NO_LOCK         // û���������������޺��ٽ�ֵ����ֵ�����Ա��޸�
  '''
  def get_lock_state(self):
    rslt = self.read_reg(CONFIG_REGISTER ,2) 
    return (rslt[1]&0xC0)

  '''
    @brief ���ñ����¶��ͺ�ķ�Χ�����������޺��ٽ�ֵ����ֵ������һ����Χ,�ͺ��ܽ������ڽ��£��������䣩
            ,Ҳ����˵������/����/�ٽ�ֵ����ȥ�ͺ��¶ȣ�ALE��ƽ�Żָ�
            ����:�¶�����Ϊ30.0�ȣ��ͺ��¶�Ϊ+1.5�ȣ���ǰ��35��ALE�Ѿ�������ƽ��ת��
            Ҫ��ALE�ָ���ƽ������ﵽ30-1.5��28.5���ȣ�ALE���Ų��ָܻ���ƽ
    @param mode
                HYSTERESIS_0_0        // û���ͺ󣬾��ǵ���ָ���¶Ⱦ���Ӧ
                HYSTERESIS_1_5        // ��������Ҫ�ͺ�1.5��
                HYSTERESIS_3_0        // ��������Ҫ�ͺ�3.0��
                HYSTERESIS_6_0        // ��������Ҫ�ͺ�6.0��
    @return state
                0x00 is set successfully
                -1 ��ǰ�Ĵ���Ϊ����״̬�������޸�
                0xFE ���õķ�Χ�������鷶Χ
  '''
  def set_alert_hysteresis(self ,mode):
    if self.get_lock_state() != 0:
      return -1
    rslt = self.read_reg(CONFIG_REGISTER ,2)
    if mode == HYSTERESIS_0_0 or mode == HYSTERESIS_1_5  or mode == HYSTERESIS_3_0 or mode == HYSTERESIS_6_0:
      rslt[0] &= 0x01
      rslt[0] |= mode
      self.write_reg(CONFIG_REGISTER ,rslt)
      return 0
    else:
      return 0xFE

  '''
    @brief ��ȡ�ͺ���¶�
    @return hysteresis
                HYSTERESIS_0_0        // û���ͺ󣬾��ǵ���ָ���¶Ⱦ���Ӧ
                HYSTERESIS_1_5        // ��������Ҫ�ͺ�1.5��
                HYSTERESIS_3_0        // ��������Ҫ�ͺ�3.0��
                HYSTERESIS_6_0        // ��������Ҫ�ͺ�6.0��
  '''
  def get_alert_hysteresis(self):
    rslt = self.read_reg(CONFIG_REGISTER ,2) 
    return (rslt[0]&0x06)

  '''
    @brief ʹ�ܻ��߽�ֹ����ģʽ��ʹ�ܱ���ģʽ��ALE���ŵ��ﱨ���������������䣬��ֹ����ģʽALE����û����Ӧ
    @param mode
                ENABLE_ALERT           // ʹ�ܱ���ģʽ��ALE���ŵ��ﱨ����������������
                DISABLE_ALERT          // ��ֹ����ģʽ����ֹ����ģʽALE����û����Ӧ
    @return state
                0x00 is set successfully
                -1   ��ǰ�Ĵ���Ϊ����״̬�������޸�
                0xFE ���õ�ģʽ��������ģʽ
  '''
  def set_alert_enable(self ,mode):
    if self.get_lock_state() != 0:
      return -1
    rslt = self.read_reg(CONFIG_REGISTER ,2)
    if mode == ENABLE_ALERT or mode == DISABLE_ALERT:
      rslt[1] &= 0xF7
      rslt[1] |= mode
      self.write_reg(CONFIG_REGISTER ,rslt)
      return 0
    else:
      return 0xFE

  '''
    @brief ��ȡ����ģʽ״̬���õ�ʱ����ģʽ���߷Ǳ���ģʽ
    @return mode
                ENABLE_ALERT           // ����ģʽ
                DISABLE_ALERT          // �Ǳ���ģʽ
  '''
  def get_alert_enable_state(self):
    rslt = self.read_reg(CONFIG_REGISTER ,2) 
    return (rslt[1]&0x08)
  
  '''
    @brief ����ALE���ŵļ��ԣ����ż���Ϊ�ߣ�ALE���Ÿߵ�ƽΪ���ƽ��Ĭ��Ϊ�͵�ƽ������������ALEΪ�ߵ�ƽ
                              ���ż���Ϊ�ͣ�ALE���ŵͼ���Ϊ���ƽ��Ĭ��Ϊ�ߵ�ƽ������������ALEΪ�͵�ƽ
    @param polarity
                POLARITY_HIGH         // ALE���Ÿߵ�ƽΪ���ƽ
                POLARITY_LOW          // ALE���ŵͼ���Ϊ���ƽ
    @return state
                0x00 is set successfully
                -1   ��ǰ�Ĵ���Ϊ����״̬�������޸�
                0xFE ���õļ��Դ������鼫��
  '''
  def set_polarity(self ,polarity):
    if self.get_lock_state() != 0:
      return -1
    rslt = self.read_reg(CONFIG_REGISTER ,2)
    if polarity == POLARITY_HIGH or polarity == POLARITY_LOW:
      rslt[1] &= 0xFD
      rslt[1] |= polarity
      self.write_reg(CONFIG_REGISTER ,rslt)
      return 0
    else:
      return 0xFE

  '''
    @brief ��ȡALE���ŵļ���״̬�����ż���Ϊ�ߣ�ALE���Ÿߵ�ƽΪ���ƽ��Ĭ��Ϊ�͵�ƽ������������ALEΪ�ߵ�ƽ
                                  ���ż���Ϊ�ͣ�ALE���ŵͼ���Ϊ���ƽ��Ĭ��Ϊ�ߵ�ƽ������������ALEΪ�͵�ƽ
    @return polarity
                POLARITY_HIGH         // ALE���Ÿߵ�ƽΪ���ƽ
                POLARITY_LOW          // ALE���ŵͼ���Ϊ���ƽ
  '''
  def get_polarity_state(self):
    rslt = self.read_reg(CONFIG_REGISTER ,2) 
    return (rslt[1]&0x02)


  '''
    @brief ���þ��������ģʽ���Ƚ������ģʽ����Ҫ����жϣ��ж�ģʽ��Ҫ����ж�
    @param mode
                COMPARATOR_OUTPUT_MODE           // �Ƚ������ģʽ����Ҫ����жϣ�
                ���磺ʹ���˱���ģʽ������ALE����Ϊ�͵�ƽ�
                      ���������޾������¶�ʱ��ALE���ŴӸߵ�ƽ���͵�ƽ�����¶ȵ������޵���������ʱ��ALE���Żָ��ߵ�ƽ
                INTERRPUT_OUTPUT_MODE            // �ж����ģʽ��Ҫ����жϣ�����������ʱ�����������ж��ж�һֱ���ڣ��ж�ģʽ�Ĵ������Ǵ�һ��״̬��Ϊ��һ��״̬��
                ���磺������������ֵ20�ȣ�������ֵ25�ȣ��ٽ���ֵ30�ȣ����¶�һֱ����20��ʱ�������жϣ����¶ȳ���25��ʱ�Ų����жϣ�ALE�������䣬��ʱӦ������жϣ�ALE����                       �ָ��������������ALE���Ŵ����ٽ��¶�30��ʱ���ж�ģʽʧЧ������ж�ҲʧЧ��������¶Ƚ���30�����£��Żָ��ж�ģʽ
     @return state
                0x00 is set successfully
                -1 ��ǰ�Ĵ���Ϊ����״̬�������޸�
                0xFE ���õľ������ģʽ��������ģʽ
  '''
  def set_alert_output_mode(self ,mode):
    if self.get_lock_state() != 0:
      return -1
    rslt = self.read_reg(CONFIG_REGISTER ,2)
    if mode == COMPARATOR_OUTPUT_MODE or mode == INTERRPUT_OUTPUT_MODE:
      rslt[1] &= 0xFE
      rslt[1] |= mode
      self.write_reg(CONFIG_REGISTER ,rslt)
      return 0
    else:
      return 0xFE

  '''
    @brief ��ȡ���������ģʽ
    @return mode
                COMPARATOR_OUTPUT_MODE           // �Ƚ������ģʽ
                INTERRPUT_OUTPUT_MODE            // �ж����ģʽ
  '''
  def get_alert_output_mode(self):
    rslt = self.read_reg(CONFIG_REGISTER ,2) 
    return (rslt[1]&0x01)

  '''
    @brief ������Ӧģʽ����Ӧ�������޺��ٽ�ֵ������ֻ��Ӧ�ٽ�ֵ��ֻ��Ӧ�ٽ�ֵ���������ж�ģʽ
    @param mode
                UPPER_LOWER_CRIT_RESPONSE         // ����/���ߺ��ٽ�ֵ ����Ӧ��
                ONLY_CRIT_RESPONSE                // ��ֹ����������Ӧ��ֻ���ٽ�ֵ��Ӧ
    @return state
                0x00 is set successfully
                -1   ��ǰ�Ĵ���Ϊ����״̬�������޸�
                0xFE ���õ���Ӧģʽ��������ģʽ
  '''
  def set_alert_response_mode(self ,mode):
    if self.get_lock_state() != 0:
      return -1
    rslt = self.read_reg(CONFIG_REGISTER ,2)
    if mode == UPPER_LOWER_CRIT_RESPONSE or mode == ONLY_CRIT_RESPONSE:
      rslt[1] &= 0xFB
      rslt[1] |= mode
      self.write_reg(CONFIG_REGISTER ,rslt)
      return 0
    else:
      return 0xFE

  '''
    @brief ��ȡ��Ӧ��ģʽ
    @return mode
                UPPER_LOWER_CRIT_RESPONSE         // ����/���ߺ��ٽ�ֵ ����Ӧ
                ONLY_CRIT_RESPONSE                // ��ֹ����������Ӧ��ֻ���ٽ�ֵ��Ӧ
  '''
  def get_alert_response_mode(self):
    rslt = self.read_reg(CONFIG_REGISTER ,2) 
    return (rslt[1]&0x04)

  '''
    @brief �������޺�������ֵ,�������õ��ж�ģʽ��Ӧ�����������¶Ⱥ͵��������¶���Ӧ
    @param upper
              // �¶����ޣ������λС�����Զ������0.25�ı�������ΧΪ-40 �� +125��
    @param lower
              // �¶����ޣ������λС�����Զ������0.25�ı�������ΧΪ-40 �� +125��
    @return state
                0x00                              // �����������޳ɹ�
                -2                                // ������������ʧ�ܣ�ԭ�����¶�����С�����ޣ����������¶Ⱥ������¶�С������
                -1                                // ������������ʧ�ܣ��Ĵ����������������
  '''
  def set_upper_lower_tereshold(self ,upper ,lower):
    rslt = [0]*2
    if (upper-lower) < 2.0:
      return -2
    if self.get_lock_state() != 0:
      return -1  
    self.data_threshold_analysis(upper ,rslt)
    self.write_reg(T_UPPER_REGISTER ,rslt)
    rslt[0] = 0
    rslt[1] = 0
    self.data_threshold_analysis(lower ,rslt)
    self.write_reg(T_LOWER_REGISTER ,rslt)
    return 0

  '''
    @brief �����¶��ٽ�ֵ,�������õ��ж�ģʽ��Ӧ��������ٽ�ֵ�¶ȱ�����������¶�
    @param value
              // �¶ȵ��ٽ�ֵ�������λС�����Զ������0.25�ı�������ΧΪ-40 �� +125��
    @return state
                0x00                              // �����ٽ�ֵ�ɹ�
                -1                                // �����ٽ�ֵʧ�ܣ��Ĵ����������������
  '''
  def set_crit_threshold(self ,value):
    rslt = [0]*2
    if self.get_lock_state() != 0:
      return -1
    self.data_threshold_analysis(value ,rslt)
    self.write_reg(T_CRIT_REGISTER ,rslt)
    return 0

  '''
    @brief ����жϣ�ֻʹ�����ж�ģʽ�£�����ģʽû��Ч��
  '''
  def clear_interrupt(self):
    rslt = self.read_reg(CONFIG_REGISTER ,2)
    rslt[1] &= 0xDF
    rslt[1] |= 0x20
    self.write_reg(CONFIG_REGISTER ,rslt)

  def read_register(self):
    rslt = self.read_reg(CONFIG_REGISTER ,2)
    print "config 0 = %#x "%rslt[0]
    print "config 1 = %#x "%rslt[1]
    
    rslt = self.read_reg(T_UPPER_REGISTER ,2)
    print "UPPER 0 = %#x "%rslt[0]
    print "UPPER 1 = %#x "%rslt[1]
    
    rslt = self.read_reg(T_LOWER_REGISTER ,2)
    print "LOWER 0 = %#x "%rslt[0]
    print "LOWER 1 = %#x "%rslt[1]
    
    rslt = self.read_reg(T_CRIT_REGISTER ,2)
    print "crit 0 = %#x "%rslt[0]
    print "crit 1 = %#x "%rslt[1]
  '''
    @brief ��ֵ����
  '''
  def data_threshold_analysis(self ,value ,data):
    symbol = 0
    decimals = 0
    integet = 0
    if value < 0.00001:
      symbol = 1
      value *= -1
    decimals = self.parsing_decimal(value)
    integer = int(value)
    data[0] |= symbol<<4
    data[0] |= integer>>4
    data[1] |= ((integer&0x0F)<<4)
    data[1] |= decimals

  '''
    @brief С��λ����
  '''  
  def parsing_decimal(self ,value):
    decimals = int(value*100) - (int(value))*100
    if decimals == 0:
      return 0x00
    elif decimals > 0 and decimals <= 25:
      return 0x04
    elif decimals > 25 and decimals <= 50:
      return 0x08
    else:
      return 0x0C

'''
  @brief An example of an i2c interface module
'''
class DFRobot_TemperatureSensor_I2C(DFRobot_TemperatureSensor):
  def __init__(self ,bus ,addr):
    self.__addr = addr
    super(DFRobot_TemperatureSensor_I2C, self).__init__(bus)

  '''
    @brief writes data to a register
    @param reg register address
    @param value written data
  '''
  def write_reg(self, reg, data):
    while 1:
      try:
        self.i2cbus.write_i2c_block_data(self.__addr ,reg ,data)
        return
      except:
        print("please check connect!")
        #os.system('i2cdetect -y 1')
        time.sleep(1)
        return
  '''
    @brief read the data from the register
    @param reg register address
    @param value read data
  '''
  def read_reg(self, reg ,len):
    try:
      rslt = self.i2cbus.read_i2c_block_data(self.__addr ,reg ,len)
      #print rslt
    except:
      rslt = -1
    return rslt

class DFRobot_TemperatureSensor_SPI(DFRobot_TemperatureSensor): 
  def __init__(self ,cs, bus = 0, dev = 0,speed = 1000000):
    self.__cs = cs
    GPIO.setup(self.__cs, GPIO.OUT)
    GPIO.output(self.__cs, GPIO.LOW)
    self.__spi = spidev.SpiDev()
    self.__spi.open(bus, dev)
    self.__spi.no_cs = True
    self.__spi.max_speed_hz = speed
    super(DFRobot_TemperatureSensor_SPI, self).__init__(0)

  '''
    @brief writes data to a register
    @param reg register address
    @param value written data
  '''
  def write_reg(self, reg, data):
    GPIO.output(self.__cs, GPIO.LOW)
    reg = reg&0x7F
    self.__spi.writebytes([reg,data[0]])
    GPIO.output(self.__cs, GPIO.HIGH)

  '''
    @brief read the data from the register
    @param reg register address
    @param value read data
  '''
  def read_reg(self, reg ,len):
    reg = reg|0x80
    GPIO.output(self.__cs, GPIO.LOW)
    self.__spi.writebytes([reg])
    rslt = self.__spi.readbytes(len)
    GPIO.output(self.__cs, GPIO.HIGH)
    return rslt