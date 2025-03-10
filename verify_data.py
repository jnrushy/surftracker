from models import get_session, SurfSession
from datetime import datetime

def verify_data():
    """Verify the imported surf session data"""
    db_session = get_session()
    try:
        # Get all surf sessions
        surf_sessions = db_session.query(SurfSession).all()
        
        print(f"\nFound {len(surf_sessions)} surf sessions in database:")
        print("\nSample of first 5 sessions:")
        for i, surf_session in enumerate(surf_sessions[:5]):
            print(f"\nSession {i + 1}:")
            print(f"Date: {surf_session.date}")
            print(f"Location: {surf_session.location}")
            print(f"Wave Height: {surf_session.wave_height}")
            print(f"Session Duration: {surf_session.session_duration}")
            print(f"Notes: {surf_session.notes}")
        
        # Print some statistics
        print("\nStatistics:")
        print(f"Total sessions: {len(surf_sessions)}")
        
        # Count sessions by location
        locations = {}
        for surf_session in surf_sessions:
            locations[surf_session.location] = locations.get(surf_session.location, 0) + 1
        
        print("\nSessions by location:")
        for location, count in sorted(locations.items(), key=lambda x: x[1], reverse=True):
            print(f"{location}: {count} sessions")
            
    finally:
        db_session.close()

if __name__ == "__main__":
    verify_data() 