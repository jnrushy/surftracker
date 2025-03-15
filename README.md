# SurfTracker

A Python application to track and analyze surf sessions. Built with Flask, SQLAlchemy, and PostgreSQL.

## Features

- Track surf sessions with details like:
  - Date and time
  - Location
  - Board used
  - Wave height
  - Session duration
  - Waves caught
  - Notes

- Web Interface:
  - Interactive dashboard with summary statistics
  - Year-by-year progress tracking
  - Visual analytics including:
    - Surfing progression over time
    - Monthly patterns
    - Location distribution
    - Board usage statistics
    - Wave height distribution
    - Performance by board type
    - Session duration analysis
  - Easy session entry form
  - Real-time visualization updates

## Setup

1. Install PostgreSQL
```bash
brew install postgresql@14
brew services start postgresql@14
```

2. Create a Python virtual environment and activate it
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install Python dependencies
```bash
pip install -r requirements.txt
```

4. Initialize the database
```bash
python init_db.py
```

5. Import surf session data (supports CSV and Excel files)
```bash
python load_data.py your_data.xlsx
```

6. Start the web application
```bash
python app.py
```

The application will be available at `http://localhost:3000`

## Database Schema

The database includes the following tables:

### surf_sessions
- `id` (Primary Key)
- `date` (DateTime)
- `location` (String)
- `board_id` (Foreign Key)
- `wave_height` (Float)
- `session_duration` (Integer)
- `waves_caught` (Integer)
- `notes` (Text)

### boards
- `id` (Primary Key)
- `name` (String)
- `type` (String)
- `length` (Float)

## Project Structure

```
surftracker/
├── app.py              # Flask web application
├── init_db.py          # Database initialization
├── load_data.py        # Data import script
├── models.py           # SQLAlchemy models
├── visualize_data.py   # Visualization generation
├── requirements.txt    # Python dependencies
├── static/            
│   └── visualizations/ # Generated visualization files
└── templates/          # HTML templates
    ├── dashboard.html
    └── add_session.html
```

## Future Enhancements

- Add user authentication
- Include weather and tide data
- Integrate with surf forecasting APIs
- Add photo uploads for sessions
- Mobile-friendly interface
- Export data functionality
- Advanced analytics and insights
- Session rating system
- Multiple surf spot tracking with maps 