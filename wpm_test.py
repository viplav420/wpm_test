import curses
from curses import wrapper
import time
import random

# Global variables
TEXT_FILE = "text.txt"
TIME_LIMIT = 60  # seconds

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the Speed Typing Test!")
    stdscr.addstr("\nPress any key to begin!")
    stdscr.refresh()
    stdscr.getkey()

def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM: {wpm}")

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)

        stdscr.addstr(0, i, char, color)

def load_text():
    with open(TEXT_FILE, "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()

def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        if time_elapsed > TIME_LIMIT:
            break

        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:  # ESC key to exit
            break

        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)

    return time_elapsed, len(target_text)

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    while True:
        stdscr.clear()
        stdscr.addstr("Press any key to start the typing test or ESC to quit...")
        key = stdscr.getkey()

        if ord(key) == 27:  # ESC key to exit
            break

        if key and ord(key) != 27:
            stdscr.clear()
            stdscr.refresh()

            duration, text_length = wpm_test(stdscr)
            if duration > TIME_LIMIT:
                stdscr.clear()
                stdscr.addstr("Time's up!\n\n")
                stdscr.addstr("Press any key to continue...")
                stdscr.getkey()

            stdscr.clear()
            stdscr.addstr("Typing test completed!\n\n")
            stdscr.addstr(f"Elapsed Time: {round(duration, 2)} seconds\n")
            stdscr.addstr(f"Text Length: {text_length} characters\n")
            stdscr.addstr(f"Words Per Minute (WPM): {round((text_length / (duration / 60)) / 5)}\n\n")
            stdscr.addstr("Press any key to start a new test or ESC to quit...")
            key = stdscr.getkey()
            
            if ord(key) == 27:  # ESC key to exit
                break

wrapper(main)
