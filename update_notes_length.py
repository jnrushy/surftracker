from sqlalchemy import create_engine, text

# Create database engine
engine = create_engine('postgresql:///surftracker')

# SQL to alter the notes column
alter_notes_sql = """
ALTER TABLE surf_sessions 
ALTER COLUMN notes TYPE TEXT;
"""

def update_schema():
    with engine.connect() as connection:
        connection.execute(text(alter_notes_sql))
        connection.commit()
        print("Successfully updated notes column to TEXT type")

if __name__ == "__main__":
    update_schema() 