all: linux

regretnumbers: regretnumbers.c
	@echo Making file...
	gcc -O3 -o output regretnumbers.c
	@echo Finish!

linux: regretnumbers.c
	@echo Making file...
	gcc -O3 -o output regretnumbers.c -lm
	@echo Finish!

clean:
	@echo Cleaning...
	del output.exe
	@echo Finish cleaning!
