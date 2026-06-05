# Desktop Hover Clock

A hyper-lightweight, customizable digital clock for Windows written purely in C using the Win32 API. 

This project was built with the goal of consuming absolutely minimal memory and CPU resources. It uses native Windows graphics and timers, avoiding the overhead of heavy runtimes like .NET, Java, or Electron.

## Features

- **Minimalist Design**: Displays only the time (including seconds).
- **Zero Overhead**: Written in pure C; no external libraries or heavy runtimes required.
- **Always on Top**: Hovers above all other windows for quick glancing.
- **Sleek Aesthetic**: Frameless window with a semi-transparent dark grey background and vibrant green text.
- **Drag to Move**: Click anywhere inside the clock to drag it around your screen.
- **Resizeable**: Hover near the edges of the box until the standard resize cursor appears, then click and drag. The font automatically scales to fit!
- **Close Button**: A subtle 'X' button stays anchored perfectly next to the time for easy closing.

## Compilation

You don't need any complex build systems. Assuming you have a standard C compiler like `gcc` (MinGW) installed, you can compile the program with a single command:

```cmd
gcc clock.c -O2 -mwindows -o clock.exe
```

> **Note:** The `-mwindows` flag is crucial as it prevents a background command prompt from opening when the executable runs.

## Usage

1. Run `clock.exe`.
2. Click and hold anywhere inside the dark grey box to drag it.
3. Grab the edges of the box to resize it.
4. Click the red **X** next to the time to exit the application.
