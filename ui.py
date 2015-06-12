######################################################################################################
# A prototype GUI
######################################################################################################
import elflab.abstracts

import tkinter as tk
import tkinter.ttk as ttk

class Text:
    def __init__(self, master):
        self.master = master
        
    def start(self):
        # Map commands to methods
        valid_commands = {
                    "help": self.master.help, "h": self.master.help,
                    "pause": self.master.pause, "p": self.master.pause,
                    "resume": self.master.resume, "r": self.master.resume,
                    "stop": self.master.stop,
                    "quit": self.master.quit,
                    "plot": self.master.plot,
                    "autoscale on": self.master.autoscaleOn, "+a": self.master.autoscaleOn,
                    "autoscale off": self.master.autoscaleOff, "-a": self.master.autoscaleOff,
                    "clear plot": self.master.clearPlot,
                    "": self.master.prompt
                    }
        # Print help infomation
        self.master.help()
        # User interaction: command parsing etc.
        while not self.master.flag_quit:
            command = input().strip().lower()
            if command in valid_commands:
                valid_commands[command]()
            else:
                self.master.wrongCommand(command)                              

class PrototypeGUI(elflab.abstracts.UIBase):
    def __init__(self, master):
        self.master = master
        
    def quit(self):
        self.master.quit()
        self.root.quit()
    
    def start(self):
        self.root = tk.Tk()
        self.root.title("Galileo")
        
        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        
        self.buttonPause = ttk.Button(self.mainframe, text="pause", command=self.master.pause)
        self.buttonPause.grid(column=1, row=1, sticky=tk.W)
        
        self.buttonResume = ttk.Button(self.mainframe, text="resume", command=self.master.resume)
        self.buttonResume.grid(column=1, row=2, sticky=tk.W)
        
        self.buttonStop = ttk.Button(self.mainframe, text="stop", command=self.master.stop)
        self.buttonStop.grid(column=1, row=3, sticky=tk.W)
        
        self.buttonPlot = ttk.Button(self.mainframe, text="plot", command=self.master.plot)
        self.buttonPlot.grid(column=2, row=1, sticky=tk.W)
        
        self.buttonAutoOn = ttk.Button(self.mainframe, text="autoscale: on", command=self.master.autoscaleOn)
        self.buttonAutoOn.grid(column=2, row=2, sticky=tk.W)
        
        self.buttonAutoOff = ttk.Button(self.mainframe, text="autoscale: off", command=self.master.autoscaleOff)
        self.buttonAutoOff.grid(column=2, row=3, sticky=tk.W)
        
        self.buttonClear = ttk.Button(self.mainframe, text="clear plots", command=self.master.clearPlot)
        self.buttonClear.grid(column=2, row=4, sticky=tk.W)
        
        self.buttonQuit = ttk.Button(self.mainframe, text="quit", command=self.quit)
        self.buttonQuit.grid(column=1, row=5, sticky=tk.W)
        
        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)
        
        self.root.mainloop()
        self.master.start()