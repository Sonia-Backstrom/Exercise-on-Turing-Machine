import sys

from tape import Symbol, Tape

#Move the head to the first value cell after START.
def rewind(tape: Tape):  
    while tape.read() is not Symbol.START:
        tape.move_left()
    tape.move_right()

#Put START at the beginning of a work tape.
def make_start(tape):
    tape.write(Symbol.START)
    tape.move_right()


#Append one ONE to a unary value.
def append_one(tape):
    while tape.read() is Symbol.ONE:
        tape.move_right()
    tape.write(Symbol.ONE)

#Increase a unary value by one.
def increment(tape):
    rewind(tape)
    append_one(tape)

#Copy the input unary word onto the remainder tape.
def copy_input(input_tape, remainder):
    while input_tape.read() is Symbol.ONE:
        append_one(remainder)
        input_tape.move_right()

#Check whether an unconsumed ONE remains.
def has_one(tape):
    rewind(tape)

    while tape.read() is Symbol.MARK:
        tape.move_right()

    return tape.read() is Symbol.ONE

#Subtract source from target using unary symbols.
def subtract(source, target):
    rewind(source)
    rewind(target)

    while source.read() is Symbol.ONE:
        while target.read() is Symbol.MARK:
            target.move_right()

        if target.read() is Symbol.BLANK:
            Tape.reject("too large")

        target.write(Symbol.MARK)
        source.move_right()
        rewind(target)

#Add the unary value in source to target.
def add(source, target):
    rewind(source)
    rewind(target)

    while source.read() is Symbol.ONE:
        append_one(target)
        rewind(target)
        target.move_right()
        source.move_right()

#Add six copies of source to target.
def add_six_times(source, target):
    add(source, target)
    add(source, target)
    add(source, target)
    add(source, target)
    add(source, target)
    add(source, target)


def main():
    input_tape = Tape.from_arguments(sys.argv)

    remainder = Tape()
    delta = Tape()
    k = Tape()

    make_start(remainder)
    make_start(delta)
    make_start(k)

    copy_input(input_tape, remainder)

    # 0 is a cube
    if not has_one(remainder):
        Tape.accept()

    # Start with k = 1 and delta = 1
    increment(k)
    increment(delta)

    while True:
        subtract(delta, remainder)

        if not has_one(remainder):
            Tape.accept()

        # Calculate the next cube difference
        add_six_times(k, delta)
        increment(k)


if __name__ == "__main__":
    main()
