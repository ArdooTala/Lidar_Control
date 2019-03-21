import serial
import time
import matplotlib.pyplot as plt
import math


dists = {}

with serial.Serial('/dev/ttyUSB0', 230400, timeout=5) as ser:
    ser.write(b'e')
    time.sleep(1)
    ser.write(b'b')

    start_count = 0
    got_scan = False
    good_sets = 0
    motor_speed = 0
    rpms = 0

    while not got_scan:
        s = ser.read(1)
        if not s:
            continue
        if start_count == 0:
            if ord(s) == 0xFA:
                start_count = 1
                print("KIR")
        elif start_count == 1:
            if ord(s) == 0xA0:
                start_count = 0
                got_scan = True
                print("Kos")

                s += ser.read(2518)
                s = bytes([0xFA]) + s
                print(len(s))

                for i in range(0, len(s), 42):
                    # print(0xA0+i/42, ord(s[i]), ord(s[i+1]))
                    if s[i] == 0xFA and s[i+1] == 0xA0+i/42:
                        # good_sets += 1
                        # motor_speed += (ord(s[i+3]) << 8) + ord(s[i+2])
                        # rpms = (ord(s[i+3]) << 8 | ord(s[i+2])) / 10

                        for j in range(i+4, i+40, 6):
                            index = 6 * (i / 42) + (j - 4 - i) / 6

                            byte0 = s[j]
                            byte1 = s[j + 1]
                            byte2 = s[j + 2]
                            byte3 = s[j + 3]

                            dist = (byte3 << 8) + byte2
                            dists[math.radians(359-index)] = dist
                            print('>>> ', dist, 359-index)
            else:
                start_count = 0

fig = plt.figure()
ax = fig.add_subplot(111, projection='polar')
ax.set_ylim(0, 300)
c = ax.scatter(dists.keys(), dists.values(), alpha=0.75)

plt.show()
