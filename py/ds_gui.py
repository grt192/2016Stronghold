from tkinter import *
from networktables import NetworkTable
from networktables.util import ChooserControl

import logging
import sys, time, threading
logging.basicConfig(level=logging.DEBUG)


class DriverStationGUI:
	def __init__(self, win, ip):
		self.win = win
		self.ip = ip
		NetworkTable.setIPAddress(self.ip)
		NetworkTable.setClientMode()
		NetworkTable.initialize()
		self.sd = NetworkTable.getTable("SmartDashboard")
		self.cc = ChooserControl("Autonomous Mode", self.on_choices, self.on_selected)
		self.choices = None

		#self.b1 = Button(win, text="One")
		#self.b2 = Button(win, text="Two")
		#self.b1.grid(row=0, column=0)
		#self.b2.grid(row=1, column=1)
		#self.b1.configure(command=self.but1)
		self.auto_number = IntVar()

		
		#self.auto_number.trace("w", self.auto_num)




		threading.Thread(target=self.nt_loop).start()

	def load_all_widgets(self):
		self.loopback_button = Button(self.win, text="Loopback Request", command=self.request_loopback).grid(row=7, column=7)
		self.auto_label = Label(self.win, text="Auto: N/A").grid(row=8, column=8)
		self.h_lower_label = Label(self.win, text = "HLower").grid(row=0, column=1)
		self.h_lower_scale = Scale(self.win, from_=0, to=100, orient=HORIZONTAL, command=self.h_lower_readout).grid(row=1, column=1)


	def h_lower_readout(self, value):
		self.sd.putNumber("HLower", value)
		#self.h_lower_label.set("HLower: ", value)

	def auto_num(self):
		i = self.auto_number.get()
		print("Number: ", i)
		if self.choices:
			self.cc.setSelected(self.choices[i])

	def on_choices(self, choices):
		for widget in self.win.winfo_children():
			widget.destroy()
		self.load_all_widgets()
		i = 0
		self.choices = choices
		for c in choices:
			Radiobutton(self.win, text=c, variable=self.auto_number, value=i, command=self.auto_num).grid(row=i, column=0)
			i += 1

	def on_selected(self, value):
		print("Selection received: ", value)

	def request_loopback(self):
		self.auto_label.set("Auto: ", self.cc.getSelected())




	def nt_loop(self):
		while True:
			try:
				time.sleep(.1)
				print(self.sd.getValue("Autonomous Mode"))
			except KeyboardInterrupt:
				exit(0)
			except KeyError:
				pass

	def auto1(self):
		print("Button 1 pushed")
		print(self.auto_number)

	def auto2(self):
		print("Button 2 pushed")


def main():
	if len(sys.argv) != 2:
		print("Error: specify an IP to connect to!")
		exit(0)
	ip = sys.argv[1]
	win = Tk()
	ds_gui = DriverStationGUI(win, ip)
	win.mainloop()


if __name__ == "__main__":
	main()

