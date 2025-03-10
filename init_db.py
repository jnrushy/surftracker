import subprocess
from models import init_db

def create_database():
    try:
        # Create database
        subprocess.run(['createdb', 'surftracker'], check=True)
        print("Database 'surftracker' created successfully!")
    except subprocess.CalledProcessError:
        print("Database might already exist, attempting to continue...")

    # Initialize database schema
    engine = init_db()
    print("Database schema created successfully!")

if __name__ == "__main__":
    create_database() 