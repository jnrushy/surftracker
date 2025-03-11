import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sqlalchemy import create_engine, text
from models import get_session, SurfSession, Board
import calendar
from datetime import datetime

def load_data_from_db():
    """Load surf session data from database into a pandas DataFrame"""
    session = get_session()
    
    # Query all surf sessions with board information
    query = """
    SELECT 
        s.date,
        s.location,
        s.wave_height,
        s.session_duration,
        s.waves_caught,
        s.notes,
        b.name as board_name
    FROM surf_sessions s
    LEFT JOIN boards b ON s.board_id = b.id
    ORDER BY s.date
    """
    
    df = pd.read_sql(query, session.bind)
    session.close()
    return df

def create_visualizations(df):
    """Create and display various visualizations"""
    # Add month and year columns for aggregation
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['month_name'] = df['date'].dt.strftime('%B')
    
    # 1. Sessions by Location (Pie Chart)
    fig_location = px.pie(df, names='location', title='Surf Sessions by Location')
    fig_location.write_html('surf_locations.html')
    
    # 2. Sessions by Board (Bar Chart)
    fig_board = px.bar(df['board_name'].value_counts(), 
                      title='Sessions by Board',
                      labels={'value': 'Number of Sessions', 'index': 'Board'})
    fig_board.write_html('surf_boards.html')
    
    # 3. Sessions Over Time (Line Chart)
    monthly_sessions = df.groupby(['year', 'month', 'month_name']).size().reset_index(name='count')
    monthly_sessions['date'] = pd.to_datetime(monthly_sessions[['year', 'month']].assign(day=1))
    fig_timeline = px.line(monthly_sessions, x='date', y='count',
                          title='Number of Sessions Over Time',
                          labels={'count': 'Number of Sessions', 'date': 'Month'})
    fig_timeline.write_html('surf_timeline.html')
    
    # 4. Wave Height Distribution (Box Plot)
    fig_waves = px.box(df, y='wave_height', title='Wave Height Distribution')
    fig_waves.write_html('wave_heights.html')
    
    # 5. Waves Caught by Board Type (Box Plot)
    fig_performance = px.box(df, x='board_name', y='waves_caught',
                           title='Waves Caught by Board Type')
    fig_performance.write_html('board_performance.html')
    
    # 6. Session Duration by Location (Box Plot)
    fig_duration = px.box(df, x='location', y='session_duration',
                         title='Session Duration by Location')
    fig_duration.write_html('session_duration.html')
    
    # Create summary statistics
    summary = pd.DataFrame([
        {'Metric': 'Total Sessions', 'Value': len(df)},
        {'Metric': 'Unique Locations', 'Value': df['location'].nunique()},
        {'Metric': 'Average Wave Height', 'Value': f"{df['wave_height'].mean():.1f}ft"},
        {'Metric': 'Average Session Duration', 'Value': f"{df['session_duration'].mean():.0f}min"},
        {'Metric': 'Total Waves Caught', 'Value': df['waves_caught'].sum()},
        {'Metric': 'Average Waves per Session', 'Value': f"{df['waves_caught'].mean():.1f}"},
        {'Metric': 'Most Used Board', 'Value': df['board_name'].mode().iloc[0]},
        {'Metric': 'Favorite Location', 'Value': df['location'].mode().iloc[0]},
    ])
    
    # Create an HTML dashboard
    html_content = """
    <html>
    <head>
        <title>Surf Session Analytics</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .summary { margin-bottom: 20px; }
            table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
            iframe { width: 100%; height: 500px; border: none; }
        </style>
    </head>
    <body>
        <h1>Surf Session Analytics Dashboard</h1>
        
        <div class="summary">
            <h2>Summary Statistics</h2>
            <table>
                <tr><th>Metric</th><th>Value</th></tr>
    """
    
    # Add summary statistics to HTML
    for _, row in summary.iterrows():
        html_content += f"<tr><td>{row['Metric']}</td><td>{row['Value']}</td></tr>"
    
    html_content += """
            </table>
        </div>
        
        <div class="grid">
            <iframe src="surf_locations.html"></iframe>
            <iframe src="surf_boards.html"></iframe>
            <iframe src="surf_timeline.html"></iframe>
            <iframe src="wave_heights.html"></iframe>
            <iframe src="board_performance.html"></iframe>
            <iframe src="session_duration.html"></iframe>
        </div>
    </body>
    </html>
    """
    
    with open('surf_dashboard.html', 'w') as f:
        f.write(html_content)
    
    print("\nVisualization files have been created:")
    print("1. surf_dashboard.html (Main dashboard)")
    print("2. surf_locations.html (Pie chart of locations)")
    print("3. surf_boards.html (Bar chart of board usage)")
    print("4. surf_timeline.html (Sessions over time)")
    print("5. wave_heights.html (Wave height distribution)")
    print("6. board_performance.html (Waves caught by board)")
    print("7. session_duration.html (Session duration by location)")
    print("\nOpen surf_dashboard.html in your web browser to view all visualizations!")

if __name__ == "__main__":
    print("Loading data from database...")
    df = load_data_from_db()
    print("Creating visualizations...")
    create_visualizations(df) 