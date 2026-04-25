# Pico Control Setup Guide

Hi friends

This repository contains scripts and instructions for running code on the **Raspberry Pi Pico** using **VS Code + MicroPython**. This setup is used for projects like haptic motor control, sensor reading (e.g., FSR + ADS1115), and real-time interaction.

## Requirements

Make sure you have:

- Raspberry Pi Pico (MicroPython already installed)
- USB cable
- A computer with VS Code installed
- Pico / MicroPython extension for VS Code

## Getting Started

Follow the official Raspberry Pi Pico setup guide:

https://pip-assets.raspberrypi.com/categories/610-raspberry-pi-pico/documents/RP-008276-DS-1-getting-started-with-pico.pdf?disposition=inline

Install the Pico extension and MicroPython support by following the steps in that document.

## VS Code Setup

1. Open VS Code  
2. Go to Extensions (left sidebar)  
3. Search for and install a Pico / MicroPython extension  
4. Plug in the Pico using USB  

## Connecting to the Pico

Once connected:

- A Pico terminal should open automatically
- You can verify connection if you see:

```
>>>
```

This means you're inside the MicroPython REPL.

If not:
- Try unplugging and reconnecting the Pico
- Make sure the correct serial port is selected

## Running a Script on the Pico

1. Open the `.py` file you want to run  
2. Press:

```
CTRL + SHIFT + P
```

5. Type and select: MicroPico: Run Current File

This uploads and runs the script on the Pico.

## Using the Pico Terminal

The terminal allows you to:

- View output 
- Send commands directly to the Pico

## Stopping a Script

To stop execution:

```
CTRL + C
```

This interrupts the running program.

