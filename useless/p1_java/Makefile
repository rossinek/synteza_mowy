# define compiler and compiler flag variables

JFLAGS = -g
JC = javac
OUTPUT = app.jar

ifeq (zad, $(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "run"
  ZAD_NUM := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(ZAD_NUM):;@:)
endif

# Clear any default targets for building .class files from .java files; we 
# will provide our own target entry to do this in this makefile.
# make has a set of default targets for different suffixes (like .c.o) 
# Currently, clearing the default for .java.class is not necessary since 
# make does not have a definition for this target, but later versions of 
# make may, so it doesn't hurt to make sure that we clear any default 
# definitions for these

.SUFFIXES: .java .class

# Here is our target entry for creating .class files from .java files 
# This is a target entry that uses the suffix rule syntax:
#	DSTS:
#		rule
#  'TS' is the suffix of the target file, 'DS' is the suffix of the dependency 
#  file, and 'rule'  is the rule for building a target	
# '$*' is a built-in macro that gets the basename of the current target 
# Remember that there must be a < tab > before the command line ('rule') 

.java.class:
	$(JC) $(JFLAGS) $*.java

# CLASSES is a macro consisting of 4 words (one for each java source file)

CLASSES = \
	synteza/zad*/Main.java
        
# the default make target entry
default: 
	echo "usage: make zad <num>"

#wavfiles:
#	$(JC) $(JFLAGS) synteza/zad3/WavFile.java
#	$(JC) $(JFLAGS) synteza/zad3/WavFileException.java

zad: clean classes mkjar

mkjar:
	jar cfe $(OUTPUT) synteza/zad$(ZAD_NUM)/Main synteza/*/*.class

run:
	java -jar $(OUTPUT)
# This target entry uses Suffix Replacement within a macro: 
# $(name:string1=string2)
# 	In the words in the macro named 'name' replace 'string1' with 'string2'
# Below we are replacing the suffix .java of all words in the macro CLASSES 
# with the .class suffix

classes: $(CLASSES:.java=.class)

clean:
	$(RM) \
	synteza/*/*.class \
	$(OUTPUT)
