"""!
@file week2.py
Run experimental and simulated first-order linear response tests and plot the results. This program
utilizes a simple GUI with a plot in it. It uses Tkinter to display the GUI. The experiemental results
are taken from the Nucleo, which is received by the serial port. This data is then used to compare it
to the theoretical output of the step response.

This file uses a template for the GUI, given by Dr. John Ridgely

@author mecha02
@date   2024-01-25 
"""

## List of imports needed to run the program
import math
import time
import tkinter
from random import random
import serial
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)

## List of variables used throughout the program
V_max = 3.3
R = 100000
C = 3.3e-6


def plot_example(plot_axes, plot_canvas, xlabel, ylabel, x_values, y_values, title):
    """!
    Makes two plots, the experimental and theoretical output
    @param plot_axes The plot axes supplied by Matplotlib
    @param plot_canvas The plot canvas supplied by Matplotlib
    @param xlabel The label for the plot's horizontal axis
    @param ylabel The label for the plot's vertical axis
    @param x_values The x-values for the experiemental output
    @param y_values The y-values for the experiemental output
    @param title The title for the graph
    """
    
    # Theoretical output
    times = [t / 1000 for t in range(1990)]
    boing = [(V_max * (1 - math.exp(-t/(R*C)))) for t in times]

    # Drawing the plot for both outputs   
    plot_axes.plot(times, boing)
    plot_axes.plot(x_values, y_values)
    plot_axes.set_xlabel(xlabel)
    plot_axes.set_ylabel(ylabel)
    plot_axes.set_title(title)
    plot_axes.grid(True)
    plot_canvas.draw()


def tk_matplot(plot_function, xlabel, ylabel, title):
    """!
    This function receives the output from the serial port using the serial class.
    It then places the output in corresponding lists, used later for plotting. This
    function also makes the GUI window, displays it, and runs the user interface
    until the user closes the window. 
    @param plot_function The function which creates a plot
    @param xlabel The label for the plot's horizontal axis
    @param ylabel The label for the plot's vertical axis
    @param title A title for the plot
    """
    
    # Parameters for serial port
    serial_port = 'COM3'  
    baud_rate = 115200
    
    # Opens serial port
    ser = serial.Serial(serial_port, baud_rate, timeout=0.5)
    
    # Writes a soft reset string (Ctrl+D, essentially)
    ser.write(b'\x04') 

    # Variables used for while loop
    end_cond = 0
    x_values = []
    y_values = []

    # Converts the printed statements of the output to float and puts them in lists 
    while end_cond <= 1990:
        try:
            response = ser.readline().decode('utf-8').strip()
            values = response.split(',')
            
            x_value = float(values[0])
            y_value = float(values[1])
            
            x_values.append(x_value/1000)
            y_values.append(y_value)
            
            end_cond += 10
        except ValueError:
            continue
        
    # Create the main program window and give it a title
    tk_root = tkinter.Tk()
    tk_root.wm_title(title)

    # Create a Matplotlib 
    fig = Figure()
    axes = fig.add_subplot()

    # Create the drawing canvas and a handy plot navigation toolbar
    canvas = FigureCanvasTkAgg(fig, master=tk_root)
    toolbar = NavigationToolbar2Tk(canvas, tk_root, pack_toolbar=False)
    toolbar.update()

    # Create the buttons that run tests, clear the screen, and exit the program
    button_quit = tkinter.Button(master=tk_root,
                                 text="Quit",
                                 command=tk_root.destroy)
    button_clear = tkinter.Button(master=tk_root,
                                  text="Clear",
                                  command=lambda: axes.clear() or canvas.draw())
    button_run = tkinter.Button(master=tk_root,
                                text="Run Test",
                                command=lambda: plot_function(axes, canvas,
                                                              xlabel, ylabel, x_values, y_values, title))

                                

    # Arrange things in a grid because "pack" is weird
    canvas.get_tk_widget().grid(row=0, column=0, columnspan=3)
    toolbar.grid(row=1, column=0, columnspan=3)
    button_run.grid(row=2, column=0)
    button_clear.grid(row=2, column=1)
    button_quit.grid(row=2, column=2)

    # This function runs the program until the user decides to quit
    tkinter.mainloop()


# This main code is run if this file is the main program but won't run if this
# file is imported as a module by some other main program
if __name__ == "__main__":
    
    tk_matplot(plot_example,
               xlabel="Time (s)",
               ylabel="Response (V)",
               title="Step Response")


