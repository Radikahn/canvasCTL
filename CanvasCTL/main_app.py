# main_app.py
"""Main application class for the calcurse-style Canvas Calendar."""

import urwid
from datetime import date
import logging

from .config import Config
from .canvas_api import CanvasAPIClient
from .ui_components import CalendarWidget, AppointmentWidget
from .ui_theme import MONOCHROME_PALETTE
from .keyboard_handler import KeyboardHandler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CalcurseCanvasApp:
    """Main application class for the calcurse-style Canvas Calendar."""
    
    def __init__(self):
        self.config = Config()
        self.api_client = CanvasAPIClient(self.config)
        self.assignments = self.api_client.load_assignments()
        
        # Create UI components
        self.calendar_widget = CalendarWidget(self.assignments, self.day_selected)
        self.appointment_widget = AppointmentWidget(self.assignments)
        
        # Setup main UI
        self.setup_ui()
        
        # Create keyboard handler (will be set after loop creation)
        self.keyboard_handler = None
    
    def setup_ui(self):
        """Setup the calcurse-like interface"""
        # Calendar section (left side, similar to calcurse calendar)
        calendar_title_text = f' Calendar {self.calendar_widget.current_date.strftime("%B %Y")}'
        calendar_title = urwid.Text(calendar_title_text, align='left')
        self.calendar_header = urwid.AttrMap(calendar_title, 'title_bar')
        
        # Make calendar box non-selectable to prevent focus issues
        calendar_content = urwid.LineBox(self.calendar_widget.listbox, title="", title_align='left')
        calendar_box = urwid.Pile([
            ('pack', self.calendar_header),
            calendar_content
        ])
        
        # Appointment section (right side, similar to calcurse appointment list)
        selected_date_str = self.calendar_widget.selected_date.strftime('%A %d %B %Y')
        appointment_title_text = f' Assignments - {selected_date_str}'
        appointment_title = urwid.Text(appointment_title_text, align='left')
        self.appointment_header = urwid.AttrMap(appointment_title, 'title_bar')
        
        # Make appointment box non-selectable to prevent focus issues
        appointment_content = urwid.LineBox(self.appointment_widget.listbox, title="", title_align='left')
        appointment_box = urwid.Pile([
            ('pack', self.appointment_header),
            appointment_content
        ])
        
        # Main columns (60/40 split like calcurse)
        main_columns = urwid.Columns([
            ('weight', 60, calendar_box),
            ('weight', 40, appointment_box)
        ])
        
        # Status bar
        status_bar = urwid.AttrMap(
            urwid.Text('Arrow keys: navigate, t: today, h: help, q: quit'),
            'status_bar'
        )
        
        # Complete layout with status bar - wrap in a container that handles input
        content = urwid.Pile([
            main_columns,
            ('pack', status_bar)
        ])
        
        # Create a top-level widget that captures all input
        self.main_widget = urwid.WidgetWrap(content)
        
        # Initial updates
        self.calendar_widget.update()
        self.appointment_widget.update_for_date(self.calendar_widget.selected_date)
    
    def day_selected(self, selected_date: date):
        """Handle day selection from calendar."""
        self.appointment_widget.update_for_date(selected_date)
        self.update_appointment_header(selected_date)
    
    def update_appointment_header(self, selected_date: date = None):
        """Update the appointment panel header"""
        if selected_date is None:
            selected_date = self.calendar_widget.selected_date
            
        selected_date_str = selected_date.strftime('%A %d %B %Y')
        appointment_title_text = f' Assignments - {selected_date_str}'
        appointment_title = urwid.Text(appointment_title_text, align='left')
        self.appointment_header = urwid.AttrMap(appointment_title, 'title_bar')
        
        # Update in the main widget
        content = self.main_widget._w  # Get the wrapped content
        main_columns = content.contents[0][0]
        appointment_box = main_columns.contents[1][0]
        appointment_box.contents[0] = (self.appointment_header, ('pack', None))
    
    def update_calendar_header(self):
        """Update the calendar header with current month"""
        calendar_title_text = f' Calendar {self.calendar_widget.current_date.strftime("%B %Y")}'
        calendar_title = urwid.Text(calendar_title_text, align='left')
        self.calendar_header = urwid.AttrMap(calendar_title, 'title_bar')
        
        # Update in the main widget
        content = self.main_widget._w  # Get the wrapped content
        main_columns = content.contents[0][0]
        calendar_box = main_columns.contents[0][0]
        calendar_box.contents[0] = (self.calendar_header, ('pack', None))
    
    def refresh_assignments(self):
        """Refresh assignments from Canvas API."""
        logger.info("Refreshing assignments from Canvas...")
        self.assignments = self.api_client.load_assignments()
        self.calendar_widget.assignments = self.assignments
        self.appointment_widget.assignments = self.assignments
        self.calendar_widget.update()
        
        # Refresh current appointment view
        if self.appointment_widget.current_date:
            self.appointment_widget.update_for_date(self.appointment_widget.current_date)
    
    def run(self):
        """Run the main application loop."""
        # Create main loop
        loop = urwid.MainLoop(
            self.main_widget,
            palette=MONOCHROME_PALETTE
        )
        
        # Create keyboard handler with loop reference
        self.keyboard_handler = KeyboardHandler(self.calendar_widget, self.appointment_widget, loop)
        
        # Override the refresh method in keyboard handler
        self.keyboard_handler.refresh_assignments = self.refresh_assignments
        self.keyboard_handler.update_appointment_header = self.update_appointment_header
        self.keyboard_handler.update_calendar_header = self.update_calendar_header
        
        # Set the input handler - back to simple unhandled_input
        loop.unhandled_input = self.keyboard_handler.handle_input
        
        try:
            logger.info("Starting calcurse-style Canvas Calendar application...")
            loop.run()
        except KeyboardInterrupt:
            logger.info("Application terminated by user.")
        except Exception as e:
            logger.error(f"Application error: {str(e)}")
            raise