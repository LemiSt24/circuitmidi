import rtmidi
import threading
import sys

midiin = rtmidi.RtMidiIn()

circuit = None
bcf2000 = None

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

	def handleMessage(self, msg):
		if msg.isController(): #ignoring note and timing messages for now
			if self.passthrough:
				bcf2000.output.sendMessage(msg)	#send message to BCF2000
		elif msg.isSysEx():
			patchData = self.unpackPatch(msg)
			#send patch data to BCF2000
	def unpackPatch(self, msg):
		return None

	def run(self):
		while True:
			if self.quit:
				return
			msg = self.input.getMessage() #listens for messages
			if msg:
				self.handleMessage(msg)
				#print_message(msg)

class BCFController(threading.Thread):
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

	def handleMessage(self, msg):
		if msg.isController(): #ignoring note and timing messages for now
			if self.passthrough:
				circuit.output.sendMessage(msg) #send message to circuit

	def run(self):
		while True:
			if self.quit:
				return
			msg = self.input.getMessage() #listens for messages
			if msg:
				self.handleMessage(msg)
				#print_message(msg)


ports = range(midiin.getPortCount())
if ports:
	circuitport = 0
	bcfport = 0
	while circuitport == 0 and bcfport == 0:
		for i in ports:
			if "Circuit" in midiin.getPortName(i):
				circuitport = i
			if "BCF2000" in midiin.getPortName(i):
				bcfport = i

	circuit = CircuitController(circuitport)
	circuit.connect()
	circuit.start()

	bcf2000 = BCFController(bcfport)
	bcf2000.connect()
	bcf2000.start()

	sys.stdin.read(1)
	circuit.quit = True
