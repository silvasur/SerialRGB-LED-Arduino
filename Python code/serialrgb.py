#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial

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
	
	def __del__(self):
		self.close_connection()
	
	def change_color(self, color):
		"""
		Send a colot to the Arduino.
		
		color - 3-Tuple representing an RGB-Color (color components must be in range 0 - 255).
		"""
		r, g, b = color
		self.ser.write(chr(r) + chr(g) + chr(b))
	
	def close_connection(self):
		"""Closes the connection to the Arduino."""
		if self.ser is not None:
			self.ser.close()
			self.ser = None
