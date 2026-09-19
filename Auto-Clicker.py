import tkinter as tk
from tkinter import ttk
import threading
import time

from pynput.mouse import Button, Controller
from pynput import keyboard

mouse = Controller()

clicking = False
running = True


def click_loop():
    global clicking

    while running:
        if clicking:
            try:
                cps = float(cps_var.get())

                if cps <= 0:
                    cps = 1

                mouse.click(Button.left)
                time.sleep(1 / cps)

            except ValueError:
                time.sleep(0.1)
        else:
            time.sleep(0.05)


def toggle_clicking():
    global clicking

    clicking = not clicking

    if clicking:
        status_var.set("Clicking")
        toggle_button.config(text="Stop")
    else:
        status_var.set("Stopped")
        toggle_button.config(text="Start")


def hotkey_listener(key):
    if key == keyboard.Key.f6:
        root.after(0, toggle_clicking)


def close_app():
    global running
    running = False
    root.destroy()


root = tk.Tk()
root.title("Auto Clicker")
root.geometry("360x250")
root.resizable(False, False)

title = ttk.Label(
    root,
    text="Auto Clicker",
    font=("Segoe UI", 18, "bold")
)
title.pack(pady=(20, 15))

ttk.Label(root, text="Clicks per second").pack()

cps_var = tk.StringVar(value="10")

cps_entry = ttk.Entry(
    root,
    textvariable=cps_var,
    width=12,
    justify="center"
)
cps_entry.pack(pady=8)

toggle_button = ttk.Button(
    root,
    text="Start",
    command=toggle_clicking
)
toggle_button.pack(pady=12)

status_var = tk.StringVar(value="Stopped")

status_label = ttk.Label(
    root,
    textvariable=status_var,
    font=("Segoe UI", 11)
)
status_label.pack()

ttk.Label(
    root,
    text="Press F6 to Start / Stop",
    font=("Segoe UI", 9)
).pack(pady=12)

threading.Thread(
    target=click_loop,
    daemon=True
).start()

listener = keyboard.Listener(on_press=hotkey_listener)
listener.daemon = True
listener.start()

root.protocol("WM_DELETE_WINDOW", close_app)

root.mainloop()
