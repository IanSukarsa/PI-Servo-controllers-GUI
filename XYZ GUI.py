## Libraries
from pipython import GCSDevice
import pipython

import numpy as np
import time
import math as ma
import tkinter as tk
from tkinter import *
from tkinter import ttk

## Goto Functions

#Up
def Up():
    if is_runningUp:
        pideviceXY.gcsdevice.MVR('1',EntryButtons.get())
        root.after(100,Up)

def on_pressUp(event):
    global is_runningUp
    is_runningUp = True
    Up()

def on_releaseUp(event):
    global is_runningUp
    is_runningUp = False

#Down
def Down():
    if is_runningDown:
        pideviceXY.gcsdevice.MVR('1',"-"+EntryButtons.get())
        root.after(100,Down)

def on_pressDown(event):
    global is_runningDown
    is_runningDown = True
    Down()

def on_releaseDown(event):
    global is_runningDown
    is_runningDown = False

#Right
def Right():
    pideviceXY.gcsdevice.RON('2',1)
    pideviceXY.gcsdevice.SVO('2',1)
    if is_runningRight:
        pideviceXY.gcsdevice.MVR('2',EntryButtons.get())
        root.after(100,Right)

def on_pressRight(event):
    global is_runningRight
    is_runningRight = True
    Right()

def on_releaseRight(event):
    global is_runningRight
    is_runningRight = False

#Left
def Left():
    if is_runningLeft:
        pideviceXY.gcsdevice.MVR('2',"-"+EntryButtons.get())
        root.after(100,Left)

def on_pressLeft(event):
    global is_runningLeft
    is_runningLeft = True
    Left()

def on_releaseLeft(event):
    global is_runningLeft
    is_runningLeft = False

#Home
def Home():
    global HomeX, HomeY
    try:
        pideviceXY.gcsdevice.MOV('1',HomeX)
        pideviceXY.gcsdevice.MOV('2',HomeY)
    except pipython.pidevice.gcserror.GCSError:
        Infotext.config(text="Error : X and/or Y axis not properly referenced (check the software)")
        

def EditWindow():
    global HomeX, HomeY, EntryEditX, EntryEditY
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Window")
    edit_window.iconbitmap("C:/Users/manip/Desktop/Ian (Alternant)/fresnel.ico")
    
    EntryEditX=tk.Entry(edit_window)
    EntryEditX.grid(row=0,column=0, sticky="nesw")
    EntryEditX.insert(0,HomeX)
    EntryEditY=tk.Entry(edit_window)
    EntryEditY.grid(row=0,column=1, sticky="nesw")
    EntryEditY.insert(0,HomeY)

    SaveButton=tk.Button(edit_window, text="Save changes", command=Save)
    SaveButton.grid(row=1,column=0)

    CloseButton=tk.Button(edit_window, text="Close", command=edit_window.destroy)
    CloseButton.grid(row=0, column=2)

    Label(edit_window, text="Consider writing down the new home for after you close the GUI").grid(row=0, column=3, sticky="W")
    

def Save():
    global HomeX, HomeY
    HomeX=EntryEditX.get()
    HomeY=EntryEditY.get()
    Label(frm,text="XY Home "+str((HomeX,HomeY))).grid(row=4, column=0)
    Infotext.config(text="XY Home changed to "+str((HomeX, HomeY)))
    
    

def closeall():
    global pideviceZ, pideviceXY
    if Zstatus :
        pideviceZ.close()
    if XYstatus :
        pideviceXY.close()
    root.destroy()

## Update Functions

def handle_focus_out(event):
    if Zstatus :
        try:
            pideviceZ.gcsdevice.MOV('Z',EntryZ.get())
            Infotext.config(text="Moved Z to "+EntryZ.get())
        except pipython.pidevice.gcserror.GCSError:
            Infotext.config(text="Error : Z position out of bounds. ([0 ; 220])")   

def update_CurrZ():
    CurrZ.config(text="Z: "+str(pideviceZ.gcsdevice.qPOS('Z')['Z'])+"μm")
    CurrZ.after(1000, update_CurrZ)

def update_CurrX():
    CurrX.config(text="X: "+str(pideviceXY.gcsdevice.qPOS('1')['1'])+"mm")
    CurrX.after(1000, update_CurrX)

def update_CurrY():
    CurrY.config(text="Y: "+str(pideviceXY.gcsdevice.qPOS('2')['2'])+"mm")
    CurrY.after(1000, update_CurrY)

## Start

def StartZ():
    #Axis Setup
    global pideviceZ, CurrZ, EntryZ,Zstatus
    pideviceZ = GCSDevice('E-709')
    try:
        pideviceZ.InterfaceSetupDlg()
        pideviceZ.gcsdevice.qPOS('Z')
    except pipython.pidevice.gcserror.GCSError:
        Infotext.config(text="Error : Select E-709 for the Z axis")
        return

    #Status Update
    Zstatus = True
    
    StartZAxis.destroy()
    CurrZ=Label(frm, text="Z: "+str(pideviceZ.gcsdevice.qPOS('Z')['Z'])+"μm")
    CurrZ.grid(column=0,row=1)
    update_CurrZ()

    EntryZ=tk.Entry(frm)
    EntryZ.grid(row=1, column=1, sticky="nesw")
    EntryZ.bind("<FocusOut>", handle_focus_out)

    Label(frm,text="μm").grid(row=1, column=2)

    

    

def StartXY():
    #Axis Setup
    global pideviceXY, CurrX, CurrY, EntryButtons
    global is_runningUp, is_runningDown, is_runningRight, is_runningLeft
    global HomeX, HomeY
    pideviceXY = GCSDevice('C-867')

    try:
        pideviceXY.InterfaceSetupDlg()
        pideviceXY.gcsdevice.qPOS('1')
    except pipython.pidevice.gcserror.GCSError:
        Infotext.config(text="Error : Select C-867 for the X & Y axis")
        return

    #Status Update
    XYstatus = True

    StartXYAxis.destroy()
    CurrX=Label(frm, text="X: "+str(pideviceXY.gcsdevice.qPOS('1')['1'])+"mm")
    CurrX.grid(row=2, column=0)
    CurrY=Label(frm, text="Y: "+str(pideviceXY.gcsdevice.qPOS('2')['2'])+"mm")
    CurrY.grid(row=3, column=0)
    update_CurrX()
    update_CurrY()
    
    #Movement initialisation
    pideviceXY.gcsdevice.RON('1',1)
    pideviceXY.gcsdevice.SVO('1',1)
    pideviceXY.gcsdevice.RON('2',1)
    pideviceXY.gcsdevice.SVO('2',1)

    #Up Button
    ButtonUp=tk.Button(frm, text="∧") 
    ButtonUp.bind('<ButtonPress-1>', on_pressUp)
    ButtonUp.bind('<ButtonRelease-1>', on_releaseUp)
    ButtonUp.grid(row=2, column=3)
    is_runningUp=False
        
    #Down Button
    ButtonDown=tk.Button(frm, text="∨")  
    ButtonDown.bind('<ButtonPress-1>', on_pressDown)
    ButtonDown.bind('<ButtonRelease-1>', on_releaseDown)
    ButtonDown.grid(row=4, column=3)
    is_runningDown=False

    #Right Button
    ButtonRight=tk.Button(frm, text=">") 
    ButtonRight.bind('<ButtonPress-1>', on_pressRight)
    ButtonRight.bind('<ButtonRelease-1>', on_releaseRight)
    ButtonRight.grid(row=3, column=4)
    is_runningRight=False

    #Left Button
    ButtonLeft=tk.Button(frm, text="<")
    ButtonLeft.bind('<ButtonPress-1>', on_pressLeft)
    ButtonLeft.bind('<ButtonRelease-1>', on_releaseLeft)
    ButtonLeft.grid(row=3, column=2)
    is_runningLeft=False

    #Step
    Label(frm,text="XY Step (mm):").grid(row=2, column=1)
    EntryButtons=tk.Entry(frm)
    EntryButtons.grid(row=3, column=1, sticky="nesw")
    EntryButtons.insert(0,"0.01")

    #Home Button
    HomeX, HomeY= 0,0
    Label(frm,text="XY Home "+str((HomeX,HomeY))).grid(row=4, column=0)
    ButtonHome=tk.Button(frm, text="⌂", command=Home)
    ButtonHome.grid(row=4, column=1)

    #Edit Home Button
    ButtonEdit=tk.Button(frm, text="Edit ⌂", command=EditWindow)
    ButtonEdit.grid(row=5, column=0)
    

#Tkinter window setup
root = tk.Tk()
root.title("XYZ GUI")
root.iconbitmap("C:/Users/manip/Desktop/Ian (Alternant)/fresnel.ico")
frm = ttk.Frame(root, padding=10)
frm.grid(row=0, column=0, sticky="nsew")
frm.grid()
frm.grid_rowconfigure(0, weight=1)
frm.grid_columnconfigure(0, weight=1)
frm.grid_columnconfigure(1, weight=1)

#Infotext setup
Infotext=Label(frm, text="Welcome !")
Infotext.grid(column=0, row=0)

#Axis setup
XYstatus = False
Zstatus = False

StartZAxis=Button(frm, text="Start Z axis (E-709)", command=StartZ)
StartZAxis.grid(column=0, row=1)

StartXYAxis=Button(frm, text="Start X & Y axis (C-867)", command=StartXY)
StartXYAxis.grid(column=0, row=2)

Quit=Button(frm, text="Quit", command=closeall)
Quit.grid(column=10, row=1)



root.mainloop()
