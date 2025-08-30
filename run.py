"""
Root project runner for Canvas Calendar.
Place this file in the root directory (same level as canvas_calendar/ folder).
"""

#!/usr/bin/env python3

import sys
import os

def main():
    """Run the Canvas Calendar application."""
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    try:
        # Import and run the application
        from CanvasCTL.main_app import CalcurseCanvasApp
        
        print("Starting Canvas Calendar...")
        app = CalcurseCanvasApp()
        app.run()
        
    except ImportError as e:
        print(f"Import Error: {e}")
        print("Make sure you have installed the required dependencies:")
        print("  pip install urwid canvasapi python-dotenv")
        print("\nAlso ensure your .env file is properly configured with:")
        print("  API_URL=your_canvas_url")
        print("  API_KEY=your_canvas_api_key") 
        print("  COURSE_LIST=course_id1,course_id2,course_id3")
        return 1
        
    except FileNotFoundError:
        print("Error: Could not find .env file or canvas_calendar module.")
        print("Make sure you're running this from the correct directory.")
        return 1
        
    except Exception as e:
        print(f"Error starting Canvas Calendar: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())