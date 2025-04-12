import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sqlalchemy import create_engine, text
from models import get_session, SurfSession, Board
import calendar
from datetime import datetime
import os

# Ensure the static/visualizations directory exists
os.makedirs('static/visualizations', exist_ok=True)

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

def create_progression_charts(df):
    """Create charts showing surfing progression"""
    # Average waves per session by month and year
    monthly_waves = df.groupby(['year', 'month']).agg({
        'waves_caught': ['mean', 'count']
    }).reset_index()
    monthly_waves.columns = ['year', 'month', 'avg_waves', 'session_count']
    monthly_waves['date'] = pd.to_datetime(monthly_waves[['year', 'month']].assign(day=1))
    
    fig_progression = make_subplots(rows=2, cols=1, 
                                  subplot_titles=('Average Waves per Session', 
                                                'Sessions per Month'))
    
    # Average waves trend
    fig_progression.add_trace(
        go.Scatter(x=monthly_waves['date'], y=monthly_waves['avg_waves'],
                  mode='lines+markers', name='Avg Waves'),
        row=1, col=1
    )
    
    # Session count
    fig_progression.add_trace(
        go.Bar(x=monthly_waves['date'], y=monthly_waves['session_count'],
               name='Session Count'),
        row=2, col=1
    )
    
    fig_progression.update_layout(height=800, title_text="Surfing Progression")
    fig_progression.write_html('static/visualizations/progression.html')
    
    # Monthly patterns across years
    monthly_patterns = df.groupby(['year', 'month'])['waves_caught'].agg(['mean', 'count']).reset_index()
    fig_monthly = px.line(monthly_patterns, x='month', y='mean', color='year',
                         title='Average Waves by Month (Year Comparison)',
                         labels={'month': 'Month', 'mean': 'Average Waves Caught'})
    fig_monthly.update_xaxes(ticktext=calendar.month_abbr[1:], tickvals=list(range(1,13)))
    fig_monthly.write_html('static/visualizations/monthly_patterns.html')
    
    return monthly_patterns

def create_summary_stats(df):
    """Create summary statistics for the dashboard"""
    total_sessions = len(df)
    total_waves = df['waves_caught'].sum()
    avg_waves_per_session = df['waves_caught'].mean()
    total_hours = df['session_duration'].sum() / 60
    favorite_spot = df['location'].mode().iloc[0]
    favorite_board = df['board_name'].mode().iloc[0]
    
    return {
        'total_sessions': total_sessions,
        'total_waves': int(total_waves),
        'avg_waves_per_session': round(avg_waves_per_session, 1),
        'total_hours': round(total_hours, 1),
        'favorite_spot': favorite_spot,
        'favorite_board': favorite_board
    }

def create_yearly_stats(df):
    """Create year-by-year statistics"""
    yearly_stats = df.groupby('year').agg({
        'waves_caught': ['count', 'sum', 'mean'],
        'session_duration': 'sum',
        'wave_height': 'mean'
    }).round(1)
    
    yearly_stats.columns = ['sessions', 'total_waves', 'avg_waves_per_session', 'total_minutes', 'avg_wave_height']
    yearly_stats['total_hours'] = (yearly_stats['total_minutes'] / 60).round(1)
    yearly_stats = yearly_stats.drop('total_minutes', axis=1)
    
    return yearly_stats.reset_index().to_dict('records')

def get_recent_sessions(df):
    """Get the last 10 surf sessions"""
    recent_sessions = df.sort_values('date', ascending=False).head(10)
    return recent_sessions[['date', 'location', 'board_name', 'wave_height', 'session_duration', 'waves_caught', 'notes']].to_dict('records')

def create_visualizations(df):
    """Create and display various visualizations"""
    # Add month and year columns for aggregation
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['month_name'] = df['date'].dt.strftime('%B')
    
    # Generate summary statistics
    summary_stats = create_summary_stats(df)
    yearly_stats = create_yearly_stats(df)
    recent_sessions = get_recent_sessions(df)
    
    # Create progression charts
    monthly_patterns = create_progression_charts(df)
    
    # Original visualizations
    fig_location = px.pie(df, names='location', title='Surf Sessions by Location')
    fig_location.write_html('static/visualizations/surf_locations.html')
    
    fig_board = px.bar(df['board_name'].value_counts(), 
                      title='Sessions by Board',
                      labels={'value': 'Number of Sessions', 'index': 'Board'})
    fig_board.write_html('static/visualizations/surf_boards.html')
    
    monthly_sessions = df.groupby(['year', 'month', 'month_name']).size().reset_index(name='count')
    monthly_sessions['date'] = pd.to_datetime(monthly_sessions[['year', 'month']].assign(day=1))
    fig_timeline = px.line(monthly_sessions, x='date', y='count',
                          title='Number of Sessions Over Time',
                          labels={'count': 'Number of Sessions', 'date': 'Month'})
    fig_timeline.write_html('static/visualizations/surf_timeline.html')
    
    fig_waves = px.box(df, y='wave_height', x='year', title='Wave Height Distribution by Year')
    fig_waves.write_html('static/visualizations/wave_heights.html')
    
    fig_performance = px.box(df, x='board_name', y='waves_caught',
                           title='Waves Caught by Board Type')
    fig_performance.write_html('static/visualizations/board_performance.html')
    
    fig_duration = px.box(df, x='location', y='session_duration',
                         title='Session Duration by Location')
    fig_duration.write_html('static/visualizations/session_duration.html')
    
    print("\nVisualization files have been created in static/visualizations/")
    
    return summary_stats, yearly_stats, recent_sessions

if __name__ == "__main__":
    print("Loading data from database...")
    df = load_data_from_db()
    print("Creating visualizations...")
    create_visualizations(df) 