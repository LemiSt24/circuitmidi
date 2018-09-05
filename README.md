# circuitmidi
Python program for interfacing a Novation Circuit with a Behringer BCF2000 without parameter jumps. Uses [pyrtmidi](https://github.com/patrickkidd/pyrtmidi).

## usage
Just run the script with python3, it automatically detects the Circuit and BCF2000. If you want to use it with another MIDI-Controller, you just have to adjust the name at the bottom of the script.

By default, pass-through is turned on so midi data from the circuit and the controller are passed on to each other. If you do not want this (if you have connected the devices with MIDI cables) you have to set the passthrough settings in both classes to False.

## disclaimer
As you might be able to see, the script is pretty rudimentary and lacks any error handling. Do not use this in a live setting at this stage.
