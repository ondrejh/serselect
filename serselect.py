#! /usr/bin/env python3
'''\
Serial port selector.
'''

""" imports:
  os.path .. used for icon file testing
  serscan .. used for scanning ports
  tkinter .. GUI elements (mostly)"""

# local import
from serscan import scan
# general imports
from tkinter import *

class SerialSelectDialog(Frame):
    ''' Serial port selector dialog
    General description: Scans serial avaible serial ports and show it in
    radiogroup to you can select one by clicking on radio button.
    Pressing OK will close dialog - you can read selected port value by
    app.portstr.get() function.
    Pressing Scan will rescan avaible serial ports. '''
     
    def __init__(self,master=None):
        self.root = Tk()
        Frame.__init__(self, master)
        self.portlist = scan()
        self.portstr = StringVar()
        self.grid()
        self.createWidgets()
        #program icon (16x16 ico type only)
        try:
            self.master.wm_iconbitmap("icon.ico")
        except:
            try:
                self.master.iconbitmap("@icon.xbm")
                self.master.iconmask("@icon-mask.xbm")
            except:
            	print('warning: program icon error')
        #self.mainloop()

    def createWidgets(self):
        #self.frame=Frame(self)
        self.label = Label(self, text='Select serial port:')
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
        if len(self.portlist)<1:
            l = Label(self.radiogroup, text='No port found!')
            l.pack(side=TOP, expand=YES, anchor='w')
        else:
            for item in self.portlist:
                b = Radiobutton(self.radiogroup, text=item[1], variable=self.portstr, value=item[1])
                b.pack(side=TOP, expand=YES, pady=2, anchor='w')
        #place it into form
        self.radiogroup.grid(row=1,column=0,columnspan=2)

    def clickOk(self):
        #self.destroy() #this works better with idle
        self.quit() #this can confuses idle, but works
                
#testser
"""print(scan())
help(scan)"""

#testapp
"""app = SerialSelectDialog()
app.mainloop()
print(app.portstr.get())"""
