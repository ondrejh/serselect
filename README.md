serselect: serial port selector
===============================

description: Scann and select serial port with GUI

![My image](https://raw.githubusercontent.com/ondrejh/serselect/master/screenshot.png)

name: serselect

language: python3

targets (tested): linux, w7

author: ondrejh.ck@email.cz

serscan.py :
  scan() function scans avaible serial ports and return list of id touples.
  return structure: [(portnumber 1, portname 1) ..,(portnumber n, portname n)]
  
serselect.pyw :
  SerialSelectDialog application is a GUI to select serial port. It uses scan().

example.py :
  Test script - runs SerialSelectDialog and print selected port value.
