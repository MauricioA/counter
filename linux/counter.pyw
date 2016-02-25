#! /usr/bin/python

import os, sys
from datetime import datetime
if os.name == "nt":
	import win32con, win32api, win32gui, pythoncom, pyHook
else:
	import pyxhook as pyHook

# TODO schedule backups
# TODO statistics

# Solo para linux!!
# requiere pyxhook.py, pyHook (1.5.1) and Xlib
# file: year-month-day.key
# formato: hour, minute, keys, total.clicks, left.clicks, right.clicks, middle.clicks

debug = False

if os.name == "nt":
	if debug:
		ruta = "C:\\Archivos\\test\\hook\\keys\\debug\\"
	else:
		ruta = "C:\\Archivos\\test\\hook\\keys\\"
	keys = 0
else:
	if debug:
		ruta = "/usr/local/google/home/malfonso/.counter/debug/"
	else:
		ruta = "/usr/local/google/home/malfonso/.counter/"
	keys = 0 + 0 + 2
	
lastDate = datetime.now()
left = right = middle = 0

def onEvent(event):
	global keys, left, right, middle, lastDate
	date = datetime.now()
	
	if date.minute != lastDate.minute or date.hour != lastDate.hour or \
			date.day != lastDate.day: 
		clear()
		keys = left = right = middle = 0
		lastDate = date

	if os.name == "nt":
		if   event.Message == 257: keys   += 1
		elif event.Message == 513: left   += 1
		elif event.Message == 516: right  += 1
		elif event.Message == 519: middle += 1
		if debug: print event.Message
	else:
		if   event.MessageName == "key up": 		    keys 	+= 1
		elif event.MessageName == "mouse left down": 	left 	+= 1
		elif event.MessageName == "mouse middle down": 	middle	+= 1
		elif event.MessageName == "mouse right down": 	right 	+= 1
		if debug: print event.MessageName

def clear(exit = False):
	global keys, left, right, middle, lastDate

	if os.name == "nt": att = "a+"
	else: att = "a"
	archivo = open("%s%d-%02d-%02d.key" % 
		(ruta, lastDate.year, lastDate.month, lastDate.day), att)

	string = '%3d,%3d,%3d,%3d,%3d,%3d,%3d\n' % (lastDate.hour, lastDate.minute, 
		keys, left+right+middle, left, right, middle)

	if exit: string += "# EXIT!\n"

	archivo.write(string)
	archivo.close()

def wndproc(hwnd, msg, wparam, lparam):
	if msg == 17: clear(True)

def onExit(sig, func=None):
	clear(True)

# solo para linux
def setExitHandler(func): 
	import signal
	signal.signal(signal.SIGTERM, func)
	signal.signal(signal.SIGINT, func)
	signal.signal(signal.SIGHUP, func)
	signal.signal(signal.SIGABRT, func)

def exitAtexit():
	clear(True)

if os.name == "nt":
	hinst = win32api.GetModuleHandle(None)
	wndclass = win32gui.WNDCLASS()
	wndclass.hInstance = hinst
	wndclass.lpszClassName = "testWindowClass"
	messageMap = {	
		win32con.WM_QUERYENDSESSION : wndproc,
		win32con.WM_ENDSESSION : wndproc,
		win32con.WM_QUIT : wndproc,
		win32con.WM_DESTROY : wndproc,
		win32con.WM_CLOSE : wndproc,
	}
	wndclass.lpfnWndProc = messageMap
	myWindowClass = win32gui.RegisterClass(wndclass)
	hwnd = win32gui.CreateWindowEx(
		win32con.WS_EX_LEFT, myWindowClass, "test", 
		0, 0, 0, win32con.CW_USEDEFAULT, 
		win32con.CW_USEDEFAULT, # win32con.HWND_MESSAGE, 
		0, 0, hinst, None
	)
else:
	setExitHandler(onExit)
	import atexit
	atexit.register(exitAtexit)

hookManager = pyHook.HookManager()
hookManager.HookKeyboard()
hookManager.KeyUp = onEvent
hookManager.MouseAllButtonsDown = onEvent
hookManager.HookMouse()

if os.name == "nt": 
	pythoncom.PumpMessages()
else: 
	hookManager.start()
