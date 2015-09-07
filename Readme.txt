功能：使用Python播放简谱。
环境：Python + pywin32
http://sourceforge.net/projects/pywin32/

简谱格式说明：sing.py程序中带有了对于程序可以识别的简谱格式的说明。并且附带了几个例子以及一个简谱知识快速入门网页。
另外我设计的记号与简谱中的记号一一对应，及时没有任何乐理知识的人也可以对照简谱写出程序可以识别的乐谱。
“#”：若在行首则表示此行注释；
“@”：若在行首则表示属性说明，用以指定速度、节拍、调式，支持在乐谱中使用多次相同的属性说明符，以实现变调；
音符：
“0”：休止符；
“1”-“7”:音高（do到si）与简谱表示法相同；
“.”:变化音高所在八度，在数字前面每出现表示升一个八度（同简谱中数字上方的点号），在数字后面每出现表示减低一个八度（同简谱中数字下方的点号）
“-”：延长四分之一个音符（同简谱中数字后方的短线）
“_”：将音符的时值减半（同简谱中数字下方的短线）
“,”：将音符的时值加长一半（同简谱中数字后方的点号）

Format of input file:
1, If a "#" at the beginning of a line, that line is commented and will not be processed.
	So you can add the name of the song or the lyric
2, If a "@" at the beginning of a line, that line is a command line.
3, Empty lines will be omitted.
4, Main part is many notes (whose format will be explained latter) separated by blanks

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

Format of notes (referenced Numbered Musical Notation(MMN)):
1, Each note is separated by a blank (space, enter)
2, Tune marks:
	2.1, Number 1,2,3,4,5,6,7 represent do,re,mi,fa,sol,la,xi, the same to MMN
	2.2, Each dot(".") BEFORE a number means an octave HIGHER, as a dot over a number in MMN
	2.3, Each dot(".") AFTER a number means an octave LOWER, as a dot under a number in MMN
	2.4, Dots can not appear on both sides of a number
3, Speed marks:
	3.1, Marks("-", "_", ",") just appear on the right side of a number as in MMN 
	3.2, Mark "-" means to ADD a quarter note length to it, as the short line AFTER a note in MMN
	3.3, Mark "_" means to HALVE a note, as the line UNDER a number in MMN
	3.4, Mark "," means to add a half of the existing length, as the "." note after the number in MMN
