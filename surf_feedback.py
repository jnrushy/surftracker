# This program asks about your surf session and responds to your feedback

# Import required Python modules
from datetime import datetime  # For handling dates and times
import json                   # For saving/loading data in JSON format
import os                     # For file operations
from typing import List, Dict # For type hints (helps with code understanding and IDE support)

class SurfSession:
    """
    A class to represent a single surf session.
    This demonstrates object-oriented programming in Python.
    """
    def __init__(self, quality: str, wave_height: float = None, location: str = None, date=None):
        """
        Constructor method - called when creating a new SurfSession
        Uses type hints and default parameters (None)
        """
        self.quality = quality
        self.date = date if date else datetime.now()  # Use provided date or current time
        self.notes = ""
        self.wave_height = wave_height  # in feet
        self.location = location

    def add_notes(self, notes: str):
        """Method to add notes to the session"""
        self.notes = notes
    
    def to_dict(self) -> Dict:
        """
        Convert session to dictionary for JSON storage
        The -> Dict is a return type hint
        """
        return {
            'quality': self.quality,
            'date': self.date.strftime('%Y-%m-%d %H:%M'),  # Convert datetime to string
            'notes': self.notes,
            'wave_height': self.wave_height,
            'location': self.location
        }
    
    @classmethod  # Decorator to indicate this is a class method
    def from_dict(cls, data: Dict) -> 'SurfSession':
        """
        Create a SurfSession from a dictionary
        This is a class method - it creates a new instance of the class
        Used when loading data from JSON
        """
        session = cls(
            quality=data['quality'],
            wave_height=data['wave_height'],
            location=data['location'],
            date=datetime.strptime(data['date'], '%Y-%m-%d %H:%M')  # Convert string back to datetime
        )
        session.notes = data['notes']
        return session

    def __str__(self):
        """
        String representation of the session
        This magic method is called when you print() the object
        """
        details = [f"Surf Session on {self.date.strftime('%Y-%m-%d %H:%M')}: {self.quality}"]
        if self.wave_height:
            details.append(f"Wave Height: {self.wave_height}ft")
        if self.location:
            details.append(f"Location: {self.location}")
        return " | ".join(details)

class SurfLog:
    """
    A class to manage multiple surf sessions
    Handles saving/loading data and calculating statistics
    """
    def __init__(self, filename: str = "surf_log.json"):
        """Initialize with a filename to store the data"""
        self.filename = filename
        self.sessions: List[SurfSession] = []  # Type hint showing this is a list of SurfSession objects
        self.load_sessions()  # Load existing sessions when created

    def add_session(self, session: SurfSession):
        """Add a new session and save to file"""
        self.sessions.append(session)
        self.save_sessions()

    def load_sessions(self):
        """
        Load sessions from JSON file
        Demonstrates file handling and error checking
        """
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:  # 'with' ensures file is properly closed
                data = json.load(f)
                # List comprehension to convert each dictionary to a SurfSession
                self.sessions = [SurfSession.from_dict(s) for s in data]

    def save_sessions(self):
        """
        Save sessions to JSON file
        Demonstrates file writing and data serialization
        """
        with open(self.filename, 'w') as f:
            # Convert each session to a dictionary, then save as JSON
            json.dump([s.to_dict() for s in self.sessions], f, indent=2)

    def get_statistics(self) -> Dict:
        """
        Calculate statistics about surf sessions
        Demonstrates data analysis and dictionary usage
        """
        if not self.sessions:
            return {"message": "No sessions recorded yet!"}

        # Calculate various statistics
        total_sessions = len(self.sessions)
        good_sessions = sum(1 for s in self.sessions if s.quality == 'good')
        
        # Calculate average wave height (only for sessions with recorded height)
        avg_wave_height = sum(s.wave_height for s in self.sessions if s.wave_height) / \
                         sum(1 for s in self.sessions if s.wave_height)
        
        # Count sessions per location using a dictionary
        locations = {}
        for session in self.sessions:
            if session.location:
                locations[session.location] = locations.get(session.location, 0) + 1

        return {
            "total_sessions": total_sessions,
            "good_sessions": good_sessions,
            "good_session_percentage": (good_sessions / total_sessions) * 100,
            "average_wave_height": round(avg_wave_height, 1),
            "favorite_spots": locations
        }

def get_surf_feedback(surf_log: SurfLog) -> SurfSession:
    """
    Get user input about a surf session
    Demonstrates input handling and data validation
    """
    while True:
        response = input("How was your surf session today? (good/bad): ").lower()
        
        if response in ['good', 'bad']:
            # Try/except could be added here for better error handling
            wave_height = float(input("Wave height in feet (press Enter to skip): ") or 0)
            location = input("Where did you surf? (press Enter to skip): ")
            
            session = SurfSession(
                response,
                wave_height if wave_height else None,
                location if location else None
            )
            
            notes = input("Any notes about your session? (press Enter to skip): ")
            if notes:
                session.add_notes(notes)
            
            return session
        
        print("Please enter either 'good' or 'bad'.")

def display_statistics(stats: Dict):
    """
    Display formatted statistics
    Demonstrates string formatting and data presentation
    """
    print("\n=== Surf Session Statistics ===")
    print(f"Total Sessions: {stats['total_sessions']}")
    print(f"Good Sessions: {stats['good_sessions']} ({stats['good_session_percentage']:.1f}%)")
    print(f"Average Wave Height: {stats['average_wave_height']}ft")
    
    if stats['favorite_spots']:
        print("\nFavorite Surf Spots:")
        for spot, count in stats['favorite_spots'].items():
            print(f"  {spot}: {count} sessions")

def main():
    """
    Main program loop
    Demonstrates program flow control and menu-driven interface
    """
    surf_log = SurfLog()
    
    while True:
        # Display menu options
        print("\n1. Record new session")
        print("2. View statistics")
        print("3. View all sessions")
        print("4. Exit")
        
        choice = input("\nWhat would you like to do? (1-4): ")
        
        # Handle user choice
        if choice == '1':
            session = get_surf_feedback(surf_log)
            surf_log.add_session(session)
            print("\nSession recorded!")
            print(session)
            
        elif choice == '2':
            stats = surf_log.get_statistics()
            display_statistics(stats)
            
        elif choice == '3':
            print("\n=== All Surf Sessions ===")
            for session in surf_log.sessions:
                print(session)
                if session.notes:
                    print(f"Notes: {session.notes}\n")
                    
        elif choice == '4':
            print("Hang loose! 🤙")
            break
            
        else:
            print("Invalid choice. Please try again.")

# This is the standard way to define the entry point of a Python program
if __name__ == "__main__":
    main() 