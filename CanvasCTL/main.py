"""Entry point for the calcurse-style Canvas Calendar application."""

from .main_app import CalcurseCanvasApp

def main():
    """Main entry point for the application."""
    try:
        app = CalcurseCanvasApp()
        app.run()
    except Exception as e:
        print(f"Error starting application: {str(e)}")
        return 1
    return 0

if __name__ == "__main__":
    exit(main())


