#! /usr/bin/python

# OSX only!
# Terminal needs to be added to privacy in OSX to register keys!

# TODO exit doesn't work
# TODO test middle button with mouse
# TODO capture special keys (brightness, etc) + caps lock

# To debug: copy script and set debug
debug = False
if debug:
	ruta = "/Users/malfonso/test/counter/debug/"
else:
	ruta = "/Users/malfonso/test/counter/keys/"

from Foundation import NSObject
from AppKit import NSApplication, NSApp
from Cocoa import (
    NSEvent, 
    NSKeyUp, NSKeyUpMask,
    NSLeftMouseDown, NSLeftMouseDownMask,
    NSRightMouseDown, NSRightMouseDownMask,
    NSOtherMouseDown, NSOtherMouseDownMask,
    NSFlagsChanged, NSFlagsChangedMask,
    NSApplicationActivationPolicyProhibited
)

from Cocoa import (
	NSAlphaShiftKeyMask, 
	NSShiftKeyMask,
	NSControlKeyMask,
	NSAlternateKeyMask,
	NSCommandKeyMask,
	NSNumericPadKeyMask,
	NSHelpKeyMask,
	NSFunctionKeyMask,
	NSDeviceIndependentModifierFlagsMask
)

from PyObjCTools import AppHelper
import signal, sys, time
from datetime import datetime

# file: year-month-day.key
# formato: hour, minute, keys, total.clicks, left.clicks, right.clicks, middle.clicks

keys = 0 + 1
	
lastDate = datetime.now()
left = right = middle = 0
flags = 0
modifier_mask = (
	NSAlphaShiftKeyMask | 
	NSShiftKeyMask | 
	NSControlKeyMask | 
	NSAlternateKeyMask | 
	NSCommandKeyMask | 
	NSNumericPadKeyMask | 
	NSHelpKeyMask | 
	NSFunctionKeyMask
)

def onEvent(event):
	global keys, left, right, middle, lastDate, flags, modifier_mask
	date = datetime.now()
	
	if (date.minute != lastDate.minute or date.hour != lastDate.hour or 
			date.day != lastDate.day): 
		clear()
		keys = left = right = middle = 0
		lastDate = date

	event_type = event.type()
	if  event_type == NSKeyUp:
		# could be down with key down and checking repeat field
		keys += 1
		if debug: print "KEY UP"
	elif event_type == NSLeftMouseDown or event_type == NSOtherMouseDown:
		left += 1
		if debug: print "LEFT DOWN"
	elif event_type == NSRightMouseDown: 
		right += 1
		if debug: print "RIGHT DOWN"
	elif event_type == NSFlagsChanged:
		new_flags = event.modifierFlags() & modifier_mask
		if ~flags & new_flags:
			keys += 1
			if debug: print "MODIF DOWN"
		flags = new_flags
	else:
		print event
		assert False

def clear(exit=False):
	if debug: print "writing"
	global keys, left, right, middle, lastDate

	archivo = open("%s%d-%02d-%02d.key" % 
		(ruta, lastDate.year, lastDate.month, lastDate.day), "a")
	string = '%3d,%3d,%3d,%3d,%3d,%3d,%3d\n' % (lastDate.hour, lastDate.minute, 
		keys, left+right+middle, left, right, middle)

	if exit: string += "# EXIT!\n"

	archivo.write(string)
	archivo.close()

def onExit(sig, func=None):
	clear(True)

def createAppDelegate():
	class AppDelegate(NSObject):
		def applicationDidFinishLaunching_(self, notification):
			mask = (NSKeyUpMask |
					NSLeftMouseDownMask |
					NSRightMouseDownMask |
					NSOtherMouseDownMask | 
					NSFlagsChangedMask)
			NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(mask, onEvent)

		def applicationWillResignActive(self, notification):
			self.applicationWillTerminate_(notification)
			return True

		def applicationShouldTerminate_(self, notification):
			self.applicationWillTerminate_(notification)
			return True

		def applicationWillTerminate_(self, notification):
			if debug: print("Exiting")
			clear(True)
			return None

	return AppDelegate

# TODO remove this and make loop work
time.sleep(30)

assert sys.platform == "darwin"
try_again = True

# Try every 5 seconds until WindowServer is up
while try_again:
	try:
		NSApplication.sharedApplication()
		delegate = createAppDelegate().alloc().init()
		NSApp().setDelegate_(delegate)
		NSApp().setActivationPolicy_(NSApplicationActivationPolicyProhibited)
		def handler(signal, frame):
			if debug: print "exit handler"
			onExit(signal)
			AppHelper.stopEventLoop()
		signal.signal(signal.SIGTERM, handler)
		signal.signal(signal.SIGINT, handler)
		signal.signal(signal.SIGHUP, handler)
		signal.signal(signal.SIGABRT, handler)
		AppHelper.runEventLoop()
		try_again = False
	except Exception as e:
		print "try failed"
		print e
		time.sleep(5)

