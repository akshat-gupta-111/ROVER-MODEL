# utils/curses_ui.py
import curses

class CursesUI:
    def __init__(self):
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)

    def display_status(self, command="", status="Idle", detection="Not Detected"):
        self.screen.clear()
        self.screen.addstr(0, 0, "🎯 Cricket Ball Detector (with curses)")
        self.screen.addstr(2, 0, f"🗣️  Last Command: {command}")
        self.screen.addstr(3, 0, f"📡 Status: {status}")
        self.screen.addstr(4, 0, f"🏏 Ball Detection: {detection}")
        self.screen.refresh()

    def end(self):
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()