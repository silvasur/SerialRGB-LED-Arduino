#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial, time

class SyncError(Exception):
	"""Synchronisation error"""
	def __init__(self, msg=""):
		self._msg = str(msg)
	
	def __str__(self):
		return msg

class SerialRGB(object):
	"""Easy controlling of the RGB-LED / Arduino"""
	def __init__(self, addr, baud=9600):
		"""
		Creating a new SerialRGB object.
		
		addr -- The address of the serial port.
		baud -- The baudrate (default: 9600)
		"""
		try:
			self.ser = serial.Serial(addr, baud)
		except:
			raise IOError("Could not connect to Arduino via serial port.")
		# Sync...
		while self.ser.inWaiting() < 1:
			self.ser.write("\x00")
			time.sleep(.01)
		if self.ser.read(1) != "1":
			raise SyncError
	
	def __del__(self):
		self.close_connection()
	
	def change_color(self, color):
		"""
		Send a colot to the Arduino.
		
		color - 3-Tuple representing an RGB-Color (color components must be in range 0 - 255).
		"""
		r, g, b = color
		self.ser.write(chr(r) + chr(g) + chr(b))
		if self.ser.read(1) != "1":
			raise SyncError
	
	def close_connection(self):
		"""Closes the connection to the Arduino."""
		if self.ser is not None:
			self.ser.close()
			self.ser = None
