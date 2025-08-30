# __init__.py
"""Calcurse-style Canvas Calendar Package."""

from .main_app import CalcurseCanvasApp
from .config import Config
from .models import Assignment, AssignmentCollection
from .canvas_api import CanvasAPIClient

__version__ = "1.0.0"
__all__ = ["CalcurseCanvasApp", "Config", "Assignment", "AssignmentCollection", "CanvasAPIClient"]