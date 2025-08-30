# keyboard_handler.py
"""Keyboard input handling for the calendar application."""

import urwid
from datetime import date, timedelta

class KeyboardHandler:
    """Handles keyboard input for the calendar application."""
    
    def __init__(self, calendar_widget, appointment_widget, main_loop):
        self.calendar_widget = calendar_widget
        self.appointment_widget = appointment_widget
        self.main_loop = main_loop
    
    def handle_input(self, key):
        """Handle keyboard input (calcurse-like shortcuts)"""
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()
        elif key == 'h':
            self.show_help()
        elif key == 't':
            self.calendar_widget.go_to_today()
            self.update_appointment_header()
        elif key in ('j', 'down'):
            self.calendar_widget.navigate_day(1)
            self.update_appointment_header()
        elif key in ('k', 'up'):
            self.calendar_widget.navigate_day(-1)
            self.update_appointment_header()
        elif key in ('l', 'right'):
            self.calendar_widget.navigate_day(7)
            self.update_appointment_header()
        elif key == 'left':
            self.calendar_widget.navigate_day(-7)
            self.update_appointment_header()
        elif key in ('>', '.'):
            self.calendar_widget.next_month(None)
            self.update_calendar_header()
        elif key in ('<', ','):
            self.calendar_widget.prev_month(None)
            self.update_calendar_header()
        elif key == 'r':
            self.refresh_assignments()
    
    def refresh_assignments(self):
        """Refresh assignments from Canvas API."""
        # This would need to be implemented by the main app
        pass
    
    def update_appointment_header(self):
        """Update appointment panel header."""
        # This would need to be implemented by the main app
        pass
    
    def update_calendar_header(self):
        """Update calendar panel header."""
        # This would need to be implemented by the main app
        pass
    
    def show_help(self):
        """Show help dialog (calcurse style)"""
        help_text = [
            "Canvas Calendar Help",
            "",
            "Navigation:",
            "  j, ↓     : Next day",
            "  k, ↑     : Previous day", 
            "  l, →     : Next week",
            "  ←        : Previous week",
            "  >, .     : Next month",
            "  <, ,     : Previous month",
            "  t        : Go to today",
            "",
            "Other:",
            "  r        : Refresh assignments",
            "  h        : Show this help",
            "  q        : Quit",
            "",
            "Press any key to close help..."
        ]
        
        help_widgets = []
        for line in help_text:
            help_widgets.append(urwid.Text(line))
        
        help_widget = urwid.ListBox(urwid.SimpleListWalker(help_widgets))
        help_dialog = urwid.LineBox(help_widget, title="Help")
        
        # Get the main widget from the main loop
        main_widget = self.main_loop.widget
        
        overlay = urwid.Overlay(
            help_dialog, main_widget,
            align='center', width=40,
            valign='middle', height=len(help_text) + 2
        )
        
        def close_help(key):
            if key:
                self.main_loop.widget = main_widget
                self.main_loop.unhandled_input = self.handle_input
        
        self.main_loop.widget = overlay
        self.main_loop.unhandled_input = close_help