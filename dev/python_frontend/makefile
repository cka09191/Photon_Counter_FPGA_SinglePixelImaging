# Makefile

# Compiler
CC = gcc

# Compiler flags
CFLAGS = -Wall -Werror

# Source files
SRCS = main.c file1.c file2.c

# Object files
OBJS = $(SRCS:.c=.o)

# Executable
TARGET = myprogram

# Default target
all: $(TARGET)

# Compile source files into object files
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Link object files into executable
$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) $^ -o $@

# Clean up object files and executable
clean:
	rm -f $(OBJS) $(TARGET)

help:
	@echo "Usage: make [all|clean|help]"
	@echo "all:    compile source files into object files and link object files into executable"
	@echo "clean:  clean up object files and executable"
	@echo "help:   display this help message"

# Using pyinstaller to make exefile
makeexe:
#pyinstaller --add all data in this folder
	pyinstaller --onefile main.py