# DFRobot_TemperatureSensor
High precision temperature sensor can get accurate temperature, but also provides low threshold and high threshold critical value interrupt and other functions
## DFRobot_TemperatureSensor
---------------------------------------------------------
DFRobot_TemperatureSensor


## Table of Contents

* [Summary](#Summary)
* [Installation](#installation)
* [Methods](#methods)
* [Compatibility](#compatibility)
* [History](#history)
* [Credits](#credits)

<snippet>
<content>


## Summary

You can get the temperature the normal way, you can set the upper and lower thresholds, you can get the temperature through the comparator, or you can use the interrupt to get the temperature

## Installation

To use this library, first download the library file, paste it into the \Arduino\libraries directory, then open the examples folder and run the demo in the folder.

## Methods

```C++

  /**
   * @brief 初始化传感器，对比传感器的芯片id 和 厂商 id
     @return state
                0x00 is init successfully
                0xFF 芯片id 或者厂商id错误，请检查
   */
  uint8_t sensorInit(void);

  /**
   * @brief 设置温度传感器的分辨率，不同的分辨率，获取的温度的精度不同
   * @param resolution
                RESOLUTION_0_5     // 获取温度的小数部分为0.5的倍数     如0.5℃ 、1.0℃、1.5℃
                RESOLUTION_0_25    // 获取温度的小数部分为0.25的倍数    如0.25℃、0.50℃、0.75℃
                RESOLUTION_0_125   // 获取温度的小数部分为0.125的倍数   如0.125℃、0.250℃、0.375℃
                RESOLUTION_0_0625  // 获取温度的小数部分为0.0625的倍数  如0.0625℃、0.1250℃、0.1875℃
     @return state
                0x00 is set successfully
                0xFE 设置的分辨率错误，请检查分辨率参数
   */
  uint8_t setResolution(uint8_t resolution);

  /**
   * @brief 获取温度传感器的分辨率 ,不同的分辨率，获取的温度的精度不同
   * @return resolution
                RESOLUTION_0_5     // 获取温度的小数部分为0.5的倍数     如0.5℃ 、1.0℃、1.5℃
                RESOLUTION_0_25    // 获取温度的小数部分为0.25的倍数    如0.25℃、0.50℃、0.75℃
                RESOLUTION_0_125   // 获取温度的小数部分为0.125的倍数   如0.125℃、0.250℃、0.375℃
                RESOLUTION_0_0625  // 获取温度的小数部分为0.0625的倍数  如0.0625℃、0.1250℃、0.1875℃
   */
  uint8_t getResolution(void);

  /**
   * @brief 获取当前的环境温度，注意设置不同分辨率能够得到的温度精度不同
   * @return 温度值为浮点数，默认保留两位小数
   */
  float getTemperature(void);

  /**
   * @brief 获取当前比较器的状态，只有在比较器模式下有效//比较器。。。
   * @return state
                TA 代表当前温度，TCRIT代表临界温度，TUPPER代表上限温度，TLOWER代表下限温度
                CRIT_0_UPPER_0_LOWER_0    // TA < TCRIT、TA ≤ TUPPER、TA ≥ TLOWER
                CRIT_0_UPPER_0_LOWER_1    // TA < TCRIT、TA ≤ TUPPER、TA < TLOWER
                CRIT_0_UPPER_1_LOWER_0    // TA < TCRIT、TA > TUPPER、TA ≥ TLOWER
                CRIT_0_UPPER_1_LOWER_1    // TA < TCRIT、TA > TUPPER、TA < TLOWER
                CRIT_1_UPPER_0_LOWER_0    // TA ≥ TCRIT、TA ≤ TUPPER、TA ≥ TLOWER
                CRIT_1_UPPER_0_LOWER_1    // TA ≥ TCRIT、TA ≤ TUPPER、TA < TLOWER
                CRIT_1_UPPER_1_LOWER_0    // TA ≥ TCRIT、TA > TUPPER、TA ≥ TLOWER
                CRIT_1_UPPER_1_LOWER_1    // TA ≥ TCRIT、TA > TUPPER、TA < TLOWER
   */
  uint8_t getComparatorState(void);

  /**
   * @brief 设置锁定模式或解锁，防止错误操作更改上限、下限、临界值的大小
   * @param state
                CRIT_LOCK       // 锁定临界值，临界值的阈值不允许被修改
                WIN_LOCK        // 锁定上限下限，上限下限的阈值不允许被修改
                CRIT_WIN_LOCK   // 锁定临界值和上限下限，上限下限和临界值的数据都不允许被修改
                NO_LOCK         // 解锁上限下限和临界值，解锁之后上限下限临界值的阈值可以被修改
     @return state
                0x00 is set successfully
                0xFE 设置的模式错误
   */
  uint8_t setLockState(uint8_t lock);

  /**
   * @brief 获取锁定的状态，来判断是否可以修改上限下限和临界值的阈值
   * @return state
                CRIT_LOCK       // 临界值锁定，临界值的阈值不允许被修改
                WIN_LOCK        // 上限下限锁定，上限下限的阈值不允许被修改
                CRIT_WIN_LOCK   // 临界值和窗口同时锁定，上限下限和临界值的数据都不允许被修改
                NO_LOCK         // 没有锁定，上限下限和临界值的阈值都可以被修改
   */
  uint8_t getLockState(void);

  /**
   * @brief 设置电源模式，上电模式：该模式下，可以正常访问寄存器，能够得到正常的温度；
                          低功耗模式：温度测量停止，可以读取或写入寄存器，但是总线活动会使耗电升高
   * @param mode
                POWER_UP_MODE         // 上电模式
                LOW_POWER_MODE        // 低功耗模式
   * @return 0x00 is set success
             0xFF 设置失败，寄存器已经锁定，请先解锁寄存器
   */
  uint8_t setPowerMode(uint8_t mode);

  /**
   * @brief 获取电源的配置模式，上电模式：该模式下，可以正常访问寄存器，能够得到正常的温度；
                                低功耗模式：温度测量停止，可以读取或写入寄存器，但是总线活动会使耗电升高
   * @return mode
                POWER_UP_MODE         // 上电模式
                LOW_POWER_MODE        // 低功耗模式
   */
  uint8_t getPowerMode(void);

  /**
   * @brief 设置报警温度滞后的范围，在上限下限和临界值的阈值上增加一个范围,滞后功能仅适用于降温（从热至冷）
            ,也就是说（上限/下限/临界值）减去滞后温度，ALE电平才恢复
            例如:温度上限为30.0度，滞后温度为+1.5度，当前是35度ALE已经产生电平翻转，
            要想ALE恢复电平，必须达到30-1.5（28.5）度，ALE引脚才能恢复电平
   * @param mode
                HYSTERESIS_0_0        // 没有滞后，就是到达指定温度就响应
                HYSTERESIS_1_5        // 从热至冷要滞后1.5℃
                HYSTERESIS_3_0        // 从热至冷要滞后3.0℃
                HYSTERESIS_6_0        // 从热至冷要滞后6.0℃
     @return state
                0x00 is set successfully
                0xFF 当前寄存器为锁定状态不允许修改
                0xFE 设置的范围错误，请检查范围
   */
  uint8_t setAlertHysteresis(uint8_t mode);

  /**
   * @brief 获取滞后的温度
   * @return hysteresis
                HYSTERESIS_0_0        // 温度滞后范围为 +0.0℃
                HYSTERESIS_1_5        // 温度滞后范围为 +1.5℃
                HYSTERESIS_3_0        // 温度滞后范围为 +3.0℃
                HYSTERESIS_6_0        // 温度滞后范围为 +6.0℃
   */
  uint8_t getAlertHysteresis(void);


  /**
   * @brief 使能或者禁止报警模式，使能报警模式后，ALE引脚到达报警条件后会产生跳变，禁止报警模式ALE引脚没有响应
   * @param mode
                ENABLE_ALERT           // 使能报警模式，ALE引脚到达报警条件后会产生跳变
                DISABLE_ALERT          // 禁止报警模式，禁止报警模式ALE引脚没有响应
     @return state
                0x00 is set successfully
                0xFF 当前寄存器为锁定状态不允许修改
                0xFE 设置的模式错误，请检查模式
   */
  uint8_t setAlertEnable(uint8_t mode);
  
  
  /**
   * @brief 获取报警模式状态，得到时报警模式或者非报警模式
   * @return mode
                ENABLE_ALERT           // 报警模式
                DISABLE_ALERT          // 非报警模式
   */
  uint8_t getAlertEnableState(void);

  /**
   * @brief 设置ALE引脚的极性，引脚极性为高：ALE引脚高电平为活动电平，默认为低电平，产生报警后ALE为高电平
                               引脚极性为低：ALE引脚低极性为活动电平，默认为高电平，产生报警后ALE为低电平
   * @param polarity
                POLARITY_HIGH         // ALE引脚高电平为活动电平
                POLARITY_LOW          // ALE引脚低极性为活动电平
     @return state
                0x00 is set successfully
                0xFF 当前寄存器为锁定状态不允许修改
                0xFE 设置的极性错误，请检查极性
   */
  uint8_t setPolarity(uint8_t polarity);

  /**
   * @brief 获取ALE引脚的极性状态，引脚极性为高：ALE引脚高电平为活动电平，默认为低电平，产生报警后ALE为高电平
                                   引脚极性为低：ALE引脚低极性为活动电平，默认为高电平，产生报警后ALE为低电平
   * @return polarity
                POLARITY_HIGH         // ALE引脚高电平为活动电平
                POLARITY_LOW          // ALE引脚低极性为活动电平
   */
  uint8_t getPolarityState(void);

  /**
   * @brief 设置警报输出的模式，比较器输出模式不需要清除中断，中断模式需要清除中断
   * @param mode
                COMPARATOR_OUTPUT_MODE           // 比较器输出模式不需要清除中断，
                例如：使能了报警模式，设置ALE引脚为低电平活动
                当超过上限警报的温度时，ALE引脚从高电平到低电平，当温度低于上限但高于下限时，ALE引脚恢复高电平
                INTERRPUT_OUTPUT_MODE            // 中断输出模式需要清除中断，当产生警报时，如果不清除中断中断一直存在，中断模式的触发，是从一种状态变为另一种状态，
                例如：设置了下限阈值20度，上限阈值25度，临界阈值30度，当温度一直低于20度时不产生中断，当温度超过25度时才产生中断，ALE引脚跳变，此时应该清空中断，ALE引脚恢复，特殊情况，当ALE引脚大于临界温度30度时，中断模式失效，清空中断也失效，必须等温度降到30度以下，才恢复中断模式
     @return state
                0x00 is set successfully
                0xFF 当前寄存器为锁定状态不允许修改
                0xFE 设置的警报输出模式错误，请检查模式
   */
  uint8_t setAlertOutputMode(uint8_t mode);

  /**
   * @brief 获取警报输出的模式
   * @return mode
                COMPARATOR_OUTPUT_MODE           // 比较器输出模式
                INTERRPUT_OUTPUT_MODE            // 中断输出模式
   */
  uint8_t getAlertOutputMode(void);

  /**
   * @brief 设置响应模式，响应上限下限和临界值，或者只响应临界值，只响应临界值不适用于中断模式
   * @param mode
                UPPER_LOWER_CRIT_RESPONSE         // 上限/下线和临界值 都响应，
                ONLY_CRIT_RESPONSE                // 禁止上限下限响应，只有临界值响应
     @return state
                0x00 is set successfully
                0xFF 当前寄存器为锁定状态不允许修改
                0xFE 设置的响应模式错误，请检查模式
   */
  uint8_t setAlertResponseMode(uint8_t mode);

  /**
   * @brief 获取中断响应的模式
   * @return mode
                UPPER_LOWER_CRIT_RESPONSE         // 上限/下线和临界值 都响应
                ONLY_CRIT_RESPONSE                // 禁止上限下限响应，只有临界值响应
   */
  uint8_t getAlertResponseMode(void);

  /**
   * @brief 设置上限和下限阈值,根据配置的中断模式响应，高于上限温度和低于下限温度响应
   * @param upper
              // 温度上限，最多两位小数，自动处理成0.25的倍数，范围为-40 到 +125度
   * @param lower
              // 温度下限，最多两位小数，自动处理成0.25的倍数，范围为-40 到 +125度
   * @return state
                0x00                              // 设置上限下限成功
                0xFF                              // 设置上限下限失败，原因是温度上限小于下限，或者上限温度和下限温度小于两度
   */
  uint8_t setUpperLowerThreshold(float upper ,float lower);

  /**
   * @brief 设置温度临界值,根据配置的中断模式响应，这里的临界值温度必须大于上限温度
   * @param value
              // 温度的临界值，最多两位小数，自动处理成0.25的倍数，范围为-40 到 +125度
   */
  void setCritThreshold(float value);

```
## Compatibility

MCU                | Work Well | Work Wrong | Untested  | Remarks
------------------ | :----------: | :----------: | :---------: | -----
Arduino uno        |      √       |              |             | 
Mega2560           |      √       |              |             | 
Lenardo            |      √       |              |             | 
ESP32              |      √       |              |             | 
ESP8266            |      √       |              |             | 

## History

-  March    22, 2021 - Version 0.1 released.

## Credits

Written by ZhiXinLiu(ZhiXin.Liu@dfrobot.com), 2020. (Welcome to our [website](https://www.dfrobot.com/))