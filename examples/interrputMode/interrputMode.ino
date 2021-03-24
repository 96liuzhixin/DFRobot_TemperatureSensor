 /*!
  * @file  interruptMode.ino
  * @brief 中断获取温度的例子，将ALE引脚连接到引脚2
  * @n 实验现象：温度在串口显示，测量温度随环境温度改变而改变
  * @n 实验现象：中断io口在状态转换时产生，例如温度在上限和下限中间或者在一直低于下限或者一直高于上限，此时不会发生中断
  * @n 实验现象：当温度状态在低于下限的状态时改变，高于了下限此时产生了中断需要清除中断，
  * @n 实验现象：清除中断后，ALE引脚电平恢复，高于临界值时清除中断失效（ALE引脚电平不恢复）
  * @n i2c 地址选择，默认i2c地址为0x1F，A2、A1、A0引脚为高电平，
  * @n 其8中组合为,1代表高电平，0代表低电平
  *               | A2 | A1 | A0 |
  *               | 0  | 0  | 0  |    0x18
  *               | 0  | 0  | 1  |    0x19
  *               | 0  | 1  | 0  |    0x1A
  *               | 0  | 1  | 1  |    0x1B
  *               | 1  | 0  | 0  |    0x1D
  *               | 1  | 0  | 1  |    0x1D
  *               | 1  | 1  | 0  |    0x1E
  *               | 1  | 1  | 1  |    0x1F   default i2c address
  *
  * @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  * @licence     The MIT License (MIT)
  * @author      ZhixinLiu(zhixin.liu@dfrobot.com)
  * @version     V0.1
  * @date        2021-03-17
  * @get         from https://www.dfrobot.com
  * @url         https://github.com/dfrobot/DFRobot_TemperatureSensor
  */
#include "DFRobot_TemperatureSensor.h"
#define I2C_ADDRESS 0x1F
#define PIN_2 2                // 中断引脚         
#define PIN_2_INTERRUPT 0      // 引脚2对应的中断号
uint8_t interruptFlag = 0;
DFRobot_TemperatureSensor_I2C mcp9808(&Wire ,I2C_ADDRESS);
void myInterrupt(void)
{
  interruptFlag = 1;   // 中断标志
}
void setup()
{
  uint8_t state = 0;
  Serial.begin(115200);
  while(mcp9808.begin() != 0){
    Serial.println("i2c device number error!");
    delay(1000);
  } Serial.println("i2c connect success!");

  while(0 != mcp9808.sensorInit()){
    Serial.println("初始化失败，请检查模块是否正确!");
    delay(100);
  } Serial.println("sensor init success!");

  /**
    设置温度的分辨率
      RESOLUTION_0_5     // 获取温度的小数部分为0.5的倍数     如0.5℃ 、1.0℃、1.5℃
      RESOLUTION_0_25    // 获取温度的小数部分为0.25的倍数    如0.25℃、0.50℃、0.75℃
      RESOLUTION_0_125   // 获取温度的小数部分为0.125的倍数   如0.125℃、0.250℃、0.375℃
      RESOLUTION_0_0625  // 获取温度的小数部分为0.0625的倍数  如0.0625℃、0.1250℃、0.1875℃
  */
  if((state = mcp9808.setResolution(RESOLUTION_0_25)) == 0){
    Serial.println("设置温度的分辨率成功!");
  }else{
    Serial.println("分辨率参数错误，请检查参数");
  }

  /**
    设置电源模式，上电模式或低功耗模式
      POWER_UP_MODE   // 上电模式，可以正常访问寄存器，所有功能都开启，能够得到正确的温度
      LOW_POWER_MODE  // 低功耗模式，可以读取或写入寄存器，但读写活动会使耗电升高，不能得到正确的温度
  */
  if((state = mcp9808.setPowerMode(POWER_UP_MODE)) == 0){
    Serial.println("设置电源模式成功！");
  }else{
    Serial.println("寄存器已经锁定，请先解锁寄存器!");
  }

  /**
    设置警报输出的模式，比较器输出模式不需要清除中断，中断模式需要清除中断
      COMPARATOR_OUTPUT_MODE           // 比较器输出模式不需要清除中断，比较模式的触发是，当温度高于上限或温度低于下限或者温度超过临界值
        例如：使能了报警模式，设置ALE引脚为低电平活动，当超过上限警报的温度时，
              ALE引脚从高电平到低电平，当温度低于上限但高于下限时，ALE引脚恢复高电平
      INTERRPUT_OUTPUT_MODE            // 中断输出模式需要清除中断，当产生警报时如果不清除中断中断一直存在，中断模式的触发，是从一种状态变为另一种状态
        例如：设置了下限阈值20度，上限阈值25度，临界阈值30度，当温度一直低于20度时不产生中断，
              当温度超过25度时才产生中断，ALE引脚跳变，此时应该清空中断，ALE引脚恢复，特殊情况，
              当ALE引脚大于临界温度30度时，中断模式失效，清空中断也失效，必须等温度降到30度以下，才恢复中断模式。
  */
  if((state = mcp9808.setAlertOutputMode(INTERRPUT_OUTPUT_MODE)) == 0){
    Serial.println("设置中断模式成功！");
  }else{
    Serial.println("寄存器已经锁定或者模式设置错误!");
  }

  /**
    设置ALE引脚的极性
      POLARITY_HIGH         // 设置ALE引脚高电平为活动电平，默认为低电平，产生报警后ALE为高电平
      POLARITY_LOW          // 设置ALE引脚低极性为活动电平，默认为高电平，产生报警后ALE为低电平
  */
  if((state = mcp9808.setPolarity(POLARITY_LOW)) == 0){
    Serial.println("设置ALE引脚极性成功！");
  }else{
    Serial.println("寄存器已经锁定或者模式设置错误!");
  }

  /**
    设置响应模式，响应上限下限和临界值，或者只响应临界值，只响应临界值不适用于中断模式
      UPPER_LOWER_CRIT_RESPONSE         // 上限/下线和临界值 都响应
      ONLY_CRIT_RESPONSE                // 禁止上限下限响应，只有临界值响应
  */
  if((state = mcp9808.setAlertResponseMode(UPPER_LOWER_CRIT_RESPONSE)) == 0){
    Serial.println("设置响应模式成功！");
  }else{
    Serial.println("寄存器已经锁定或者模式设置错误!");
  }

  /**
    设置上限和下限阈值,根据配置的中断模式响应，高于这个温度和低于这个温度的响应，最多两位小数
      upper
        // 设置的温度上限，自动处理成0.25的倍数，范围为-40 到 +125度
      lower
        // 设置的温度下限，自动处理成0.25的倍数，范围为-40 到 +125度
  */
  if((state = mcp9808.setUpperLowerThreshold(32.5 ,20.5)) == 0){
    Serial.println("设置上限下限的温度成功！");
  }else{
    Serial.println("设置上限下限失败，原因是温度上限小于下限，或者上限温度和下限温度小于两度,或者寄存器锁定！");
  }

  /**
    设置温度临界值,根据配置的中断模式响应，这里的临界值温度必须大于上限温度
      value
        // 温度的临界值，最多两位小数，自动处理成0.25的倍数，范围为-40 到 +125度
  */
  if((state = mcp9808.setCritThreshold(40.5)) == 0){
    Serial.println("设置临界值的温度成功！");
  }else{
    Serial.println("寄存器已经锁定!");
  }

  /**
    设置报警温度滞后的范围，在上限下限和临界值的阈值上增加一个范围,滞后功能仅适用于降温（从热至冷）,
    也就是说上限减去滞后温度，ALE电平才恢复
    例如:温度上限为30.0度，滞后温度为+1.5度，当前是35度ALE已经产生电平翻转，
         要想ALE恢复电平，必须达到30-1.5（28.5）度，ALE引脚才能恢复电平
      HYSTERESIS_0_0        // 没有滞后，就是到达指定温度就响应
      HYSTERESIS_1_5        // 从热至冷要滞后1.5℃
      HYSTERESIS_3_0        // 从热至冷要滞后3.0℃
      HYSTERESIS_6_0        // 从热至冷要滞后6.0℃
  */
  if((state = mcp9808.setAlertHysteresis(HYSTERESIS_1_5)) == 0){
    Serial.println("设置温度滞后成功！");
  }else{
    Serial.println("设置的模式错误或者寄存器为锁定状态！");
  }

  /**
    使能或者禁止报警模式，使能报警模式后，ALE引脚到达报警条件后会产生跳变，禁止报警模式ALE引脚没有响应
      ENABLE_ALERT           // 使能报警模式，ALE引脚到达报警条件后会产生跳变
      DISABLE_ALERT          // 禁止报警模式，禁止报警模式ALE引脚没有响应
  */
  if((state = mcp9808.setAlertEnable(ENABLE_ALERT)) == 0){
    Serial.println("使能报警模式成功");
  }else{
    Serial.println("使能报警模式失败,参数错误或者当前为寄存器锁定状态!");
  }

  /**
    设置锁定模式和解锁，防止错误操作更改上限、下限、临界值、阈值的大小
      CRIT_LOCK       // 锁定临界值，临界值的阈值不允许被修改
      WIN_LOCK        // 锁定上限下限，上限下限的阈值不允许被修改
      CRIT_WIN_LOCK   // 锁定临界值和上限下限，上限下限和临界值的数据都不允许被修改
      NO_LOCK         // 解锁上限下限和临界值，解锁之后上限下限临界值的阈值可以被修改
  */
  if((state = mcp9808.setLockState(NO_LOCK)) == 0){
    Serial.println("锁定上限下限和临界值成功！");
  }else{
    Serial.println("设置的模式错误，请检查模式！");
  }

  /**
    根据设置ALE引脚极性选择
      INPUT_PULLUP    // 设置极性为低电平，设置2号引脚为上拉输入
      INPUT_PULLDOWN  // 设置极性为高电平，设置2号引脚为下拉输入
  */
  pinMode(PIN_2 ,INPUT_PULLUP);
  
  /**
    设置2号引脚为中断模式
      FALLING         // 当2号引脚由高电平到低电平后产生中断，进入interrupt函数
      RISING          // 当2号引脚由低电平到高电平后产生中断，进入interrupt函数
  */
  attachInterrupt(PIN_2_INTERRUPT ,myInterrupt ,FALLING);
}
void loop()
{
  Serial.print("Temperature is ="); 
  Serial.print(mcp9808.getTemperature());
  Serial.println("℃");

  /**
    当ALE io口产生了中断，清除报警中断
    清空上限下限阈值温度所产生的中断，临界值中断不能清除
  */
  if(interruptFlag == 1){
    mcp9808.clearInterrupt();
    interruptFlag = 0;
  }
  delay(1000);
}