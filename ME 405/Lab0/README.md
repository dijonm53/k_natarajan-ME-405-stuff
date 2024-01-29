Team mecha02 Lab 0 

Week 2 lab code can be found in the /src folder, as week2.py. main.py is the initial lab file testing the input and output, 
and step_respones.py is the step_response code loaded onto the Nucleo.

Our program (specifically week2.py) creates a GUI environment for plotting the experimental and simulated
first-order linear response. It runs a step response (loaded onto the Nucleo) through the Serial class and receives 
the step response results through what was printed on the Nucleo. The program then plots the results, along with the 
theoretical output (for which the step response should match). The plotted results are shown below.

![image](https://github.com/dijonm53/k_natarajan-ME-405-stuff/assets/79309467/b661d5e7-f2d8-49b8-bf25-3062d669461a)

The blue curve represents the theoretical output and the orange dotted line represents the experimental output. 
As you can see, the curves do not match. The output curve is relatively steady (on an oscilloscope, the output 
looks more like a sine wave) and does not increase at all. We believe the issue is with the wiring of the circuit.
More specifically, the electrical components. After removing various wires in different combinations and 
running the step response, the printed results didn't differ much. This even happened after running main.py, the initial
testing code. 
