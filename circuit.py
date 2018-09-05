import rtmidi
import threading
import sys
import time

midiin = rtmidi.RtMidiIn()

circuit = None
bcf2000 = None

#class for the two synths, holds config data and offers functions for data conversion
class SynthController():
	def __init__(self, id):
		self.id = id
		self.config={
			32:{"CC":"3","value":"2","min":"0","max":"2","name":"Voice_PolyphonyMode"},
			33:{"CC":"5","value":"0","min":"0","max":"127","name":"Voice_PortamentoRate"},
			34:{"CC":"9","value":"64","min":"52","max":"76","name":"Voice_PreGlide"},
			35:{"CC":"13","value":"64","min":"58","max":"69","name":"Voice_KeyboardOctave"},
			36:{"CC":"19","value":"2","min":"0","max":"29","name":"Osc1_Wave"},
			37:{"CC":"20","value":"127","min":"0","max":"127","name":"Osc1_WaveInterpolate"},
			38:{"CC":"21","value":"64","min":"0","max":"127","name":"Osc1_PulseWidthIndex"},
			39:{"CC":"22","value":"0","min":"0","max":"127","name":"Osc1_VirtualSyncDepth"},
			40:{"CC":"24","value":"0","min":"0","max":"127","name":"Osc1_Density"},
			41:{"CC":"25","value":"0","min":"0","max":"127","name":"Osc1_DensityDetune"},
			42:{"CC":"26","value":"64","min":"0","max":"127","name":"Osc1_Semitones"},
			43:{"CC":"27","value":"64","min":"0","max":"127","name":"Osc1_Cents"},
			44:{"CC":"28","value":"76","min":"52","max":"76","name":"Osc1_PitchBend"},
			45:{"CC":"29","value":"2","min":"0","max":"29","name":"Osc2_Wave"},
			46:{"CC":"30","value":"127","min":"0","max":"127","name":"Osc2_WaveInterpolate"},
			47:{"CC":"31","value":"64","min":"0","max":"127","name":"Osc2_PulseWidthIndex"},
			48:{"CC":"33","value":"0","min":"0","max":"127","name":"Osc2_VirtualSyncDepth"},
			49:{"CC":"35","value":"0","min":"0","max":"127","name":"Osc2_Density"},
			50:{"CC":"36","value":"0","min":"0","max":"127","name":"Osc2_DensityDetune"},
			51:{"CC":"37","value":"64","min":"0","max":"127","name":"Osc2_Semitones"},
			52:{"CC":"39","value":"64","min":"0","max":"127","name":"Osc2_Cents"},
			53:{"CC":"40","value":"76","min":"52","max":"76","name":"Osc2_PitchBend"},
			54:{"CC":"51","value":"127","min":"0","max":"127","name":"Mixer_Osc1Level"},
			55:{"CC":"52","value":"0","min":"0","max":"127","name":"Mixer_Osc2Level"},
			56:{"CC":"54","value":"0","min":"0","max":"127","name":"Mixer_RingModLevel12"},
			57:{"CC":"56","value":"0","min":"0","max":"127","name":"Mixer_NoiseLevel"},
			58:{"CC":"58","value":"64","min":"52","max":"82","name":"Mixer_PreFXLevel"},
			59:{"CC":"59","value":"64","min":"52","max":"82","name":"Mixer_PostFXLevel"},
			60:{"CC":"60","value":"0","min":"0","max":"2","name":"Filter_Routing"},
			61:{"CC":"63","value":"0","min":"0","max":"127","name":"Filter_Drive"},
			62:{"CC":"65","value":"0","min":"0","max":"6","name":"Filter_DriveType"},
			63:{"CC":"68","value":"1","min":"0","max":"5","name":"Filter_Type"},
			64:{"CC":"74","value":"127","min":"0","max":"127","name":"Filter_Frequency"},
			65:{"CC":"69","value":"127","min":"0","max":"127","name":"Filter_Track"},
			66:{"CC":"71","value":"0","min":"0","max":"127","name":"Filter_Resonance"},
			67:{"CC":"78","value":"64","min":"0","max":"127","name":"Filter_QNormalise"},
			68:{"CC":"79","value":"64","min":"0","max":"127","name":"Filter_Env2ToFreq"},
			69:{"CC":"108","value":"64","min":"0","max":"127","name":"Envelope1_Velocity"},
			70:{"CC":"73","value":"2","min":"0","max":"127","name":"Envelope1_Attack"},
			71:{"CC":"75","value":"90","min":"0","max":"127","name":"Envelope1_Decay"},
			72:{"CC":"70","value":"127","min":"0","max":"127","name":"Envelope1_Sustain"},
			73:{"CC":"72","value":"40","min":"0","max":"127","name":"Envelope1_Release"},
			74:{"CC":"-","value":"64","min":"0","max":"127","name":"Envelope2_Velocity"},
			75:{"CC":"-","value":"2","min":"0","max":"127","name":"Envelope2_Attack"},
			76:{"CC":"-","value":"75","min":"0","max":"127","name":"Envelope2_Decay"},
			77:{"CC":"-","value":"35","min":"0","max":"127","name":"Envelope2_Sustain"},
			78:{"CC":"-","value":"45","min":"0","max":"127","name":"Envelope2_Release"},
			79:{"CC":"-","value":"0","min":"0","max":"127","name":"Envelope3_Delay"},
			80:{"CC":"-","value":"10","min":"0","max":"127","name":"Envelope3_Attack"},
			81:{"CC":"-","value":"70","min":"0","max":"127","name":"Envelope3_Decay"},
			82:{"CC":"-","value":"64","min":"0","max":"127","name":"Envelope3_Sustain"},
			83:{"CC":"-","value":"40","min":"0","max":"127","name":"Envelope3_Release"},
			84:{"CC":"-","value":"0","min":"0","max":"37","name":"LFO1_Waveform"},
			85:{"CC":"-","value":"0","min":"0","max":"119","name":"LFO1_PhaseOffset"},
			86:{"CC":"-","value":"0","min":"0","max":"127","name":"LFO1_SlewRate"},
			87:{"CC":"-","value":"0","min":"0","max":"127","name":"LFO1_Delay"},
			88:{"CC":"-","value":"0","min":"0","max":"35","name":"LFO1_DelaySync"},
			89:{"CC":"-","value":"68","min":"0","max":"127","name":"LFO1_Rate"},
			90:{"CC":"-","value":"0","min":"0","max":"35","name":"LFO1_RateSync"},
			91:{"CC":"-","value":"0","min":"-","max":"-","name":"LFO1_OneShot (bit 0), LFO1_KeySync (bit 1), LFO1_CommonSync (bit2), LFO1_DelayTrigger (bit 3), LFO1_FadeMode (bits 4-5)"},
			92:{"CC":"-","value":"0","min":"0","max":"37","name":"LFO2_Waveform"},
			93:{"CC":"-","value":"0","min":"0","max":"119","name":"LFO2_PhaseOffset"},
			94:{"CC":"-","value":"0","min":"0","max":"127","name":"LFO2_SlewRate"},
			95:{"CC":"-","value":"0","min":"0","max":"127","name":"LFO2_Delay"},
			96:{"CC":"-","value":"0","min":"0","max":"35","name":"LFO2_DelaySync"},
			97:{"CC":"-","value":"68","min":"0","max":"127","name":"LFO2_Rate"},
			98:{"CC":"-","value":"0","min":"0","max":"35","name":"LFO2_RateSync"},
			99:{"CC":"-","value":"0","min":"","max":"","name":"LFO2_OneShot (bit 0), LFO2_KeySync (bit 1), LFO2_CommonSync (bit 2), LFO2_DelayTrigger (bit 3), LFO2_FadeMode (bits 4-5)"},
			100:{"CC":"91","value":"0","min":"0","max":"127","name":"Distortion_Level"},
			101:{"CC":"-","value":"0","min":"0","max":"127","name":"FX_Reserved1"},
			102:{"CC":"93","value":"0","min":"0","max":"127","name":"Chorus_Level"},
			103:{"CC":"-","value":"0","min":"-","max":"-","name":"FX_Reserved2"},
			104:{"CC":"-","value":"0","min":"-","max":"-","name":"FX_Reserved3"},
			105:{"CC":"-","value":"64","min":"0","max":"127","name":"Equaliser_BassFrequency"},
			106:{"CC":"-","value":"64","min":"0","max":"127","name":"Equaliser_BassLevel"},
			107:{"CC":"-","value":"64","min":"0","max":"127","name":"Equaliser_MidFrequency"},
			108:{"CC":"-","value":"64","min":"0","max":"127","name":"Equaliser_MidLevel"},
			109:{"CC":"-","value":"125","min":"0","max":"127","name":"Equaliser_TrebleFrequency"},
			110:{"CC":"-","value":"64","min":"0","max":"127","name":"Equaliser_TrebleLevel"},
			111:{"CC":"-","value":"0","min":"-","max":"-","name":"FX_Reserved4"},
			112:{"CC":"-","value":"0","min":"-","max":"-","name":"FX_Reserved5"},
			113:{"CC":"-","value":"0","min":"-","max":"-","name":"FX_Reserved6"},
			114:{"CC":"-","value":"0","min":"-","max":"-","name":"FX_Reserved7"},
			115:{"CC":"-","value":"0","min":"-","max":"-","name":"FX_Reserved8"},
			116:{"CC":"-","value":"0","min":"0","max":"6","name":"Distortion_Type"},
			117:{"CC":"-","value":"100","min":"0","max":"127","name":"Distortion_Compensation"},
			118:{"CC":"-","value":"1","min":"0","max":"1","name":"Chorus_Type"},
			119:{"CC":"-","value":"20","min":"0","max":"127","name":"Chorus_Rate"},
			120:{"CC":"-","value":"0","min":"0","max":"35","name":"Chorus_RateSync"},
			121:{"CC":"-","value":"74","min":"0","max":"127","name":"Chorus_Feedback"},
			122:{"CC":"-","value":"64","min":"0","max":"127","name":"Chorus_ModDepth"},
			123:{"CC":"-","value":"64","min":"0","max":"127","name":"Chorus_Delay"},
			124:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix1_Source1"},
			125:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix1_Source2"},
			126:{"CC":"-","value":"64","min":"0","max":"127","name":"ModMatrix1_Depth"},
			127:{"CC":"-","value":"0","min":"0","max":"17","name":"ModMatrix1_Destination"},
			128:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix2_Source1"},
			129:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix2_Source2"},
			130:{"CC":"-","value":"64","min":"0","max":"127","name":"ModMatrix2_Depth"},
			131:{"CC":"-","value":"0","min":"0","max":"17","name":"ModMatrix2_Destination"},
			132:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix3_Source1"},
			133:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix3_Source2"},
			134:{"CC":"-","value":"64","min":"0","max":"127","name":"ModMatrix3_Depth"},
			135:{"CC":"-","value":"0","min":"0","max":"17","name":"ModMatrix3_Destination"},
			136:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix4_Source1"},
			137:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix4_Source2"},
			138:{"CC":"-","value":"64","min":"0","max":"127","name":"ModMatrix4_Depth"},
			139:{"CC":"-","value":"0","min":"0","max":"17","name":"ModMatrix4_Destination"},
			140:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix5_Source1"},
			141:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix5_Source2"},
			142:{"CC":"-","value":"64","min":"0","max":"127","name":"ModMatrix5_Depth"},
			143:{"CC":"-","value":"0","min":"0","max":"17","name":"ModMatrix5_Destination"},
			144:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix6_Source1"},
			145:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix6_Source2"},
			146:{"CC":"-","value":"64","min":"0","max":"127","name":"ModMatrix6_Depth"},
			147:{"CC":"-","value":"0","min":"0","max":"17","name":"ModMatrix6_Destination"},
			148:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix7_Source1"},
			149:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix7_Source2"},
			150:{"CC":"-","value":"64","min":"0","max":"127","name":"ModMatrix7_Depth"},
			151:{"CC":"-","value":"0","min":"0","max":"17","name":"ModMatrix7_Destination"},
			152:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix8_Source1"},
			153:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix8_Source2"},
			154:{"CC":"-","value":"64","min":"0","max":"127","name":"ModMatrix8_Depth"},
			155:{"CC":"-","value":"0","min":"0","max":"17","name":"ModMatrix8_Destination"},
			156:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix9_Source1"},
			157:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix9_Source2"},
			158:{"CC":"-","value":"64","min":"0","max":"127","name":"ModMatrix9_Depth"},
			159:{"CC":"-","value":"0","min":"0","max":"17","name":"ModMatrix9_Destination"},
			160:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix10_Source1"},
			161:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix10_Source2"},
			162:{"CC":"-","value":"64","min":"0","max":"127","name":"ModMatrix10_Depth"},
			163:{"CC":"-","value":"0","min":"0","max":"17","name":"ModMatrix10_Destination"},
			164:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix11_Source1"},
			165:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix11_Source2"},
			166:{"CC":"-","value":"64","min":"0","max":"127","name":"ModMatrix11_Depth"},
			167:{"CC":"-","value":"0","min":"0","max":"17","name":"ModMatrix11_Destination"},
			168:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix12_Source1"},
			169:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix12_Source2"},
			170:{"CC":"-","value":"64","min":"0","max":"127","name":"ModMatrix12_Depth"},
			171:{"CC":"-","value":"0","min":"0","max":"17","name":"ModMatrix12_Destination"},
			172:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix13_Source1"},
			173:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix13_Source2"},
			174:{"CC":"-","value":"64","min":"0","max":"127","name":"ModMatrix13_Depth"},
			175:{"CC":"-","value":"0","min":"0","max":"17","name":"ModMatrix13_Destination"},
			176:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix14_Source1"},
			177:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix14_Source2"},
			178:{"CC":"-","value":"64","min":"0","max":"127","name":"ModMatrix14_Depth"},
			179:{"CC":"-","value":"0","min":"0","max":"17","name":"ModMatrix14_Destination"},
			180:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix15_Source1"},
			181:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix15_Source2"},
			182:{"CC":"-","value":"64","min":"0","max":"127","name":"ModMatrix15_Depth"},
			183:{"CC":"-","value":"0","min":"0","max":"17","name":"ModMatrix15_Destination"},
			184:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix16_Source1"},
			185:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix16_Source2"},
			186:{"CC":"-","value":"64","min":"0","max":"127","name":"ModMatrix16_Depth"},
			187:{"CC":"-","value":"0","min":"0","max":"17","name":"ModMatrix16_Destination"},
			188:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix17_Source1"},
			189:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix17_Source2"},
			190:{"CC":"-","value":"64","min":"0","max":"127","name":"ModMatrix17_Depth"},
			191:{"CC":"-","value":"0","min":"0","max":"17","name":"ModMatrix17_Destination"},
			192:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix18_Source1"},
			193:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix18_Source2"},
			194:{"CC":"-","value":"64","min":"0","max":"127","name":"ModMatrix18_Depth"},
			195:{"CC":"-","value":"0","min":"0","max":"17","name":"ModMatrix18_Destination"},
			196:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix19_Source1"},
			197:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix19_Source2"},
			198:{"CC":"-","value":"64","min":"0","max":"127","name":"ModMatrix19_Depth"},
			199:{"CC":"-","value":"0","min":"0","max":"17","name":"ModMatrix19_Destination"},
			200:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix20_Source1"},
			201:{"CC":"-","value":"0","min":"0","max":"12","name":"ModMatrix20_Source2"},
			202:{"CC":"-","value":"64","min":"0","max":"127","name":"ModMatrix20_Depth"},
			203:{"CC":"-","value":"0","min":"0","max":"17","name":"ModMatrix20_Destination"},
			204:{"CC":"80","value":"0","min":"0","max":"127","name":"MacroKnob1_Position"},
			205:{"CC":"-","value":"0","min":"0","max":"70","name":"MacroKnob1_DestinationA"},
			206:{"CC":"-","value":"0","min":"0","max":"127","name":"MacroKnob1_StartPosA"},
			207:{"CC":"-","value":"127","min":"0","max":"127","name":"MacroKnob1_EndPosA"},
			208:{"CC":"-","value":"64","min":"0","max":"127","name":"MacroKnob1_DepthA"},
			209:{"CC":"-","value":"0","min":"0","max":"70","name":"MacroKnob1_DestinationB"},
			210:{"CC":"-","value":"0","min":"0","max":"127","name":"MacroKnob1_StartPosB"},
			211:{"CC":"-","value":"127","min":"0","max":"127","name":"MacroKnob1_EndPosB"},
			212:{"CC":"-","value":"64","min":"0","max":"127","name":"MacroKnob1_DepthB"},
			213:{"CC":"-","value":"0","min":"0","max":"70","name":"MacroKnob1_DestinationC"},
			214:{"CC":"-","value":"0","min":"0","max":"127","name":"MacroKnob1_StartPosC"},
			215:{"CC":"-","value":"127","min":"0","max":"127","name":"MacroKnob1_EndPosC"},
			216:{"CC":"-","value":"64","min":"0","max":"127","name":"MacroKnob1_DepthC"},
			217:{"CC":"-","value":"0","min":"0","max":"70","name":"MacroKnob1_DestinationD"},
			218:{"CC":"-","value":"0","min":"0","max":"127","name":"MacroKnob1_StartPosD"},
			219:{"CC":"-","value":"127","min":"0","max":"127","name":"MacroKnob1_EndPosD"},
			220:{"CC":"-","value":"64","min":"0","max":"127","name":"MacroKnob1_DepthD"},
			221:{"CC":"81","value":"0","min":"0","max":"127","name":"MacroKnob2_Position"},
			222:{"CC":"-","value":"0","min":"0","max":"70","name":"MacroKnob2_DestinationA"},
			223:{"CC":"-","value":"0","min":"0","max":"127","name":"MacroKnob2_StartPosA"},
			224:{"CC":"-","value":"127","min":"0","max":"127","name":"MacroKnob2_EndPosA"},
			225:{"CC":"-","value":"64","min":"0","max":"127","name":"MacroKnob2_DepthA"},
			226:{"CC":"-","value":"0","min":"0","max":"70","name":"MacroKnob2_DestinationB"},
			227:{"CC":"-","value":"0","min":"0","max":"127","name":"MacroKnob2_StartPosB"},
			228:{"CC":"-","value":"127","min":"0","max":"127","name":"MacroKnob2_EndPosB"},
			229:{"CC":"-","value":"64","min":"0","max":"127","name":"MacroKnob2_DepthB"},
			230:{"CC":"-","value":"0","min":"0","max":"70","name":"MacroKnob2_DestinationC"},
			231:{"CC":"-","value":"0","min":"0","max":"127","name":"MacroKnob2_StartPosC"},
			232:{"CC":"-","value":"127","min":"0","max":"127","name":"MacroKnob2_EndPosC"},
			233:{"CC":"-","value":"64","min":"0","max":"127","name":"MacroKnob2_DepthC"},
			234:{"CC":"-","value":"0","min":"0","max":"70","name":"MacroKnob2_DestinationD"},
			235:{"CC":"-","value":"0","min":"0","max":"127","name":"MacroKnob2_StartPosD"},
			236:{"CC":"-","value":"127","min":"0","max":"127","name":"MacroKnob2_EndPosD"},
			237:{"CC":"-","value":"64","min":"0","max":"127","name":"MacroKnob2_DepthD"},
			238:{"CC":"82","value":"0","min":"0","max":"127","name":"MacroKnob3_Position"},
			239:{"CC":"-","value":"0","min":"0","max":"70","name":"MacroKnob3_DestinationA"},
			240:{"CC":"-","value":"0","min":"0","max":"127","name":"MacroKnob3_StartPosA"},
			241:{"CC":"-","value":"127","min":"0","max":"127","name":"MacroKnob3_EndPosA"},
			242:{"CC":"-","value":"64","min":"0","max":"127","name":"MacroKnob3_DepthA"},
			243:{"CC":"-","value":"0","min":"0","max":"70","name":"MacroKnob3_DestinationB"},
			244:{"CC":"-","value":"0","min":"0","max":"127","name":"MacroKnob3_StartPosB"},
			245:{"CC":"-","value":"127","min":"0","max":"127","name":"MacroKnob3_EndPosB"},
			246:{"CC":"-","value":"64","min":"0","max":"127","name":"MacroKnob3_DepthB"},
			247:{"CC":"-","value":"0","min":"0","max":"70","name":"MacroKnob3_DestinationC"},
			248:{"CC":"-","value":"0","min":"0","max":"127","name":"MacroKnob3_StartPosC"},
			249:{"CC":"-","value":"127","min":"0","max":"127","name":"MacroKnob3_EndPosC"},
			250:{"CC":"-","value":"64","min":"0","max":"127","name":"MacroKnob3_DepthC"},
			251:{"CC":"-","value":"0","min":"0","max":"70","name":"MacroKnob3_DestinationD"},
			252:{"CC":"-","value":"0","min":"0","max":"127","name":"MacroKnob3_StartPosD"},
			253:{"CC":"-","value":"127","min":"0","max":"127","name":"MacroKnob3_EndPosD"},
			254:{"CC":"-","value":"64","min":"0","max":"127","name":"MacroKnob3_DepthD"},
			255:{"CC":"83","value":"0","min":"0","max":"127","name":"MacroKnob4_Position"},
			256:{"CC":"-","value":"0","min":"0","max":"70","name":"MacroKnob4_DestinationA"},
			257:{"CC":"-","value":"0","min":"0","max":"127","name":"MacroKnob4_StartPosA"},
			258:{"CC":"-","value":"127","min":"0","max":"127","name":"MacroKnob4_EndPosA"},
			259:{"CC":"-","value":"64","min":"0","max":"127","name":"MacroKnob4_DepthA"},
			260:{"CC":"-","value":"0","min":"0","max":"70","name":"MacroKnob4_DestinationB"},
			261:{"CC":"-","value":"0","min":"0","max":"127","name":"MacroKnob4_StartPosB"},
			262:{"CC":"-","value":"127","min":"0","max":"127","name":"MacroKnob4_EndPosB"},
			263:{"CC":"-","value":"64","min":"0","max":"127","name":"MacroKnob4_DepthB"},
			264:{"CC":"-","value":"0","min":"0","max":"70","name":"MacroKnob4_DestinationC"},
			265:{"CC":"-","value":"0","min":"0","max":"127","name":"MacroKnob4_StartPosC"},
			266:{"CC":"-","value":"127","min":"0","max":"127","name":"MacroKnob4_EndPosC"},
			267:{"CC":"-","value":"64","min":"0","max":"127","name":"MacroKnob4_DepthC"},
			268:{"CC":"-","value":"0","min":"0","max":"70","name":"MacroKnob4_DestinationD"},
			269:{"CC":"-","value":"0","min":"0","max":"127","name":"MacroKnob4_StartPosD"},
			270:{"CC":"-","value":"127","min":"0","max":"127","name":"MacroKnob4_EndPosD"},
			271:{"CC":"-","value":"64","min":"0","max":"127","name":"MacroKnob4_DepthD"},
			272:{"CC":"84","value":"0","min":"0","max":"127","name":"MacroKnob5_Position"},
			273:{"CC":"-","value":"0","min":"0","max":"70","name":"MacroKnob5_DestinationA"},
			274:{"CC":"-","value":"0","min":"0","max":"127","name":"MacroKnob5_StartPosA"},
			275:{"CC":"-","value":"127","min":"0","max":"127","name":"MacroKnob5_EndPosA"},
			276:{"CC":"-","value":"64","min":"0","max":"127","name":"MacroKnob5_DepthA"},
			277:{"CC":"-","value":"0","min":"0","max":"70","name":"MacroKnob5_DestinationB"},
			278:{"CC":"-","value":"0","min":"0","max":"127","name":"MacroKnob5_StartPosB"},
			279:{"CC":"-","value":"127","min":"0","max":"127","name":"MacroKnob5_EndPosB"},
			280:{"CC":"-","value":"64","min":"0","max":"127","name":"MacroKnob5_DepthB"},
			281:{"CC":"-","value":"0","min":"0","max":"70","name":"MacroKnob5_DestinationC"},
			282:{"CC":"-","value":"0","min":"0","max":"127","name":"MacroKnob5_StartPosC"},
			283:{"CC":"-","value":"127","min":"0","max":"127","name":"MacroKnob5_EndPosC"},
			284:{"CC":"-","value":"64","min":"0","max":"127","name":"MacroKnob5_DepthC"},
			285:{"CC":"-","value":"0","min":"0","max":"70","name":"MacroKnob5_DestinationD"},
			286:{"CC":"-","value":"0","min":"0","max":"127","name":"MacroKnob5_StartPosD"},
			287:{"CC":"-","value":"127","min":"0","max":"127","name":"MacroKnob5_EndPosD"},
			288:{"CC":"-","value":"64","min":"0","max":"127","name":"MacroKnob5_DepthD"},
			289:{"CC":"85","value":"0","min":"0","max":"127","name":"MacroKnob6_Position"},
			290:{"CC":"-","value":"0","min":"0","max":"70","name":"MacroKnob6_DestinationA"},
			291:{"CC":"-","value":"0","min":"0","max":"127","name":"MacroKnob6_StartPosA"},
			292:{"CC":"-","value":"127","min":"0","max":"127","name":"MacroKnob6_EndPosA"},
			293:{"CC":"-","value":"64","min":"0","max":"127","name":"MacroKnob6_DepthA"},
			294:{"CC":"-","value":"0","min":"0","max":"70","name":"MacroKnob6_DestinationB"},
			295:{"CC":"-","value":"0","min":"0","max":"127","name":"MacroKnob6_StartPosB"},
			296:{"CC":"-","value":"127","min":"0","max":"127","name":"MacroKnob6_EndPosB"},
			297:{"CC":"-","value":"64","min":"0","max":"127","name":"MacroKnob6_DepthB"},
			298:{"CC":"-","value":"0","min":"0","max":"70","name":"MacroKnob6_DestinationC"},
			299:{"CC":"-","value":"0","min":"0","max":"127","name":"MacroKnob6_StartPosC"},
			300:{"CC":"-","value":"127","min":"0","max":"127","name":"MacroKnob6_EndPosC"},
			301:{"CC":"-","value":"64","min":"0","max":"127","name":"MacroKnob6_DepthC"},
			302:{"CC":"-","value":"0","min":"0","max":"70","name":"MacroKnob6_DestinationD"},
			303:{"CC":"-","value":"0","min":"0","max":"127","name":"MacroKnob6_StartPosD"},
			304:{"CC":"-","value":"127","min":"0","max":"127","name":"MacroKnob6_EndPosD"},
			305:{"CC":"-","value":"64","min":"0","max":"127","name":"MacroKnob6_DepthD"},
			306:{"CC":"86","value":"0","min":"0","max":"127","name":"MacroKnob7_Position"},
			307:{"CC":"-","value":"0","min":"0","max":"70","name":"MacroKnob7_DestinationA"},
			308:{"CC":"-","value":"0","min":"0","max":"127","name":"MacroKnob7_StartPosA"},
			309:{"CC":"-","value":"127","min":"0","max":"127","name":"MacroKnob7_EndPosA"},
			310:{"CC":"-","value":"64","min":"0","max":"127","name":"MacroKnob7_DepthA"},
			311:{"CC":"-","value":"0","min":"0","max":"70","name":"MacroKnob7_DestinationB"},
			312:{"CC":"-","value":"0","min":"0","max":"127","name":"MacroKnob7_StartPosB"},
			313:{"CC":"-","value":"127","min":"0","max":"127","name":"MacroKnob7_EndPosB"},
			314:{"CC":"-","value":"64","min":"0","max":"127","name":"MacroKnob7_DepthB"},
			315:{"CC":"-","value":"0","min":"0","max":"70","name":"MacroKnob7_DestinationC"},
			316:{"CC":"-","value":"0","min":"0","max":"127","name":"MacroKnob7_StartPosC"},
			317:{"CC":"-","value":"127","min":"0","max":"127","name":"MacroKnob7_EndPosC"},
			318:{"CC":"-","value":"64","min":"0","max":"127","name":"MacroKnob7_DepthC"},
			319:{"CC":"-","value":"0","min":"0","max":"70","name":"MacroKnob7_DestinationD"},
			320:{"CC":"-","value":"0","min":"0","max":"127","name":"MacroKnob7_StartPosD"},
			321:{"CC":"-","value":"127","min":"0","max":"127","name":"MacroKnob7_EndPosD"},
			322:{"CC":"-","value":"64","min":"0","max":"127","name":"MacroKnob7_DepthD"},
			323:{"CC":"87","value":"0","min":"0","max":"127","name":"MacroKnob8_Position"},
			324:{"CC":"-","value":"0","min":"0","max":"70","name":"MacroKnob8_DestinationA"},
			325:{"CC":"-","value":"0","min":"0","max":"127","name":"MacroKnob8_StartPosA"},
			326:{"CC":"-","value":"127","min":"0","max":"127","name":"MacroKnob8_EndPosA"},
			327:{"CC":"-","value":"64","min":"0","max":"127","name":"MacroKnob8_DepthA"},
			328:{"CC":"-","value":"0","min":"0","max":"70","name":"MacroKnob8_DestinationB"},
			329:{"CC":"-","value":"0","min":"0","max":"127","name":"MacroKnob8_StartPosB"},
			330:{"CC":"-","value":"127","min":"0","max":"127","name":"MacroKnob8_EndPosB"},
			331:{"CC":"-","value":"64","min":"0","max":"127","name":"MacroKnob8_DepthB"},
			332:{"CC":"-","value":"0","min":"0","max":"70","name":"MacroKnob8_DestinationC"},
			333:{"CC":"-","value":"0","min":"0","max":"127","name":"MacroKnob8_StartPosC"},
			334:{"CC":"-","value":"127","min":"0","max":"127","name":"MacroKnob8_EndPosC"},
			335:{"CC":"-","value":"64","min":"0","max":"127","name":"MacroKnob8_DepthC"},
			336:{"CC":"-","value":"0","min":"0","max":"70","name":"MacroKnob8_DestinationD"},
			337:{"CC":"-","value":"0","min":"0","max":"127","name":"MacroKnob8_StartPosD"},
			338:{"CC":"-","value":"127","min":"0","max":"127","name":"MacroKnob8_EndPosD"},
			339:{"CC":"-","value":"64","min":"0","max":"127","name":"MacroKnob8_DepthD"}
		}

	def parsePatch(self, data):
		data=data[32:] #cut first 32 bytes with patch name and other info we don't need
		counter = 32
		for byte in data:
			self.config[counter]["value"] = int(byte)
			counter = counter + 1

	def dumpCC(self, output):
		print("Sending patch data from synth",self.id + 1, "as CC")
		for parameter in self.config:
			if self.config[parameter]["CC"].isdigit():
				message = rtmidi.MidiMessage.controllerEvent(self.id + 1, int(self.config[parameter]["CC"]), int(self.config[parameter]["value"]))
				output.sendMessage(message)

synth1=SynthController(0)
synth2=SynthController(1)

#class for asynchronously requesting patch data
#kinda Q&D but it works
class PatchRequester(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self) #threading
		self.setDaemon(True) #threading
		self.requestSynths = False
		self.quit = False #threading

	def requestCurrentPatch(self, synth):
		print("Requesting patch data for synth", synth + 1)
		message = rtmidi.MidiMessage.createSysExMessage(bytes([0, 32, 41, 1, 96, 64, synth])) #Sysex Message requesting current patch dump
		circuit.output.sendMessage(message) #send sysex to circuit

	def run(self):
		while True:
			if self.quit:
				return
			if self.requestSynths:
				self.requestCurrentPatch(0)
				time.sleep(0.6)
				self.requestCurrentPatch(1)
				self.requestSynths = False

requester = PatchRequester()
requester.start()

#class for accessing and handling of functions specific to the novation circuit
#listens on the assigned port and handles messages accordingly
class CircuitController(threading.Thread):
	def __init__(self, port):
		threading.Thread.__init__(self) #threading
		self.setDaemon(True) #threading
		self.port = port #the internal midi port
		self.input = None #object for rtmidiin
		self.output = None #object for rtmidiout
		self.passthrough = True #enable if the two devices are not connected outside of the computer running this software
		self.quit = False #threading

	def connect(self): #open midi port for sending and receiving data
		self.input = rtmidi.RtMidiIn()
		self.input.ignoreTypes(False, True, True) #enable sysex messages so we can receive patch data
		self.input.openPort(self.port)
		self.output = rtmidi.RtMidiOut()
		self.output.openPort(self.port)

	def handleMessage(self, msg):
		if msg.isProgramChange(): #request patch data for both synths on session change
			requester.requestSynths = True
		if msg.isController(): #ignoring note and timing messages for now
			if self.passthrough:
				bcf2000.output.sendMessage(msg)	#send message to BCF2000
		elif msg.isSysEx():
			if msg.getSysExData()[6] == 0: #patch data for synth 1 received
				print("Patch Data for synth 1 received")
				synth1.parsePatch(msg.getSysExData()[8:])
				synth1.dumpCC(bcf2000.output)
			else:#patch data for synth 2 received
				print("Patch Data for synth 2 received")
				synth2.parsePatch(msg.getSysExData()[8:])
				synth2.dumpCC(bcf2000.output)

	def run(self):
		while True:
			if self.quit:
				return
			msg = self.input.getMessage() #listens for messages
			if msg:
				self.handleMessage(msg)


#class which represents the midi controller for communication
#listens on the assigned port and handles messages accordingly
class BCFController(threading.Thread):
	def __init__(self, port):
		threading.Thread.__init__(self) #threading
		self.setDaemon(True) #threading
		self.port = port #the internal midi port
		self.input = None #object for rtmidiin
		self.output = None #object for rtmidiout
		self.passthrough = True #enable if the two devices are not connected outside of the computer running this software
		self.quit = False #threading

	def connect(self): #open midi port for sending and receiving data
		self.input = rtmidi.RtMidiIn()
		self.input.openPort(self.port)
		self.output = rtmidi.RtMidiOut()
		self.output.openPort(self.port)

	def handleMessage(self, msg):
		if msg.isNoteOn():
			if msg.getNoteNumber == 0 and msg.getChannel() == 16: #emit a 0-note on channel 16 from the midi controller to request an update on synth 1
				requester.requestCurrentPatch(0)
			if msg.getNoteNumber == 1 and msg.getChannel() == 16: #emit a 1-note on channel 16 from the midi controller to request an update on synth 2
				requester.requestCurrentPatch(1)
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

	print("Connecting to Circuit on Port", circuitport, "and to BCF2000 on Port", bcfport)

	circuit = CircuitController(circuitport)
	circuit.connect()
	circuit.start()

	bcf2000 = BCFController(bcfport)
	bcf2000.connect()
	bcf2000.start()

	sys.stdin.read(1)
	circuit.quit = True
	bcf2000.quit = True
