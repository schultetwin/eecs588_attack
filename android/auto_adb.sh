#!/bin/bash

./bin/adb wait-for-device
./bin/adb install Pwned.apk
./bin/adb shell am start -n co.sparkey.pwned/co.sparkey.pwned.PwnedActivity
