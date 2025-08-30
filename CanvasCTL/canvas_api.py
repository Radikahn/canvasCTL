"""Canvas API integration module."""

from canvasapi import Canvas
from datetime import datetime
from typing import List
import logging

from .config import Config
from .models import Assignment, AssignmentCollection

logger = logging.getLogger(__name__)

class CanvasAPIClient:
    """Client for interacting with Canvas API."""
    
    def __init__(self, config: Config):
        self.config = config
        self.canvas = Canvas(base_url=config.api_url, access_token=config.api_key)
    
    def load_assignments(self) -> AssignmentCollection:
        """Load assignments from Canvas API."""
        collection = AssignmentCollection()
        
        try:
            for course_id in self.config.course_list:
                if not course_id.strip():  # Skip empty course IDs
                    continue
                    
                self._load_course_assignments(course_id.strip(), collection)
                
        except Exception as e:
            logger.error(f"Error loading assignments: {str(e)}")
            # Add error assignment for debugging
            error_assignment = Assignment(
                name=f'Error loading assignments: {str(e)}',
                course='System',
                due_date=datetime.now(),
                due_time='--:--',
                url=None
            )
            collection.add_assignment(error_assignment)
        
        return collection
    
    def _load_course_assignments(self, course_id: str, collection: AssignmentCollection):
        """Load assignments for a specific course."""
        try:
            curr_course = self.canvas.get_course(course_id)
            assignments = curr_course.get_assignments()
            
            for assignment in assignments:
                if assignment.due_at:
                    # Parse due date
                    due_date = datetime.fromisoformat(assignment.due_at.replace('Z', '+00:00'))
                    
                    canvas_assignment = Assignment(
                        name=assignment.name,
                        course=curr_course.name,
                        due_date=due_date,
                        due_time=due_date.strftime('%H:%M'),
                        url=getattr(assignment, 'html_url', None)
                    )
                    
                    collection.add_assignment(canvas_assignment)
                    
        except Exception as e:
            logger.error(f"Error loading assignments for course {course_id}: {str(e)}")