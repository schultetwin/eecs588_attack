import serial
import io
import sys
import time

command_file_name = "commands.txt"
auto_click_file_name = "auto_click.sh"

def wait_for_prompt(ser, prompt, timeout = None):
    exit = False
    laststring = ""
    time0 = time.time()
    while not exit:
        ser_in = ser.readline()
        if (len(ser_in) > 0):
            sys.stdout.write(ser_in)
        laststring = laststring + ser_in.decode("ascii", "ignore")
        if prompt in laststring and len(ser_in) == 0:
            exit = True
        if not timeout == None and time.time() - time0 > timeout:
            raise Exception("Timeout Waiting from Prompt {}".format(prompt))

def write(ser, string):
    sys.stdout.write(string)
    ser.write(string)

def write_command_and_wait(ser, string, timeout = None):
    write(ser, string + "\n")
    ret = wait_for_prompt(ser, "shell@crespo", timeout)
    return ret

def load_commands_from_file(name):
    ins = open(name, "r")
    array = []
    for line in ins:
        if len(line.lstrip()) > 0 and not line.lstrip()[0] == "#":
            array.append(line)
    ins.close()
    return array


ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

write(ser, "\n\n")

wait_for_prompt(ser, "debug>")

write(ser, "console\n")
write(ser, "\n\n")
wait_for_prompt(ser, "shell@crespo", 10)

commands = load_commands_from_file(command_file_name)
for command in commands:
    write_command_and_wait(ser, command, 5)

write_command_and_wait(ser, "cd /data/local/tmp", 5)
auto_click_file = open(auto_click_file_name, "r")
auto_click_name = "auto_click.sh"
write_command_and_wait(ser, "rm {}".format(auto_click_name))
for line in auto_click_file:
    write_command_and_wait(ser, "echo '{}' >> {}".format(line.replace("'", "'\\''"), auto_click_name), 5)

write_command_and_wait(ser, "bash {} &".format(auto_click_name), 5)
io.stdout.write("\n\n")

print "Congrats!! We are now ready for you to plug in your device for adb"
