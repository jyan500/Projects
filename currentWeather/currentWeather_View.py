# currentWeather_View
from currentWeather import main
from currentWeather import decode_picture
import tkinter
from tkinter import ttk
from datetime import date

class ForeCast:
    
    def __init__(self, info):
        
        self._info = info
        self._top = tkinter.Toplevel()
        convert = { 'Monday' : 0, 'Tuesday' : 2, 'Wednesday' : 4, 
                   'Thursday' : 6, 'Friday' : 8, 
                   'Saturday' : 10, 'Sunday' : 12}
        
        self._label1 = ttk.Label(master = self._top, text = '3-Day Forecast')
        self._label1.pack()
        new_dict = {}
        for item in self._info:
            if type(item) is dict:
                for d in item:
                    if d in convert:
                        new_dict[d] = item[d]
        for item in sorted(new_dict, key = lambda x: new_dict[x]["period"]):
            
            self._label_left = ttk.Label(master = self._top, text = item)
            img2 = tkinter.PhotoImage(data = decode_picture(new_dict[item]["icon"]))
            self._label_image = ttk.Label(master = self._top, image = img2)
            self._label_image.image2 = img2
            self._label_right = ttk.Label(master = self._top, text = new_dict[item]["forecast"])
            self._label_left.pack()
            self._label_image.pack()
            self._label_right.pack()
            
        self._button = ttk.Button(master = self._top, text = "OK, return to main screen",
                                      command = self.destroy)
        self._button.pack()

        

        
    def show(self):
        
        self._top.grab_set()
        self._top.wait_window()

    def destroy(self):
        
        self._top.destroy()
        
class TopLevel:
    
    def __init__(self):
        ''' The entry bars ''' 
        self._top = tkinter.Toplevel()
        self._label1 = ttk.Label(master = self._top, text = 'Please enter City and State')
        
        self._city = tkinter.StringVar()
        self._state = tkinter.StringVar()

        self._label2 = ttk.Label(master = self._top, text = "City")
        self._label3 = ttk.Label(master = self._top, text = "State")
        self._entry = ttk.Entry(master = self._top, textvariable = self._city)
        self._entry2 = ttk.Entry(master = self._top, textvariable = self._state)
        self._button1 = ttk.Button(master = self._top, text = 'OK', command = self.getText)
        self._button2 = ttk.Button(master = self._top, text = 'Cancel',
                                      command = self.destroy)
        
        self._label1.grid(row = 0, column = 1)
        self._label2.grid(row = 1)
        self._entry.grid(row = 1, column = 1)
        self._label3.grid(row = 2)
        self._entry2.grid(row = 2, column = 1)
        self._button1.grid(row = 3, column = 0)
        self._button2.grid(row = 3, column = 1)
        self._button_clicked = False
        
    def getText(self):
        ''' boolean value becomes true, and the top level object is destroyed ''' 
        self._button_clicked = True
        self.destroy()

    def show(self):
        
        self._top.grab_set()
        self._top.wait_window()

    def destroy(self):
        
        self._top.destroy()
        
class Application:
    
    def __init__(self):
        
        self._window = tkinter.Tk()
        
        self._str1 = tkinter.StringVar()
        self._str2 = tkinter.StringVar()
        self._str3 = tkinter.StringVar()
        self._str4 = tkinter.StringVar()

        
        self._str1.set("No location Set")
        self._str2.set("")
        self._str3.set("")
        self._str4.set("")
        
        self.city = None
        self.state = None
        img64 = decode_picture("http://icons.wxug.com/i/c/k/nt_partlycloudy.gif")
        self._image_link = tkinter.PhotoImage(data = img64)
        self._info = None
        self._did_show = False

        self._button = ttk.Button(master = self._window, text = 'Press to Update')
        self._button2 = ttk.Button(master = self._window, text = 'Refresh')
        self._button3 = ttk.Button(master = self._window, text = 'Press to see forecast')
        self._button.bind('<Button-1>', self.trigger)
        self._button2.bind('<Button-1>', self.refresh)
        self._button3.bind('<Button-1>', self.forecast)
        
        self._label1 = tkinter.Label(master = self._window, text = 'Welcome to the Weather Program')
        self._label2 = tkinter.Label(master = self._window, textvariable = self._str1,
                                     highlightthickness = 10, padx = 5, pady = 5)
        self._label3 = tkinter.Label(master = self._window, textvariable = self._str2)
        self._label4 = tkinter.Label(master = self._window, textvariable = self._str3)
        self._label5 = tkinter.Label(master = self._window, textvariable = self._str4)
        self._label6 = tkinter.Label(master = self._window, image = self._image_link)
        
        self._label1.pack()
        self._label6.pack()
        self._label2.pack()
        self._label3.pack()
        self._label4.pack()
        self._label5.pack()
        
        self._button.pack()
        self._button2.pack()
        self._button3.pack()
        
  
    def run(self):
        
        self._window.mainloop()

    def trigger(self, event: tkinter.Event):
        ''' when button is clicked, toplevel is shown ''' 
        t = TopLevel()
        t.show()
        if t._button_clicked == True:
            self._did_show = True
            self.city = t._city.get()
            self.state = t._state.get()
            self._info = main(self.state, self.city)
            self.update()

    def update(self):
        ''' updates the label information with entry information from TopLevel '''
        if self._did_show == True:
            for item in self._info:
                if type(item) is tuple:
                    self._str1.set(item[0])
                    self._str2.set(item[1])
                    self._str3.set(item[2])
                    self._str4.set(item[3])


    def refresh(self, event: tkinter.Event):
        ''' if update has been pressed once, the app can be updated by re-requesting url information '''
        if self._did_show == True:
            self._info = main(self.state, self.city)
            self.update()

    def forecast(self, event: tkinter.Event):
        if self._did_show == True:
            f = ForeCast(self._info)
            f.show()
        
        
                    
                
            
            
        

    
        
if __name__ == "__main__":
    d = date.today()
    new_d = date(d.year, d.month, d.day + 1)                      
    a = Application()
    a.run()
