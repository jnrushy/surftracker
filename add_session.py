# Import required modules
from models import SurfSession, get_session  # Database models and session management
from datetime import datetime  # For handling dates and timestamps

# Define standard wave height ranges and their corresponding numerical values
# The numerical values represent the average height for the range
# For ranges with '+', we use a slightly higher value to indicate larger waves
WAVE_HEIGHT_RANGES = {
    '0-1': 0.5,   # Ankle to knee high
    '1-2': 1.5,   # Knee to waist high
    '2-3': 2.5,   # Waist to chest high
    '2-3+': 3.0,  # Chest high plus
    '3-4': 3.5,   # Head high
    '3-4+': 4.0   # Head high plus
}

def get_wave_height():
    """
    Interactive function to get wave height from user.
    Displays predefined wave height ranges and validates user input.
    
    Returns:
        float or None: The numerical wave height value, or None if no input
    """
    while True:
        # Display available wave height ranges
        print("\nWave height ranges:")
        for range_option in WAVE_HEIGHT_RANGES.keys():
            print(f"  {range_option}")
        
        # Get user input
        height_str = input("\nSelect wave height range: ").strip()
        
        # Handle empty input
        if not height_str:
            return None
        
        # Validate and convert input to numerical value
        if height_str in WAVE_HEIGHT_RANGES:
            return WAVE_HEIGHT_RANGES[height_str]
        else:
            print("Please select a valid wave height range from the list")

def get_waves_caught():
    """
    Interactive function to get number of waves caught.
    Validates that input is a non-negative integer.
    
    Returns:
        int or None: Number of waves caught, or None if no input
    """
    while True:
        waves = input("Number of waves caught: ").strip()
        # Handle empty input
        if not waves:
            return None
        try:
            # Convert input to integer and validate
            waves = int(waves)
            if waves < 0:
                print("Number of waves cannot be negative")
                continue
            return waves
        except ValueError:
            print("Please enter a valid number")

def add_new_session():
    """
    Main function to add a new surf session to the database.
    Collects all session details through interactive prompts,
    validates the data, and saves it to the database.
    """
    print("\nAdd New Surf Session")
    print("-------------------")
    
    # Get session date - either today or a specific date
    date_str = input("Date (YYYY-MM-DD, press Enter for today): ").strip()
    if date_str:
        date = datetime.strptime(date_str, "%Y-%m-%d")  # Convert string to datetime
    else:
        date = datetime.now()  # Use current date/time
    
    # Get required location
    location = input("Location: ").strip()
    
    # Get wave height using helper function
    wave_height = get_wave_height()
    
    # Get session duration
    duration = input("Session duration (in minutes): ").strip()
    duration = int(duration) if duration else None
    
    # Get number of waves caught
    waves_caught = get_waves_caught()
    
    # Get any additional notes
    notes = input("Session notes: ").strip()
    
    # Create a new SurfSession object with collected data
    # Some fields are left as None for future implementation
    session = SurfSession(
        date=date,
        location=location,
        wave_height=wave_height,
        wave_quality=None,  # Future enhancement
        wind_speed=None,    # Future enhancement
        wind_direction=None, # Future enhancement
        tide_height=None,   # Future enhancement
        water_temp=None,    # Future enhancement
        session_duration=duration,
        waves_caught=waves_caught,
        notes=notes,
        rating=None         # Future enhancement
    )
    
    # Initialize database session
    db_session = get_session()
    try:
        # Add and commit the new session to the database
        db_session.add(session)
        db_session.commit()
        print("\nSession successfully added!")
        
        # Display the saved session details for confirmation
        print("\nAdded Session Details:")
        print(f"Date: {session.date}")
        print(f"Location: {session.location}")
        print(f"Wave Height: {session.wave_height}ft")
        print(f"Duration: {session.session_duration} minutes")
        print(f"Waves Caught: {session.waves_caught}")
        print(f"Notes: {session.notes}")
        
    except Exception as e:
        # Handle any database errors
        print(f"Error adding session: {str(e)}")
        db_session.rollback()  # Rollback changes if there's an error
    finally:
        # Always close the database session
        db_session.close()

# Script entry point
if __name__ == "__main__":
    add_new_session() 