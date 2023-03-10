import tkinter as tk
from assets import *
from ctypes import windll
import os
import pickle as pck
import math
import pickle 

#Settings
run_height = 700
run_width = 700
run_size = str(run_width) + "x" + str(run_height)
pencil_size = 1
eraser_size = 5

#Open Window
root = tk.Tk()
root.geometry(run_size)
root.title("Sketch v0")



#--------------Basic Drawing Functions---------------------

# This function colours a singular pixel on the canvas
def graphite(stroke, point, colour):
    x = point[0]
    y = point[1]
    stroke.coverage.append(Userspace.create_rectangle(x,y,x,y,fill=colour))
    stroke.coverage_points.append((x,y))
    Userboard.link_point(x,y, stroke)

# uses graphite() to colour an small area
def round_point(stroke, center, radius, colour="black"):
    for i in range(center[0]-radius,center[0]+radius+1):
        for j in range(center[1]-radius,center[1]+radius+1):
            if (i - center[0])**2 + (j - center[1])**2 <= radius**2:
                    graphite(stroke,(i,j), colour)

# uses graphite to colour a round dot
def pencil_tip(stroke, center,radius,colour="black"):
    for i in range(center[0]-radius,center[0]+radius):
        for j in range(center[1]-radius,center[1]+radius):
            graphite(stroke,(i,j), colour)

#--------------Event Handling---------------------------
# global variables are used so that events can share data
Userboard = Board(run_width,run_height)
global last_point
global pencil_mode
global stroke_record
stroke_record = Userboard.stroke_list
pencil_mode = "draw"


def on_hold_down(event):
    global last_point
    global stroke_record

    x, y = event.x, event.y
    if pencil_mode == "draw":
        
        displacement = (x - last_point[0], y - last_point[1])
        displacement_magnitude_square = displacement[0]**2 + displacement[1]**2

        if displacement_magnitude_square > 4:
            displacement_magnitude = math.sqrt(displacement_magnitude_square)
            for i in range(int(displacement_magnitude)):
                unit = (displacement[0]/displacement_magnitude, displacement[1]/displacement_magnitude)
                pencil_tip(stroke_record[-1], (int(last_point[0] + i*unit[0]), int(last_point[1] + i*unit[1])), pencil_size)
            

        pencil_tip(stroke_record[-1], (x,y), pencil_size)
        last_point = (x,y)
    elif pencil_mode == "erase":
        for i in Userboard.get_point(x,y).linked_strokes:
            if i in Userboard.get_point(x,y).linked_strokes:
                Userboard.delete_stroke(i)


def on_tap(event):
    global last_point
    global stroke_record
    x, y = event.x, event.y
    if pencil_mode == "draw":
        #create a stroke object
        stroke_record.append(Stroke("black", Userspace))

        
        last_point = (x,y)
        round_point(stroke_record[-1], (x,y), pencil_size)
    elif pencil_mode == "erase":
        for i in Userboard.get_point(x,y).linked_strokes:
            Userboard.delete_stroke(i)



def on_release(event):
    global stroke_record
    if pencil_mode == "draw":
        x, y = event.x, event.y

        round_point(stroke_record[-1], (x,y), pencil_size)

def on_erase():
    global pencil_mode
    pencil_mode = "erase"


def on_pencil():
    global pencil_mode
    pencil_mode = "draw"
    
    garbage = True
    while garbage:
        try:
            Userboard.stroke_list.remove(None)
        except:
            garbage = False

def on_debug():
    print(Userboard.stroke_list)

#def save():
#    with open('Saves\\savefile'+'.huf', 'wb') as compressed:
#        pickle.dump(Userboard, compressed)

Userspace = tk.Canvas(root, height=(run_height) - 30, width=run_width)
Userspace.grid(row=1,column=0, columnspan=5)

EraserButton = tk.Button(root, text="Eraser", font=("Arieal", 10), command=on_erase)
EraserButton.grid(row=0,column=1)
PencilButton = tk.Button(root, text="Pencil", font=("Arieal", 10), command=on_pencil)
PencilButton.grid(row=0,column=2)
DebugButton = tk.Button(root, text="Debug", font=("Arieal", 10), command=on_debug)
DebugButton.grid(row=0,column=3)
#SaveButton = tk.Button(root, text="Save", font=("Arieal", 10),command=save)
#SaveButton.grid(row=0,column=0)

Userspace.bind('<B1-Motion>', on_hold_down)
Userspace.bind('<Button-1>', on_tap)
Userspace.bind('<ButtonRelease-1>', on_release)




root.mainloop()