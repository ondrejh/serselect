#! /usr/bin/env python3
'''\
Serial port selector.
'''

from serscan import scan
from tkinter import *

class SerialSelectDialog(Frame):
    def __init__(self,master=None):
        Frame.__init__(self, master)
        self.portlist = scan()
        self.portstr = StringVar()
        self.grid()
        self.createWidgets()
        #self.mainloop()

    def createWidgets(self):
        #self.frame=Frame(self)
        self.label = Label(self, text='Serial ports found:')
        self.label.grid(row=0,column=0,columnspan=2)
        # create radio group
        self.fillList()
        # crete scan button
        self.scanbutton = Button(text='Scan',command=self.clickScan)
        self.scanbutton.grid(row=2,column=0,sticky=W+E)
        # create ok button
        self.okbutton = Button(text='Ok',command=self.clickOk)
        self.okbutton.grid(row=2,column=1,sticky=W+E)

    def clickScan(self):
        #delete old radiogroup
        self.radiogroup.grid_forget()
        self.radiogroup.destroy()
        #scan for serial ports
        self.portlist = scan()
        #create new list
        self.fillList()
        
    def fillList(self):
        #create list of serial ports from portlist
        self.radiogroup = Frame()
        for item in self.portlist:
            b = Radiobutton(self.radiogroup, text=item[1], variable=self.portstr, value=item[1])
            b.pack(side=TOP, expand=YES, pady=2, anchor='w')
        #place it into form
        self.radiogroup.grid(row=1,column=0,columnspan=2)

    def clickOk(self):
        #exit application
        self.destroy()
                
#testser
"""print(scan())
help(scan)"""

#testapp
"""app = SerialSelectDialog()
app.mainloop()
print(app.portstr.get())"""
