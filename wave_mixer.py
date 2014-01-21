from Tkinter import *
import wave
import tkFileDialog
import pyaudio
import wave
import sys

#frame 1
root = Tk()
label=Label(root,text="WAVE MIXER")
label.pack(fill="both",expand="yes")
#frame1 = Frame(root)
#frame1.pack(side=LEFT)
frame1=LabelFrame(root,text="WAVE 1")
frame1.pack(fill="both",expand="yes",side=LEFT)

def browsefile():
	file1=tkFileDialog.askopenfile(parent=root,mode='rb',title='Choose a file')
	return file1
wave1=Button(frame1,text="Wave 1", command=browsefile)
wave1.pack()


amp1=DoubleVar()
scale_amp1=Scale(frame1,variable=amp1,orient=HORIZONTAL)
scale_amp1.pack(anchor=CENTER)

shift1=DoubleVar()
scale_shift1=Scale(frame1,variable=shift1,orient=HORIZONTAL)
scale_shift1.pack(anchor=CENTER)

scaling1=DoubleVar()
scale_scaling1=Scale(frame1,variable=scaling1,orient=HORIZONTAL)
scale_scaling1.pack(anchor=CENTER)

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
#frame2 = Frame(root)
#frame2.pack(side=LEFT)
frame2=LabelFrame(root,text="WAVE 2")
frame2.pack(fill="both",expand="yes",side=LEFT)

wave2=Button(frame2,text="Wave 2")
wave2.pack()

amp2=DoubleVar()
scale_amp2=Scale(frame2,variable=amp2,orient=HORIZONTAL)
scale_amp2.pack(anchor=CENTER)

shift2=DoubleVar()
scale_shift2=Scale(frame2,variable=shift2,orient=HORIZONTAL)
scale_shift2.pack(anchor=CENTER)

scaling2=DoubleVar()
scale_scaling2=Scale(frame2,variable=scaling2,orient=HORIZONTAL)
scale_scaling2.pack(anchor=CENTER)

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
#frame3 = Frame(root)
#frame3.pack(side=LEFT)
frame3=LabelFrame(root,text="WAVE 3")
frame3.pack(fill="both",expand="yes",side=LEFT)

wave3=Button(frame3,text="Wave 3")
wave3.pack()

amp3=DoubleVar()
scale_amp3=Scale(frame3,variable=amp3,orient=HORIZONTAL)
scale_amp3.pack(anchor=CENTER)

shift3=DoubleVar()
scale_shift3=Scale(frame3,variable=shift3,orient=HORIZONTAL)
scale_shift3.pack(anchor=CENTER)

scaling3=DoubleVar()
scale_scaling3=Scale(frame3,variable=scaling3,orient=HORIZONTAL)
scale_scaling3.pack(anchor=CENTER)

f3_s1=IntVar()
f3_s2=IntVar()
f3_s3=IntVar()
f3_ss1=Checkbutton(frame3,text="Time Reversal",variable=f3_s1,onvalue=1,offvalue=0,height=5,width=20)
f3_ss2=Checkbutton(frame3,text="Select for Modulation",variable=f3_s2,onvalue=1,offvalue=0,height=5,width=20)
f3_ss3=Checkbutton(frame3,text="Select for Mixing",variable=f3_s3,onvalue=1,offvalue=0,height=5,width=20)
f3_ss1.pack()	
f3_ss2.pack()	
f3_ss3.pack()	
root.mainloop()

wf = wave.open(file, 'rb')
# create an audio object
p = pyaudio.PyAudio()

# open stream based on the wave object which has been input.
stream = p.open(format =
                p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True)

# read data (based on the chunk size)
data = wf.readframes(chunk)

# play stream (looping from beginning of file to the end)
while data != '':
    # writing to the stream is what *actually* plays the sound.
    stream.write(data)
    data = wf.readframes(chunk)

# cleanup stuff.
stream.close()    
p.terminate()

