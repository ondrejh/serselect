#!/usr/bin/env python3
'''
Serial port setup gui with address (focused on modbus rtu)
'''

stdBaudrates = ('9600','19200','38400','57600','115200')
dflBaudrate = 1
strParities = ('None','Even','Odd','Mark','Space')
dflParity = 0
strStopbits = ('1','1.5','2')
dflStopbit = 2

from serscan import scan
from tkinter import *
from tkinter.ttk import *

class ModbusSetupWindow():

    def __init__(self,cfg_filename=None):
        self.cfg_filename = cfg_filename
        self.root = Tk()
        self.root.title('Configuration')
        self.root.resizable(width=False,height=False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_delete)
        self.mainframe = Frame(self.root,padding='7 7 7 7')
        self.mainframe.pack()

        self.basicFrm = LabelFrame(self.mainframe,text='Basic',padding='7 7 7 7')
        self.basicFrm.pack(fill=X)
        self.advanFrm = LabelFrame(self.mainframe,text='Advanced',padding='7 7 7 7')
        self.advanFrm.pack(fill=X)

        self.portstr = StringVar()
        self.adrstr  = StringVar()
        self.baudstr = StringVar()
        self.parstr  = StringVar()
        self.stopstr = StringVar()
        
        self.baudstr.set(stdBaudrates[dflBaudrate])

        self.pLabel = Label(self.basicFrm,text='Port')
        self.pLabel.grid(row=0,column=0,sticky='W')
        self.basicFrm.grid_columnconfigure(0,weight=1)
        self.pComboBox = Combobox(self.basicFrm,textvariable=self.portstr,justify=CENTER,font=(14))
        self.pComboBox.grid(row=0,column=1,columnspan=2,pady=5,padx=5,sticky='E')
        self.aLabel = Label(self.basicFrm,text='RTU Address')
        self.aLabel.grid(row=1,column=0,columnspan=2,sticky='W')
        self.aSpinbox = Spinbox(self.basicFrm,textvariable=self.adrstr,from_=1,to=254,width=7,justify=CENTER,font=(14))
        self.aSpinbox.grid(row=1,column=2,pady=5,padx=5,sticky='E')
        self.brLabel = Label(self.advanFrm,text='Baudrate')
        self.brLabel.grid(row=0,column=0,sticky='W')
        self.advanFrm.grid_columnconfigure(0,weight=1)
        self.brComboBox = Combobox(self.advanFrm,textvariable=self.baudstr,values=stdBaudrates,width=10,justify=CENTER)
        self.brComboBox.grid(row=0,column=1,pady=5,padx=5,sticky='E')
        self.bruLabel = Label(self.advanFrm,text='Bd')
        self.bruLabel.grid(row=0,column=2,sticky='E')
        self.parLabel = Label(self.advanFrm,text='Parity')
        self.parLabel.grid(row=1,column=0,sticky='W')
        self.parComboBox = Combobox(self.advanFrm,textvariable=self.parstr,values=strParities,state='readonly',width=10,justify=CENTER)
        self.parComboBox.current(dflParity)
        self.parComboBox.grid(row=1,column=1,pady=5,padx=5,sticky='E')
        self.stopLabel = Label(self.advanFrm,text='Stop bit(s)')
        self.stopLabel.grid(row=2,column=0,sticky='W')
        self.stopComboBox = Combobox(self.advanFrm,textvariable=self.stopstr,values=strStopbits,state='readonly',width=10,justify=CENTER)
        self.stopComboBox.grid(row=2,column=1)
        self.stopComboBox.current(dflStopbit)

        self.scanPorts()

    def scanPorts(self):

        self.portlist = scan()
        #print(self.portlist)

        if len(self.portlist):
            self.pComboBox['values']=tuple()
            for item in self.portlist:
                self.pComboBox['values']+=(item[1],)

    def on_delete(self):
        self.root.destroy()
        self.retVal = {'port_name':self.portstr.get(),
                       'rtu_addres':self.adrstr.get(),
                       'baud_rate':self.baudstr.get(),
                       'parity':self.parstr.get(),
                       'stop_bits':self.stopstr.get()}

def ModbusSetupDialog(cfg_filename=None):

    app = ModbusSetupWindow(cfg_filename)
    app.root.mainloop()
    return(app.retVal)

#run app
if __name__=="__main__":

    print(ModbusSetupDialog())
