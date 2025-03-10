from models import get_session, Board, SurfSession
from datetime import datetime

def list_boards(db_session):
    """List all boards in the database"""
    boards = db_session.query(Board).all()
    
    print("\nSurfboards:")
    print("-----------")
    for i, board in enumerate(boards, 1):
        print(f"\n{i}. {board.name}")
        print(f"   Length: {board.length}ft")
        print(f"   Volume: {board.volume}L" if board.volume else "   Volume: Not specified")
        print(f"   Type: {board.board_type}")
        print(f"   Condition: {board.condition}")
        if board.notes:
            print(f"   Notes: {board.notes}")
        
        # Get session count for this board
        session_count = db_session.query(SurfSession).filter(SurfSession.board_id == board.id).count()
        print(f"   Sessions: {session_count}")
    
    return boards

def add_board():
    """Add a new surfboard to the database"""
    print("\nAdd New Surfboard")
    print("----------------")
    
    # Get board details
    name = input("Board name/model: ").strip()
    if not name:
        print("Board name is required")
        return
    
    length = input("Length (in feet): ").strip()
    length = float(length) if length else None
    
    volume = input("Volume (in liters, press Enter if unknown): ").strip()
    volume = float(volume) if volume else None
    
    board_type = input("Board type (shortboard, longboard, etc.): ").strip()
    
    purchase_date_str = input("Purchase date (YYYY-MM-DD, press Enter if unknown): ").strip()
    if purchase_date_str:
        try:
            purchase_date = datetime.strptime(purchase_date_str, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format, setting to None")
            purchase_date = None
    else:
        purchase_date = None
    
    condition = input("Current condition: ").strip()
    notes = input("Notes: ").strip()
    
    # Create board object
    board = Board(
        name=name,
        length=length,
        volume=volume,
        board_type=board_type,
        purchase_date=purchase_date,
        condition=condition,
        notes=notes
    )
    
    # Save to database
    db_session = get_session()
    try:
        db_session.add(board)
        db_session.commit()
        print("\nBoard added successfully!")
        
        # Show the added board
        print("\nAdded Board Details:")
        print(f"Name: {board.name}")
        print(f"Length: {board.length}ft")
        if board.volume:
            print(f"Volume: {board.volume}L")
        print(f"Type: {board.board_type}")
        print(f"Condition: {board.condition}")
        if board.notes:
            print(f"Notes: {board.notes}")
            
    except Exception as e:
        print(f"Error adding board: {str(e)}")
        db_session.rollback()
    finally:
        db_session.close()

def main():
    """Main menu for board management"""
    while True:
        print("\nBoard Management")
        print("1. List boards")
        print("2. Add new board")
        print("3. Exit")
        
        choice = input("\nSelect an option (1-3): ").strip()
        
        if choice == "1":
            db_session = get_session()
            try:
                list_boards(db_session)
            finally:
                db_session.close()
        elif choice == "2":
            add_board()
        elif choice == "3":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main() 