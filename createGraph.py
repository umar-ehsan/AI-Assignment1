''' Some starter code for your A* search '''

# for GUI things
import tkinter as tk
# for parsing XML
import xml.etree.ElementTree as ET
# for math
import math
import struct

# some constants about the earth
MPERLAT = 111000 # meters per degree of latitude, approximately
MPERLON = MPERLAT * math.cos(42*math.pi/180) # meters per degree longitude at 42N

WINWIDTH = 500
WINHEIGHT = 500

class MyWin(tk.Frame):
    '''
    Here is a Tkinter window with a canvas, a button, and a text label
    It also includes a callback (event handler) on the button and one
    on the canvas itself.
    '''
    def __init__(self,master,line,circle):
        '''
        you probably want to pass in your own data structures, but this shows
        how to draw a line and a circle in the canvas, and also add widgets
        
        args:
           master: the Tk master object
           line: a line that gets drawn
           circle: a circle that gets drawn
        '''
        thewin = tk.Frame(master)
        w = tk.Canvas(thewin, width=WINWIDTH, height=WINHEIGHT, cursor="crosshair")

        # callbacks for mouse events in the window, if you want:
        w.bind("<Button-1>", self.mapclick)
        #w.bind("<Motion>", self.maphover)

        # do whatever you need to do for this, lines are just defined by four pixel values
        # x1 y1 x2 y2 (and can continue x3 y3 ...)
        w.create_line(line[0], line[1], line[2], line[3])

        w.create_line(20,20,40,40,30,60,70,90)
        
        # same for circles (ovals), give the bounding box - for both circles and lines
        # we can pass in a tuple directly for the coordinates.
        w.create_oval(circle, outline='blue',fill='green',tag='greendot')
        # by giving it a tag we can easily poke it later (see callback)

        w.pack(fill=tk.BOTH) # put canvas in window, fill the window

        self.canvas = w # save the canvas object to talk to it later

        cb = tk.Button(thewin, text="Button", command=self.click)
        # put the button in the window, on the right
        # I really have not much idea how Python/Tkinter layout managers work
        cb.pack(side=tk.RIGHT,pady=5)

        thewin.pack()

    def click(self):
        '''
        Callback for the button.
        '''
        print ("Clicky!")

    def mapclick(self,event):
        ''' 
        Callback for clicking on the canvas, click location is used
        to redraw the circle at the location of the click

        args:
           event: click event, includes the x,y location of the click
        '''
        self.canvas.coords('greendot',event.x-5,event.y-5,event.x+5,event.y+5)

'''
Here are some other functions we will need:
'''

def read_elevations(filename):
    ''' This reads in an HGT file of elevation data.  
    It is a little tricky since the file is a series of 
    raw 2-byte signed shorts.
    
    args: filename - the name of an HGT file
    '''
    
    efile = open(filename, "rb")
    estr = efile.read()
    elevs = []
    for spot in range(0,len(estr),2):
        # this magic builds a list of values (1-d, not 2-d!) and deals with the
        # fact that the data file is given in big-endian format which is unusual these days...
        # you may of course load this into some other data structure as you see best
        elevs.append(struct.unpack('<h',estr[spot:spot+2])[0])
    print("Elevations:")
    for elevation in elevs:
        print(elevation)
        #input()

def read_xml(filename):
    '''
    This function reads in a piece of OpenStreetMap XML and prints
    out all of the names of all of the "ways" (linear features).
    You should replace the print with something that adds the way
    to a data structure useful for searching.
    '''
    tree = ET.parse(filename)
    root = tree.getroot()

    for item in root:
        # we will need nodes and ways, here we look at a way:
        if item.tag == 'way':
            # in OSM data, most info we want is stored as key-value pairs
            # inside the XML element (not as the usual XML elements) -
            # so instead of looking for a tag named 'name', we look for a tag
            # named 'tag' with a key inside it called 'name'
            for subitem in item:
                if subitem.tag == 'tag' and subitem.get('k') == 'name':
                    # also note names are Unicode strings, depends on your system how
                    # they will look, I don't care too much.
                    print ("Name is " +  subitem.get('v'))
                    break

def main():
    read_xml("map.osm")

    master = tk.Tk()
    line = (60,10,70,20)
    circle = (120,150,130,160)
    #thewin = MyWin(master,line,circle)
    MyWin(master,line,circle)

    read_elevations("n43_w114_1arc_v2.bil")
    # in Python you have to start the event loop yourself:
    tk.mainloop()

if __name__ == "__main__":
    main()
    
