# PySing
make the machine sing a pitch according to given notes. The note format is very easy to learn and directly related to the Numbered Musical Notation (MMN).
Depend on pywin32

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
