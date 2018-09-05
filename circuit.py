import rtmidi
import threading
import sys

midiin = rtmidi.RtMidiIn()

def print_message(midi):
	if midi.isNoteOn():
		print("ON: ", midi.getMidiNoteName(midi.getNoteNumber()), midi.getVelocity())
	elif midi.isNoteOff():
		print("OFF: ", midi.getNoteName(midi.getNoteNumber()))
	elif midi.isController():
		print("CC: ", midi.getControllerNumber(), midi.getControllerValue())

#class for accessing and handling of functions specific to the novation circuit
#listens on the assigned port and handles messages accordingly
class CircuitController(threading.Thread):
	def __init__(self, port):
		threading.Thread.__init__(self) #threading
		self.setDaemon(True) #threading
		self.port = port #the internal midi port
		self.input = None #object for rtmidiin
		self.output = None #object for rtmidiout
		self.passthrough = False #enable if the two devices are not connected outside of the computer running this software
		self.quit = False #threading

	def connect(self): #open midi port for sending and receiving data
		self.input = rtmidi.RtMidiIn()
		self.input.openPort(self.port)
		self.output = rtmidi.RtMidiOut()
		self.output.openPort(self.port)

	def run(self):
		while True:
			if self.quit:
				return
			msg = self.input.getMessage()
			if msg:
				print_message(msg)


ports = range(midiin.getPortCount())
if ports:
	selected = 0
	while selected == 0:
		for i in ports:
			if "Circuit" in midiin.getPortName(i):
				selected = i
	print("Oeffne Port ", selected)
	circuit = CircuitController(selected)
	circuit.connect()
	circuit.start()


	sys.stdin.read(1)
	circuit.quit = True
