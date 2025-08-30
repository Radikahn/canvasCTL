"""Data models for the Canvas Calendar application."""

from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional, Dict, List
from collections import defaultdict

@dataclass
class Assignment:
    """Represents a Canvas assignment."""
    name: str
    course: str
    due_date: datetime
    due_time: str
    url: Optional[str] = None
    
    @property
    def date_key(self) -> date:
        """Return the date portion for grouping assignments."""
        return self.due_date.date()

class AssignmentCollection:
    """Collection of assignments organized by date."""
    
    def __init__(self):
        self._assignments_by_date: Dict[date, List[Assignment]] = defaultdict(list)
    
    def add_assignment(self, assignment: Assignment):
        """Add an assignment to the collection."""
        self._assignments_by_date[assignment.date_key].append(assignment)
    
    def get_assignments_for_date(self, target_date: date) -> List[Assignment]:
        """Get all assignments for a specific date."""
        assignments = self._assignments_by_date.get(target_date, [])
        # Sort by due time
        assignments.sort(key=lambda x: x.due_date)
        return assignments
    
    def has_assignments_for_date(self, target_date: date) -> bool:
        """Check if there are assignments for a specific date."""
        return target_date in self._assignments_by_date
    
    def clear(self):
        """Clear all assignments."""
        self._assignments_by_date.clear()
