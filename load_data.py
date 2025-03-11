import pandas as pd
from sqlalchemy import create_engine
from models import SurfSession, get_session, WaveQuality, Board
from datetime import datetime
import os

def convert_wave_quality(quality_str):
    """Convert string wave quality to enum value"""
    quality_map = {
        'poor': WaveQuality.POOR,
        'fair': WaveQuality.FAIR,
        'good': WaveQuality.GOOD,
        'excellent': WaveQuality.EXCELLENT
    }
    return quality_map.get(quality_str.lower(), None) if quality_str else None

def get_board_by_name(db_session, board_name):
    """Get board by name, handling variations in naming"""
    if not board_name:
        return None
        
    # Clean up board name
    board_name = board_name.strip().lower()
    
    # Handle common variations
    if 'zen' in board_name:
        board_name = 'Zen'
    elif 'joe' in board_name.lower() or 'log' in board_name.lower():
        board_name = 'JoeLog'
    elif 'wave' in board_name.lower() or 'storm' in board_name.lower():
        board_name = 'Wavestorm'
    elif 'nps' in board_name.lower() or 'nsp' in board_name.lower() or 'egg' in board_name.lower():
        board_name = 'NSP Egg'
    
    board = db_session.query(Board).filter(Board.name.ilike(f"%{board_name}%")).first()
    if not board:
        print(f"DEBUG: Could not find board matching '{board_name}'")
    return board

def clean_dataframe(df):
    """Clean and prepare the dataframe"""
    print("\nDEBUG: Starting dataframe cleaning...")
    print(f"DEBUG: Initial shape: {df.shape}")
    
    # Remove unnamed columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    # Remove rows where all values are NaN
    df = df.dropna(how='all')
    print(f"DEBUG: Shape after dropping empty rows: {df.shape}")
    
    # Rename columns to match our schema
    column_mapping = {
        'Date': 'date',
        'Location': 'location',
        'Swell Size (surfline)': 'wave_height',
        'Time in water': 'session_duration',
        'Waves Caught': 'waves_caught',
        'Boards': 'board',
        'Notes': 'notes'
    }
    
    # Rename only the columns that exist
    existing_columns = {k: v for k, v in column_mapping.items() if k in df.columns}
    df = df.rename(columns=existing_columns)
    
    # Convert time duration to minutes if it exists
    if 'session_duration' in df.columns:
        df['session_duration'] = pd.to_numeric(df['session_duration'], errors='coerce')
    
    # Convert wave height to numeric, removing any text
    if 'wave_height' in df.columns:
        print("\nDEBUG: Converting wave heights...")
        df['wave_height'] = df['wave_height'].apply(lambda x: str(x) if pd.notnull(x) else '')
        df['wave_height'] = df['wave_height'].str.extract(r'(\d+(?:\.\d+)?)', expand=False)
        df['wave_height'] = pd.to_numeric(df['wave_height'], errors='coerce')
        print(f"DEBUG: Unique wave heights after conversion: {df['wave_height'].unique()}")
    
    # Convert waves caught to numeric
    if 'waves_caught' in df.columns:
        df['waves_caught'] = pd.to_numeric(df['waves_caught'], errors='coerce')
    
    # Handle dates
    if 'date' in df.columns:
        print("\nDEBUG: Converting dates...")
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        # Fix specific date typo: 2020-09-28 should be 2023-09-28
        df.loc[df['date'] == '2020-09-28', 'date'] = pd.to_datetime('2023-09-28')
        # Replace NaT with None
        df['date'] = df['date'].where(df['date'].notna(), None)
        print(f"DEBUG: Date range: {df['date'].min()} to {df['date'].max()}")
        print(f"DEBUG: Null dates: {df['date'].isnull().sum()}")
    
    return df

def load_surf_data(file_path):
    """Load surf session data from CSV or Excel file into database"""
    # Determine file type by extension
    _, ext = os.path.splitext(file_path)
    
    try:
        # Read file based on extension
        if ext.lower() == '.xlsx':
            df = pd.read_excel(file_path)
        else:  # Try different encodings for CSV
            encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
            for encoding in encodings:
                try:
                    df = pd.read_csv(file_path, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    if encoding == encodings[-1]:  # If we've tried all encodings
                        raise
                    continue
    
        # Print original column names for debugging
        print("Original columns found in file:", df.columns.tolist())
        
        # Clean and prepare the dataframe
        df = clean_dataframe(df)
        
        print("\nProcessed columns:", df.columns.tolist())
        print(f"\nFound {len(df)} rows to import")
        
        # Get database session
        db_session = get_session()
        
        try:
            successful_imports = 0
            # Convert DataFrame rows to SurfSession objects
            for idx, row in df.iterrows():
                try:
                    # Skip rows with no date or location
                    if pd.isna(row.get('date')):
                        print(f"DEBUG: Skipping row {idx + 1}: No date")
                        continue
                    if pd.isna(row.get('location')):
                        print(f"DEBUG: Skipping row {idx + 1}: No location")
                        continue
                    
                    print(f"\nDEBUG: Processing row {idx + 1}")
                    print(f"DEBUG: Date: {row.get('date')}")
                    print(f"DEBUG: Location: {row.get('location')}")
                    print(f"DEBUG: Board: {row.get('board')}")
                    
                    # Get board if specified
                    board = None
                    if 'board' in row and not pd.isna(row['board']):
                        board = get_board_by_name(db_session, row['board'])
                        if board:
                            print(f"Found board: {board.name} for session {idx + 1}")
                        else:
                            print(f"Warning: Board not found for session {idx + 1}: {row['board']}")
                    
                    session = SurfSession(
                        date=row['date'] if row.get('date') else datetime.now(),
                        location=row['location'],
                        wave_height=row.get('wave_height'),
                        wave_quality=None,  # We don't have this in the Excel file
                        wind_speed=None,    # We don't have this in the Excel file
                        wind_direction=None, # We don't have this in the Excel file
                        tide_height=None,   # We don't have this in the Excel file
                        water_temp=None,    # We don't have this in the Excel file
                        session_duration=row.get('session_duration'),
                        waves_caught=row.get('waves_caught'),
                        notes=row.get('notes'),
                        rating=None,        # We don't have this in the Excel file
                        board=board         # Add board relationship
                    )
                    db_session.add(session)
                    successful_imports += 1
                except Exception as e:
                    print(f"Error processing row {idx + 1}: {str(e)}")
                    print(f"Row data: {row.to_dict()}")
                    continue
            
            # Commit all changes
            db_session.commit()
            print(f"\nSuccessfully loaded {successful_imports} surf sessions into database!")
        
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            db_session.rollback()
            raise
        finally:
            db_session.close()
    
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        print("\nExpected columns in your file:")
        print("- Date")
        print("- Location")
        print("- Swell Size (surfline)")
        print("- Time in water")
        print("- Waves Caught")
        print("- Boards")
        print("- Notes")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python load_data.py <file_path>")
        print("Supported formats: .csv, .xlsx")
        sys.exit(1)
    
    file_path = sys.argv[1]
    load_surf_data(file_path) 