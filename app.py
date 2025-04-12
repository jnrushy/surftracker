from flask import Flask, render_template, request, redirect, url_for, flash
import visualize_data
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev')

# Ensure the templates directory exists
os.makedirs('templates', exist_ok=True)

@app.route('/')
def dashboard():
    """Serve the dashboard"""
    # Generate fresh visualizations and get statistics
    summary_stats, yearly_stats, recent_sessions = visualize_data.create_visualizations(visualize_data.load_data_from_db())
    return render_template('dashboard.html', 
                         summary_stats=summary_stats, 
                         yearly_stats=yearly_stats,
                         recent_sessions=recent_sessions)

@app.route('/add_session', methods=['GET', 'POST'])
def add_session():
    """Add a new surf session"""
    if request.method == 'POST':
        try:
            # Get form data
            date = request.form['date']
            location = request.form['location']
            board_id = request.form['board']
            wave_height = float(request.form['wave_height'])
            session_duration = int(request.form['duration'])
            waves_caught = int(request.form['waves'])
            notes = request.form['notes']

            # Add session to database
            visualize_data.add_session_to_db(date, location, board_id, wave_height, 
                                          session_duration, waves_caught, notes)
            
            flash('Session added successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f'Error adding session: {str(e)}', 'error')
            return redirect(url_for('add_session'))

    # Get boards for the form
    boards = visualize_data.get_boards()
    return render_template('add_session.html', boards=boards)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True) 