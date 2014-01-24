from Tkinter import *
import wave
import tkFileDialog
import pyaudio
import wave
import sys
import struct
import os
################global variables##################
root=Tk()
###################File Browser####################
def browsefile(val):
	global fil1
	global fil2
	global fil3
	fil=tkFileDialog.askopenfilename(parent=root,title='Choose a file')
	if val==1:
		fil1=fil
	elif val==2:
		fil2=fil
	elif val==3:
		fil3=fil

def callb(in_data, frame_count, time_info, status):
	data=wf.readframes(frame_count)
	return (data, pyaudio.paContinue)

def pl():
	chunk=1024
	cur=os.getcwd()
	cur+=str("/output.wav")
	f = wave.open(cur, 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(
            format = p.get_format_from_width(f.getsampwidth()),
            channels = f.getnchannels(),
            rate = f.getframerate(),
            output = True
        )
        data =f.readframes(chunk)	
        while data != '':
            stream.write(data)
            data = f.readframes(chunk)
	stream.close()
        p.terminate()
    
def amplitude(val):
	max_amplification=32767
	min_amplification=-32768
	if val==1:
		val=amp1.get()
	elif val==2:
		val=amp2.get()
	elif val==3:
		val=amp3.get()
	else:
		return 
	for i in xrange(len(formatted_data)):
		if formatted_data[i]*val>max_amplification:
			formatted_data[i]=max_amplification
		elif formatted_data[i]*val<min_amplification:
			formatted_data[i]=min_amplification
		else:
			formatted_data[i]=formatted_data[i]*val

def scale(val):
	global formatted_data
	a=[]
	if val==1:
		val=scaling1.get()
	elif val==2:
		val=scaling2.get()
	elif val==3:
		val=scaling3.get()
	else:
		return 
	if val==0:
	 	val=1
	if type_channel==1:
		k=int(len(formatted_data)/val)
		for i in range(k):
			a.append(formatted_data[int(val*i)])
	
	else:
		e_li=[]
		o_li=[]
		for i in range(len(formatted_data)):
			if i%2==0:
				e_li.append(formatted_data[i])
			else:
				o_li.append(formatted_data[i])
		k=int(len(e_li)/val)
		for i in range(k):
			a.append(e_li[int(val*i)])
			a.append(o_li[int(val*i)])

	formatted_data=a
	num_frames=len(formatted_data)/type_channel

def shift(val):
	global formatted_data
	if val==1:
		val=shift1.get()
	elif val==2:
		val=shift2.get()
	elif val==3:
		val=shift3.get()
	else:
		return 
	shift_frames=int(val*sample_rate)
	if val>0:
		if type_channel==1:
			a=[]
			for i in range(shift_frames):
				a.append(0)
			formatted_data=a+formatted_data
		else:
		  	a=[]
		  	for i in range(2*shift_frames):
				a.append(0)
			formatted_data=a+formatted_data
	else:
	   	if type_channel==1:
	   		formatted_data=formatted_data[shift_frames::1]
	   	else:
	   		formatted_data=formatted_data[2*shift_frames::1]
	num_frames=len(formatted_data)/type_channel
def reverse(val):
	if val==1:
		val=f1_s1.get()
	elif val==2:
		val=f2_s1.get()
	elif val==3:
		val=f3_s1.get()
	if val==0:
		return
	if type_channel==1:
		formatted_data.reverse()
	else:
		formatted_data.reverse()
		for i in xrange(len(formatted_data)-1):
			temp=formatted_data[i]
			formatted_data[i]=formatted_data[i+1]
			formatted_data[i+1]=temp
def read_file(file_name):
	music_file=wave.open(file_name,'rb')
	type_channel=music_file.getnchannels()
	sample_rate=music_file.getframerate()
	sample_width=music_file.getsampwidth()
	num_frames=music_file.getnframes()
	raw_data=music_file.readframes(num_frames)
	music_file.close()
	num_samples=num_frames*type_channel
	if sample_width==1:
		fmt="%iB" % num_samples
	elif sample_width==2:
		fmt="%ih" % num_samples
	else:
		raise ValueError("Only supports 8 and 16 bit audio formats.")
	data=list(struct.unpack(fmt,raw_data))
	return data
		
def mixing():
	SHRT_MIN=32767-1
	SHRT_MAX=32767
	fl1=0
	fl2=0
	fl3=0
	if f1_s3.get():
		fl1=1
	if f2_s3.get():
		fl2=1
	if f3_s3.get():
		fl3=1
	print fl1, fl2, fl3
	if (fl1==1 & fl2==1) or (fl2==1 & fl3==1) or (fl1==1 & fl3==1):	
		if (fl1==1 & fl2==1):
#			frame1.onread()
			cur=os.getcwd()
			cur+=str("/output_file.wav")
			data=read_file(fil1)
			fi=wave.open(fil1,"rb")
#			frame2.onread()
			cur=os.getcwd()
			cur+=str("/output_file.wav")
			data2=read_file(fil2)
			fi2 = wave.open(fil2,"rb")
		elif (fl1==1 & fl3==1):
#			frame1.onread()
			cur=os.getcwd()
			cur+=str("/output_file.wav")
			data=read_file(fil1)
			fi = wave.open(fil1,"rb")
#			frame3.onread()
			cur=os.getcwd()
			cur+=str("/output_file.wav")
			data2=read_file(fil3)
			fi2 = wave.open(fil3,"rb")
		elif (fl2==1 & fl3==1):
#			frame2.onread()
			cur=os.getcwd()
			cur+=str("/output_file.wav")
			data=read_file(fil2)
			fi = wave.open(fil2,"rb")
#			frame3.onread()
			cur=os.getcwd()
			cur+=str("/output_file.wav")
			data2=read_file(fil3)
			fi2 = wave.open(fil3,"rb")
		fo = wave.open("output.wav","w")
		fo.setparams(fi.getparams())
		width=fi.getsampwidth()
		width2=fi2.getsampwidth()	
		if width<width2:
			width=width2
		fmts=(None, "=B", "=h", None, "=l")
		fmt=fmts[width]
		dcs=(None, 128, 0, None, 0)
		dc=dcs[width]
		if fi.getnframes()>fi2.getnframes():
			maxi=fi.getnframes()
			flag=1		
		else:
			maxi=fi2.getnframes()
			flag=2
		amp=[]
		print flag
		for i in range(maxi):
			if flag==1 and i>=fi2.getnframes():
				if data[i]<SHRT_MIN: 
					iframe=SHRT_MIN
				elif data[i]>SHRT_MAX:
					iframe=SHRT_MAX
				else:
					iframe=data[i]
			elif flag==2 and i>=fi.getnframes():
				if data2[i]<SHRT_MIN:
					iframe=SHRT_MIN
				elif data2[i]>SHRT_MAX:
					iframe=SHRT_MAX
				else:
					iframe=data2[i]
			else:
				if data2[i]+data[i]<SHRT_MIN:
					iframe=SHRT_MIN
				elif data2[i]+data[i]>SHRT_MAX:
					iframe=SHRT_MAX
				else:
					iframe=data2[i]+data[i]
			iframe-=dc
			oframe=iframe/2;
			oframe+=dc
			oframe=struct.pack(fmt, oframe)
			fo.writeframes(oframe)
		fi.close()
		fo.close()
		pl()
	elif (fl1==1 & fl2==1 & fl3==1):
#		frame1.onread()
		cur=os.getcwd()
		cur+="output_file.wav"
		data=read_file(fil1)
		fi = wave.open(fil1,"rb")
		
#		wave2.onread()
		cur=os.getcwd()
		cur+="output_file.wav"
		data2=read_file(fil2)
		fi2 = wave.open(fil2,"rb")
		
#		wave3.onread()
		cur=os.getcwd()
		cur+="output_file.wav"
		data3=read_file(fil3)	
		fi3 = wave.open(fil3,"rb")
		fo = wave.open("output.wav","w")
		fo.setparams(fi.getparams())
		width=fi.getsampwidth()
		width2=fi2.getsampwidth()
		width3=fi3.getsampwidth()	
		if width<width2:
			width=width2
		if width<width3:
			width=width3
		fmts=(None, "=B", "=h", None, "=l")
		fmt=fmts[width]
		dcs=(None, 128, 0, None, 0)
		dc=dcs[width]
		if fi.getnframes()>fi2.getnframes():
			maxi=fi.getnframes()
			flag=1		
		else:
			maxi=fi2.getnframes()
			flag=2
		if fi3.getnframes()>maxi:
			maxi=fi3.getnframes()
			flag=3
		amp=[]
		for i in range(maxi):
			if flag==1 and i>=fi2.getnframes():
				if data[i]<SHRT_MIN: 
					iframe=SHRT_MIN
				elif data[i]>SHRT_MAX:
					iframe=SHRT_MAX
				else:
					iframe=data[i]
			elif flag==2 and i>=fi.getnframes():
				if data2[i]<SHRT_MIN:
					iframe=SHRT_MIN
				elif data2[i]>SHRT_MAX:
					iframe=SHRT_MAX
				else:
					iframe=data2[i]
			elif flag==3 and i>=fi3.getnframes():
				if data3[i]<SHRT_MIN:
					iframe=SHRT_MIN
				elif data3[i]>SHRT_MAX:
					iframe=SHRT_MAX
				else:
					iframe=data3[i]
			else:
				if data2[i]+data[i]+data3[i]<SHRT_MIN:
					iframe=SHRT_MIN
				elif data2[i]+data[i]+data3[i]>SHRT_MAX:
					iframe=SHRT_MAX
				else:
					iframe=data2[i]+data[i]+data3[i]
			#	print int(iframe)
			iframe-=dc
			oframe=iframe/2;
			oframe+=dc
			oframe=struct.pack(fmt, oframe)
			fo.writeframes(oframe)
		fi.close()
		fo.close()
		play_file()
def record():
	CHUNK = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS = 2
	RATE = 44100
	RECORD_SECONDS = 5
	WAVE_OUTPUT_FILENAME = "output.wav"

#	if sys.platform == 'darwin':
#	    CHANNELS = 1

	p = pyaudio.PyAudio()
	
	stream = p.open(format=FORMAT,
	                channels=CHANNELS,
	                rate=RATE,
	                input=True,
	                frames_per_buffer=CHUNK)
	
	print("* recording")
	
	frames = []
	
	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	    data = stream.read(CHUNK)
	    frames.append(data)

	print("* done recording")

	stream.stop_stream()
	stream.close()
	p.terminate()

	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()


def modulation():
	SHRT_MIN=-32767 - 1
	SHRT_MAX=32767
	fl1=0
	fl2=0
	fl3=0
	if f1_s2.get():
		fl1=1
	elif f2_s2.get():
		fl2=1
	elif f3_s2.get():
		fl3=1
	if (fl1==1 & fl2==1) or (fl2==1 & fl3==1) or (fl1==1 & fl3==1):	
		if (fl1==1 & fl2==1):
#			frame1.onread()
			cur=os.getcwd()
			cur+=str("/output_file.wav")
			data=read_file(cur)
			fi = wave.open(cur,"rb")
			frame2.onread()
			cur=os.getcwd()
			cur+=str("/output_file.wav")
			data2=read_file(cur)
			fi2 = wave.open(cur,"rb")
		elif (fl1==1 & fl3==1):
#			frame1.onread()
			cur=os.getcwd()
			cur+=str("/output_file.wav")
			data=read_file(cur)
			fi = wave.open(cur,"rb")
			frame3.onread()
			cur=os.getcwd()
			cur+=str("/output_file.wav")
			data2=read_file(cur)
			fi2 = wave.open(cur,"rb")
		elif (fl2==1 & fl3==1):
#			frame2.onread()
			cur=os.getcwd()
			cur+=str("/output_file.wav")
			data=read_file(cur)
			fi = wave.open(cur,"rb")
			frame3.onread()
			cur=os.getcwd()
			cur+=str("/output_file.wav")
			data2=read_file(cur)
			fi2 = wave.open(cur,"rb")
		fo=wave.open("output.wav","w")
		fo.setparams(fi.getparams())
		width=fi.getsampwidth()
		width2=fi2.getsampwidth()	
		if width>width2:
			width=width2
		fmts=(None, "=B", "=h", None, "=l")
		fmt=fmts[width]
		dcs=(None, 128, 0, None, 0)
		dc=dcs[width]
		if fi.getnframes()<fi2.getnframes():
			maxi=fi.getnframes()
			flag=1		
		else:
			maxi=fi2.getnframes()
			flag=2
		amp=[]
		print flag
		for i in range(maxi):
			if flag==1 and i>=fi2.getnframes():
				if data[i]<SHRT_MIN: 
					iframe=SHRT_MIN
				elif data[i]>SHRT_MAX:
					iframe=SHRT_MAX
				else:
					iframe=data[i]
			elif flag==2 and i>=fi.getnframes():
				if data2[i]<SHRT_MIN:
					iframe=SHRT_MIN
				elif data2[i]>SHRT_MAX:
					iframe=SHRT_MAX
				else:
					iframe=data2[i]
			else:
				if data2[i]*data[i]<SHRT_MIN:
					iframe=SHRT_MIN
				elif data2[i]*data[i]>SHRT_MAX:
					iframe=SHRT_MAX
				else:
					iframe=data2[i]*data[i]
			iframe-=dc
			oframe=iframe/2;
			oframe+=dc
			oframe=struct.pack(fmt, oframe)
			fo.writeframes(oframe)
		fi.close()
		fo.close()
		pl()
	elif (fl1==1 & fl2==1 & fl3==1):
#		frame1.onread()
		cur=os.getcwd()
		cur+="output_file.wav"
		data=read_file(cur)
		fi = wave.open(cur,"rb")
		
#		frame2.onread()
		cur=os.getcwd()
		cur+="output_file.wav"
		data2=read_file(cur)
		fi2 = wave.open(cur,"rb")
		
#		frame3.onread()
		cur=os.getcwd()
		cur+="output_file.wav"
		data3=read_file(cur)	
		fi3 = wave.open(cur,"rb")
		fo = wave.open("output.wav","w")
		fo.setparams(fi.getparams())
		width=fi.getsampwidth()
		width2=fi2.getsampwidth()
		width3=fi3.getsampwidth()	
		if width>width2:
			width=width2
		if width>width3:
			width=width3
		fmts=(None, "=B", "=h", None, "=l")
		fmt=fmts[width]
		dcs=(None, 128, 0, None, 0)
		dc=dcs[width]
		if fi.getnframes()<fi2.getnframes():
			maxi=fi.getnframes()
			flag=1		
		else:
			maxi=fi2.getnframes()
			flag=2
		if fi3.getnframes()<maxi:
			maxi=fi3.getnframes()
			flag=3
		amp=[]
		for i in range(maxi):
			if flag==1 and i>=fi2.getnframes():
				if data[i]<SHRT_MIN: 
					iframe=SHRT_MIN
				elif data[i]>SHRT_MAX:
					iframe=SHRT_MAX
				else:
					iframe=data[i]
			elif flag==2 and i>=fi.getnframes():
				if data2[i]<SHRT_MIN:
					iframe=SHRT_MIN
				elif data2[i]>SHRT_MAX:
					iframe=SHRT_MAX
				else:
					iframe=data2[i]
			elif flag==3 and i>=fi3.getnframes():
				if data3[i]<SHRT_MIN:
					iframe=SHRT_MIN
				elif data3[i]>SHRT_MAX:
					iframe=SHRT_MAX
				else:
					iframe=data3[i]
			else:
				if data2[i]*data[i]*data3[i]<SHRT_MIN:
					iframe=SHRT_MIN
				elif data2[i]*data[i]*data3[i]>SHRT_MAX:
					iframe=SHRT_MAX
				else:
					iframe=data2[i]*data[i]*data3[i]
			#	print int(iframe)
			iframe-=dc
			oframe=iframe/2;
			oframe+=dc
			oframe=struct.pack(fmt, oframe)
			fo.writeframes(oframe)
		fi.close()
		fo.close()
		pl()
		 
def packfile(fil,val):
	print formatted_data
#	type_channel = music_file.getnchannels()
#	sample_rate = music_file.getframerate()
#	sample_width = music_file.getsampwidth()
#	num_frames = music_file.getnframes()

        if sample_width==1:
                        fmt="%iB" % num_frames*type_channel
        else:
                        fmt="%ih" % num_frames*type_channel
 
        out_data=struct.pack(fmt,*(formatted_data))
        out_music_file=wave.open("output_file.wav",'w')
#	out_music_file.setparams(music_file.getparams())
        out_music_file.setframerate(sample_rate)
        out_music_file.setnframes(num_frames)
        out_music_file.setsampwidth(sample_width)
        out_music_file.setnchannels(type_channel)
        out_music_file.writeframes(out_data)
        out_music_file.close()

def readfile(fil):
	global formatted_data
	global type_channel
	global sample_rate
	global sample_width
	global num_frames
        music_file = wave.open(fil, 'rb')
        type_channel = music_file.getnchannels()
        sample_rate = music_file.getframerate()
        sample_width = music_file.getsampwidth()
        num_frames = music_file.getnframes()
        raw_data = music_file.readframes(num_frames ) # Returns byte data
        music_file.close()
        num_samples = num_frames * type_channel
        if sample_width == 1:
                 fmt = "%iB" % num_samples # read unsigned chars
        elif sample_width == 2:
                 fmt = "%ih" % num_samples # read signed 2 byte shorts
        else:
                 raise ValueError("Only supports 8 and 16 bit audio formats.")
        formatted_data = list(struct.unpack(fmt,raw_data))

###################Function to play music################	
def playfile(fil,val):
	global formatted_data
	readfile(fil)
	amplitude(val)
	scale(val)
	shift(val)
	reverse(val)
	packfile(fil,val)
	global wf
	wf=wave.open('output_file.wav', 'rb')
	chunk=1024
	# create an audio object
	p = pyaudio.PyAudio()
	# open stream based on the wave object which has been input.
	stream = p.open(format =
                p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True,
		stream_callback=callb)
	stream.start_stream()
	root.mainloop()
	while stream.is_active():
		time.sleep(0.1)
	
	stream.stop_stream()
	stream.close()
	wf.close()
	p.terminate()

def gui():
	#root = Tk()
	label=Label(root,text="WAVE MIXER")
	label.pack(fill="both",expand="yes")

	#frame 1
	global frame1
	frame1=LabelFrame(root,text="WAVE 1")
	frame1.pack(fill="both",expand="yes",side=LEFT)
	wave1=Button(frame1,text="Wave 1", command=lambda:browsefile(1))
	wave1.pack()
	play=Button(frame1,text="play",command=lambda:playfile(fil1,1))
	play.pack()

	global amp1
	amp1=DoubleVar()
	scale_amp1=Scale(frame1,variable=amp1,orient=HORIZONTAL,to=5.0,from_=0.0,label="Amplification",resolution=0.1)
	scale_amp1.pack(anchor=CENTER)

	global shift1
	shift1=DoubleVar()
	scale_shift1=Scale(frame1,variable=shift1,orient=HORIZONTAL,to=1.0,from_=-1.0,label="Time Shift",resolution=0.1)
	scale_shift1.pack(anchor=CENTER)

	global scaling1
	scaling1=DoubleVar()
	scale_scaling1=Scale(frame1,variable=scaling1,orient=HORIZONTAL,label="Time scaling",resolution=0.1)
	scale_scaling1.pack(anchor=CENTER)
	global f1_s1
	global f1_s2
	global f1_s3
	f1_s1=IntVar()
	f1_s2=IntVar()
	f1_s3=IntVar()
	f1_ss1=Checkbutton(frame1,text="Time Reversal",variable=f1_s1,onvalue=1,offvalue=0,height=5,width=20)
	f1_ss2=Checkbutton(frame1,text="Select for Modulation",variable=f1_s2,onvalue=1,offvalue=0,height=5,width=20)
	f1_ss3=Checkbutton(frame1,text="Select for Mixing",variable=f1_s3,onvalue=1,offvalue=0,height=5,width=20)
	f1_ss1.pack()	
	f1_ss2.pack()	
	f1_ss3.pack()	
	
	#frame 2
	global frame2
	frame2=LabelFrame(root,text="WAVE 2")
	frame2.pack(fill="both",expand="yes",side=LEFT)
	wave2=Button(frame2,text="Wave 2",command=lambda:browsefile(2))
	wave2.pack()
	play=Button(frame2,text="play",command=lambda:playfile(fil2))
	play.pack()

	global amp2
	amp2=DoubleVar()
	scale_amp2=Scale(frame2,variable=amp2,orient=HORIZONTAL,to=5.0,from_=0.0,label="Amplification",resolution=0.1)
	scale_amp2.pack(anchor=CENTER)

	global shift2
	shift2=DoubleVar()
	scale_shift2=Scale(frame2,variable=shift2,orient=HORIZONTAL,to=1.0,from_=-1.0,label="Time Shift",resolution=0.1)
	scale_shift2.pack(anchor=CENTER)

	global scaling2
	scaling2=DoubleVar()
	scale_scaling2=Scale(frame2,variable=scaling2,orient=HORIZONTAL,label="Time scaling",resolution=0.1)
	scale_scaling2.pack(anchor=CENTER)

	global f2_s1
	global f2_s2
	global f2_s3
	f2_s1=IntVar()
	f2_s2=IntVar()
	f2_s3=IntVar()
	f2_ss1=Checkbutton(frame2,text="Time Reversal",variable=f2_s1,onvalue=1,offvalue=0,height=5,width=20)
	f2_ss2=Checkbutton(frame2,text="Select for Modulation",variable=f2_s2,onvalue=1,offvalue=0,height=5,width=20)
	f2_ss3=Checkbutton(frame2,text="Select for Mixing",variable=f2_s3,onvalue=1,offvalue=0,height=5,width=20)
	f2_ss1.pack()	
	f2_ss2.pack()	
	f2_ss3.pack()	
	
	#frame 3
	global frame3
	frame3=LabelFrame(root,text="WAVE 3")
	frame3.pack(fill="both",expand="yes",side=LEFT)

	wave3=Button(frame3,text="Wave 3",command=lambda:browsefile(3))
	wave3.pack()
	play=Button(frame3,text="play",command=lambda:playfile(fil3))
	play.pack()

	global amp3
	amp3=DoubleVar()
	scale_amp3=Scale(frame3,variable=amp3,orient=HORIZONTAL,to=5.0, from_=0.0,label="Amplification",resolution=0.1)
	scale_amp3.pack(anchor=CENTER)

	global shift3
	shift3=DoubleVar()
	scale_shift3=Scale(frame3,variable=shift3,orient=HORIZONTAL,to=1.0,from_=-1.0,label="Time Shift",resolution=0.1)
	scale_shift3.pack(anchor=CENTER)

	global scaling3
	scaling3=DoubleVar()
	scale_scaling3=Scale(frame3,variable=scaling3,orient=HORIZONTAL,label="Time scaling",resolution=0.1)
	scale_scaling3.pack(anchor=CENTER)
	
	global f3_s1
	global f3_s2
	global f3_s3
	f3_s1=IntVar()
	f3_s2=IntVar()
	f3_s3=IntVar()
	f3_ss1=Checkbutton(frame3,text="Time Reversal",variable=f3_s1,onvalue=1,offvalue=0,height=5,width=20)
	f3_ss2=Checkbutton(frame3,text="Select for Modulation",variable=f3_s2,onvalue=1,offvalue=0,height=5,width=20)
	f3_ss3=Checkbutton(frame3,text="Select for Mixing",variable=f3_s3,onvalue=1,offvalue=0,height=5,width=20)
	f3_ss1.pack()	
	f3_ss2.pack()	
	f3_ss3.pack()	

	bottom=Frame(root)
	bottom.pack(side=BOTTOM,expand="yes",fill="both")
	#Modulate AND Play Button
	mod=Button(bottom, text="Modulate And Play", command=modulation)
	mod.pack()

	#Mix AND Play Button
	mix=Button(bottom,text="Mix And Play", command=mixing)
	mix.pack()

	#Record sound
	rec=Button(bottom,text="Record",command=record)
	rec.pack()
	root.mainloop()

gui()
