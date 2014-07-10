#! /usr/bin/env python3
'''\
Serial port selector example usage.
'''

from serselect import SerialSelectDialog

#test dialog
app = SerialSelectDialog()
app.mainloop()
portname = app.portretval.get()

if portname=='':
  print('No port selected !')
else:
  print('Port {} selected'.format(portname))
