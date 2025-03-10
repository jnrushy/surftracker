# SurfTracker

A Python application to track and analyze surf sessions. Built with SQLAlchemy and PostgreSQL.

## Features

- Track surf sessions with details like:
  - Date and time
  - Location
  - Wave height
  - Session duration
  - Notes
  - Wave quality
  - Wind conditions
  - Tide information
  - Water temperature

## Setup

1. Install PostgreSQL
```bash
brew install postgresql@14
brew services start postgresql@14
```

2. Install Python dependencies
```bash
pip install -r requirements.txt
```

3. Initialize the database
```bash
python init_db.py
```

4. Import surf session data
```bash
python load_data.py your_data.xlsx
```

5. Verify imported data
```bash
python verify_data.py
```

## Database Schema

The main table `surf_sessions` includes:
- `id` (Primary Key)
- `date` (DateTime)
- `location` (String)
- `wave_height` (Float)
- `wave_quality` (Enum)
- `wind_speed` (Float)
- `wind_direction` (String)
- `tide_height` (Float)
- `water_temp` (Float)
- `session_duration` (Integer)
- `notes` (String)
- `rating` (Integer)

## Future Enhancements

- Add user authentication
- Include surfboard tracking
- Integrate with forecast data
- Add visualization and analytics 