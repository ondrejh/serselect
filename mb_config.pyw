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
strWordlens = ('5','6','7','8')
dflWordlen = 3

try:
    from serscan import scan
except:
    from serselect.serscan import scan
    subfolder=True

import serial
    
from tkinter import *
from tkinter.ttk import *

def validate_parity_input(parity):
    if parity in ('Even','E','e','even','EVEN',serial.PARITY_EVEN):
        return 'Even'
    if parity in ('Odd','O','o','odd','ODD',serial.PARITY_ODD):
        return 'Odd'
    if parity in ('Mark','M','m','mark','MARK',serial.PARITY_MARK):
        return 'Mark'
    if parity in ('Space','S','s','space','SPACE',serial.PARITY_SPACE):
        return 'Space'
    #if parity in ('None','N','n','none','NONE',serial.PARITY_NONE,None):
    #    return 'None'
    return 'None'

class ModbusSetupDialog(simpledialog.Dialog):

    def __init__(self,parent,portsetup=(1,'COM1',19200,8,'None',2)):
        self.portsetup=portsetup
        simpledialog.Dialog.__init__(self,parent)

    def body(self,master):
        self.mainframe = Frame(master,padding='5 5 5 5')
        self.mainframe.pack()

        self.title('Serial setup')
        
        #program icon (16x16 ico type only)
        try:
            self.wm_iconbitmap("icon.ico" if not(subfolder) else "serselect/icon.ico")    
        except:
            try:
                self.iconbitmap("@icon.xbm")
                self.iconmask("@icon-mask.xbm")
            except:
                print('warning: program icon error')

        self.basicFrm = LabelFrame(self.mainframe,text='Basic',padding='5 5 5 5')
        self.basicFrm.pack(fill=X)
        self.advanFrm = LabelFrame(self.mainframe,text='Advanced',padding='5 5 5 5')
        self.advanFrm.pack(fill=X)

        self.adrstr  = StringVar()
        self.portstr = StringVar()
        self.baudstr = StringVar()
        self.wordstr = StringVar()
        self.parstr  = StringVar()
        self.stopstr = StringVar()

        try:
            self.adrstr.set(str(self.portsetup[0]))
            self.portstr.set(str(self.portsetup[1]))
            self.baudstr.set(str(self.portsetup[2]))
            self.wordstr.set(str(self.portsetup[3]))
            self.parstr.set(validate_parity_input(self.portsetup[4]))
            self.stopstr.set(str(self.portsetup[5]))
        except:
            print('warning: there is some problem with port setup - getting default')
            self.adrstr.set('1')
            self.portstr.set('COM1')
            self.baudstr.set('19200')
            self.wordstr.set('8')
            self.parstr.set('None')
            self.stopstr.set('2')

        self.pLabel = Label(self.basicFrm,text='Port')
        self.pLabel.grid(row=0,column=0,sticky='W')
        self.basicFrm.grid_columnconfigure(0,weight=1)
        self.pComboBox = Combobox(self.basicFrm,textvariable=self.portstr,justify=CENTER,font=(14))
        self.pComboBox.grid(row=0,column=1,columnspan=2,pady=3,padx=3,sticky='E')
        self.aLabel = Label(self.basicFrm,text='RTU Address')
        self.aLabel.grid(row=1,column=0,columnspan=2,sticky='W')
        self.aSpinbox = Spinbox(self.basicFrm,textvariable=self.adrstr,from_=1,to=254,width=7,justify=CENTER,font=(14))
        self.aSpinbox.grid(row=1,column=2,pady=3,padx=3,sticky='E')
        self.brLabel = Label(self.advanFrm,text='Baudrate')
        self.brLabel.grid(row=0,column=0,sticky='W')
        self.advanFrm.grid_columnconfigure(0,weight=1)
        self.brComboBox = Combobox(self.advanFrm,textvariable=self.baudstr,values=stdBaudrates,width=10,justify=CENTER)
        self.brComboBox.grid(row=0,column=1,pady=3,padx=3,sticky='E')
        self.bruLabel = Label(self.advanFrm,text='Bd')
        self.bruLabel.grid(row=0,column=2,sticky='E')
        self.bitsLabel = Label(self.advanFrm,text='Word length')
        self.bitsLabel.grid(row=1,column=0,sticky='W')
        self.bitsComboBox = Combobox(self.advanFrm,textvariable=self.wordstr,values=strWordlens,width=10,justify=CENTER,state='readonly')
        #self.bitsComboBox.current(dflWordlen)
        self.bitsComboBox.grid(row=1,column=1,pady=3,padx=3,sticky='E')
        self.bitsuLabel = Label(self.advanFrm,text='b')
        self.bitsuLabel.grid(row=1,column=2,sticky='E')
        self.parLabel = Label(self.advanFrm,text='Parity')
        self.parLabel.grid(row=2,column=0,sticky='W')
        self.parComboBox = Combobox(self.advanFrm,textvariable=self.parstr,values=strParities,state='readonly',width=10,justify=CENTER)
        #self.parComboBox.current(dflParity)
        self.parComboBox.grid(row=2,column=1,pady=3,padx=3,sticky='E')
        self.stopLabel = Label(self.advanFrm,text='Stop bit(s)')
        self.stopLabel.grid(row=3,column=0,sticky='W')
        self.stopComboBox = Combobox(self.advanFrm,textvariable=self.stopstr,values=strStopbits,state='readonly',width=10,justify=CENTER)
        #self.stopComboBox.current(dflStopbit)
        self.stopComboBox.grid(row=3,column=1,pady=3,padx=3)
        self.stopuLabel = Label(self.advanFrm,text='b')
        self.stopuLabel.grid(row=3,column=2,sticky='E')

        self.scanPorts()

        return(None)#self.aSpinbox)

    def scanPorts(self):

        self.portlist = scan()
        #print(self.portlist)

        if len(self.portlist):
            self.pComboBox['values']=tuple()
            for item in self.portlist:
                self.pComboBox['values']+=(item[1],)

    def validate(self):
        try:
            adr = int(self.adrstr.get())
            self.resstr='{}'.format(adr)
            if (adr>255) or (adr<0):
                raise ValueError('RTU address out of range')
        except:
            return False

        try:
            port = self.portstr.get()
            self.resstr+='@{}'.format(port)
            if port=='':
                raise ValueError('Port name not defined')
        except:
            return False

        try:
            baud = int(self.baudstr.get())
            self.resstr+=' {}'.format(baud)
            if (baud<1):
                raise ValueError('Baudrate value less than 1')
        except:
            return False

        try:
            word = self.wordstr.get()
            self.resstr+=' {}'.format(word)
            if word=='5':
                word = serial.FIVEBITS
            elif word=='6':
                word = serial.SIXBITS
            elif word=='7':
                word = serial.SEVENBITS
            elif word=='8':
                word = serial.EIGHTBITS
            else:
                raise ValueError('Invalid word lenght')
        except:
            return False

        try:
            par = self.parstr.get()
            if par in ('None','N','n','none','NONE',None):
                par=serial.PARITY_NONE
            elif par in ('Even','E','e','even','EVEN'):
                par=serial.PARITY_EVEN
            elif par in ('Odd','O','o','odd','ODD'):
                par=serial.PARITY_ODD
            elif par in ('Mark','M','m','mark','MARK'):
                par=serial.PARITY_MARK
            elif par in ('Space','S','s','space','SPACE'):
                par=serial.PARITY_SPACE
            else:
                raise ValueError('Invalid parity')
        except:
            return False

        try:
            stop = self.stopstr.get()
            if stop=='1':
                stop=serial.STOPBITS_ONE
            elif stop in ('1.5','1,5'):
                stop=serial.STOPBITS_ONE_POINT_FIVE
            elif stop=='2':
                stop=serial.STOPBITS_TWO
            else:
                raise ValueError('Invalid stopbit')
        except:
            return False

        self.result=(adr,port,baud,word,par,stop)
        
        return True

    def apply(self):

        self.resstr='{}@{} {} {}{}{}'.format(self.result[0],
                                             self.result[1],
                                             self.result[2],
                                             self.result[3],
                                             self.result[4],
                                             self.result[5])            

#run app
if __name__=="__main__":

    def btnClick():
        d = ModbusSetupDialog(root)
        print(d.result)
        #print(d.resstr)

    root = Tk()

    Button(root, text="Try ModbusSetup Dialog!", command=btnClick).pack()
    root.mainloop()
    
