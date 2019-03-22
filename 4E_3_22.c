/* ========================================
 *
 * Copyright YOUR COMPANY, THE YEAR
 * All Rights Reserved
 * UNPUBLISHED, LICENSED SOFTWARE.
 *
 * CONFIDENTIAL AND PROPRIETARY INFORMATION
 * WHICH IS THE PROPERTY OF your company.
 *
 * ========================================
*/
#include <project.h>
#include<stdio.h>
#include<stdlib.h>

#define T 40 // largest delta
#define BT 2020
#define WT 1900
#define SBASE 1000

extern uint8 const CYCODE LCD_Char_1_customFonts[];//载入传统字体

uint16 white_ref, black_ref, THERESHOLD;
uint16 left, mid, right, min, black;
char grayScale[5];
int LSExp;//, LSErr, LSErrPre, LSErrDiff, LSErrSum;
int RSExp;//, RSErr, RSErrPre, RSErrDiff, RSErrSum;
int right_output=0, left_output=0;
int b, a, offset=0;
double Kp, Ki, Kd, PID;
int error=0, last_error=0, error_all=0;
int last_left=0, last_right=0;
int ts = 1;

int main()
{
    /* Place your initialization/startup code here (e.g. MyInst_Start()) */
    CyGlobalIntEnable;
    UART_Start();
    LCD_Char_1_Start();
    LCD_Char_1_LoadCustomFonts(LCD_Char_1_customFonts);
    LCD_Char_1_ClearDisplay();
    Clock_1_Enable();
    Clock_2_Enable();
    PWM_1_Start();
    PWM_2_Start();
    ADC_SAR_Seq_1_Start();
    ADC_SAR_Seq_1_StartConvert();    //开始AD转换，
    PWM_1_WriteCompare(4500);
    PWM_2_WriteCompare(4500);
    Kp = 0.5;
    Ki = 0;
    Kd = 0;
    
    /*LSErrPre = 0;
    LSErrSum = 0;
    RSErrPre = 0;
    RSErrSum = 0;*/
    /*
    for(;;)
    {
        CyDelay(1000);
        ADC_SAR_Seq_1_IsEndConversion(ADC_SAR_Seq_1_WAIT_FOR_RESULT);//ADC的转换结束，存储结束前一直待机
        left = ADC_SAR_Seq_1_GetResult16(0);//值大于2000（2047）为黑，小于1000为白
        mid = ADC_SAR_Seq_1_GetResult16(1);
        right = ADC_SAR_Seq_1_GetResult16(2);
        if (abs(right - left) < T && mid > BT && left < WT && right < WT) // Not start condition
        {
            LCD_Char_1_Position(0,0);
		    LCD_Char_1_PrintString("1");
            white_ref = (left + right) / 2;
            black_ref = mid;
            break;
        }
        else
        {
            LCD_Char_1_Position(0,0);
		    LCD_Char_1_PrintString("0");
            sprintf(grayScale, "%d", left);
            LCD_Char_1_Position(1,0);
		    LCD_Char_1_PrintString(grayScale);
            sprintf(grayScale, "%d", mid);
            LCD_Char_1_Position(0,3);
		    LCD_Char_1_PrintString(grayScale);
            sprintf(grayScale, "%d", right);
            LCD_Char_1_Position(1,6);
		    LCD_Char_1_PrintString(grayScale); 
        } 
    }
    */
    for(;;)
    {
        CyDelay(300);
        
        LCD_Char_1_ClearDisplay();
        ADC_SAR_Seq_1_IsEndConversion(ADC_SAR_Seq_1_WAIT_FOR_RESULT);//ADC的转换结束，存储结束前一直待机
        left = ADC_SAR_Seq_1_GetResult16(0);//450黑，1600为白
        mid = ADC_SAR_Seq_1_GetResult16(1);//750黑，2047为白
        right = ADC_SAR_Seq_1_GetResult16(2);//320黑，1300为白
        /*
        if (mid > BT)
        {
            offset = right - left;
            right = right - offset;
        }
        */
        /*
        error = (right-last_right) - (left-last_left);
        */
        error = right - left + 300; // 300 is the origin offset of the left and right sensor
        error_all += error * ts;
        PID = Kp * error + Kd * (error - last_error) / ts + Ki * (error_all);
        last_error = error;
        last_left = left;
        last_right = right;
        //limiter
        if (PID > 300)
            PID = 300;
        else if (PID < -300)
            PID = -300;
        /*
        if (2047 - mid) > xxx
        {
            this should not happen
            just for test
            error
            back or stop or...
        }
        */
        left_output = 5000 + (int)PID; // > 4500 forward
        right_output = 4000 + (int)PID;// < 4500 forward
        
        /*
        if (right < left)
        {
            min = right < mid ? right : mid;
            
            if (abs(left - min) < T)
            {
                if (abs(mid - min) < T)
                {
                    //error
                    LSExp = -SBASE;
                    RSExp = -SBASE;
                }
                else
                {
                    //straight
                    black = mid;
                    LSExp = SBASE;
                    RSExp = SBASE;
                }
            }
            else
            {
                if (abs(mid - min) < T)
                {
                    LSExp = SBASE - b*(black-left)/min - offset;
                    RSExp = SBASE + a*(black-left)/min + offset;
                }
                else
                {
                    LSExp = SBASE - b*(left-min)/min;
                    RSExp = SBASE + a*(left-min)/min;
                }
            }
        }
        else
        {
            min = left < mid ? left : mid;
            
            if (abs(right - min) < T)
            {
                if (abs(mid - min) < T)
                {
                    //error
                    LSExp = -SBASE;
                    RSExp = -SBASE;
                }
                else
                {
                    //straight
                    black = mid;
                    LSExp = SBASE;
                    RSExp = SBASE;
                }
            }
            else
            {
                if (abs(mid - min) < T)
                {
                    LSExp = SBASE + a*(black-right)/min + offset;
                    RSExp = SBASE - b*(black-right)/min - offset;
                }
                else
                {
                    LSExp = SBASE + a*(right-min)/min;
                    RSExp = SBASE - b*(right-min)/min;
                }
            }
        }
        right_output = 4500 + RSExp;
        left_output = 4500 - LSExp;
        */
        PWM_1_WriteCompare(left_output);
        PWM_2_WriteCompare(right_output);
        
        //
        //display
        sprintf(grayScale, "%d", left);
        LCD_Char_1_Position(0,0);
        LCD_Char_1_PrintString(grayScale);
        sprintf(grayScale, "%d", mid);
        LCD_Char_1_Position(0,6);
        LCD_Char_1_PrintString(grayScale);
        sprintf(grayScale, "%d", right);
        LCD_Char_1_Position(0,12);
        LCD_Char_1_PrintString(grayScale);
        sprintf(grayScale, "%d", 500 + (int)PID); // grayScale just a name 
        LCD_Char_1_Position(1,0);
		LCD_Char_1_PrintString(grayScale);
        sprintf(grayScale, "%d", 500 - (int)PID);
        LCD_Char_1_Position(1,6);
		LCD_Char_1_PrintString(grayScale);
        
    }
    return 0;
}


/* [] END OF FILE */
