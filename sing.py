#coding=UTF-8
'''
Tian Zhou (https://github.com/yanxiangtianji/PySing)
2013 Feb. 14

A simple Python program composing music according to an input file.
This program is dependent on pywin32.

Format of input file:
1, If a "#" at the beginning of a line, that line is commented and will not be processed.
	So you can add the name of the song or the lyric
2, If a "@" at the beginning of a line, that line is a command line.
3, Empty lines will be omitted.
4, Main part is many notes (whose format will be explained latter) separated by blanks
'''
'''
Format for command:
0, Command name is "@xxxx", and separated from its content by a space 
1, "@tune" (no quote mark) means which tune the following part are:
	Only "ABCDEFG" and "abcdefg" are supported.
	The capital words "X" means X major and the lowercase word "x" means X minor.
	Example: "@tune A"
	Default: C major
2, "@bpm" (no quote mark) means the speed of the following part:
	It should be an integer which means how many beats per second.
	Example: "@bpm 120"
	Default: 120
3, "@rhythm" (no quote mark) means what time the the following part is:
	It is two integers connected by a splash.
	The integer before the splash means how many beats per bar.
	The integer after the splash means which note is considered as a beat.
	Example: "@rhythm 4/4"
	Default: 4/4
'''
'''
Format of notes (referenced Numbered Musical Notation(MMN)):
1, Each note is separated by a blank (space, enter)
2, Tune marks:
	2.1, Number 1,2,3,4,5,6,7 represent do,re,mi,fa,sol,la,xi, the same to MMN
	2.2, Each dot(".") BEFORE a number means an octave HIGHER, as a dot over a number in MMN
	2.3, Each dot(".") AFTER a number means an octave LOWER, as a dot under a number in MMN
	2.4, Dots can not appear on both sides of a number
3, Speed marks:
	3.1, Marks("-", "_", ",") just appear on the right side of a number as in MMN 
	3.2, Mark "-" means to add a quarter note length to it, as the short line after a note in MMN
	3.3, Mark "_" means to halve a note, as the line under a number in MMN
	3.4, Mark "," means to add a half of the existing length, as the "." note after the number in MMN
'''
import win32api
import types,re,sys

def sound_basic(feq,dur):
	win32api.Beep(feq,dur) if feq>37 else win32api.Sleep(dur)
	#win32api.Sleep(dur)
	
class Tune:
	#	A	#A	B	C	#C	D	#D	E	F	#F	G	#G
	# 0 for silence note
	frequency=[0,
		28, 29, 31, 33, 35, 37, 39, 41, 44, 46, 49, 52,
		55, 58, 62, 65, 69, 73, 78, 82, 87, 92, 98, 104,
		110, 117, 123, 131, 139, 147, 156, 165, 175, 185, 196, 208,
		220, 233, 247, 262, 277, 294, 311, 330, 349, 370, 392, 415,
		440, 466, 494, 523, 554, 587, 622, 659, 698, 740, 784, 831,
		880, 932, 988, 1047, 1109, 1175, 1245, 1319, 1397, 1480, 1568, 1661,
		1760, 1865, 1976, 2093, 2217, 2349, 2489, 2637, 2794, 2960, 3136, 3322,
		3520, 3729, 3951, 4186]
	tune_base={'A':37 ,'B':39, 'C':40, 'D':42, 'E':44, 'F':45, 'G':47}
	big_tune=[0,2,4,5,7,9,11]
	small_tune=[0,2,3,5,7,8,10]

#readable part
	naming={'do':1,'re':2,'mi':3,'fa':4,'sol':5,'la':6,'si':7}
	naming_re={0:'empty',1:'do',2:'re',3:'mi',4:'fa',5:'sol',6:'la',7:'si'}
	reg_num=re.compile(r'\d')
	reg_sub=re.compile(r'-|_|,')
	@staticmethod
	def readable_name(note):
		res=Tune.reg_sub.sub('',note)
		num=Tune.reg_num.search(res).group()
		return res.replace(num, Tune.naming_re[int(num)])
#end readable part

	def __init__(self,name='C'):
		self.name=name
		self.base=Tune.tune_base[name.upper()]
		self.tune=Tune.big_tune if name.isupper() else Tune.small_tune
	def transfer(self,num,c_dot):
		index=(0 if num==0 else self.base+self.tune[num-1]+12*c_dot)
		return self.frequency[index]
	def get(self,note):
		found_num=False
		num=0
		f_before=0
		f_after=0
		for ch in note:
			if '0'<=ch<='7':
				found_num=True
				num=int(ch)
			elif ch=='.':
				if found_num:
					f_after+=1
				else:
					f_before+=1
		if f_before!=0 and f_after!=0:
			raise Exception('Wrong note in tune!('+note+')')
		return self.transfer(num,f_before-f_after)
#end class Tune

class Speed:
	naming={'1/2':1.0/2, '1/4':1.0/4, '1/8':1.0/8, '1/16': 1.0/16,
		 '1/32':1.0/32, '1/64':1.0/64, '1/128':1.0/128}
	
	def __init__(self,name='default',bpm='120',rhythm='4/4'):
		'''
		bpm - int : beats per minute (120,90)
		base - float/str : which kind note is a beat (0.25,'1/4','1/8')
		bar - int : how many beats per bar
		'''
		self.name=name
		self.bpm=int(bpm)
		self.set_rhythm(rhythm)
		self._cal_unit()
	def set_bpm(self,bpm):
		self.bpm=int(bpm)
		self._cal_unit()
	def set_base(self,base):
		self.base=Speed.naming[base] if type(base)==types.StringType else base
		self._cal_unit()
	def set_bar(self,bar):
		self.bar=bar
		self._cal_unit()
	def set_rhythm(self,rhythm):
		s=rhythm.split('/')
		base='1/'+s[1]
		self.base=Speed.naming[base] if type(base)==types.StringType else base
		self.bar=int(s[0])
		self._cal_unit()
	def _cal_unit(self):
		self.unit=60.0/self.bpm/self.base*1000.0
	def transfer(self,n_quarter):
		return self.unit*n_quarter/4.0
	def get(self,note):
		found_num=False
		onehalf=False
		dur=0
		divide=0
		for ch in note:
			if '0'<=ch<='7':
				found_num=True
			elif found_num==False:
				continue
			elif ch=='-':
				dur+=1
			elif ch=='_':
				divide+=1
			elif ch==',':
				onehalf=True
		if (dur>0 and divide>0) or (onehalf and dur>0):
			raise Exception('Wrong note in speed! ('+note+')')
		return self.transfer(2**(-divide)*(1.5 if onehalf else 1.0)+dur)
#end class Speed

class FileReader:
	def __init__(self,filename):
		self.filename=filename
		self.f=open(filename,'r')
	def __del__(self):
		self.f.close()
	def open(self):
		self.f=open(self.filename)
	def close(self):
		self.f.close()
	def _parse(self,line,line_num):
		res=[]
		if len(line)==0 or line[0]=='#':
			pass
		elif line[0]=='@':
			s=line.split(' ')
			if not self.check_command(s):
				raise Exception('Wrong command line ('+line+') in #: '+str(line_num))
			res.append(s)
		else:
			s=line.split(' ')
			for item in s:
				if item=='':
					continue
				res.append(item)
		return res
	def readnextline(self):
		line=self.f.readline()
		return self._parse(line[:-1], 0)
	def read(self,start_line=0,end_line=0x7fffffff):
		'''
		Read original file and pre-process it into notes.
		Just read lines from start_line to end_line.
		Default: all lines
		'''
		res=[]
		self.f=open(self.filename,'r')	#if have opened, reopen to the beginning
		line_num=0
		for line in self.f:
			line_num+=1
			if line_num<start_line:
				continue
			elif line_num>end_line:
				break
			res+=self._parse(line[:-1] if line[-1]=='\n' else line,line_num)
		self.f.close()
		return res
	def check_command(self,s):
		'''
		return True when length(s)==2 and the command is supported
		'''
		return (len(s)==2 and s[0] in ('@tune','@bpm','@rhythm'))
#end class FileReader

class Song:
	def __init__(self,filename=None,content=None,read=False):
		'''
		Read raw data from file (whose name is filename) if content==None,
		else get raw data from content.
		If read==True, print all readable note and its last time.
		'''
		self.filename=filename
		self.content=content
		self.read=read
		if filename:
			self.file_reader=FileReader(filename)
		self.tune=Tune()
		self.speed=Speed()
	def set_content(self,content):
		self.content=content
	def set_tune(self,tune):
		self.tune=tune
	def set_speed(self,speed):
		self.speed=speed
	def handle_command(self,command_pair):
		if command_pair[0]=='@tune':
			self.tune=Tune(command_pair[1])
		elif command_pair[0]=='@bpm':
			self.speed.set_bpm(command_pair[1])
		elif command_pair[0]=='@rhythm':
			self.speed.set_rhythm(command_pair[1])
		else:
			print 'Wrong command_pair[0]!'
	def getdata(self):
		if self.content:
			return self.content 
		return self.file_reader.read()
	def play(self,start_time=0,end_time=0x7fffffff):
		'''
		Play start from start_time to end_time
		Default: all
		'''
		for note_cmd in self.getdata():
			if type(note_cmd)==types.StringType:
				#note:
				pitch=self.tune.get(note_cmd)
				duration=self.speed.get(note_cmd)
				if self.read:
					try:
						print Tune.readable_name(note_cmd),duration
					except Exception,e:
						print 'Error in '+note_cmd+'\n'+e
				sound_basic(pitch,int(duration))
			else:
				#command pair:
				if self.read:
					print note_cmd
				self.handle_command(note_cmd)
#end class Song 

def main():
#	data=['1','2','3','4','5','6','7']
#	song=Song(content=data, read=True)
	song=Song('canon.txt', read=True)
#	song=Song('zxmzf.txt', read=True)
#	song=Song('myheartwillgoon.txt', read=True)
#	song=Song('gangnamstyle.txt', read=True)
#	song=Song('whkl.txt', read=True)
	song.play()
	
def go(fn,read=True):
	song=Song(fn,read=read);
	song.play();
	
if __name__ == '__main__':
	print sys.argv
	print 'start'
#	main()
	go(sys.argv[1],len(sys.argv)<3 or bool(sys.argv[2]))
	print 'end'
