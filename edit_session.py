from models import get_session, SurfSession
from datetime import datetime

def show_sessions(db_session, limit=10):
    """Show the most recent sessions"""
    sessions = db_session.query(SurfSession).order_by(SurfSession.date.desc()).limit(limit).all()
    
    print("\nRecent Sessions:")
    print("---------------")
    for i, session in enumerate(sessions, 1):
        print(f"\n{i}. Date: {session.date.strftime('%Y-%m-%d')}")
        print(f"   Location: {session.location}")
        print(f"   Wave Height: {session.wave_height}ft")
        print(f"   Waves Caught: {session.waves_caught or 'Not recorded'}")
        print(f"   Notes: {session.notes}")
    
    return sessions

def edit_session():
    """Edit an existing surf session"""
    db_session = get_session()
    try:
        while True:
            # Show recent sessions
            sessions = show_sessions(db_session)
            
            # Get session selection
            print("\nEnter the number of the session to edit (or 'q' to quit):")
            choice = input("> ").strip().lower()
            
            if choice == 'q':
                break
            
            try:
                session_idx = int(choice) - 1
                if 0 <= session_idx < len(sessions):
                    session = sessions[session_idx]
                    
                    # Show current values
                    print("\nCurrent session details:")
                    print(f"Date: {session.date.strftime('%Y-%m-%d')}")
                    print(f"Location: {session.location}")
                    print(f"Wave Height: {session.wave_height}ft")
                    print(f"Duration: {session.session_duration} minutes")
                    print(f"Waves Caught: {session.waves_caught or 'Not recorded'}")
                    print(f"Current notes: {session.notes}")
                    
                    # Get new values
                    print("\nEnter new values (or press Enter to keep current value)")
                    
                    # Update notes
                    new_notes = input("New notes: ").strip()
                    if new_notes:
                        session.notes = new_notes
                    
                    # Update waves caught
                    new_waves = input("New waves caught count: ").strip()
                    if new_waves:
                        try:
                            session.waves_caught = int(new_waves)
                        except ValueError:
                            print("Invalid number, keeping current value")
                    
                    # Update duration
                    new_duration = input("New session duration (minutes): ").strip()
                    if new_duration:
                        try:
                            session.session_duration = int(new_duration)
                        except ValueError:
                            print("Invalid number, keeping current value")
                    
                    # Save changes
                    db_session.commit()
                    print("\nSession updated successfully!")
                    
                    # Show updated session
                    print("\nUpdated session details:")
                    print(f"Date: {session.date.strftime('%Y-%m-%d')}")
                    print(f"Location: {session.location}")
                    print(f"Wave Height: {session.wave_height}ft")
                    print(f"Duration: {session.session_duration} minutes")
                    print(f"Waves Caught: {session.waves_caught or 'Not recorded'}")
                    print(f"Notes: {session.notes}")
                    
                else:
                    print("Invalid session number")
            except ValueError:
                print("Please enter a valid number")
            
            print("\nWould you like to edit another session? (y/n)")
            if input("> ").strip().lower() != 'y':
                break
    
    finally:
        db_session.close()

if __name__ == "__main__":
    edit_session() 