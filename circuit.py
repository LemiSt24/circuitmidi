import rtmidi

midiin = rtmidi.RtMidiIn()

def print_message(midi):
	if midi.isNoteOn():
		print("ON: ", midi.getMidiNoteName(midi.getNoteNumber()), midi.getVelocity())
	elif midi.isNoteOff():
		print("OFF: ", midi.getNoteName(midi.getNoteNumber()))
	elif midi.isController():
		print("CC: ", midi.getControllerNumber(), midi.getControllerValue())

#class for accessing functions specific to the novation circuit
class CircuitController:
	def __init__(self, port):
		self.port = port
		self.input = None
		self.output = None



ports = range(midiin.getPortCount())
if ports:
	selected = 0
	while selected == 0:
		for i in ports:
			if "Circuit" in midiin.getPortName(i):
				selected = i
	print("Oeffne Port ", selected)
	midiin.openPort(selected)
	while True:
		m = midiin.getMessage(250)
		if m:
			print_message(m)
else:
	print("Keine Ports gefunden :(")
