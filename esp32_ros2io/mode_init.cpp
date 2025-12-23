#include <Arduino.h>

// microROS関連
#include <micro_ros_arduino.h>
#include <rcl/error_handling.h>
#include <rcl/rcl.h>
#include <rclc/executor.h>
#include <rclc/rclc.h>
#include <std_msgs/msg/int16_multi_array.h>

// 自作ヘッダーファイル
#include "config.h"       //モードやIDを管理
#include "defs.h"         //定数を管理
#include "input_task.h"   //入力系のタスクを管理
#include "mode_init.h"    //各モードの初期化関数を管理
#include "output_task.h"  //出力系のタスクを管理
#include "ros_defs.h"     //microROS関連を管理

// 各モードの初期化関数

void mode1_init()
{
    // モード1用の初期化

    // MDの方向ピンを出力に設定
    pinMode(MD1D, OUTPUT);
    pinMode(MD2D, OUTPUT);
    pinMode(MD3D, OUTPUT);
    pinMode(MD4D, OUTPUT);

    // PWMの初期化
    ledcAttach(MD1P, MD_PWM_FREQ, MD_PWM_RESOLUTION);
    ledcAttach(MD2P, MD_PWM_FREQ, MD_PWM_RESOLUTION);
    ledcAttach(MD3P, MD_PWM_FREQ, MD_PWM_RESOLUTION);
    ledcAttach(MD4P, MD_PWM_FREQ, MD_PWM_RESOLUTION);

    // サーボのPWMの初期化
    ledcAttach(SERVO1, SERVO_PWM_FREQ, SERVO_PWM_RESOLUTION);
    ledcAttach(SERVO2, SERVO_PWM_FREQ, SERVO_PWM_RESOLUTION);
    ledcAttach(SERVO3, SERVO_PWM_FREQ, SERVO_PWM_RESOLUTION);
    ledcAttach(SERVO4, SERVO_PWM_FREQ, SERVO_PWM_RESOLUTION);

    // 受信＆ピン操作のスレッド（タスク）の作成
    xTaskCreateUniversal(
        Output_Task,
        "Output_Task",
        4096,
        NULL,
        2, // 優先度、最大25？
        NULL,
        PRO_CPU_NUM);
}

void mode2_init()
{
    // モード2用の初期化
    while (1)
    {
        ;
    }
}

void mode3_init()
{
    // モード3用の初期化

    // エンコーダの初期化
    enc_init_all();

    // スイッチのピンを入力に設定し内蔵プルアップ抵抗を有効化
    pinMode(SW1, INPUT_PULLUP);
    pinMode(SW2, INPUT_PULLUP);
    pinMode(SW3, INPUT_PULLUP);
    pinMode(SW4, INPUT_PULLUP);

    // Rev.3からそのまま、そのうち変える
    msg.data.data = (int16_t *)malloc(sizeof(int16_t) * 8);
    msg.data.size = 8;
    msg.data.capacity = 8;

    xTaskCreateUniversal(
        ENC_PRI_Read_Publish_Task,
        "ENC_PRI_Read_Publish_Task",
        4096,
        NULL,
        2, // 優先度、最大25？
        NULL,
        APP_CPU_NUM);

    xTaskCreateUniversal(
        LED_PWM_Task,
        "LED_PWM_Task",
        2048,
        NULL,
        1, // 優先度、最大25？
        &led_pwm_handle,
        APP_CPU_NUM);
}

void mode4_init()
{
    // エンコーダの初期化
    enc_init_half();

    // スイッチのピンを入力に設定し内蔵プルアップ抵抗を有効化
    pinMode(SW1, INPUT_PULLUP);
    pinMode(SW2, INPUT_PULLUP);
    pinMode(SW3, INPUT_PULLUP);
    pinMode(SW4, INPUT_PULLUP);
    pinMode(SW5, INPUT_PULLUP);
    pinMode(SW6, INPUT_PULLUP);
    pinMode(SW7, INPUT_PULLUP);
    pinMode(SW8, INPUT_PULLUP);

    // Rev.3からそのまま、そのうち変える
    msg.data.data = (int16_t *)malloc(sizeof(int16_t) * 11);
    msg.data.size = 11;
    msg.data.capacity = 11;

    xTaskCreateUniversal(
        SW_PRI_Read_Publish_Task,
        "SW_PRI_Read_Publish_Task",
        4096,
        NULL,
        2, // 優先度、最大25？
        NULL,
        APP_CPU_NUM);

    xTaskCreateUniversal(
        LED_PWM_Task,
        "LED_PWM_Task",
        2048,
        NULL,
        1, // 優先度、最大25？
        &led_pwm_handle,
        APP_CPU_NUM);
}



// テストモード　※実機で「絶対」に実行するな！
// シリアルモニターからEnterが押されるまで待機する
void mode0_init()
{
    while (1)
    {
        // テストモード実装予定
        ;
    }
}