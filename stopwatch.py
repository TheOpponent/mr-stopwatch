import time
import os
from tkinter import *

session_time = 0
running = False
TIME_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),"time.txt")

try:
    # Read time.txt and convert total time in second line to seconds.
    with open(TIME_PATH,"r") as time_file:
        time_data = time_file.readlines()
        total_time_list = [int(i) for i in time_data[1].split(":")]
        total_hours = total_time_list[0]
        total_minutes = total_time_list[1]
        total_seconds = total_time_list[2]
        total_time = (total_hours * 3600) + (total_minutes * 60) + total_seconds
except:
    total_time = 0

ws = Tk()
ws.geometry("400x200+1000+300")
ws.title("Mr. Stopwatch")
ws.resizable(0,0)

def get_times():
    """Return session and total time as tuple.
    The time module is not used here as it does not support hours greater than 23.
    """

    global session_time, total_time

    if session_time == 0:
        session_str = "00:00:00"
    else:
        session_hours = session_time // 3600
        session_minutes = (session_time - (session_hours * 3600)) // 60
        session_seconds = (session_time - (session_hours * 3600)) - (session_minutes * 60)
        session_str = ":".join([str(i).zfill(2) for i in [session_hours,session_minutes,session_seconds]])

    if total_time == 0:
        total_str = "00:00:00"
    else:
        total_hours = total_time // 3600
        total_minutes = (total_time - (total_hours * 3600)) // 60
        total_seconds = (total_time - (total_hours * 3600)) - (total_minutes * 60)
        total_str = ":".join([str(i).zfill(2) for i in [total_hours,total_minutes,total_seconds]])

    return (session_str,total_str)


def counter_label(label):
    """Draw times as formatted strings and output to time.txt."""

    def count():
        """Count 1 second and update labels."""
        global session_time, total_time

        if running:

            label["text"] = "\n".join(get_times())

            # TODO: Find more reliable wait method.
            label.after(1000, count)
            session_time += 1
            total_time += 1

            with open(TIME_PATH,"w") as time_file:
                time_file.write(label["text"])

    count()


def StartTimer(label):
    global running

    running = True
    counter_label(label)
    start_btn["state"] = "disabled"
    stop_btn["state"] = "normal"
    reset_btn["state"] = "disabled"


def PauseTimer():
    global running

    start_btn["state"] = "normal"
    stop_btn["state"] = "disabled"
    reset_btn["state"] = "normal"
    running = False

    time.sleep(1) # Pause for 1 second to workaround faster counting if timer is restarted sooner than 1 second.


def ResetTimer(label):
    global session_time, total_time
    session_time = 0
    total_time = 0

    label["text"]= "00:00:00\n00:00:00"
    with open(TIME_PATH,"w") as time_file:
        time_file.write("00:00:00\n00:00:00")


label_times = Label(
    ws,
    text = "\n".join(get_times()),
    fg = "black",
    font = "Verdana 40 bold"
    )

label_string1 = Label(
    ws,
    text = "Session",
    fg = "black",
    font = "Verdana 12 bold"
    )

label_string2 = Label(
    ws,
    text = "Total",
    fg = "black",
    font = "Verdana 12 bold"
    )

label_times.place(x=110, y=0)
label_string1.place(x=5, y=38)
label_string2.place(x=5, y=103)

start_btn=Button(
    ws,
    text="Start",
    width=15,
    command = lambda: StartTimer(label_times)
    )

stop_btn = Button(
    ws,
    text = "Pause",
    width = 15,
    state = "disabled",
    command=PauseTimer
    )

reset_btn = Button(
    ws,
    text = "Reset",
    width = 15,
    command = lambda: ResetTimer(label_times)
    )

start_btn.place(x=23, y=150)
stop_btn.place(x=143, y=150)
reset_btn.place(x=263, y=150)

def on_close():
    global session_time, total_time

    # Subtract 1 second from total time only if stopwatch was started.
    if session_time > 0:
        total_time -= 1

    with open(TIME_PATH,"w") as time_file:
        time_file.write("00:00:00\n" + get_times()[1])

    ws.destroy()

ws.protocol("WM_DELETE_WINDOW", on_close)
ws.mainloop()