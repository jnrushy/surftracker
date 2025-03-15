from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from models import get_session, SurfSession, Board
import visualize_data
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages

# Ensure the templates directory exists
os.makedirs('templates', exist_ok=True)

@app.route('/')
def dashboard():
    """Serve the dashboard"""
    # Generate fresh visualizations
    visualize_data.create_visualizations(visualize_data.load_data_from_db())
    return render_template('dashboard.html')

@app.route('/add_session', methods=['GET', 'POST'])
def add_session():
    """Handle new session form"""
    db_session = get_session()
    
    # Get list of boards for the form
    boards = db_session.query(Board).all()
    
    if request.method == 'POST':
        try:
            # Get form data
            date = datetime.strptime(request.form['date'], '%Y-%m-%d')
            location = request.form['location']
            board_id = int(request.form['board'])
            wave_height = float(request.form['wave_height'])
            session_duration = int(request.form['session_duration'])
            waves_caught = int(request.form['waves_caught'])
            notes = request.form['notes']

            # Create new session
            new_session = SurfSession(
                date=date,
                location=location,
                board_id=board_id,
                wave_height=wave_height,
                session_duration=session_duration,
                waves_caught=waves_caught,
                notes=notes
            )
            
            # Add and commit to database
            db_session.add(new_session)
            db_session.commit()
            
            # Flash success message
            flash('New surf session added successfully!', 'success')
            
            # Regenerate visualizations
            visualize_data.create_visualizations(visualize_data.load_data_from_db())
            
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            flash(f'Error adding session: {str(e)}', 'error')
            db_session.rollback()
    
    return render_template('add_session.html', boards=boards)

if __name__ == '__main__':
    app.run(debug=True) 