from sqlalchemy import create_engine, text

# Database connection configuration
DATABASE_URL = "postgresql://localhost/surftracker"

def update_schema():
    """Add waves_caught column to surf_sessions table"""
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as connection:
        # Check if column exists
        check_column = text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='surf_sessions' AND column_name='waves_caught';
        """)
        result = connection.execute(check_column)
        column_exists = result.fetchone() is not None
        
        if not column_exists:
            # Add the waves_caught column
            print("Adding waves_caught column...")
            add_column = text("""
                ALTER TABLE surf_sessions 
                ADD COLUMN waves_caught INTEGER;
            """)
            connection.execute(add_column)
            connection.commit()
            print("Column added successfully!")
        else:
            print("waves_caught column already exists.")

if __name__ == "__main__":
    update_schema() 