"""! @file step_response.py
This file contains code which runs a step response to the Nucleo,
which is connected to a circuit. The program then reads the time response
of the output and prints it in a 'CSV' style format

@author mecha02
@date   15-Jan-2024 SPL Original file
"""

## List of imports needed to run the program
import micropython
import cqueue
import utime

micropython.alloc_emergency_exception_buf(100)

## List of variables used throughout the program
volt_q = cqueue.IntQueue(200)
queue_nfull = True
timing = 0
first_time = True

## Setting up and Defining Pins
inp = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.IN)
out = pyb.Pin(pyb.Pin.board.PB0, pyb.Pin.OUT_PP)
adc = pyb.ADC(inp)

def timer_int(tim_num):
    """!
    This is the interrupt callback function, and runs every interrupt.
    It takes output readings (voltage) and stores it in a queue. This is
    done until the queue is full. 
    @param tim_num Interrupt Timer
    """
    global queue_nfull
    global volt_q
    global adc
     
    if queue_nfull == True:
        voltage = adc.read()
        volt_q.put(voltage)
        if volt_q.full() == True:
            queue_nfull = False

def step_response ():
    """!
    This function is responsible for setting up the interrupt and running
    the interrupt callback function
    """   
    global queue_nfull
    global inp

    # Sets up Interrupts and Runs the Callback function
    timmy = pyb.Timer(1, freq = 100)
    timmy.callback(timer_int)
    
    # Turns on input port 
    inp.high()
    
    # Keeps running callback function until the queue is full
    while queue_nfull == True:
        timmy.callback(timer_int)
        
        # If the queue is full, the interrupts are turned off
        if queue_nfull == False:
            timmy.callback(None)

# This main code is run if this file is the main program but won't run if this
# file is imported as a module by some other main program
if __name__ == "__main__":
    step_response()
    
    # Prints out the output in CSV style format
    while volt_q.any() == True:
        volt = float(volt_q.get())
        print(f"{timing},{(3.3/4095) * volt}")
        timing += 10
    
    # Prints once the response has reached a certain point
    print("End")
