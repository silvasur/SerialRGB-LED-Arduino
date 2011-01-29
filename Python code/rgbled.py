#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import wx, math
from wx.lib.colourchooser.pycolourchooser import PyColourChooser
from serialrgb import SerialRGB

def hsv2rgb(h, s, v):
	h *= 360.0
	hi = math.floor(h / 60)
	f = (h / 60) - hi
	p = v * (1 - s)
	q = v * (1 - s * f)
	t = v * (1 - s * (1 - f))
	if hi == 0 or hi == 6:
		return (v, t, p)
	elif hi == 1:
		return (q, v, p)
	elif hi == 2:
		return (p, v, t)
	elif hi == 3:
		return (p, q, v)
	elif hi == 4:
		return (t, p, v)
	else:
		return (v, p, q)

def rgb2hsv(r, g, b):
	minimum = min([r, g, b])
	maximum = max([r, g, b])
	if maximum == minimum:
		h = 0
	elif maximum == r:
		h= 60 * (0 + ((g - b) / (maximum - minimum)))
	elif maximum == g:
		h= 60 * (2 + ((b - r) / (maximum - minimum)))
	else:
		h= 60 * (4 + ((r - g) / (maximum - minimum)))
	if h < 0:
		h += 360
	s = 0 if maximum == 0 else ((maximum - minimum) / maximum)
	return (h / 360.0, s, maximum)

class rgbled_frame(wx.Frame):
	def __init__(self, rgbled):
		wx.Frame.__init__(self, None, title="RGBLED", size=(500, 300))
		self.rgbled = rgbled
		
		mainpanel = wx.Panel(self, -1)
		
		self.cpctrl = PyColourChooser(mainpanel, -1)
		self.cpctrl.SetValue(wx.Colour(0,0,0,255))
		
		self.timer = wx.Timer(self)
		
		self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
		self.timer.Start(100)
	
	def on_timer(self, evt):
		colour = self.cpctrl.GetValue()
		r = colour.Red()
		g = colour.Green()
		b = colour.Blue()
		if isinstance(self.rgbled, SerialRGB):
			self.rgbled.change_color((r, g, b))

class rgbled_app(wx.App):
	def OnInit(self):
		self.rgbled = None
		portdlg = wx.TextEntryDialog(None, "Serial port:")
		if portdlg.ShowModal() == wx.ID_OK:
			self.rgbled = SerialRGB(portdlg.GetValue())
			frame = rgbled_frame(self.rgbled)
			portdlg.Destroy()
			frame.Show()
			self.SetTopWindow(frame)
		return True
	def OnExit(self):
		if isinstance(self.rgbled,SerialRGB):
			self.rgb2hsv.close_connection()

if __name__ == '__main__':
	myapp = rgbled_app()
	myapp.MainLoop()
