# ui_components.py
"""UI components for the calcurse-style calendar interface."""

import urwid
import calendar
from datetime import date, datetime, timedelta
from typing import Callable, Optional

from .models import AssignmentCollection

class CalendarWidget:
    """Calendar widget component in calcurse style."""
    
    def __init__(self, assignments: AssignmentCollection, day_callback: Callable):
        self.assignments = assignments
        self.day_callback = day_callback
        self.current_date = datetime.now()
        self.selected_date = date.today()
        self.walker = urwid.SimpleListWalker([])
        self.listbox = urwid.ListBox(self.walker)
        
    def update(self):
        """Update the calendar display."""
        self.walker.clear()
        
        # Get calendar for current month
        cal = calendar.monthcalendar(self.current_date.year, self.current_date.month)
        
        # Month header
        month_text = f'{self.current_date.strftime("%B %Y")}'
        self.walker.append(urwid.Text(month_text, align='center'))
        self.walker.append(urwid.Divider('-'))
        
        # Day headers - larger spacing
        day_headers = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        header_text = ''.join(f'{day:^6}' for day in day_headers)
        self.walker.append(urwid.Text(header_text, align='left'))
        
        today = date.today()
        
        # Calendar weeks - each day gets more space
        for week in cal:
            week_widgets = []
            
            for day in week:
                if day == 0:
                    # Empty day - just spacing
                    day_widget = urwid.Text('      ')  # 6 spaces
                else:
                    day_date = date(self.current_date.year, self.current_date.month, day)
                    has_assignments = self.assignments.has_assignments_for_date(day_date)
                    
                    # Day display with assignment indicator
                    if has_assignments:
                        day_text = f' {day:2d}* '
                    else:
                        day_text = f' {day:2d}  '
                    
                    # Determine styling
                    if day_date == today:
                        attr = 'today'
                        day_text = f'[{day:2d}]' + ('*' if has_assignments else ' ')
                    elif day_date == self.selected_date:
                        attr = 'selected_day'  
                        day_text = f'({day:2d})' + ('*' if has_assignments else ' ')
                    elif has_assignments:
                        attr = 'appointment_day'
                    else:
                        attr = 'normal_day'
                    
                    day_widget = urwid.AttrMap(
                        urwid.Button(f'{day_text:^6}', on_press=self.select_day, user_data=day_date),
                        attr, 'focused_day'
                    )
                
                week_widgets.append(day_widget)
            
            # Create week row with proper spacing
            week_row = urwid.Columns(week_widgets, dividechars=0)
            self.walker.append(week_row)
        
        # Add minimal spacing and next month info
        self.walker.append(urwid.Divider())
        if self.current_date.month == 12:
            next_month = self.current_date.replace(year=self.current_date.year + 1, month=1)
        else:
            next_month = self.current_date.replace(month=self.current_date.month + 1)
        
        next_text = f'Next: {next_month.strftime("%B")}'
        self.walker.append(urwid.Text(next_text, align='center'))
    
    def add_minimal_next_month(self):
        """Add minimal next month preview - just one line"""
        # This is now handled in the main update method
        pass
    
    def _week_selected(self, button, week_data):
        """Handle week selection - select the first non-zero day"""
        for day in week_data:
            if day != 0:
                day_date = date(self.current_date.year, self.current_date.month, day)
                self.select_day(None, day_date)
                break
    
    def add_compact_next_month(self):
        """Add a very compact preview of next month"""
        # This method is now replaced by add_minimal_next_month
        pass
    
    def add_next_month_preview(self):
        """Add a small preview of next month like calcurse"""
        # This method is replaced by add_compact_next_month
        pass
    
    def select_day(self, button, day_date):
        """Handle day selection"""
        self.selected_date = day_date
        self.day_callback(day_date)
        self.update()
    
    def prev_month(self, button):
        """Navigate to previous month"""
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(year=self.current_date.year - 1, month=12)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month - 1)
        self.update()
    
    def next_month(self, button):
        """Navigate to next month"""
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month + 1)
        self.update()
    
    def navigate_day(self, days: int):
        """Navigate by days (for keyboard shortcuts)"""
        self.selected_date += timedelta(days=days)
        # Change month if necessary
        if self.selected_date.month != self.current_date.month or self.selected_date.year != self.current_date.year:
            self.current_date = datetime(self.selected_date.year, self.selected_date.month, 1)
        self.day_callback(self.selected_date)
        self.update()
    
    def go_to_today(self):
        """Navigate to current date"""
        self.selected_date = date.today()
        self.current_date = datetime.now()
        self.day_callback(self.selected_date)
        self.update()
    
    def get_header_text(self) -> str:
        """Get the header text for current month."""
        return f"Calendar {self.current_date.strftime('%B %Y')}"

class AppointmentWidget:
    """Appointment widget component in calcurse style."""
    
    def __init__(self, assignments: AssignmentCollection):
        self.assignments = assignments
        self.walker = urwid.SimpleListWalker([])
        self.listbox = urwid.ListBox(self.walker)
        self.current_date: Optional[date] = None
    
    def update_for_date(self, selected_date: date):
        """Update appointments for selected date."""
        self.current_date = selected_date
        self.walker.clear()
        
        # Get assignments for selected date
        assignments = self.assignments.get_assignments_for_date(selected_date)
        
        if not assignments:
            self.walker.append(
                urwid.Text('[No Assignments]')
            )
        else:
            for assignment in assignments:
                # Time and title (calcurse format: HH:MM Assignment Name)
                time_title = f"{assignment.due_time} {assignment.name}"
                assignment_item = urwid.Text(time_title)
                self.walker.append(assignment_item)
                
                # Course name (indented, like calcurse details)
                course_detail = f"  └ {assignment.course}"
                course_item = urwid.Text(course_detail)
                self.walker.append(course_item)
                
                # Add spacing
                self.walker.append(urwid.Text(''))
    
    def get_header_text(self, selected_date: date) -> str:
        """Get the header text for selected date."""
        return f"Assignments - {selected_date.strftime('%A %d %B %Y')}"