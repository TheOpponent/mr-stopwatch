# Mr. Stopwatch

![007489](https://user-images.githubusercontent.com/8432212/120903761-0b886380-c616-11eb-868f-05fd21d9f76d.png)

A simple Python program using Tkinter that keeps time and writes it to time.txt. Two times are kept:
- Session time, kept until the program is closed.
- Total time, kept until the Reset button is pressed.

time.txt is intended to be read by another program, e.g. OBS, to show time elapsed for a single stream and for a whole playthrough across multiple streams.

The timer is not precise and keeps seconds, not milliseconds. Days are not tracked either; the hour counter can go into triple digits.
