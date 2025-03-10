from sqlalchemy import create_engine, text

# Database connection configuration
DATABASE_URL = "postgresql://localhost/surftracker"

def update_schema():
    """Add boards table and board relationship to surf_sessions"""
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as connection:
        # Create boards table if it doesn't exist
        create_boards_table = text("""
            CREATE TABLE IF NOT EXISTS boards (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                length FLOAT,
                volume FLOAT,
                board_type VARCHAR(50),
                purchase_date TIMESTAMP,
                condition VARCHAR(50),
                notes VARCHAR(500)
            );
        """)
        
        # Add board_id column to surf_sessions if it doesn't exist
        add_board_column = text("""
            DO $$ 
            BEGIN 
                IF NOT EXISTS (
                    SELECT 1 
                    FROM information_schema.columns 
                    WHERE table_name='surf_sessions' AND column_name='board_id'
                ) THEN 
                    ALTER TABLE surf_sessions 
                    ADD COLUMN board_id INTEGER REFERENCES boards(id);
                END IF;
            END $$;
        """)
        
        print("Creating boards table...")
        connection.execute(create_boards_table)
        print("Adding board_id column to surf_sessions...")
        connection.execute(add_board_column)
        connection.commit()
        print("Schema update completed successfully!")

if __name__ == "__main__":
    update_schema() 