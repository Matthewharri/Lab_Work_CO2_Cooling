# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
## Signs on W (in T2 and T3) and Temp Diff sign, graphical interface
## Comment 1


import tkinter as Tk
from tkinter import Button
from tkinter import Frame
from tkinter import Label
from tkinter import *

#modification
#secondone



## Measured values
c_CO2 = 1.9 * 10**3 #J/(kg*K)*10**3
c_H2O = 4185.5   #J/(kg*K)



T_H2O_In = 10.
T_H2O_Out = 15.
T_CO2_In = 4.
DP_H2O = 1.
P_CO2 = 1.
CO2_Flow = 4.*10**-3 #kg/s       ####INPUT!
H2O_Flow = 50.*10**-3 #kg/s ?????
V =  24. #V


Resistivity_al = 0.008 #W/m K  ### thermal resistivity of aluminum

## Function Values 
Desired_CO2_Temp = -4 ####float(input('Enter Out Temp: '))
T_CO2_Out= 4. ##temporary! #####Measured Value!
W=1. ##temp again probably measured value
I=1. ## Measured Value 

## Simplifying Temp Differences
dT_CO2 = (T_CO2_Out - T_CO2_In)
dT_H2O = (T_H2O_Out - T_H2O_In)


#Function of Flow
def R_Plate(flow1):     ## flow1 -g/s  flow2 -g/min
    flow2 = flow1 * 60.
    return 0.0157 - 0.0099*flow2 + 0.0047*flow2**2

#Calculations
## Everything with underscore at end is dynamic (eg variable_)
def Power(Desired_CO2_Temp_):
    return c_CO2 * CO2_Flow * (T_CO2_In - Desired_CO2_Temp_)

W = Power(Desired_CO2_Temp) 
print(W)

def Current(dT_):    ### current fit function
    return ((0.11*dT_-25.2) + ((25.2-0.11*dT_)*(25.2-0.11*dT_)+4*(-0.77+0.002*dT_)*(1.825*dT_+W))**(1/2))/(2*(0.002*dT_-0.77)) 

def H2O_Flow_(I_):
    return (W + V*I_)/(c_H2O * dT_H2O)


# Temperature of CO2 in bottom plate
def T6(T_CO2_Out_):
    return (T_CO2_In + T_CO2_Out_)/2

# Temperature of bottom plate (pump-side) in contact with CO2
def T5(T6_):
    R_Plate_ = R_Plate(CO2_Flow)
    return R_Plate_ * (-W) + T6_

# Temperature between bottom plate and aluminum
def T4(T5_):
    return ((Resistivity_al * 0.009525) /0.0508**2)* (-W) + T5_

#Temperature between top plate and aluminum
def T3(T2_, I_):
    return ((Resistivity_al * 0.009525) /0.0508**2)*(W + V*I_) + T2_

# Temperature of top plate (pump-side) in contact with H2O
def T2(T1_, I_, H2O_Flow_):
    R_Plate_ = R_Plate(H2O_Flow_)
    return R_Plate_ * (W + V*I_) + T1_

# Temperature of H2O in top plate
def T1(T_H2O_Out_):
    return (T_H2O_In + T_H2O_Out_)/2





#Future While Loop
while T_CO2_Out > Desired_CO2_Temp:
    
    Temp_6 = T6(T_CO2_Out)
    Temp_5 = T5(Temp_6)
    Temp_4 = T4(Temp_5)
    
    Temp_1 = T1(T_H2O_Out)
    
    H2O_Flow = H2O_Flow_(I)
    
    Temp_2 = T2(Temp_1, I, H2O_Flow)
    Temp_3 = T3(Temp_2, I)
    
    Temp_Diff = Temp_3 - Temp_4
    
    I = Current(Temp_Diff)
    
    T_CO2_Out = T_CO2_Out - 0.2
    ## print (T_CO2_Out, I, Temp_Diff, Temp_6, Temp_5, Temp_4, Temp_3, Temp_2, Temp_1)

print('Done!')


##2x2x(3/8)


root = Tk()


def Quit():
    root.destroy()
    


CO2_In_Label = Label(root, text="Temp of CO2 In:").grid(row=0,sticky=E)
CO2_In_Display = Label(root, text=T_CO2_In).grid(row=0, column=1)


CO2_Out_Label = Label(root, text="Temp of CO2 Out:").grid(row=1,sticky=E)
CO2_Out_Display = Label(root, text=T_CO2_Out).grid(row=1, column=1)

H2O_In_Label = Label(root, text="Temp of H2O In:").grid(row=2,sticky=E)
H2O_In_Display = Label(root, text=T_H2O_In).grid(row=2, column=1)


H2O_Out_Label = Label(root, text="Temp of H2O Out:").grid(row=3,sticky=E)
H2O_Out_Display = Label(root, text=T_H2O_Out).grid(row=3, column=1)

Current_Label = Label(root, text="DP_H2O:").grid(row=4, sticky=E)
Current_Display = Label(root, text=DP_H2O).grid(row=4, column=1)

Current_Label = Label(root, text="P_CO2:").grid(row=5, sticky=E)
Current_Display = Label(root, text=P_CO2).grid(row=5, column=1)

Current_Label = Label(root, text="CO2_Flow:").grid(row=6, sticky=E)
Current_Display = Label(root, text=CO2_Flow).grid(row=6, column=1)

Current_Label = Label(root, text="Current:").grid(row=7, sticky=E)
Current_Display = Label(root, text=I).grid(row=7, column=1)

QUIT = Button(root, text="Close", bg="red", fg="white", command=Quit).grid(row=8, column=4)


mainloop()
