#include <Arduino.h>
#include <CAN.h>
#include <esp32-hal-ledc.h>

// microROS関連
#include <micro_ros_arduino.h>
#include <rcl/error_handling.h>
#include <rcl/rcl.h>
#include <rclc/executor.h>
#include <rclc/rclc.h>
#include <std_msgs/msg/int16_multi_array.h>

//  パルスカウンタ関連
#include "driver/pcnt.h"

// 自作ヘッダーファイル
#include "config.h"       //モードやIDを管理
#include "defs.h"         //定数を管理
#include "input_task.h"   //入力系のタスクを管理
#include "mode_init.h"    //各モードの初期化関数を管理
#include "output_task.h"  //出力系のタスクを管理
#include "ros_defs.h"     //microROS関連を管理

// デバッグ出力用のマクロ
// #if DEBUG_SERIAL
// #define DEBUG_BEGIN(baud) Serial.begin(baud, SERIAL_8N1, DEBUG_SERIAL_TxD, DEBUG_SERIAL_RxD);
// #define DEBUG_PRINT(x) Serial.print(x);
// #define DEBUG_PRINTLN(x) Serial.println(x);
// #else
// #define DEBUG_BEGIN(baud)
// #define DEBUG_PRINT(x)
// #define DEBUG_PRINTLN(x)
// #endif

void setup()
{

    DEBUG_BEGIN(115200);
    DEBUG_PRINTLN("Debug Serial Started");

    // 状態表示LEDの初期化
    pinMode(LED, OUTPUT);

    // MODEに応じた初期化
    switch (MODE)
    {
    case 0:
        break;
    case 1:
        // 1:出力（モタドラ、サーボ）
        ros_init();
        mode1_init();
        break;
    case 2:
        break;
    case 3:
        // 3:入力（エンコーダー優先）
        ros_init();
        mode3_init();
        break;
    case 4:
        // 4:入力（マイクロスイッチ優先）
        ros_init();
        mode4_init();
        break;
    default:;
        ;
    }
}

void loop()
{
    while (1)
    {
        rclc_executor_spin_some(&executor, RCL_MS_TO_NS(5));
        vTaskDelay(1); // 1msスリープ
    }
}
