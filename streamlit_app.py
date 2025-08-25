import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Configuration
SHEETS_URLS = {
    "Male Boulder Semis": "https://docs.google.com/spreadsheets/d/1MwVp1mBUoFrzRSIIu4UdMcFlXpxHAi_R7ztp1E4Vgx0/export?format=csv&gid=911620167",
    "Female Boulder Semis": "https://docs.google.com/spreadsheets/d/1MwVp1mBUoFrzRSIIu4UdMcFlXpxHAi_R7ztp1E4Vgx0/export?format=csv&gid=920221506",
    "Male Boulder Final": "https://docs.google.com/spreadsheets/d/1MwVp1mBUoFrzRSIIu4UdMcFlXpxHAi_R7ztp1E4Vgx0/export?format=csv&gid=1415967322",
    "Female Boulder Final": "https://docs.google.com/spreadsheets/d/1MwVp1mBUoFrzRSIIu4UdMcFlXpxHAi_R7ztp1E4Vgx0/export?format=csv&gid=299577805",
    "Male Lead Semis": "https://docs.google.com/spreadsheets/d/1MwVp1mBUoFrzRSIIu4UdMcFlXpxHAi_R7ztp1E4Vgx0/export?format=csv&gid=0",
    "Female Lead Semis": "https://docs.google.com/spreadsheets/d/1MwVp1mBUoFrzRSIIu4UdMcFlXpxHAi_R7ztp1E4Vgx0/export?format=csv&gid=352924417",
    "Male Lead Final": "https://docs.google.com/spreadsheets/d/1MwVp1mBUoFrzRSIIu4UdMcFlXpxHAi_R7ztp1E4Vgx0/export?format=csv&gid=1091240908",
    "Female Lead Final": "https://docs.google.com/spreadsheets/d/1MwVp1mBUoFrzRSIIu4UdMcFlXpxHAi_R7ztp1E4Vgx0/export?format=csv&gid=528108640"
}

def setup_page():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="IFSC 2025 Seoul World Championships", 
        layout="wide",
        initial_sidebar_state="expanded",
        page_icon="🧗‍♀️"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f4e79;
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
        border-bottom: 3px solid #e74c3c;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
    }
    
    .round-header {
        background: linear-gradient(90deg, #3498db, #2ecc71);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
        font-size: 1.8rem;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .athlete-card {
        background: white;
        border: 2px solid #ecf0f1;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .athlete-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #3498db, #2ecc71);
    }
    
    .rank-badge {
        background: #e74c3c;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: bold;
        font-size: 1.1rem;
        display: inline-block;
        margin-right: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    
    .rank-badge.gold { 
        background: linear-gradient(135deg, #f1c40f, #f39c12); 
        color: #2c3e50; 
    }
    .rank-badge.silver { 
        background: linear-gradient(135deg, #bdc3c7, #95a5a6); 
        color: white; 
    }
    .rank-badge.bronze { 
        background: linear-gradient(135deg, #e67e22, #d35400); 
        color: white; 
    }
    
    .position-info {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
    }
    
    .worst-case {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        color: white;
        padding: 0.8rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        text-align: center;
        font-weight: bold;
    }
    
    .boulder-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.5rem;
        margin: 1rem 0;
    }
    
    .boulder-score {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 0.8rem;
        text-align: center;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        border: 2px solid #ecf0f1;
        transition: all 0.3s ease;
    }
    
    .boulder-top {
        border-color: #27ae60;
        background: linear-gradient(135deg, #2ecc71, #27ae60);
        color: white;
    }
    
    .boulder-zone {
        border-color: #f39c12;
        background: linear-gradient(135deg, #f1c40f, #f39c12);
        color: #2c3e50;
    }
    
    .boulder-fail {
        border-color: #e74c3c;
        background: linear-gradient(135deg, #e74c3c, #c0392b);
        color: white;
    }
    
    .lead-targets {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .lead-target {
        background: linear-gradient(135deg, #9b59b6, #8e44ad);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
    }
    
    .lead-qualification {
        background: linear-gradient(135deg, #27ae60, #229954);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .qualification-status {
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: bold;
        font-size: 0.9rem;
        display: inline-block;
        margin-left: 1rem;
    }
    
    .qualified {
        background: #2ecc71;
        color: white;
    }
    
    .eliminated {
        background: #e74c3c;
        color: white;
    }
    
    .sidebar-section {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 1px solid #dee2e6;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .athlete-name {
        font-size: 1.3rem;
        font-weight: bold;
        color: #2c3e50;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_data(sheets_url):
    """Load data from Google Sheets with error handling"""
    try:
        df = pd.read_csv(sheets_url)
        # Clean up column names
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=300)
def load_all_data():
    """Load all competition data"""
    all_data = {}
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, (round_name, url) in enumerate(SHEETS_URLS.items()):
        status_text.text(f"Loading {round_name}...")
        df = load_data(url)
        if not df.empty:
            all_data[round_name] = df
        progress_bar.progress((i + 1) / len(SHEETS_URLS))
    
    status_text.text("✅ Data loading complete!")
    progress_bar.empty()
    status_text.empty()
    
    return all_data

def get_column_mapping(round_name):
    """Get the correct column mapping based on round type"""
    if "Boulder Semis" in round_name:
        return {
            'name': 'Athlete Name',
            'rank': 'Current Position',
            'score': 'Total Score',
            'worst_case': 'Worst Case Finish',
            'boulder_cols': ['Boulder 1 Score', 'Boulder 2 Score', 'Boulder 3 Score', 'Boulder 4 Score'],
            'strategy_cols': ['1st Place Strategy', '2nd Place Strategy', '3rd Place Strategy']
        }
    elif "Boulder Final" in round_name:
        return {
            'name': 'Name',
            'rank': 'Current Rank',
            'score': 'Manual Score',
            'status': 'Status',
            'worst_case': 'Worst Case Finish',
            'boulder_cols': ['Boulder 1 Score', 'Boulder 2 Score', 'Boulder 3 Score', 'Boulder 4 Score'],
            'points_cols': ['Points to 1st', 'Points to 2nd', 'Points to 3rd']
        }
    elif "Lead Semis" in round_name:
        return {
            'name': 'Name',
            'rank': 'Current Rank', 
            'score': 'Manual Score',
            'status': 'Status',
            'worst_case': 'Worst Case Finish',
            'qualification_hold': 'Min to Qualify',
            'hold_for_1st': 'Hold for 1st',
            'hold_for_2nd': 'Hold for 2nd',
            'hold_for_3rd': 'Hold for 3rd'
        }
    elif "Lead Final" in round_name:
        return {
            'name': 'Name',
            'rank': 'Current Rank', 
            'score': 'Manual Score',
            'status': 'Status',
            'worst_case': 'Worst Case Finish',
            'hold_for_1st': 'Hold for 1st',
            'hold_for_2nd': 'Hold for 2nd',
            'hold_for_3rd': 'Hold for 3rd'
        }
    
    return {}

def format_boulder_score(score):
    """Format boulder score for display"""
    if pd.isna(score) or score == 0:
        return "0T0Z"
    
    score_str = str(int(score))
    if len(score_str) == 1:
        return f"0T{score_str}Z"
    elif len(score_str) == 2:
        return f"{score_str[0]}T{score_str[1]}Z"
    else:
        return str(score)

def get_boulder_status_class(score):
    """Get CSS class for boulder performance"""
    if pd.isna(score) or score == 0:
        return "boulder-fail"
    
    score_str = str(int(score))
    if len(score_str) >= 1 and score_str[0] == '1':  # Has top
        return "boulder-top"
    elif len(score_str) >= 2 and score_str[1] == '1':  # Has zone
        return "boulder-zone"
    else:
        return "boulder-fail"

def display_boulder_performance(athlete_data, cols_mapping):
    """Display boulder performance using Streamlit components only"""
    if 'boulder_cols' not in cols_mapping:
        return
    
    st.markdown("**Boulder Performance:**")
    
    # Create 4 columns for the 4 boulders
    boulder_cols = st.columns(4)
    
    for i, col in enumerate(cols_mapping['boulder_cols']):
        score = athlete_data.get(col, 0) if col in athlete_data.index else 0
        formatted_score = format_boulder_score(score)
        
        # Determine status emoji and color
        if pd.isna(score) or score == 0:
            status_emoji = "🔴"
            bg_color = "#e74c3c"
        else:
            score_str = str(int(score))
            if len(score_str) >= 1 and score_str[0] == '1':  # Has top
                status_emoji = "🟢"
                bg_color = "#2ecc71"
            elif len(score_str) >= 2 and score_str[1] == '1':  # Has zone
                status_emoji = "🟡"
                bg_color = "#f1c40f"
            else:
                status_emoji = "🔴"
                bg_color = "#e74c3c"
        
        with boulder_cols[i]:
            st.markdown(f"""
            <div style="
                background: {bg_color};
                color: white;
                padding: 0.8rem;
                border-radius: 10px;
                text-align: center;
                font-family: monospace;
                font-weight: bold;
                margin-bottom: 0.5rem;
            ">
                <div style="font-size: 0.9rem;">B{i+1}</div>
                <div style="font-size: 1.1rem;">{formatted_score}</div>
            </div>
            """, unsafe_allow_html=True)

def display_lead_performance(athlete_data, cols_mapping):
    """Display lead performance using Streamlit components only"""
    # Qualification hold (for semis)
    if 'qualification_hold' in cols_mapping:
        qual_hold = athlete_data.get(cols_mapping['qualification_hold'], "N/A")
        if pd.notna(qual_hold) and str(qual_hold) != "N/A":
            st.success(f"🎯 Need for Qualification: Hold {qual_hold}")
    
    # Target holds for positions
    st.markdown("**Target Holds:**")
    
    target_holds = [
        ('hold_for_1st', '🥇 1st Place', '#f1c40f'),
        ('hold_for_2nd', '🥈 2nd Place', '#bdc3c7'), 
        ('hold_for_3rd', '🥉 3rd Place', '#e67e22')
    ]
    
    # Filter to only show holds that have values
    valid_holds = []
    for hold_key, label, color in target_holds:
        if hold_key in cols_mapping:
            hold_value = athlete_data.get(cols_mapping[hold_key], "N/A")
            if pd.notna(hold_value) and str(hold_value) != "N/A":
                valid_holds.append((hold_key, label, color, hold_value))
    
    if valid_holds:
        target_cols = st.columns(len(valid_holds))
        
        for i, (hold_key, label, color, hold_value) in enumerate(valid_holds):
            with target_cols[i]:
                st.markdown(f"""
                <div style="
                    background: {color};
                    color: white;
                    padding: 1rem;
                    border-radius: 10px;
                    text-align: center;
                    font-weight: bold;
                    margin-bottom: 0.5rem;
                ">
                    <div style="font-size: 0.9rem;">{label}</div>
                    <div style="font-size: 1.2rem;">Hold {hold_value}</div>
                </div>
                """, unsafe_allow_html=True)

def get_qualification_status(athlete_data, cols_mapping):
    """Determine qualification status"""
    if 'status' in cols_mapping and cols_mapping['status'] in athlete_data.index:
        status = str(athlete_data.get(cols_mapping['status'], "")).lower()
        if 'qualified' in status or 'podium' in status:
            return "✅ Qualified", "#2ecc71"
        elif 'eliminated' in status:
            return "❌ Eliminated", "#e74c3c"
    
    return "", ""

def display_athlete_card(athlete_data, rank, cols_mapping, round_name):
    """Display an enhanced athlete card using Streamlit components only"""
    name = athlete_data.get(cols_mapping.get('name', 'Name'), "Unknown")
    score = athlete_data.get(cols_mapping.get('score', 'Total Score'), "N/A")
    
    # Handle rank display
    if pd.isna(rank) or rank == "":
        rank_display = "N/A"
    else:
        try:
            rank_display = int(float(rank))
        except:
            rank_display = str(rank)
    
    # Get qualification status
    qual_status, qual_color = get_qualification_status(athlete_data, cols_mapping)
    
    # Use Streamlit container WITHOUT border parameter
    with st.container():
        # Create custom border using CSS
        st.markdown("""
        <div style="
            border: 2px solid #ecf0f1;
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            background: white;
            position: relative;
        ">
        """, unsafe_allow_html=True)
        
        # Header row with rank and name
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Determine medal emoji
            if rank_display == 1:
                medal = "🥇"
            elif rank_display == 2:
                medal = "🥈"
            elif rank_display == 3:
                medal = "🥉"
            else:
                medal = "🏃"
            
            st.markdown(f"### {medal} #{rank_display} - {name}")
            
            if qual_status:
                if "Qualified" in qual_status:
                    st.success(qual_status)
                else:
                    st.error(qual_status)
        
        with col2:
            st.metric("Score", score)
        
        # Position information
        current_pos = athlete_data.get(cols_mapping.get('rank', 'Current Rank'), "N/A")
        worst_case = athlete_data.get(cols_mapping.get('worst_case', 'Worst Case Finish'), "N/A")
        
        pos_col1, pos_col2 = st.columns(2)
        with pos_col1:
            st.info(f"📍 Current: #{current_pos}")
        
        if pd.notna(worst_case) and str(worst_case) != "N/A":
            with pos_col2:
                st.warning(f"⚠️ Worst: #{worst_case}")
        
        # Add performance data based on round type
        if "Boulder" in round_name:
            display_boulder_performance(athlete_data, cols_mapping)
        elif "Lead" in round_name:
            display_lead_performance(athlete_data, cols_mapping)
        
        # Close the custom border div
        st.markdown("</div>", unsafe_allow_html=True)

def create_athlete_progression_chart(all_data, athlete_name):
    """Create a chart showing athlete's progression through competition"""
    progression_data = []
    
    # Define round order
    round_order = [
        "Male Boulder Semis", "Male Boulder Final",
        "Female Boulder Semis", "Female Boulder Final",
        "Male Lead Semis", "Male Lead Final",
        "Female Lead Semis", "Female Lead Final"
    ]
    
    for round_name in round_order:
        if round_name in all_data:
            df = all_data[round_name]
            cols_mapping = get_column_mapping(round_name)
            name_col = cols_mapping.get('name', 'Name')
            rank_col = cols_mapping.get('rank', 'Current Rank')
            
            if name_col in df.columns:
                athlete_row = df[df[name_col].str.contains(athlete_name, case=False, na=False)]
                if not athlete_row.empty:
                    rank = athlete_row.iloc[0].get(rank_col, None)
                    if pd.notna(rank):
                        try:
                            rank_num = int(float(rank))
                            progression_data.append({
                                'Round': round_name.replace("Male ", "").replace("Female ", ""),
                                'Rank': rank_num,
                                'Full_Round': round_name
                            })
                        except:
                            pass
    
    if len(progression_data) > 1:
        prog_df = pd.DataFrame(progression_data)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=prog_df['Round'],
            y=prog_df['Rank'],
            mode='lines+markers',
            name=athlete_name,
            line=dict(width=4, color='#3498db'),
            marker=dict(size=12, color='#e74c3c', line=dict(width=2, color='white'))
        ))
        
        fig.update_layout(
            title=f"🏆 {athlete_name}'s Competition Progression",
            yaxis=dict(autorange='reversed', title="Rank"),
            xaxis=dict(title="Round"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        
        return fig
    
    return None

def athlete_detail_view(all_data, athlete_name):
    """Show detailed view for a specific athlete across all rounds"""
    st.markdown(f"""
    <div class="round-header">
        🎯 Complete Profile: {athlete_name}
    </div>
    """, unsafe_allow_html=True)
    
    athlete_rounds = {}
    
    # Collect data from all rounds
    for round_name, df in all_data.items():
        cols_mapping = get_column_mapping(round_name)
        name_col = cols_mapping.get('name', 'Name')
        
        if name_col in df.columns:
            athlete_row = df[df[name_col].str.contains(athlete_name, case=False, na=False)]
            if not athlete_row.empty:
                athlete_rounds[round_name] = {
                    'data': athlete_row.iloc[0],
                    'mapping': cols_mapping
                }
    
    if not athlete_rounds:
        st.warning(f"❌ No data found for athlete: {athlete_name}")
        return
    
    # Show progression chart
    prog_chart = create_athlete_progression_chart(all_data, athlete_name)
    if prog_chart:
        st.plotly_chart(prog_chart, use_container_width=True)
    
    # Display performance in each round
    st.markdown("### 📊 Round-by-Round Performance")
    
    cols = st.columns(min(len(athlete_rounds), 2))
    
    for i, (round_name, round_info) in enumerate(athlete_rounds.items()):
        with cols[i % 2]:
            data = round_info['data']
            mapping = round_info['mapping']
            
            rank = data.get(mapping.get('rank', 'Current Rank'), "N/A")
            score = data.get(mapping.get('score', 'Total Score'), "N/A")
            worst_case = data.get(mapping.get('worst_case', 'Worst Case Finish'), "N/A")
            
            st.markdown(f"**🏆 {round_name}**")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Current Rank", rank)
            with col2:
                st.metric("Score", score)
            with col3:
                st.metric("Worst Case", worst_case)
            
            # Show specific performance data
            if "Boulder" in round_name:
                st.markdown("**Boulder Performance:**")
                if 'boulder_cols' in mapping:
                    for j, col in enumerate(mapping['boulder_cols'], 1):
                        if col in data.index:
                            boulder_score = data.get(col, 0)
                            formatted = format_boulder_score(boulder_score)
                            status = "🟢" if "1T" in formatted else "🟡" if "1Z" in formatted else "🔴"
                            st.write(f"{status} B{j}: {formatted}")
            
            elif "Lead" in round_name:
                st.markdown("**Lead Targets:**")
                # Show target holds
                target_holds = [
                    ('qualification_hold', '🎯 Qualification'),
                    ('hold_for_1st', '🥇 1st Place'),
                    ('hold_for_2nd', '🥈 2nd Place'),
                    ('hold_for_3rd', '🥉 3rd Place')
                ]
                
                for hold_key, label in target_holds:
                    if hold_key in mapping and mapping[hold_key] in data.index:
                        hold_value = data.get(mapping[hold_key], "N/A")
                        if pd.notna(hold_value) and str(hold_value) != "N/A":
                            st.write(f"{label}: Hold {hold_value}")
            
            st.markdown("---")

def display_round_results(df, round_name):
    """Display results for a specific round with enhanced information"""
    cols_mapping = get_column_mapping(round_name)
    
    if not cols_mapping:
        st.error(f"Unknown round format: {round_name}")
        return
    
    name_col = cols_mapping.get('name', 'Name')
    rank_col = cols_mapping.get('rank', 'Current Rank')
    
    if name_col not in df.columns:
        st.error(f"Column '{name_col}' not found in data")
        st.write("Available columns:", list(df.columns))
        return
    
    # Sort by rank if available
    if rank_col and rank_col in df.columns:
        # Handle mixed data types in rank column
        df_copy = df.copy()
        df_copy[rank_col] = pd.to_numeric(df_copy[rank_col], errors='coerce')
        df_sorted = df_copy.sort_values(by=rank_col, na_position='last')
    else:
        df_sorted = df
    
    # Filter out empty rows
    df_sorted = df_sorted[df_sorted[name_col].notna() & (df_sorted[name_col] != "")]
    
    # Display athletes in a grid
    cols = st.columns(2)
    
    for idx, (_, athlete_data) in enumerate(df_sorted.iterrows()):
        rank = athlete_data.get(rank_col, idx + 1) if rank_col else idx + 1
        
        with cols[idx % 2]:
            display_athlete_card(athlete_data, rank, cols_mapping, round_name)

def create_competition_overview(all_data):
    """Create an overview of the entire competition"""
    st.markdown("""
    <div class="round-header">
        🏆 Competition Overview
    </div>
    """, unsafe_allow_html=True)
    
    # Create metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_athletes = 0
    boulder_athletes = 0
    lead_athletes = 0
    
    for round_name, df in all_data.items():
        athlete_count = len(df[df.iloc[:, 0].notna()])  # Count non-empty first column
        total_athletes += athlete_count
        
        if "Boulder" in round_name:
            boulder_athletes += athlete_count
        elif "Lead" in round_name:
            lead_athletes += athlete_count
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>👥 Total Athletes</h3>
            <h2>{}</h2>
        </div>
        """.format(total_athletes), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🪨 Boulder Entries</h3>
            <h2>{}</h2>
        </div>
        """.format(boulder_athletes), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🧗 Lead Entries</h3>
            <h2>{}</h2>
        </div>
        """.format(lead_athletes), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>🏅 Rounds</h3>
            <h2>{}</h2>
        </div>
        """.format(len(all_data)), unsafe_allow_html=True)
    
    # Competition structure visualization
    st.markdown("### 📋 Competition Structure")
    
    structure_data = []
    for round_name, df in all_data.items():
        structure_data.append({
            'Round': round_name,
            'Athletes': len(df[df.iloc[:, 0].notna()]),
            'Gender': 'Male' if 'Male' in round_name else 'Female',
            'Discipline': 'Boulder' if 'Boulder' in round_name else 'Lead',
            'Stage': 'Semifinals' if 'Semis' in round_name else 'Final'
        })
    
    structure_df = pd.DataFrame(structure_data)
    
    fig = px.sunburst(
        structure_df,
        path=['Discipline', 'Gender', 'Stage'],
        values='Athletes',
        title="Competition Structure by Discipline, Gender, and Stage"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show recent highlights
    st.markdown("### 🔥 Recent Highlights")
    
    highlights_cols = st.columns(2)
    
    with highlights_cols[0]:
        st.markdown("#### 🪨 Boulder Leaders")
        # Get boulder final results
        for round_name in ["Male Boulder Final", "Female Boulder Final"]:
            if round_name in all_data:
                df = all_data[round_name]
                cols_mapping = get_column_mapping(round_name)
                name_col = cols_mapping.get('name', 'Name')
                rank_col = cols_mapping.get('rank', 'Current Rank')
                
                if name_col in df.columns and rank_col in df.columns:
                    # Get top 3
                    df_copy = df.copy()
                    df_copy[rank_col] = pd.to_numeric(df_copy[rank_col], errors='coerce')
                    top_3 = df_copy.nsmallest(3, rank_col)
                    
                    st.markdown(f"**{round_name}:**")
                    for _, athlete in top_3.iterrows():
                        name = athlete.get(name_col, "Unknown")
                        rank = athlete.get(rank_col, "N/A")
                        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉"
                        st.write(f"{medal} {name}")
    
    with highlights_cols[1]:
        st.markdown("#### 🧗 Lead Leaders")
        # Get lead final results
        for round_name in ["Male Lead Final", "Female Lead Final"]:
            if round_name in all_data:
                df = all_data[round_name]
                cols_mapping = get_column_mapping(round_name)
                name_col = cols_mapping.get('name', 'Name')
                rank_col = cols_mapping.get('rank', 'Current Rank')
                
                if name_col in df.columns and rank_col in df.columns:
                    # Get top 3
                    df_copy = df.copy()
                    df_copy[rank_col] = pd.to_numeric(df_copy[rank_col], errors='coerce')
                    top_3 = df_copy.nsmallest(3, rank_col)
                    
                    st.markdown(f"**{round_name}:**")
                    for _, athlete in top_3.iterrows():
                        name = athlete.get(name_col, "Unknown")
                        rank = athlete.get(rank_col, "N/A")
                        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉"
                        st.write(f"{medal} {name}")

def main():
    """Main application function"""
    setup_page()
    
    # Header
    st.markdown("""
    <div class="main-header">
        🧗‍♀️ IFSC 2025 Seoul World Championships
        <div style="font-size: 1rem; margin-top: 0.5rem; color: #7f8c8d;">
            Live Results & Athlete Tracking
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load all data
    with st.spinner("🔄 Loading competition data..."):
        all_data = load_all_data()
    
    if not all_data:
        st.error("❌ No data could be loaded. Please check your internet connection.")
        return
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("### 🎯 Navigation")
        
        app_mode = st.selectbox(
            "Choose view:",
            ["Competition Overview", "Round Results", "Athlete Profile", "Live Comparison", "Debug Mode"],
            help="Select how you want to view the competition data"
        )
        
        if app_mode == "Round Results":
            selected_round = st.selectbox("Select Round:", list(all_data.keys()))
        
        elif app_mode == "Live Comparison":
            # Get all unique athlete names
            all_athletes = set()
            for round_name, df in all_data.items():
                cols_mapping = get_column_mapping(round_name)
                name_col = cols_mapping.get('name', 'Name')
                if name_col in df.columns:
                    athletes = df[name_col].dropna().astype(str)
                    all_athletes.update(athletes[athletes != ""].tolist())
            
            selected_athletes = st.multiselect(
                "Select athletes to compare:",
                sorted(list(all_athletes)),
                max_selections=5,
                help="Compare up to 5 athletes across all rounds"
            )
        
        elif app_mode == "Athlete Profile":
            # Get all unique athlete names
            all_athletes = set()
            for round_name, df in all_data.items():
                cols_mapping = get_column_mapping(round_name)
                name_col = cols_mapping.get('name', 'Name')
                if name_col in df.columns:
                    athletes = df[name_col].dropna().astype(str)
                    all_athletes.update(athletes[athletes != ""].tolist())
            
            selected_athlete = st.selectbox(
                "Select athlete:",
                [""] + sorted(list(all_athletes)),
                help="View detailed performance across all rounds"
            )
        
        elif app_mode == "Debug Mode":
            selected_round = st.selectbox("Select Round for Debug:", list(all_data.keys()))
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick stats
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("### 📊 Quick Stats")
        total_entries = sum(len(df) for df in all_data.values())
        st.metric("Total Entries", total_entries)
        st.metric("Active Rounds", len(all_data))
        
        # Show last update time
        st.markdown("### ⏰ Last Updated")
        st.write(datetime.now().strftime("%H:%M:%S"))
        if st.button("🔄 Refresh Data"):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content based on selected mode
    if app_mode == "Competition Overview":
        create_competition_overview(all_data)
    
    elif app_mode == "Round Results":
        df = all_data.get(selected_round, pd.DataFrame())
        
        if df.empty:
            st.error(f"❌ No data available for {selected_round}")
            return
        
        # Round header with live indicator
        st.markdown(f"""
        <div class="round-header">
            🏆 {selected_round}
            <div style="font-size: 1rem; margin-top: 0.5rem; opacity: 0.9;">
                🔴 LIVE • {len(df)} Athletes
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display results
        display_round_results(df, selected_round)
    
    elif app_mode == "Athlete Profile":
        if selected_athlete:
            athlete_detail_view(all_data, selected_athlete)
        else:
            st.info("👆 Please select an athlete from the sidebar to view their complete profile.")
            
            # Show random featured athletes
            st.markdown("### ⭐ Featured Athletes")
            
            featured_cols = st.columns(3)
            featured_count = 0
            
            for round_name, df in all_data.items():
                if featured_count >= 3:
                    break
                    
                cols_mapping = get_column_mapping(round_name)
                name_col = cols_mapping.get('name', 'Name')
                
                if name_col in df.columns:
                    # Get a random athlete from top 5
                    top_athletes = df.head(5)
                    if not top_athletes.empty:
                        sample_athlete = top_athletes.sample(1).iloc[0]
                        name = sample_athlete.get(name_col, "Unknown")
                        
                        with featured_cols[featured_count]:
                            if st.button(f"🎯 View {name}", key=f"featured_{featured_count}"):
                                st.session_state.selected_athlete = name
                                st.rerun()
                        
                        featured_count += 1
    
    elif app_mode == "Live Comparison":
        if selected_athletes:
            st.markdown(f"""
            <div class="round-header">
                ⚔️ Live Athlete Comparison
                <div style="font-size: 1rem; margin-top: 0.5rem; opacity: 0.9;">
                    Comparing {len(selected_athletes)} athletes across all rounds
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Create comparison data
            comparison_data = []
            detailed_data = []
            
            for athlete_name in selected_athletes:
                athlete_performance = {'Athlete': athlete_name}
                
                for round_name, df in all_data.items():
                    cols_mapping = get_column_mapping(round_name)
                    name_col = cols_mapping.get('name', 'Name')
                    rank_col = cols_mapping.get('rank', 'Current Rank')
                    score_col = cols_mapping.get('score', 'Total Score')
                    
                    if name_col in df.columns:
                        athlete_row = df[df[name_col].str.contains(athlete_name, case=False, na=False)]
                        if not athlete_row.empty:
                            data = athlete_row.iloc[0]
                            rank = data.get(rank_col, None)
                            score = data.get(score_col, None)
                            
                            if pd.notna(rank):
                                try:
                                    rank_num = int(float(rank))
                                    comparison_data.append({
                                        'Athlete': athlete_name,
                                        'Round': round_name,
                                        'Rank': rank_num,
                                        'Score': score
                                    })
                                    athlete_performance[round_name] = f"#{rank_num}"
                                except:
                                    athlete_performance[round_name] = "N/A"
                            else:
                                athlete_performance[round_name] = "N/A"
                        else:
                            athlete_performance[round_name] = "N/A"
                
                detailed_data.append(athlete_performance)
            
            # Show comparison chart
            if comparison_data:
                comparison_df = pd.DataFrame(comparison_data)
                
                fig = px.line(
                    comparison_df, 
                    x='Round', 
                    y='Rank', 
                    color='Athlete',
                    title='🏆 Rank Progression Across Rounds',
                    markers=True,
                    hover_data=['Score']
                )
                
                fig.update_layout(
                    yaxis=dict(autorange='reversed', title="Rank (lower is better)"),
                    xaxis=dict(tickangle=45),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                )
                
                fig.update_traces(line=dict(width=3), marker=dict(size=8))
                st.plotly_chart(fig, use_container_width=True)
            
            # Show detailed comparison table
            st.markdown("### 📊 Detailed Comparison")
            if detailed_data:
                detailed_df = pd.DataFrame(detailed_data)
                st.dataframe(detailed_df, use_container_width=True)
        
        else:
            st.info("👆 Please select athletes from the sidebar to compare their performance.")
    
    elif app_mode == "Debug Mode":
        df = all_data.get(selected_round, pd.DataFrame())
        
        st.markdown(f"""
        <div class="round-header">
            🔧 Debug Mode: {selected_round}
        </div>
        """, unsafe_allow_html=True)
        
        if df.empty:
            st.error(f"❌ No data available for {selected_round}")
            return
        
        # Debug information
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 DataFrame Info")
            st.write(f"**Shape:** {df.shape}")
            st.write(f"**Columns:** {len(df.columns)}")
            st.write(f"**Non-empty rows:** {len(df[df.iloc[:, 0].notna()])}")
            
            st.markdown("#### 📋 All Columns")
            for i, col in enumerate(df.columns):
                non_null = df[col].count()
                st.write(f"{i+1}. `{col}` ({df[col].dtype}) - {non_null} values")
        
        with col2:
            st.markdown("#### 🎯 Column Mapping")
            cols_mapping = get_column_mapping(selected_round)
            
            for key, value in cols_mapping.items():
                if isinstance(value, list):
                    st.write(f"**{key}:** {', '.join(value)}")
                else:
                    st.write(f"**{key}:** `{value}`")
            
            st.markdown("#### 🔍 Sample Data")
            st.dataframe(df.head(5))
        
        # Show raw data toggle
        if st.checkbox("Show Full Raw Data"):
            st.markdown("#### 📋 Complete Dataset")
            st.dataframe(df)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"🚫 Application Error: {e}")
        st.markdown("Please refresh the page or contact support if the issue persists.")
        
        with st.expander("🔧 Debug Information"):
            st.code(f"Error: {e}")
            st.code(f"Time: {datetime.now()}")
            import traceback
            st.code(traceback.format_exc())

def is_placeholder_athlete(name: str) -> bool:
    """Check if name is a placeholder like 'Athlete 1', 'Athlete 23', etc."""
    name_str = str(name).strip()
    if name_str.startswith('Athlete '):
        remaining = name_str[8:].strip()
        return remaining.isdigit()
    return False


def display_qualification_thresholds(qualification_info: Dict[str, str]):
    """Display qualification thresholds if available"""
    if qualification_info:
        threshold_items = []
        threshold_mapping = {
            'Hold for 1st': ('🥇 1st', '#FFD700'),
            'Hold for 2nd': ('🥈 2nd', '#C0C0C0'),
            'Hold for 3rd': ('🥉 3rd', '#CD7F32'),
            'Hold to Qualify': ('✅ Qualify', '#28a745'),
            'Min to Qualify': ('⚠️ Min', '#ffc107')
        }
        
        for key, value in qualification_info.items():
            if key in threshold_mapping:
                label, color = threshold_mapping[key]
                threshold_items.append(f'<span style="color: {color}; font-weight: bold;">{label}: {value}</span>')
        
        if threshold_items:
            st.markdown(f"""
            <div class="threshold-card">
                <h5>🎯 Qualification Thresholds</h5>
                {' | '.join(threshold_items)}
            </div>
            """, unsafe_allow_html=True)


def display_lead_athletes(active_df: pd.DataFrame, qualification_info: Dict[str, str]):
    """Display lead competition athletes with enhanced formatting"""
    # Sort by rank if available
    try:
        if 'Current Rank' in active_df.columns:
            active_df['Current Rank'] = pd.to_numeric(active_df['Current Rank'], errors='coerce')
            active_df = active_df.sort_values('Current Rank', ascending=True).reset_index(drop=True)
    except Exception as e:
        logger.warning(f"Could not sort by rank: {e}")
    
    # Display athlete cards
    for _, row in active_df.iterrows():
        name = DataProcessor.clean_text(str(row.get('Name', 'Unknown')))
        score = row.get('Manual Score', 'N/A')
        rank = row.get('Current Rank', 'N/A')
        status = DataProcessor.clean_text(str(row.get('Status', 'Unknown')))
        worst_finish = row.get('Worst Finish', 'N/A')
        
        # Determine if athlete has a score
        has_score = score not in ['N/A', '', None] and not pd.isna(score)
        
        # Create threshold display for athletes without scores
        threshold_display = create_threshold_display(has_score, qualification_info)
        
        # Determine card styling
        card_class, status_emoji = determine_lead_athlete_status(status, has_score)
        
        # Set position emoji
        position_emoji = get_lead_position_emoji(rank, has_score, card_class, status_emoji)
        
        # Format displays
        score_display = score if has_score else "Awaiting Result"
        worst_finish_display = format_worst_finish(worst_finish, has_score)
        
        # Create athlete card
        st.markdown(f"""
        <div class="athlete-row {card_class}">
            <strong>{position_emoji} #{rank} - {name}</strong><br>
            <small>Score: {score_display} | Status: {status}{worst_finish_display}</small>{threshold_display}
        </div>
        """, unsafe_allow_html=True)


def create_threshold_display(has_score: bool, qualification_info: Dict[str, str]) -> str:
    """Create threshold display for athletes without scores"""
    if has_score or not qualification_info:
        return ""
    
    thresholds = []
    for key, value in qualification_info.items():
        if key == 'Hold for 1st':
            thresholds.append(f'🥇 1st: {value}')
        elif key == 'Hold for 2nd':
            thresholds.append(f'🥈 2nd: {value}')
        elif key == 'Hold for 3rd':
            thresholds.append(f'🥉 3rd: {value}')
        elif key in ['Hold to Qualify', 'Min to Qualify']:
            thresholds.append(f'🎯 Target: {value}')
    
    if thresholds:
        return f"<br><div class='targets'><strong>Targets:</strong> {' | '.join(thresholds)}</div>"
    return ""


def determine_lead_athlete_status(status: str, has_score: bool) -> Tuple[str, str]:
    """Determine lead athlete status and styling"""
    if not has_score:
        return "", "📄"
    
    if "Qualified" in status or "✓✓" in status:
        return "qualified", "✅"
    elif "Eliminated" in status or "✗" in status:
        return "eliminated", "❌"
    elif "Podium" in status and "No Podium" not in status and "Contention" not in status:
        return "podium-position", "🏆"
    elif "Podium Contention" in status or "Contention" in status:
        return "podium-contention", "⚠️"
    elif "No Podium" in status:
        return "no-podium", "❌"
    else:
        return "", "📄"


def get_lead_position_emoji(rank: any, has_score: bool, card_class: str, status_emoji: str) -> str:
    """Get position emoji for lead athletes"""
    rank_num = DataProcessor.safe_numeric_conversion(rank)
    if rank_num > 0:
        return status_emoji if has_score and card_class else f"#{rank_num}"
    return "📄"


def format_worst_finish(worst_finish: any, has_score: bool) -> str:
    """Format worst finish display"""
    if not has_score or worst_finish in ['N/A', '', None] or pd.isna(worst_finish):
        return ""
    
    worst_finish_clean = DataProcessor.clean_text(str(worst_finish))
    return f" | Worst Finish: {worst_finish_clean}" if worst_finish_clean and worst_finish_clean != '-' else ""


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"🚫 Application Error: {e}")
        st.markdown("Please refresh the page or contact support if the issue persists.")
        
        with st.expander("🔧 Debug Information"):
            st.code(f"Error: {e}")
            st.code(f"Time: {datetime.now()}")
            import traceback
            st.code(traceback.format_exc()), na=False)) &      # Remove "25+" style entries
            (~df['Name'].apply(is_placeholder_athlete))
        ]
        
        # Second pass: If we have rank information, use it to filter properly
        if 'Current Rank' in filtered_df.columns:
            filtered_df['temp_rank'] = pd.to_numeric(filtered_df['Current Rank'], errors='coerce')
            
            # Keep only rows with valid ranks within expected range
            ranked_df = filtered_df[
                (filtered_df['temp_rank'].notna()) & 
                (filtered_df['temp_rank'] >= 1) & 
                (filtered_df['temp_rank'] <= expected_max)
            ]
            
            if len(ranked_df) > 0:
                # Sort by rank and take only the expected number
                ranked_df = ranked_df.sort_values('temp_rank').head(expected_max)
                filtered_df = ranked_df.drop('temp_rank', axis=1)
            else:
                # If no valid ranks, fall back to manual filtering
                filtered_df = manual_athlete_filter(filtered_df, expected_max)
        else:
            # No rank column available, use manual filtering
            filtered_df = manual_athlete_filter(filtered_df, expected_max)
        
        # Third pass: Additional validation for lead competitions
        if "Lead" in competition_name:
            filtered_df = validate_lead_athletes(filtered_df, expected_max)
        
        logger.info(f"Filtered to {len(filtered_df)} athletes for {competition_name} (expected: {expected_max})")
        return filtered_df
        
    except Exception as e:
        logger.error(f"Error filtering athletes for {competition_name}: {e}")
        # Fallback to basic filtering with count limit
        basic_filtered = df[
            df['Name'].notna() & 
            (df['Name'] != '') &
            (~df['Name'].astype(str).str.contains('Hold for', na=False))
        ].head(expected_max)
        return basic_filtered


def manual_athlete_filter(df: pd.DataFrame, expected_max: int) -> pd.DataFrame:
    """Manually filter athletes when rank information is not reliable"""
    # Look for patterns that indicate real athlete names vs reference data
    potential_athletes = []
    
    for idx, row in df.iterrows():
        name = str(row.get('Name', '')).strip()
        
        # Skip if name looks like reference data
        if any(keyword in name.lower() for keyword in [
            'hold', 'min', 'max', 'qualification', 'threshold', 'zone', 'top',
            'points', 'score', 'rank', 'position', 'place', 'finish'
        ]):
            continue
        
        # Skip if name is too short or looks like a number/code
        if len(name) < 3 or name.isdigit() or not any(c.isalpha() for c in name):
            continue
        
        # Look for typical athlete name patterns (First Last or similar)
        name_parts = name.split()
        if len(name_parts) >= 2 and all(part.isalpha() or part.replace('.', '').isalpha() for part in name_parts):
            potential_athletes.append(idx)
        elif len(name_parts) == 1 and len(name) > 4 and name.isalpha():
            # Single names that are long enough and all letters
            potential_athletes.append(idx)
    
    # Return the filtered dataframe, limited to expected count
    return df.loc[potential_athletes[:expected_max]]


def validate_lead_athletes(df: pd.DataFrame, expected_max: int) -> pd.DataFrame:
    """Additional validation specifically for lead competitions"""
    if len(df) <= expected_max:
        return df
    
    # For lead competitions, prioritize athletes with actual climbing data
    scored_athletes = df[df['Manual Score'].notna() & (df['Manual Score'] != '')].copy()
    unscored_athletes = df[df['Manual Score'].isna() | (df['Manual Score'] == '')].copy()
    
    # Combine scored athletes first, then fill with unscored up to limit
    result_df = scored_athletes.copy()
    remaining_slots = expected_max - len(scored_athletes)
    
    if remaining_slots > 0 and len(unscored_athletes) > 0:
        result_df = pd.concat([result_df, unscored_athletes.head(remaining_slots)], ignore_index=True)
    
    return result_df.head(expected_max)


def is_placeholder_athlete(name: str) -> bool:
    """Check if name is a placeholder like 'Athlete 1', 'Athlete 23', etc."""
    name_str = str(name).strip()
    if name_str.startswith('Athlete '):
        remaining = name_str[8:].strip()
        return remaining.isdigit()
    return False


def display_qualification_thresholds(qualification_info: Dict[str, str]):
    """Display qualification thresholds if available"""
    if qualification_info:
        threshold_items = []
        threshold_mapping = {
            'Hold for 1st': ('🥇 1st', '#FFD700'),
            'Hold for 2nd': ('🥈 2nd', '#C0C0C0'),
            'Hold for 3rd': ('🥉 3rd', '#CD7F32'),
            'Hold to Qualify': ('✅ Qualify', '#28a745'),
            'Min to Qualify': ('⚠️ Min', '#ffc107')
        }
        
        for key, value in qualification_info.items():
            if key in threshold_mapping:
                label, color = threshold_mapping[key]
                threshold_items.append(f'<span style="color: {color}; font-weight: bold;">{label}: {value}</span>')
        
        if threshold_items:
            st.markdown(f"""
            <div class="threshold-card">
                <h5>🎯 Qualification Thresholds</h5>
                {' | '.join(threshold_items)}
            </div>
            """, unsafe_allow_html=True)


def display_lead_athletes(active_df: pd.DataFrame, qualification_info: Dict[str, str]):
    """Display lead competition athletes with enhanced formatting"""
    # Sort by rank if available
    try:
        if 'Current Rank' in active_df.columns:
            active_df['Current Rank'] = pd.to_numeric(active_df['Current Rank'], errors='coerce')
            active_df = active_df.sort_values('Current Rank', ascending=True).reset_index(drop=True)
    except Exception as e:
        logger.warning(f"Could not sort by rank: {e}")
    
    # Display athlete cards
    for _, row in active_df.iterrows():
        name = DataProcessor.clean_text(str(row.get('Name', 'Unknown')))
        score = row.get('Manual Score', 'N/A')
        rank = row.get('Current Rank', 'N/A')
        status = DataProcessor.clean_text(str(row.get('Status', 'Unknown')))
        worst_finish = row.get('Worst Finish', 'N/A')
        
        # Determine if athlete has a score
        has_score = score not in ['N/A', '', None] and not pd.isna(score)
        
        # Create threshold display for athletes without scores
        threshold_display = create_threshold_display(has_score, qualification_info)
        
        # Determine card styling
        card_class, status_emoji = determine_lead_athlete_status(status, has_score)
        
        # Set position emoji
        position_emoji = get_lead_position_emoji(rank, has_score, card_class, status_emoji)
        
        # Format displays
        score_display = score if has_score else "Awaiting Result"
        worst_finish_display = format_worst_finish(worst_finish, has_score)
        
        # Create athlete card
        st.markdown(f"""
        <div class="athlete-row {card_class}">
            <strong>{position_emoji} #{rank} - {name}</strong><br>
            <small>Score: {score_display} | Status: {status}{worst_finish_display}</small>{threshold_display}
        </div>
        """, unsafe_allow_html=True)


def create_threshold_display(has_score: bool, qualification_info: Dict[str, str]) -> str:
    """Create threshold display for athletes without scores"""
    if has_score or not qualification_info:
        return ""
    
    thresholds = []
    for key, value in qualification_info.items():
        if key == 'Hold for 1st':
            thresholds.append(f'🥇 1st: {value}')
        elif key == 'Hold for 2nd':
            thresholds.append(f'🥈 2nd: {value}')
        elif key == 'Hold for 3rd':
            thresholds.append(f'🥉 3rd: {value}')
        elif key in ['Hold to Qualify', 'Min to Qualify']:
            thresholds.append(f'🎯 Target: {value}')
    
    if thresholds:
        return f"<br><div class='targets'><strong>Targets:</strong> {' | '.join(thresholds)}</div>"
    return ""


def determine_lead_athlete_status(status: str, has_score: bool) -> Tuple[str, str]:
    """Determine lead athlete status and styling"""
    if not has_score:
        return "", "📄"
    
    if "Qualified" in status or "✓✓" in status:
        return "qualified", "✅"
    elif "Eliminated" in status or "✗" in status:
        return "eliminated", "❌"
    elif "Podium" in status and "No Podium" not in status and "Contention" not in status:
        return "podium-position", "🏆"
    elif "Podium Contention" in status or "Contention" in status:
        return "podium-contention", "⚠️"
    elif "No Podium" in status:
        return "no-podium", "❌"
    else:
        return "", "📄"


def get_lead_position_emoji(rank: any, has_score: bool, card_class: str, status_emoji: str) -> str:
    """Get position emoji for lead athletes"""
    rank_num = DataProcessor.safe_numeric_conversion(rank)
    if rank_num > 0:
        return status_emoji if has_score and card_class else f"#{rank_num}"
    return "📄"


def format_worst_finish(worst_finish: any, has_score: bool) -> str:
    """Format worst finish display"""
    if not has_score or worst_finish in ['N/A', '', None] or pd.isna(worst_finish):
        return ""
    
    worst_finish_clean = DataProcessor.clean_text(str(worst_finish))
    return f" | Worst Finish: {worst_finish_clean}" if worst_finish_clean and worst_finish_clean != '-' else ""


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"🚫 Application Error: {e}")
        st.markdown("Please refresh the page or contact support if the issue persists.")
        
        with st.expander("🔧 Debug Information"):
            st.code(f"Error: {e}")
            st.code(f"Time: {datetime.now()}")
            import traceback
            st.code(traceback.format_exc()),           # "Athlete 1", "Athlete 23"
        r'^climber\s+\d+


def display_qualification_thresholds(qualification_info: Dict[str, str]):
    """Display qualification thresholds if available"""
    if qualification_info:
        threshold_items = []
        threshold_mapping = {
            'Hold for 1st': ('🥇 1st', '#FFD700'),
            'Hold for 2nd': ('🥈 2nd', '#C0C0C0'),
            'Hold for 3rd': ('🥉 3rd', '#CD7F32'),
            'Hold to Qualify': ('✅ Qualify', '#28a745'),
            'Min to Qualify': ('⚠️ Min', '#ffc107')
        }
        
        for key, value in qualification_info.items():
            if key in threshold_mapping:
                label, color = threshold_mapping[key]
                threshold_items.append(f'<span style="color: {color}; font-weight: bold;">{label}: {value}</span>')
        
        if threshold_items:
            st.markdown(f"""
            <div class="threshold-card">
                <h5>🎯 Qualification Thresholds</h5>
                {' | '.join(threshold_items)}
            </div>
            """, unsafe_allow_html=True)


def display_lead_athletes(active_df: pd.DataFrame, qualification_info: Dict[str, str]):
    """Display lead competition athletes with enhanced formatting"""
    # Sort by rank if available
    try:
        if 'Current Rank' in active_df.columns:
            active_df['Current Rank'] = pd.to_numeric(active_df['Current Rank'], errors='coerce')
            active_df = active_df.sort_values('Current Rank', ascending=True).reset_index(drop=True)
    except Exception as e:
        logger.warning(f"Could not sort by rank: {e}")
    
    # Display athlete cards
    for _, row in active_df.iterrows():
        name = DataProcessor.clean_text(str(row.get('Name', 'Unknown')))
        score = row.get('Manual Score', 'N/A')
        rank = row.get('Current Rank', 'N/A')
        status = DataProcessor.clean_text(str(row.get('Status', 'Unknown')))
        worst_finish = row.get('Worst Finish', 'N/A')
        
        # Determine if athlete has a score
        has_score = score not in ['N/A', '', None] and not pd.isna(score)
        
        # Create threshold display for athletes without scores
        threshold_display = create_threshold_display(has_score, qualification_info)
        
        # Determine card styling
        card_class, status_emoji = determine_lead_athlete_status(status, has_score)
        
        # Set position emoji
        position_emoji = get_lead_position_emoji(rank, has_score, card_class, status_emoji)
        
        # Format displays
        score_display = score if has_score else "Awaiting Result"
        worst_finish_display = format_worst_finish(worst_finish, has_score)
        
        # Create athlete card
        st.markdown(f"""
        <div class="athlete-row {card_class}">
            <strong>{position_emoji} #{rank} - {name}</strong><br>
            <small>Score: {score_display} | Status: {status}{worst_finish_display}</small>{threshold_display}
        </div>
        """, unsafe_allow_html=True)


def create_threshold_display(has_score: bool, qualification_info: Dict[str, str]) -> str:
    """Create threshold display for athletes without scores"""
    if has_score or not qualification_info:
        return ""
    
    thresholds = []
    for key, value in qualification_info.items():
        if key == 'Hold for 1st':
            thresholds.append(f'🥇 1st: {value}')
        elif key == 'Hold for 2nd':
            thresholds.append(f'🥈 2nd: {value}')
        elif key == 'Hold for 3rd':
            thresholds.append(f'🥉 3rd: {value}')
        elif key in ['Hold to Qualify', 'Min to Qualify']:
            thresholds.append(f'🎯 Target: {value}')
    
    if thresholds:
        return f"<br><div class='targets'><strong>Targets:</strong> {' | '.join(thresholds)}</div>"
    return ""


def determine_lead_athlete_status(status: str, has_score: bool) -> Tuple[str, str]:
    """Determine lead athlete status and styling"""
    if not has_score:
        return "", "📄"
    
    if "Qualified" in status or "✓✓" in status:
        return "qualified", "✅"
    elif "Eliminated" in status or "✗" in status:
        return "eliminated", "❌"
    elif "Podium" in status and "No Podium" not in status and "Contention" not in status:
        return "podium-position", "🏆"
    elif "Podium Contention" in status or "Contention" in status:
        return "podium-contention", "⚠️"
    elif "No Podium" in status:
        return "no-podium", "❌"
    else:
        return "", "📄"


def get_lead_position_emoji(rank: any, has_score: bool, card_class: str, status_emoji: str) -> str:
    """Get position emoji for lead athletes"""
    rank_num = DataProcessor.safe_numeric_conversion(rank)
    if rank_num > 0:
        return status_emoji if has_score and card_class else f"#{rank_num}"
    return "📄"


def format_worst_finish(worst_finish: any, has_score: bool) -> str:
    """Format worst finish display"""
    if not has_score or worst_finish in ['N/A', '', None] or pd.isna(worst_finish):
        return ""
    
    worst_finish_clean = DataProcessor.clean_text(str(worst_finish))
    return f" | Worst Finish: {worst_finish_clean}" if worst_finish_clean and worst_finish_clean != '-' else ""


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"🚫 Application Error: {e}")
        st.markdown("Please refresh the page or contact support if the issue persists.")
        
        
        with st.expander("🔧 Debug Information"):
            st.code(f"Error: {e}")
            st.code(f"Time: {datetime.now()}")
            import traceback
            st.code(traceback.format_exc())
            (~df['Name'].astype(str).str.match(r'^\d+\+'


def is_placeholder_athlete(name: str) -> bool:
    """Check if name is a placeholder like 'Athlete 1', 'Athlete 23', etc."""
    name_str = str(name).strip()
    if name_str.startswith('Athlete '):
        remaining = name_str[8:].strip()
        return remaining.isdigit()
    return False


def display_qualification_thresholds(qualification_info: Dict[str, str]):
    """Display qualification thresholds if available"""
    if qualification_info:
        threshold_items = []
        threshold_mapping = {
            'Hold for 1st': ('🥇 1st', '#FFD700'),
            'Hold for 2nd': ('🥈 2nd', '#C0C0C0'),
            'Hold for 3rd': ('🥉 3rd', '#CD7F32'),
            'Hold to Qualify': ('✅ Qualify', '#28a745'),
            'Min to Qualify': ('⚠️ Min', '#ffc107')
        }
        
        for key, value in qualification_info.items():
            if key in threshold_mapping:
                label, color = threshold_mapping[key]
                threshold_items.append(f'<span style="color: {color}; font-weight: bold;">{label}: {value}</span>')
        
        if threshold_items:
            st.markdown(f"""
            <div class="threshold-card">
                <h5>🎯 Qualification Thresholds</h5>
                {' | '.join(threshold_items)}
            </div>
            """, unsafe_allow_html=True)


def display_lead_athletes(active_df: pd.DataFrame, qualification_info: Dict[str, str]):
    """Display lead competition athletes with enhanced formatting"""
    # Sort by rank if available
    try:
        if 'Current Rank' in active_df.columns:
            active_df['Current Rank'] = pd.to_numeric(active_df['Current Rank'], errors='coerce')
            active_df = active_df.sort_values('Current Rank', ascending=True).reset_index(drop=True)
    except Exception as e:
        logger.warning(f"Could not sort by rank: {e}")
    
    # Display athlete cards
    for _, row in active_df.iterrows():
        name = DataProcessor.clean_text(str(row.get('Name', 'Unknown')))
        score = row.get('Manual Score', 'N/A')
        rank = row.get('Current Rank', 'N/A')
        status = DataProcessor.clean_text(str(row.get('Status', 'Unknown')))
        worst_finish = row.get('Worst Finish', 'N/A')
        
        # Determine if athlete has a score
        has_score = score not in ['N/A', '', None] and not pd.isna(score)
        
        # Create threshold display for athletes without scores
        threshold_display = create_threshold_display(has_score, qualification_info)
        
        # Determine card styling
        card_class, status_emoji = determine_lead_athlete_status(status, has_score)
        
        # Set position emoji
        position_emoji = get_lead_position_emoji(rank, has_score, card_class, status_emoji)
        
        # Format displays
        score_display = score if has_score else "Awaiting Result"
        worst_finish_display = format_worst_finish(worst_finish, has_score)
        
        # Create athlete card
        st.markdown(f"""
        <div class="athlete-row {card_class}">
            <strong>{position_emoji} #{rank} - {name}</strong><br>
            <small>Score: {score_display} | Status: {status}{worst_finish_display}</small>{threshold_display}
        </div>
        """, unsafe_allow_html=True)


def create_threshold_display(has_score: bool, qualification_info: Dict[str, str]) -> str:
    """Create threshold display for athletes without scores"""
    if has_score or not qualification_info:
        return ""
    
    thresholds = []
    for key, value in qualification_info.items():
        if key == 'Hold for 1st':
            thresholds.append(f'🥇 1st: {value}')
        elif key == 'Hold for 2nd':
            thresholds.append(f'🥈 2nd: {value}')
        elif key == 'Hold for 3rd':
            thresholds.append(f'🥉 3rd: {value}')
        elif key in ['Hold to Qualify', 'Min to Qualify']:
            thresholds.append(f'🎯 Target: {value}')
    
    if thresholds:
        return f"<br><div class='targets'><strong>Targets:</strong> {' | '.join(thresholds)}</div>"
    return ""


def determine_lead_athlete_status(status: str, has_score: bool) -> Tuple[str, str]:
    """Determine lead athlete status and styling"""
    if not has_score:
        return "", "📄"
    
    if "Qualified" in status or "✓✓" in status:
        return "qualified", "✅"
    elif "Eliminated" in status or "✗" in status:
        return "eliminated", "❌"
    elif "Podium" in status and "No Podium" not in status and "Contention" not in status:
        return "podium-position", "🏆"
    elif "Podium Contention" in status or "Contention" in status:
        return "podium-contention", "⚠️"
    elif "No Podium" in status:
        return "no-podium", "❌"
    else:
        return "", "📄"


def get_lead_position_emoji(rank: any, has_score: bool, card_class: str, status_emoji: str) -> str:
    """Get position emoji for lead athletes"""
    rank_num = DataProcessor.safe_numeric_conversion(rank)
    if rank_num > 0:
        return status_emoji if has_score and card_class else f"#{rank_num}"
    return "📄"


def format_worst_finish(worst_finish: any, has_score: bool) -> str:
    """Format worst finish display"""
    if not has_score or worst_finish in ['N/A', '', None] or pd.isna(worst_finish):
        return ""
    
    worst_finish_clean = DataProcessor.clean_text(str(worst_finish))
    return f" | Worst Finish: {worst_finish_clean}" if worst_finish_clean and worst_finish_clean != '-' else ""


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"🚫 Application Error: {e}")
        st.markdown("Please refresh the page or contact support if the issue persists.")
        
        with st.expander("🔧 Debug Information"):
            st.code(f"Error: {e}")
            st.code(f"Time: {datetime.now()}")
            import traceback
            st.code(traceback.format_exc()), na=False)) &      # Remove "25+" style entries
            (~df['Name'].apply(is_placeholder_athlete))
        ]
        
        # Second pass: If we have rank information, use it to filter properly
        if 'Current Rank' in filtered_df.columns:
            filtered_df['temp_rank'] = pd.to_numeric(filtered_df['Current Rank'], errors='coerce')
            
            # Keep only rows with valid ranks within expected range
            ranked_df = filtered_df[
                (filtered_df['temp_rank'].notna()) & 
                (filtered_df['temp_rank'] >= 1) & 
                (filtered_df['temp_rank'] <= expected_max)
            ]
            
            if len(ranked_df) > 0:
                # Sort by rank and take only the expected number
                ranked_df = ranked_df.sort_values('temp_rank').head(expected_max)
                filtered_df = ranked_df.drop('temp_rank', axis=1)
            else:
                # If no valid ranks, fall back to manual filtering
                filtered_df = manual_athlete_filter(filtered_df, expected_max)
        else:
            # No rank column available, use manual filtering
            filtered_df = manual_athlete_filter(filtered_df, expected_max)
        
        # Third pass: Additional validation for lead competitions
        if "Lead" in competition_name:
            filtered_df = validate_lead_athletes(filtered_df, expected_max)
        
        logger.info(f"Filtered to {len(filtered_df)} athletes for {competition_name} (expected: {expected_max})")
        return filtered_df
        
    except Exception as e:
        logger.error(f"Error filtering athletes for {competition_name}: {e}")
        # Fallback to basic filtering with count limit
        basic_filtered = df[
            df['Name'].notna() & 
            (df['Name'] != '') &
            (~df['Name'].astype(str).str.contains('Hold for', na=False))
        ].head(expected_max)
        return basic_filtered


def manual_athlete_filter(df: pd.DataFrame, expected_max: int) -> pd.DataFrame:
    """Manually filter athletes when rank information is not reliable"""
    # Look for patterns that indicate real athlete names vs reference data
    potential_athletes = []
    
    for idx, row in df.iterrows():
        name = str(row.get('Name', '')).strip()
        
        # Skip if name looks like reference data
        if any(keyword in name.lower() for keyword in [
            'hold', 'min', 'max', 'qualification', 'threshold', 'zone', 'top',
            'points', 'score', 'rank', 'position', 'place', 'finish'
        ]):
            continue
        
        # Skip if name is too short or looks like a number/code
        if len(name) < 3 or name.isdigit() or not any(c.isalpha() for c in name):
            continue
        
        # Look for typical athlete name patterns (First Last or similar)
        name_parts = name.split()
        if len(name_parts) >= 2 and all(part.isalpha() or part.replace('.', '').isalpha() for part in name_parts):
            potential_athletes.append(idx)
        elif len(name_parts) == 1 and len(name) > 4 and name.isalpha():
            # Single names that are long enough and all letters
            potential_athletes.append(idx)
    
    # Return the filtered dataframe, limited to expected count
    return df.loc[potential_athletes[:expected_max]]


def validate_lead_athletes(df: pd.DataFrame, expected_max: int) -> pd.DataFrame:
    """Additional validation specifically for lead competitions"""
    if len(df) <= expected_max:
        return df
    
    # For lead competitions, prioritize athletes with actual climbing data
    scored_athletes = df[df['Manual Score'].notna() & (df['Manual Score'] != '')].copy()
    unscored_athletes = df[df['Manual Score'].isna() | (df['Manual Score'] == '')].copy()
    
    # Combine scored athletes first, then fill with unscored up to limit
    result_df = scored_athletes.copy()
    remaining_slots = expected_max - len(scored_athletes)
    
    if remaining_slots > 0 and len(unscored_athletes) > 0:
        result_df = pd.concat([result_df, unscored_athletes.head(remaining_slots)], ignore_index=True)
    
    return result_df.head(expected_max)


def is_placeholder_athlete(name: str) -> bool:
    """Check if name is a placeholder like 'Athlete 1', 'Athlete 23', etc."""
    name_str = str(name).strip()
    if name_str.startswith('Athlete '):
        remaining = name_str[8:].strip()
        return remaining.isdigit()
    return False


def display_qualification_thresholds(qualification_info: Dict[str, str]):
    """Display qualification thresholds if available"""
    if qualification_info:
        threshold_items = []
        threshold_mapping = {
            'Hold for 1st': ('🥇 1st', '#FFD700'),
            'Hold for 2nd': ('🥈 2nd', '#C0C0C0'),
            'Hold for 3rd': ('🥉 3rd', '#CD7F32'),
            'Hold to Qualify': ('✅ Qualify', '#28a745'),
            'Min to Qualify': ('⚠️ Min', '#ffc107')
        }
        
        for key, value in qualification_info.items():
            if key in threshold_mapping:
                label, color = threshold_mapping[key]
                threshold_items.append(f'<span style="color: {color}; font-weight: bold;">{label}: {value}</span>')
        
        if threshold_items:
            st.markdown(f"""
            <div class="threshold-card">
                <h5>🎯 Qualification Thresholds</h5>
                {' | '.join(threshold_items)}
            </div>
            """, unsafe_allow_html=True)


def display_lead_athletes(active_df: pd.DataFrame, qualification_info: Dict[str, str]):
    """Display lead competition athletes with enhanced formatting"""
    # Sort by rank if available
    try:
        if 'Current Rank' in active_df.columns:
            active_df['Current Rank'] = pd.to_numeric(active_df['Current Rank'], errors='coerce')
            active_df = active_df.sort_values('Current Rank', ascending=True).reset_index(drop=True)
    except Exception as e:
        logger.warning(f"Could not sort by rank: {e}")
    
    # Display athlete cards
    for _, row in active_df.iterrows():
        name = DataProcessor.clean_text(str(row.get('Name', 'Unknown')))
        score = row.get('Manual Score', 'N/A')
        rank = row.get('Current Rank', 'N/A')
        status = DataProcessor.clean_text(str(row.get('Status', 'Unknown')))
        worst_finish = row.get('Worst Finish', 'N/A')
        
        # Determine if athlete has a score
        has_score = score not in ['N/A', '', None] and not pd.isna(score)
        
        # Create threshold display for athletes without scores
        threshold_display = create_threshold_display(has_score, qualification_info)
        
        # Determine card styling
        card_class, status_emoji = determine_lead_athlete_status(status, has_score)
        
        # Set position emoji
        position_emoji = get_lead_position_emoji(rank, has_score, card_class, status_emoji)
        
        # Format displays
        score_display = score if has_score else "Awaiting Result"
        worst_finish_display = format_worst_finish(worst_finish, has_score)
        
        # Create athlete card
        st.markdown(f"""
        <div class="athlete-row {card_class}">
            <strong>{position_emoji} #{rank} - {name}</strong><br>
            <small>Score: {score_display} | Status: {status}{worst_finish_display}</small>{threshold_display}
        </div>
        """, unsafe_allow_html=True)


def create_threshold_display(has_score: bool, qualification_info: Dict[str, str]) -> str:
    """Create threshold display for athletes without scores"""
    if has_score or not qualification_info:
        return ""
    
    thresholds = []
    for key, value in qualification_info.items():
        if key == 'Hold for 1st':
            thresholds.append(f'🥇 1st: {value}')
        elif key == 'Hold for 2nd':
            thresholds.append(f'🥈 2nd: {value}')
        elif key == 'Hold for 3rd':
            thresholds.append(f'🥉 3rd: {value}')
        elif key in ['Hold to Qualify', 'Min to Qualify']:
            thresholds.append(f'🎯 Target: {value}')
    
    if thresholds:
        return f"<br><div class='targets'><strong>Targets:</strong> {' | '.join(thresholds)}</div>"
    return ""


def determine_lead_athlete_status(status: str, has_score: bool) -> Tuple[str, str]:
    """Determine lead athlete status and styling"""
    if not has_score:
        return "", "📄"
    
    if "Qualified" in status or "✓✓" in status:
        return "qualified", "✅"
    elif "Eliminated" in status or "✗" in status:
        return "eliminated", "❌"
    elif "Podium" in status and "No Podium" not in status and "Contention" not in status:
        return "podium-position", "🏆"
    elif "Podium Contention" in status or "Contention" in status:
        return "podium-contention", "⚠️"
    elif "No Podium" in status:
        return "no-podium", "❌"
    else:
        return "", "📄"


def get_lead_position_emoji(rank: any, has_score: bool, card_class: str, status_emoji: str) -> str:
    """Get position emoji for lead athletes"""
    rank_num = DataProcessor.safe_numeric_conversion(rank)
    if rank_num > 0:
        return status_emoji if has_score and card_class else f"#{rank_num}"
    return "📄"


def format_worst_finish(worst_finish: any, has_score: bool) -> str:
    """Format worst finish display"""
    if not has_score or worst_finish in ['N/A', '', None] or pd.isna(worst_finish):
        return ""
    
    worst_finish_clean = DataProcessor.clean_text(str(worst_finish))
    return f" | Worst Finish: {worst_finish_clean}" if worst_finish_clean and worst_finish_clean != '-' else ""


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"🚫 Application Error: {e}")
        st.markdown("Please refresh the page or contact support if the issue persists.")
        
        with st.expander("🔧 Debug Information"):
            st.code(f"Error: {e}")
            st.code(f"Time: {datetime.now()}")
            import traceback
            st.code(traceback.format_exc()),           # "Climber 1", "Climber 23"  
        r'^competitor\s+\d+


def display_qualification_thresholds(qualification_info: Dict[str, str]):
    """Display qualification thresholds if available"""
    if qualification_info:
        threshold_items = []
        threshold_mapping = {
            'Hold for 1st': ('🥇 1st', '#FFD700'),
            'Hold for 2nd': ('🥈 2nd', '#C0C0C0'),
            'Hold for 3rd': ('🥉 3rd', '#CD7F32'),
            'Hold to Qualify': ('✅ Qualify', '#28a745'),
            'Min to Qualify': ('⚠️ Min', '#ffc107')
        }
        
        for key, value in qualification_info.items():
            if key in threshold_mapping:
                label, color = threshold_mapping[key]
                threshold_items.append(f'<span style="color: {color}; font-weight: bold;">{label}: {value}</span>')
        
        if threshold_items:
            st.markdown(f"""
            <div class="threshold-card">
                <h5>🎯 Qualification Thresholds</h5>
                {' | '.join(threshold_items)}
            </div>
            """, unsafe_allow_html=True)


def display_lead_athletes(active_df: pd.DataFrame, qualification_info: Dict[str, str]):
    """Display lead competition athletes with enhanced formatting"""
    # Sort by rank if available
    try:
        if 'Current Rank' in active_df.columns:
            active_df['Current Rank'] = pd.to_numeric(active_df['Current Rank'], errors='coerce')
            active_df = active_df.sort_values('Current Rank', ascending=True).reset_index(drop=True)
    except Exception as e:
        logger.warning(f"Could not sort by rank: {e}")
    
    # Display athlete cards
    for _, row in active_df.iterrows():
        name = DataProcessor.clean_text(str(row.get('Name', 'Unknown')))
        score = row.get('Manual Score', 'N/A')
        rank = row.get('Current Rank', 'N/A')
        status = DataProcessor.clean_text(str(row.get('Status', 'Unknown')))
        worst_finish = row.get('Worst Finish', 'N/A')
        
        # Determine if athlete has a score
        has_score = score not in ['N/A', '', None] and not pd.isna(score)
        
        # Create threshold display for athletes without scores
        threshold_display = create_threshold_display(has_score, qualification_info)
        
        # Determine card styling
        card_class, status_emoji = determine_lead_athlete_status(status, has_score)
        
        # Set position emoji
        position_emoji = get_lead_position_emoji(rank, has_score, card_class, status_emoji)
        
        # Format displays
        score_display = score if has_score else "Awaiting Result"
        worst_finish_display = format_worst_finish(worst_finish, has_score)
        
        # Create athlete card
        st.markdown(f"""
        <div class="athlete-row {card_class}">
            <strong>{position_emoji} #{rank} - {name}</strong><br>
            <small>Score: {score_display} | Status: {status}{worst_finish_display}</small>{threshold_display}
        </div>
        """, unsafe_allow_html=True)


def create_threshold_display(has_score: bool, qualification_info: Dict[str, str]) -> str:
    """Create threshold display for athletes without scores"""
    if has_score or not qualification_info:
        return ""
    
    thresholds = []
    for key, value in qualification_info.items():
        if key == 'Hold for 1st':
            thresholds.append(f'🥇 1st: {value}')
        elif key == 'Hold for 2nd':
            thresholds.append(f'🥈 2nd: {value}')
        elif key == 'Hold for 3rd':
            thresholds.append(f'🥉 3rd: {value}')
        elif key in ['Hold to Qualify', 'Min to Qualify']:
            thresholds.append(f'🎯 Target: {value}')
    
    if thresholds:
        return f"<br><div class='targets'><strong>Targets:</strong> {' | '.join(thresholds)}</div>"
    return ""


def determine_lead_athlete_status(status: str, has_score: bool) -> Tuple[str, str]:
    """Determine lead athlete status and styling"""
    if not has_score:
        return "", "📄"
    
    if "Qualified" in status or "✓✓" in status:
        return "qualified", "✅"
    elif "Eliminated" in status or "✗" in status:
        return "eliminated", "❌"
    elif "Podium" in status and "No Podium" not in status and "Contention" not in status:
        return "podium-position", "🏆"
    elif "Podium Contention" in status or "Contention" in status:
        return "podium-contention", "⚠️"
    elif "No Podium" in status:
        return "no-podium", "❌"
    else:
        return "", "📄"


def get_lead_position_emoji(rank: any, has_score: bool, card_class: str, status_emoji: str) -> str:
    """Get position emoji for lead athletes"""
    rank_num = DataProcessor.safe_numeric_conversion(rank)
    if rank_num > 0:
        return status_emoji if has_score and card_class else f"#{rank_num}"
    return "📄"


def format_worst_finish(worst_finish: any, has_score: bool) -> str:
    """Format worst finish display"""
    if not has_score or worst_finish in ['N/A', '', None] or pd.isna(worst_finish):
        return ""
    
    worst_finish_clean = DataProcessor.clean_text(str(worst_finish))
    return f" | Worst Finish: {worst_finish_clean}" if worst_finish_clean and worst_finish_clean != '-' else ""


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"🚫 Application Error: {e}")
        st.markdown("Please refresh the page or contact support if the issue persists.")
        
        with st.expander("🔧 Debug Information"):
            st.code(f"Error: {e}")
            st.code(f"Time: {datetime.now()}")
            import traceback
            st.code(traceback.format_exc()), na=False)) &  # Remove pure numbers
            (~df['Name'].astype(str).str.match(r'^\d+\+


def is_placeholder_athlete(name: str) -> bool:
    """Check if name is a placeholder like 'Athlete 1', 'Athlete 23', etc."""
    name_str = str(name).strip()
    if name_str.startswith('Athlete '):
        remaining = name_str[8:].strip()
        return remaining.isdigit()
    return False


def display_qualification_thresholds(qualification_info: Dict[str, str]):
    """Display qualification thresholds if available"""
    if qualification_info:
        threshold_items = []
        threshold_mapping = {
            'Hold for 1st': ('🥇 1st', '#FFD700'),
            'Hold for 2nd': ('🥈 2nd', '#C0C0C0'),
            'Hold for 3rd': ('🥉 3rd', '#CD7F32'),
            'Hold to Qualify': ('✅ Qualify', '#28a745'),
            'Min to Qualify': ('⚠️ Min', '#ffc107')
        }
        
        for key, value in qualification_info.items():
            if key in threshold_mapping:
                label, color = threshold_mapping[key]
                threshold_items.append(f'<span style="color: {color}; font-weight: bold;">{label}: {value}</span>')
        
        if threshold_items:
            st.markdown(f"""
            <div class="threshold-card">
                <h5>🎯 Qualification Thresholds</h5>
                {' | '.join(threshold_items)}
            </div>
            """, unsafe_allow_html=True)


def display_lead_athletes(active_df: pd.DataFrame, qualification_info: Dict[str, str]):
    """Display lead competition athletes with enhanced formatting"""
    # Sort by rank if available
    try:
        if 'Current Rank' in active_df.columns:
            active_df['Current Rank'] = pd.to_numeric(active_df['Current Rank'], errors='coerce')
            active_df = active_df.sort_values('Current Rank', ascending=True).reset_index(drop=True)
    except Exception as e:
        logger.warning(f"Could not sort by rank: {e}")
    
    # Display athlete cards
    for _, row in active_df.iterrows():
        name = DataProcessor.clean_text(str(row.get('Name', 'Unknown')))
        score = row.get('Manual Score', 'N/A')
        rank = row.get('Current Rank', 'N/A')
        status = DataProcessor.clean_text(str(row.get('Status', 'Unknown')))
        worst_finish = row.get('Worst Finish', 'N/A')
        
        # Determine if athlete has a score
        has_score = score not in ['N/A', '', None] and not pd.isna(score)
        
        # Create threshold display for athletes without scores
        threshold_display = create_threshold_display(has_score, qualification_info)
        
        # Determine card styling
        card_class, status_emoji = determine_lead_athlete_status(status, has_score)
        
        # Set position emoji
        position_emoji = get_lead_position_emoji(rank, has_score, card_class, status_emoji)
        
        # Format displays
        score_display = score if has_score else "Awaiting Result"
        worst_finish_display = format_worst_finish(worst_finish, has_score)
        
        # Create athlete card
        st.markdown(f"""
        <div class="athlete-row {card_class}">
            <strong>{position_emoji} #{rank} - {name}</strong><br>
            <small>Score: {score_display} | Status: {status}{worst_finish_display}</small>{threshold_display}
        </div>
        """, unsafe_allow_html=True)


def create_threshold_display(has_score: bool, qualification_info: Dict[str, str]) -> str:
    """Create threshold display for athletes without scores"""
    if has_score or not qualification_info:
        return ""
    
    thresholds = []
    for key, value in qualification_info.items():
        if key == 'Hold for 1st':
            thresholds.append(f'🥇 1st: {value}')
        elif key == 'Hold for 2nd':
            thresholds.append(f'🥈 2nd: {value}')
        elif key == 'Hold for 3rd':
            thresholds.append(f'🥉 3rd: {value}')
        elif key in ['Hold to Qualify', 'Min to Qualify']:
            thresholds.append(f'🎯 Target: {value}')
    
    if thresholds:
        return f"<br><div class='targets'><strong>Targets:</strong> {' | '.join(thresholds)}</div>"
    return ""


def determine_lead_athlete_status(status: str, has_score: bool) -> Tuple[str, str]:
    """Determine lead athlete status and styling"""
    if not has_score:
        return "", "📄"
    
    if "Qualified" in status or "✓✓" in status:
        return "qualified", "✅"
    elif "Eliminated" in status or "✗" in status:
        return "eliminated", "❌"
    elif "Podium" in status and "No Podium" not in status and "Contention" not in status:
        return "podium-position", "🏆"
    elif "Podium Contention" in status or "Contention" in status:
        return "podium-contention", "⚠️"
    elif "No Podium" in status:
        return "no-podium", "❌"
    else:
        return "", "📄"


def get_lead_position_emoji(rank: any, has_score: bool, card_class: str, status_emoji: str) -> str:
    """Get position emoji for lead athletes"""
    rank_num = DataProcessor.safe_numeric_conversion(rank)
    if rank_num > 0:
        return status_emoji if has_score and card_class else f"#{rank_num}"
    return "📄"


def format_worst_finish(worst_finish: any, has_score: bool) -> str:
    """Format worst finish display"""
    if not has_score or worst_finish in ['N/A', '', None] or pd.isna(worst_finish):
        return ""
    
    worst_finish_clean = DataProcessor.clean_text(str(worst_finish))
    return f" | Worst Finish: {worst_finish_clean}" if worst_finish_clean and worst_finish_clean != '-' else ""


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"🚫 Application Error: {e}")
        st.markdown("Please refresh the page or contact support if the issue persists.")
        
        with st.expander("🔧 Debug Information"):
            st.code(f"Error: {e}")
            st.code(f"Time: {datetime.now()}")
            import traceback
            st.code(traceback.format_exc()), na=False)) &      # Remove "25+" style entries
            (~df['Name'].apply(is_placeholder_athlete))
        ]
        
        # Second pass: If we have rank information, use it to filter properly
        if 'Current Rank' in filtered_df.columns:
            filtered_df['temp_rank'] = pd.to_numeric(filtered_df['Current Rank'], errors='coerce')
            
            # Keep only rows with valid ranks within expected range
            ranked_df = filtered_df[
                (filtered_df['temp_rank'].notna()) & 
                (filtered_df['temp_rank'] >= 1) & 
                (filtered_df['temp_rank'] <= expected_max)
            ]
            
            if len(ranked_df) > 0:
                # Sort by rank and take only the expected number
                ranked_df = ranked_df.sort_values('temp_rank').head(expected_max)
                filtered_df = ranked_df.drop('temp_rank', axis=1)
            else:
                # If no valid ranks, fall back to manual filtering
                filtered_df = manual_athlete_filter(filtered_df, expected_max)
        else:
            # No rank column available, use manual filtering
            filtered_df = manual_athlete_filter(filtered_df, expected_max)
        
        # Third pass: Additional validation for lead competitions
        if "Lead" in competition_name:
            filtered_df = validate_lead_athletes(filtered_df, expected_max)
        
        logger.info(f"Filtered to {len(filtered_df)} athletes for {competition_name} (expected: {expected_max})")
        return filtered_df
        
    except Exception as e:
        logger.error(f"Error filtering athletes for {competition_name}: {e}")
        # Fallback to basic filtering with count limit
        basic_filtered = df[
            df['Name'].notna() & 
            (df['Name'] != '') &
            (~df['Name'].astype(str).str.contains('Hold for', na=False))
        ].head(expected_max)
        return basic_filtered


def manual_athlete_filter(df: pd.DataFrame, expected_max: int) -> pd.DataFrame:
    """Manually filter athletes when rank information is not reliable"""
    # Look for patterns that indicate real athlete names vs reference data
    potential_athletes = []
    
    for idx, row in df.iterrows():
        name = str(row.get('Name', '')).strip()
        
        # Skip if name looks like reference data
        if any(keyword in name.lower() for keyword in [
            'hold', 'min', 'max', 'qualification', 'threshold', 'zone', 'top',
            'points', 'score', 'rank', 'position', 'place', 'finish'
        ]):
            continue
        
        # Skip if name is too short or looks like a number/code
        if len(name) < 3 or name.isdigit() or not any(c.isalpha() for c in name):
            continue
        
        # Look for typical athlete name patterns (First Last or similar)
        name_parts = name.split()
        if len(name_parts) >= 2 and all(part.isalpha() or part.replace('.', '').isalpha() for part in name_parts):
            potential_athletes.append(idx)
        elif len(name_parts) == 1 and len(name) > 4 and name.isalpha():
            # Single names that are long enough and all letters
            potential_athletes.append(idx)
    
    # Return the filtered dataframe, limited to expected count
    return df.loc[potential_athletes[:expected_max]]


def validate_lead_athletes(df: pd.DataFrame, expected_max: int) -> pd.DataFrame:
    """Additional validation specifically for lead competitions"""
    if len(df) <= expected_max:
        return df
    
    # For lead competitions, prioritize athletes with actual climbing data
    scored_athletes = df[df['Manual Score'].notna() & (df['Manual Score'] != '')].copy()
    unscored_athletes = df[df['Manual Score'].isna() | (df['Manual Score'] == '')].copy()
    
    # Combine scored athletes first, then fill with unscored up to limit
    result_df = scored_athletes.copy()
    remaining_slots = expected_max - len(scored_athletes)
    
    if remaining_slots > 0 and len(unscored_athletes) > 0:
        result_df = pd.concat([result_df, unscored_athletes.head(remaining_slots)], ignore_index=True)
    
    return result_df.head(expected_max)


def is_placeholder_athlete(name: str) -> bool:
    """Check if name is a placeholder like 'Athlete 1', 'Athlete 23', etc."""
    name_str = str(name).strip()
    if name_str.startswith('Athlete '):
        remaining = name_str[8:].strip()
        return remaining.isdigit()
    return False


def display_qualification_thresholds(qualification_info: Dict[str, str]):
    """Display qualification thresholds if available"""
    if qualification_info:
        threshold_items = []
        threshold_mapping = {
            'Hold for 1st': ('🥇 1st', '#FFD700'),
            'Hold for 2nd': ('🥈 2nd', '#C0C0C0'),
            'Hold for 3rd': ('🥉 3rd', '#CD7F32'),
            'Hold to Qualify': ('✅ Qualify', '#28a745'),
            'Min to Qualify': ('⚠️ Min', '#ffc107')
        }
        
        for key, value in qualification_info.items():
            if key in threshold_mapping:
                label, color = threshold_mapping[key]
                threshold_items.append(f'<span style="color: {color}; font-weight: bold;">{label}: {value}</span>')
        
        if threshold_items:
            st.markdown(f"""
            <div class="threshold-card">
                <h5>🎯 Qualification Thresholds</h5>
                {' | '.join(threshold_items)}
            </div>
            """, unsafe_allow_html=True)


def display_lead_athletes(active_df: pd.DataFrame, qualification_info: Dict[str, str]):
    """Display lead competition athletes with enhanced formatting"""
    # Sort by rank if available
    try:
        if 'Current Rank' in active_df.columns:
            active_df['Current Rank'] = pd.to_numeric(active_df['Current Rank'], errors='coerce')
            active_df = active_df.sort_values('Current Rank', ascending=True).reset_index(drop=True)
    except Exception as e:
        logger.warning(f"Could not sort by rank: {e}")
    
    # Display athlete cards
    for _, row in active_df.iterrows():
        name = DataProcessor.clean_text(str(row.get('Name', 'Unknown')))
        score = row.get('Manual Score', 'N/A')
        rank = row.get('Current Rank', 'N/A')
        status = DataProcessor.clean_text(str(row.get('Status', 'Unknown')))
        worst_finish = row.get('Worst Finish', 'N/A')
        
        # Determine if athlete has a score
        has_score = score not in ['N/A', '', None] and not pd.isna(score)
        
        # Create threshold display for athletes without scores
        threshold_display = create_threshold_display(has_score, qualification_info)
        
        # Determine card styling
        card_class, status_emoji = determine_lead_athlete_status(status, has_score)
        
        # Set position emoji
        position_emoji = get_lead_position_emoji(rank, has_score, card_class, status_emoji)
        
        # Format displays
        score_display = score if has_score else "Awaiting Result"
        worst_finish_display = format_worst_finish(worst_finish, has_score)
        
        # Create athlete card
        st.markdown(f"""
        <div class="athlete-row {card_class}">
            <strong>{position_emoji} #{rank} - {name}</strong><br>
            <small>Score: {score_display} | Status: {status}{worst_finish_display}</small>{threshold_display}
        </div>
        """, unsafe_allow_html=True)


def create_threshold_display(has_score: bool, qualification_info: Dict[str, str]) -> str:
    """Create threshold display for athletes without scores"""
    if has_score or not qualification_info:
        return ""
    
    thresholds = []
    for key, value in qualification_info.items():
        if key == 'Hold for 1st':
            thresholds.append(f'🥇 1st: {value}')
        elif key == 'Hold for 2nd':
            thresholds.append(f'🥈 2nd: {value}')
        elif key == 'Hold for 3rd':
            thresholds.append(f'🥉 3rd: {value}')
        elif key in ['Hold to Qualify', 'Min to Qualify']:
            thresholds.append(f'🎯 Target: {value}')
    
    if thresholds:
        return f"<br><div class='targets'><strong>Targets:</strong> {' | '.join(thresholds)}</div>"
    return ""


def determine_lead_athlete_status(status: str, has_score: bool) -> Tuple[str, str]:
    """Determine lead athlete status and styling"""
    if not has_score:
        return "", "📄"
    
    if "Qualified" in status or "✓✓" in status:
        return "qualified", "✅"
    elif "Eliminated" in status or "✗" in status:
        return "eliminated", "❌"
    elif "Podium" in status and "No Podium" not in status and "Contention" not in status:
        return "podium-position", "🏆"
    elif "Podium Contention" in status or "Contention" in status:
        return "podium-contention", "⚠️"
    elif "No Podium" in status:
        return "no-podium", "❌"
    else:
        return "", "📄"


def get_lead_position_emoji(rank: any, has_score: bool, card_class: str, status_emoji: str) -> str:
    """Get position emoji for lead athletes"""
    rank_num = DataProcessor.safe_numeric_conversion(rank)
    if rank_num > 0:
        return status_emoji if has_score and card_class else f"#{rank_num}"
    return "📄"


def format_worst_finish(worst_finish: any, has_score: bool) -> str:
    """Format worst finish display"""
    if not has_score or worst_finish in ['N/A', '', None] or pd.isna(worst_finish):
        return ""
    
    worst_finish_clean = DataProcessor.clean_text(str(worst_finish))
    return f" | Worst Finish: {worst_finish_clean}" if worst_finish_clean and worst_finish_clean != '-' else ""


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"🚫 Application Error: {e}")
        st.markdown("Please refresh the page or contact support if the issue persists.")
        
        with st.expander("🔧 Debug Information"):
            st.code(f"Error: {e}")
            st.code(f"Time: {datetime.now()}")
            import traceback
            st.code(traceback.format_exc()),        # "Competitor 1"
        r'^\d+


def display_qualification_thresholds(qualification_info: Dict[str, str]):
    """Display qualification thresholds if available"""
    if qualification_info:
        threshold_items = []
        threshold_mapping = {
            'Hold for 1st': ('🥇 1st', '#FFD700'),
            'Hold for 2nd': ('🥈 2nd', '#C0C0C0'),
            'Hold for 3rd': ('🥉 3rd', '#CD7F32'),
            'Hold to Qualify': ('✅ Qualify', '#28a745'),
            'Min to Qualify': ('⚠️ Min', '#ffc107')
        }
        
        for key, value in qualification_info.items():
            if key in threshold_mapping:
                label, color = threshold_mapping[key]
                threshold_items.append(f'<span style="color: {color}; font-weight: bold;">{label}: {value}</span>')
        
        if threshold_items:
            st.markdown(f"""
            <div class="threshold-card">
                <h5>🎯 Qualification Thresholds</h5>
                {' | '.join(threshold_items)}
            </div>
            """, unsafe_allow_html=True)


def display_lead_athletes(active_df: pd.DataFrame, qualification_info: Dict[str, str]):
    """Display lead competition athletes with enhanced formatting"""
    # Sort by rank if available
    try:
        if 'Current Rank' in active_df.columns:
            active_df['Current Rank'] = pd.to_numeric(active_df['Current Rank'], errors='coerce')
            active_df = active_df.sort_values('Current Rank', ascending=True).reset_index(drop=True)
    except Exception as e:
        logger.warning(f"Could not sort by rank: {e}")
    
    # Display athlete cards
    for _, row in active_df.iterrows():
        name = DataProcessor.clean_text(str(row.get('Name', 'Unknown')))
        score = row.get('Manual Score', 'N/A')
        rank = row.get('Current Rank', 'N/A')
        status = DataProcessor.clean_text(str(row.get('Status', 'Unknown')))
        worst_finish = row.get('Worst Finish', 'N/A')
        
        # Determine if athlete has a score
        has_score = score not in ['N/A', '', None] and not pd.isna(score)
        
        # Create threshold display for athletes without scores
        threshold_display = create_threshold_display(has_score, qualification_info)
        
        # Determine card styling
        card_class, status_emoji = determine_lead_athlete_status(status, has_score)
        
        # Set position emoji
        position_emoji = get_lead_position_emoji(rank, has_score, card_class, status_emoji)
        
        # Format displays
        score_display = score if has_score else "Awaiting Result"
        worst_finish_display = format_worst_finish(worst_finish, has_score)
        
        # Create athlete card
        st.markdown(f"""
        <div class="athlete-row {card_class}">
            <strong>{position_emoji} #{rank} - {name}</strong><br>
            <small>Score: {score_display} | Status: {status}{worst_finish_display}</small>{threshold_display}
        </div>
        """, unsafe_allow_html=True)


def create_threshold_display(has_score: bool, qualification_info: Dict[str, str]) -> str:
    """Create threshold display for athletes without scores"""
    if has_score or not qualification_info:
        return ""
    
    thresholds = []
    for key, value in qualification_info.items():
        if key == 'Hold for 1st':
            thresholds.append(f'🥇 1st: {value}')
        elif key == 'Hold for 2nd':
            thresholds.append(f'🥈 2nd: {value}')
        elif key == 'Hold for 3rd':
            thresholds.append(f'🥉 3rd: {value}')
        elif key in ['Hold to Qualify', 'Min to Qualify']:
            thresholds.append(f'🎯 Target: {value}')
    
    if thresholds:
        return f"<br><div class='targets'><strong>Targets:</strong> {' | '.join(thresholds)}</div>"
    return ""


def determine_lead_athlete_status(status: str, has_score: bool) -> Tuple[str, str]:
    """Determine lead athlete status and styling"""
    if not has_score:
        return "", "📄"
    
    if "Qualified" in status or "✓✓" in status:
        return "qualified", "✅"
    elif "Eliminated" in status or "✗" in status:
        return "eliminated", "❌"
    elif "Podium" in status and "No Podium" not in status and "Contention" not in status:
        return "podium-position", "🏆"
    elif "Podium Contention" in status or "Contention" in status:
        return "podium-contention", "⚠️"
    elif "No Podium" in status:
        return "no-podium", "❌"
    else:
        return "", "📄"


def get_lead_position_emoji(rank: any, has_score: bool, card_class: str, status_emoji: str) -> str:
    """Get position emoji for lead athletes"""
    rank_num = DataProcessor.safe_numeric_conversion(rank)
    if rank_num > 0:
        return status_emoji if has_score and card_class else f"#{rank_num}"
    return "📄"


def format_worst_finish(worst_finish: any, has_score: bool) -> str:
    """Format worst finish display"""
    if not has_score or worst_finish in ['N/A', '', None] or pd.isna(worst_finish):
        return ""
    
    worst_finish_clean = DataProcessor.clean_text(str(worst_finish))
    return f" | Worst Finish: {worst_finish_clean}" if worst_finish_clean and worst_finish_clean != '-' else ""


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"🚫 Application Error: {e}")
        st.markdown("Please refresh the page or contact support if the issue persists.")
        
        with st.expander("🔧 Debug Information"):
            st.code(f"Error: {e}")
            st.code(f"Time: {datetime.now()}")
            import traceback
            st.code(traceback.format_exc()), na=False)) &  # Remove pure numbers
            (~df['Name'].astype(str).str.match(r'^\d+\+


def is_placeholder_athlete(name: str) -> bool:
    """Check if name is a placeholder like 'Athlete 1', 'Athlete 23', etc."""
    name_str = str(name).strip()
    if name_str.startswith('Athlete '):
        remaining = name_str[8:].strip()
        return remaining.isdigit()
    return False


def display_qualification_thresholds(qualification_info: Dict[str, str]):
    """Display qualification thresholds if available"""
    if qualification_info:
        threshold_items = []
        threshold_mapping = {
            'Hold for 1st': ('🥇 1st', '#FFD700'),
            'Hold for 2nd': ('🥈 2nd', '#C0C0C0'),
            'Hold for 3rd': ('🥉 3rd', '#CD7F32'),
            'Hold to Qualify': ('✅ Qualify', '#28a745'),
            'Min to Qualify': ('⚠️ Min', '#ffc107')
        }
        
        for key, value in qualification_info.items():
            if key in threshold_mapping:
                label, color = threshold_mapping[key]
                threshold_items.append(f'<span style="color: {color}; font-weight: bold;">{label}: {value}</span>')
        
        if threshold_items:
            st.markdown(f"""
            <div class="threshold-card">
                <h5>🎯 Qualification Thresholds</h5>
                {' | '.join(threshold_items)}
            </div>
            """, unsafe_allow_html=True)


def display_lead_athletes(active_df: pd.DataFrame, qualification_info: Dict[str, str]):
    """Display lead competition athletes with enhanced formatting"""
    # Sort by rank if available
    try:
        if 'Current Rank' in active_df.columns:
            active_df['Current Rank'] = pd.to_numeric(active_df['Current Rank'], errors='coerce')
            active_df = active_df.sort_values('Current Rank', ascending=True).reset_index(drop=True)
    except Exception as e:
        logger.warning(f"Could not sort by rank: {e}")
    
    # Display athlete cards
    for _, row in active_df.iterrows():
        name = DataProcessor.clean_text(str(row.get('Name', 'Unknown')))
        score = row.get('Manual Score', 'N/A')
        rank = row.get('Current Rank', 'N/A')
        status = DataProcessor.clean_text(str(row.get('Status', 'Unknown')))
        worst_finish = row.get('Worst Finish', 'N/A')
        
        # Determine if athlete has a score
        has_score = score not in ['N/A', '', None] and not pd.isna(score)
        
        # Create threshold display for athletes without scores
        threshold_display = create_threshold_display(has_score, qualification_info)
        
        # Determine card styling
        card_class, status_emoji = determine_lead_athlete_status(status, has_score)
        
        # Set position emoji
        position_emoji = get_lead_position_emoji(rank, has_score, card_class, status_emoji)
        
        # Format displays
        score_display = score if has_score else "Awaiting Result"
        worst_finish_display = format_worst_finish(worst_finish, has_score)
        
        # Create athlete card
        st.markdown(f"""
        <div class="athlete-row {card_class}">
            <strong>{position_emoji} #{rank} - {name}</strong><br>
            <small>Score: {score_display} | Status: {status}{worst_finish_display}</small>{threshold_display}
        </div>
        """, unsafe_allow_html=True)


def create_threshold_display(has_score: bool, qualification_info: Dict[str, str]) -> str:
    """Create threshold display for athletes without scores"""
    if has_score or not qualification_info:
        return ""
    
    thresholds = []
    for key, value in qualification_info.items():
        if key == 'Hold for 1st':
            thresholds.append(f'🥇 1st: {value}')
        elif key == 'Hold for 2nd':
            thresholds.append(f'🥈 2nd: {value}')
        elif key == 'Hold for 3rd':
            thresholds.append(f'🥉 3rd: {value}')
        elif key in ['Hold to Qualify', 'Min to Qualify']:
            thresholds.append(f'🎯 Target: {value}')
    
    if thresholds:
        return f"<br><div class='targets'><strong>Targets:</strong> {' | '.join(thresholds)}</div>"
    return ""


def determine_lead_athlete_status(status: str, has_score: bool) -> Tuple[str, str]:
    """Determine lead athlete status and styling"""
    if not has_score:
        return "", "📄"
    
    if "Qualified" in status or "✓✓" in status:
        return "qualified", "✅"
    elif "Eliminated" in status or "✗" in status:
        return "eliminated", "❌"
    elif "Podium" in status and "No Podium" not in status and "Contention" not in status:
        return "podium-position", "🏆"
    elif "Podium Contention" in status or "Contention" in status:
        return "podium-contention", "⚠️"
    elif "No Podium" in status:
        return "no-podium", "❌"
    else:
        return "", "📄"


def get_lead_position_emoji(rank: any, has_score: bool, card_class: str, status_emoji: str) -> str:
    """Get position emoji for lead athletes"""
    rank_num = DataProcessor.safe_numeric_conversion(rank)
    if rank_num > 0:
        return status_emoji if has_score and card_class else f"#{rank_num}"
    return "📄"


def format_worst_finish(worst_finish: any, has_score: bool) -> str:
    """Format worst finish display"""
    if not has_score or worst_finish in ['N/A', '', None] or pd.isna(worst_finish):
        return ""
    
    worst_finish_clean = DataProcessor.clean_text(str(worst_finish))
    return f" | Worst Finish: {worst_finish_clean}" if worst_finish_clean and worst_finish_clean != '-' else ""


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"🚫 Application Error: {e}")
        st.markdown("Please refresh the page or contact support if the issue persists.")
        
        with st.expander("🔧 Debug Information"):
            st.code(f"Error: {e}")
            st.code(f"Time: {datetime.now()}")
            import traceback
            st.code(traceback.format_exc()), na=False)) &      # Remove "25+" style entries
            (~df['Name'].apply(is_placeholder_athlete))
        ]
        
        # Second pass: If we have rank information, use it to filter properly
        if 'Current Rank' in filtered_df.columns:
            filtered_df['temp_rank'] = pd.to_numeric(filtered_df['Current Rank'], errors='coerce')
            
            # Keep only rows with valid ranks within expected range
            ranked_df = filtered_df[
                (filtered_df['temp_rank'].notna()) & 
                (filtered_df['temp_rank'] >= 1) & 
                (filtered_df['temp_rank'] <= expected_max)
            ]
            
            if len(ranked_df) > 0:
                # Sort by rank and take only the expected number
                ranked_df = ranked_df.sort_values('temp_rank').head(expected_max)
                filtered_df = ranked_df.drop('temp_rank', axis=1)
            else:
                # If no valid ranks, fall back to manual filtering
                filtered_df = manual_athlete_filter(filtered_df, expected_max)
        else:
            # No rank column available, use manual filtering
            filtered_df = manual_athlete_filter(filtered_df, expected_max)
        
        # Third pass: Additional validation for lead competitions
        if "Lead" in competition_name:
            filtered_df = validate_lead_athletes(filtered_df, expected_max)
        
        logger.info(f"Filtered to {len(filtered_df)} athletes for {competition_name} (expected: {expected_max})")
        return filtered_df
        
    except Exception as e:
        logger.error(f"Error filtering athletes for {competition_name}: {e}")
        # Fallback to basic filtering with count limit
        basic_filtered = df[
            df['Name'].notna() & 
            (df['Name'] != '') &
            (~df['Name'].astype(str).str.contains('Hold for', na=False))
        ].head(expected_max)
        return basic_filtered


def manual_athlete_filter(df: pd.DataFrame, expected_max: int) -> pd.DataFrame:
    """Manually filter athletes when rank information is not reliable"""
    # Look for patterns that indicate real athlete names vs reference data
    potential_athletes = []
    
    for idx, row in df.iterrows():
        name = str(row.get('Name', '')).strip()
        
        # Skip if name looks like reference data
        if any(keyword in name.lower() for keyword in [
            'hold', 'min', 'max', 'qualification', 'threshold', 'zone', 'top',
            'points', 'score', 'rank', 'position', 'place', 'finish'
        ]):
            continue
        
        # Skip if name is too short or looks like a number/code
        if len(name) < 3 or name.isdigit() or not any(c.isalpha() for c in name):
            continue
        
        # Look for typical athlete name patterns (First Last or similar)
        name_parts = name.split()
        if len(name_parts) >= 2 and all(part.isalpha() or part.replace('.', '').isalpha() for part in name_parts):
            potential_athletes.append(idx)
        elif len(name_parts) == 1 and len(name) > 4 and name.isalpha():
            # Single names that are long enough and all letters
            potential_athletes.append(idx)
    
    # Return the filtered dataframe, limited to expected count
    return df.loc[potential_athletes[:expected_max]]


def validate_lead_athletes(df: pd.DataFrame, expected_max: int) -> pd.DataFrame:
    """Additional validation specifically for lead competitions"""
    if len(df) <= expected_max:
        return df
    
    # For lead competitions, prioritize athletes with actual climbing data
    scored_athletes = df[df['Manual Score'].notna() & (df['Manual Score'] != '')].copy()
    unscored_athletes = df[df['Manual Score'].isna() | (df['Manual Score'] == '')].copy()
    
    # Combine scored athletes first, then fill with unscored up to limit
    result_df = scored_athletes.copy()
    remaining_slots = expected_max - len(scored_athletes)
    
    if remaining_slots > 0 and len(unscored_athletes) > 0:
        result_df = pd.concat([result_df, unscored_athletes.head(remaining_slots)], ignore_index=True)
    
    return result_df.head(expected_max)


def is_placeholder_athlete(name: str) -> bool:
    """Check if name is a placeholder like 'Athlete 1', 'Athlete 23', etc."""
    name_str = str(name).strip()
    if name_str.startswith('Athlete '):
        remaining = name_str[8:].strip()
        return remaining.isdigit()
    return False


def display_qualification_thresholds(qualification_info: Dict[str, str]):
    """Display qualification thresholds if available"""
    if qualification_info:
        threshold_items = []
        threshold_mapping = {
            'Hold for 1st': ('🥇 1st', '#FFD700'),
            'Hold for 2nd': ('🥈 2nd', '#C0C0C0'),
            'Hold for 3rd': ('🥉 3rd', '#CD7F32'),
            'Hold to Qualify': ('✅ Qualify', '#28a745'),
            'Min to Qualify': ('⚠️ Min', '#ffc107')
        }
        
        for key, value in qualification_info.items():
            if key in threshold_mapping:
                label, color = threshold_mapping[key]
                threshold_items.append(f'<span style="color: {color}; font-weight: bold;">{label}: {value}</span>')
        
        if threshold_items:
            st.markdown(f"""
            <div class="threshold-card">
                <h5>🎯 Qualification Thresholds</h5>
                {' | '.join(threshold_items)}
            </div>
            """, unsafe_allow_html=True)


def display_lead_athletes(active_df: pd.DataFrame, qualification_info: Dict[str, str]):
    """Display lead competition athletes with enhanced formatting"""
    # Sort by rank if available
    try:
        if 'Current Rank' in active_df.columns:
            active_df['Current Rank'] = pd.to_numeric(active_df['Current Rank'], errors='coerce')
            active_df = active_df.sort_values('Current Rank', ascending=True).reset_index(drop=True)
    except Exception as e:
        logger.warning(f"Could not sort by rank: {e}")
    
    # Display athlete cards
    for _, row in active_df.iterrows():
        name = DataProcessor.clean_text(str(row.get('Name', 'Unknown')))
        score = row.get('Manual Score', 'N/A')
        rank = row.get('Current Rank', 'N/A')
        status = DataProcessor.clean_text(str(row.get('Status', 'Unknown')))
        worst_finish = row.get('Worst Finish', 'N/A')
        
        # Determine if athlete has a score
        has_score = score not in ['N/A', '', None] and not pd.isna(score)
        
        # Create threshold display for athletes without scores
        threshold_display = create_threshold_display(has_score, qualification_info)
        
        # Determine card styling
        card_class, status_emoji = determine_lead_athlete_status(status, has_score)
        
        # Set position emoji
        position_emoji = get_lead_position_emoji(rank, has_score, card_class, status_emoji)
        
        # Format displays
        score_display = score if has_score else "Awaiting Result"
        worst_finish_display = format_worst_finish(worst_finish, has_score)
        
        # Create athlete card
        st.markdown(f"""
        <div class="athlete-row {card_class}">
            <strong>{position_emoji} #{rank} - {name}</strong><br>
            <small>Score: {score_display} | Status: {status}{worst_finish_display}</small>{threshold_display}
        </div>
        """, unsafe_allow_html=True)


def create_threshold_display(has_score: bool, qualification_info: Dict[str, str]) -> str:
    """Create threshold display for athletes without scores"""
    if has_score or not qualification_info:
        return ""
    
    thresholds = []
    for key, value in qualification_info.items():
        if key == 'Hold for 1st':
            thresholds.append(f'🥇 1st: {value}')
        elif key == 'Hold for 2nd':
            thresholds.append(f'🥈 2nd: {value}')
        elif key == 'Hold for 3rd':
            thresholds.append(f'🥉 3rd: {value}')
        elif key in ['Hold to Qualify', 'Min to Qualify']:
            thresholds.append(f'🎯 Target: {value}')
    
    if thresholds:
        return f"<br><div class='targets'><strong>Targets:</strong> {' | '.join(thresholds)}</div>"
    return ""


def determine_lead_athlete_status(status: str, has_score: bool) -> Tuple[str, str]:
    """Determine lead athlete status and styling"""
    if not has_score:
        return "", "📄"
    
    if "Qualified" in status or "✓✓" in status:
        return "qualified", "✅"
    elif "Eliminated" in status or "✗" in status:
        return "eliminated", "❌"
    elif "Podium" in status and "No Podium" not in status and "Contention" not in status:
        return "podium-position", "🏆"
    elif "Podium Contention" in status or "Contention" in status:
        return "podium-contention", "⚠️"
    elif "No Podium" in status:
        return "no-podium", "❌"
    else:
        return "", "📄"


def get_lead_position_emoji(rank: any, has_score: bool, card_class: str, status_emoji: str) -> str:
    """Get position emoji for lead athletes"""
    rank_num = DataProcessor.safe_numeric_conversion(rank)
    if rank_num > 0:
        return status_emoji if has_score and card_class else f"#{rank_num}"
    return "📄"


def format_worst_finish(worst_finish: any, has_score: bool) -> str:
    """Format worst finish display"""
    if not has_score or worst_finish in ['N/A', '', None] or pd.isna(worst_finish):
        return ""
    
    worst_finish_clean = DataProcessor.clean_text(str(worst_finish))
    return f" | Worst Finish: {worst_finish_clean}" if worst_finish_clean and worst_finish_clean != '-' else ""


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"🚫 Application Error: {e}")
        st.markdown("Please refresh the page or contact support if the issue persists.")
        
        with st.expander("🔧 Debug Information"):
            st.code(f"Error: {e}")
            st.code(f"Time: {datetime.now()}")
            import traceback
            st.code(traceback.format_exc()),                     # Just numbers
        r'^\d+\.\d+


def display_qualification_thresholds(qualification_info: Dict[str, str]):
    """Display qualification thresholds if available"""
    if qualification_info:
        threshold_items = []
        threshold_mapping = {
            'Hold for 1st': ('🥇 1st', '#FFD700'),
            'Hold for 2nd': ('🥈 2nd', '#C0C0C0'),
            'Hold for 3rd': ('🥉 3rd', '#CD7F32'),
            'Hold to Qualify': ('✅ Qualify', '#28a745'),
            'Min to Qualify': ('⚠️ Min', '#ffc107')
        }
        
        for key, value in qualification_info.items():
            if key in threshold_mapping:
                label, color = threshold_mapping[key]
                threshold_items.append(f'<span style="color: {color}; font-weight: bold;">{label}: {value}</span>')
        
        if threshold_items:
            st.markdown(f"""
            <div class="threshold-card">
                <h5>🎯 Qualification Thresholds</h5>
                {' | '.join(threshold_items)}
            </div>
            """, unsafe_allow_html=True)


def display_lead_athletes(active_df: pd.DataFrame, qualification_info: Dict[str, str]):
    """Display lead competition athletes with enhanced formatting"""
    # Sort by rank if available
    try:
        if 'Current Rank' in active_df.columns:
            active_df['Current Rank'] = pd.to_numeric(active_df['Current Rank'], errors='coerce')
            active_df = active_df.sort_values('Current Rank', ascending=True).reset_index(drop=True)
    except Exception as e:
        logger.warning(f"Could not sort by rank: {e}")
    
    # Display athlete cards
    for _, row in active_df.iterrows():
        name = DataProcessor.clean_text(str(row.get('Name', 'Unknown')))
        score = row.get('Manual Score', 'N/A')
        rank = row.get('Current Rank', 'N/A')
        status = DataProcessor.clean_text(str(row.get('Status', 'Unknown')))
        worst_finish = row.get('Worst Finish', 'N/A')
        
        # Determine if athlete has a score
        has_score = score not in ['N/A', '', None] and not pd.isna(score)
        
        # Create threshold display for athletes without scores
        threshold_display = create_threshold_display(has_score, qualification_info)
        
        # Determine card styling
        card_class, status_emoji = determine_lead_athlete_status(status, has_score)
        
        # Set position emoji
        position_emoji = get_lead_position_emoji(rank, has_score, card_class, status_emoji)
        
        # Format displays
        score_display = score if has_score else "Awaiting Result"
        worst_finish_display = format_worst_finish(worst_finish, has_score)
        
        # Create athlete card
        st.markdown(f"""
        <div class="athlete-row {card_class}">
            <strong>{position_emoji} #{rank} - {name}</strong><br>
            <small>Score: {score_display} | Status: {status}{worst_finish_display}</small>{threshold_display}
        </div>
        """, unsafe_allow_html=True)


def create_threshold_display(has_score: bool, qualification_info: Dict[str, str]) -> str:
    """Create threshold display for athletes without scores"""
    if has_score or not qualification_info:
        return ""
    
    thresholds = []
    for key, value in qualification_info.items():
        if key == 'Hold for 1st':
            thresholds.append(f'🥇 1st: {value}')
        elif key == 'Hold for 2nd':
            thresholds.append(f'🥈 2nd: {value}')
        elif key == 'Hold for 3rd':
            thresholds.append(f'🥉 3rd: {value}')
        elif key in ['Hold to Qualify', 'Min to Qualify']:
            thresholds.append(f'🎯 Target: {value}')
    
    if thresholds:
        return f"<br><div class='targets'><strong>Targets:</strong> {' | '.join(thresholds)}</div>"
    return ""


def determine_lead_athlete_status(status: str, has_score: bool) -> Tuple[str, str]:
    """Determine lead athlete status and styling"""
    if not has_score:
        return "", "📄"
    
    if "Qualified" in status or "✓✓" in status:
        return "qualified", "✅"
    elif "Eliminated" in status or "✗" in status:
        return "eliminated", "❌"
    elif "Podium" in status and "No Podium" not in status and "Contention" not in status:
        return "podium-position", "🏆"
    elif "Podium Contention" in status or "Contention" in status:
        return "podium-contention", "⚠️"
    elif "No Podium" in status:
        return "no-podium", "❌"
    else:
        return "", "📄"


def get_lead_position_emoji(rank: any, has_score: bool, card_class: str, status_emoji: str) -> str:
    """Get position emoji for lead athletes"""
    rank_num = DataProcessor.safe_numeric_conversion(rank)
    if rank_num > 0:
        return status_emoji if has_score and card_class else f"#{rank_num}"
    return "📄"


def format_worst_finish(worst_finish: any, has_score: bool) -> str:
    """Format worst finish display"""
    if not has_score or worst_finish in ['N/A', '', None] or pd.isna(worst_finish):
        return ""
    
    worst_finish_clean = DataProcessor.clean_text(str(worst_finish))
    return f" | Worst Finish: {worst_finish_clean}" if worst_finish_clean and worst_finish_clean != '-' else ""


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"🚫 Application Error: {e}")
        st.markdown("Please refresh the page or contact support if the issue persists.")
        
        with st.expander("🔧 Debug Information"):
            st.code(f"Error: {e}")
            st.code(f"Time: {datetime.now()}")
            import traceback
            st.code(traceback.format_exc()), na=False)) &  # Remove pure numbers
            (~df['Name'].astype(str).str.match(r'^\d+\+


def is_placeholder_athlete(name: str) -> bool:
    """Check if name is a placeholder like 'Athlete 1', 'Athlete 23', etc."""
    name_str = str(name).strip()
    if name_str.startswith('Athlete '):
        remaining = name_str[8:].strip()
        return remaining.isdigit()
    return False


def display_qualification_thresholds(qualification_info: Dict[str, str]):
    """Display qualification thresholds if available"""
    if qualification_info:
        threshold_items = []
        threshold_mapping = {
            'Hold for 1st': ('🥇 1st', '#FFD700'),
            'Hold for 2nd': ('🥈 2nd', '#C0C0C0'),
            'Hold for 3rd': ('🥉 3rd', '#CD7F32'),
            'Hold to Qualify': ('✅ Qualify', '#28a745'),
            'Min to Qualify': ('⚠️ Min', '#ffc107')
        }
        
        for key, value in qualification_info.items():
            if key in threshold_mapping:
                label, color = threshold_mapping[key]
                threshold_items.append(f'<span style="color: {color}; font-weight: bold;">{label}: {value}</span>')
        
        if threshold_items:
            st.markdown(f"""
            <div class="threshold-card">
                <h5>🎯 Qualification Thresholds</h5>
                {' | '.join(threshold_items)}
            </div>
            """, unsafe_allow_html=True)


def display_lead_athletes(active_df: pd.DataFrame, qualification_info: Dict[str, str]):
    """Display lead competition athletes with enhanced formatting"""
    # Sort by rank if available
    try:
        if 'Current Rank' in active_df.columns:
            active_df['Current Rank'] = pd.to_numeric(active_df['Current Rank'], errors='coerce')
            active_df = active_df.sort_values('Current Rank', ascending=True).reset_index(drop=True)
    except Exception as e:
        logger.warning(f"Could not sort by rank: {e}")
    
    # Display athlete cards
    for _, row in active_df.iterrows():
        name = DataProcessor.clean_text(str(row.get('Name', 'Unknown')))
        score = row.get('Manual Score', 'N/A')
        rank = row.get('Current Rank', 'N/A')
        status = DataProcessor.clean_text(str(row.get('Status', 'Unknown')))
        worst_finish = row.get('Worst Finish', 'N/A')
        
        # Determine if athlete has a score
        has_score = score not in ['N/A', '', None] and not pd.isna(score)
        
        # Create threshold display for athletes without scores
        threshold_display = create_threshold_display(has_score, qualification_info)
        
        # Determine card styling
        card_class, status_emoji = determine_lead_athlete_status(status, has_score)
        
        # Set position emoji
        position_emoji = get_lead_position_emoji(rank, has_score, card_class, status_emoji)
        
        # Format displays
        score_display = score if has_score else "Awaiting Result"
        worst_finish_display = format_worst_finish(worst_finish, has_score)
        
        # Create athlete card
        st.markdown(f"""
        <div class="athlete-row {card_class}">
            <strong>{position_emoji} #{rank} - {name}</strong><br>
            <small>Score: {score_display} | Status: {status}{worst_finish_display}</small>{threshold_display}
        </div>
        """, unsafe_allow_html=True)


def create_threshold_display(has_score: bool, qualification_info: Dict[str, str]) -> str:
    """Create threshold display for athletes without scores"""
    if has_score or not qualification_info:
        return ""
    
    thresholds = []
    for key, value in qualification_info.items():
        if key == 'Hold for 1st':
            thresholds.append(f'🥇 1st: {value}')
        elif key == 'Hold for 2nd':
            thresholds.append(f'🥈 2nd: {value}')
        elif key == 'Hold for 3rd':
            thresholds.append(f'🥉 3rd: {value}')
        elif key in ['Hold to Qualify', 'Min to Qualify']:
            thresholds.append(f'🎯 Target: {value}')
    
    if thresholds:
        return f"<br><div class='targets'><strong>Targets:</strong> {' | '.join(thresholds)}</div>"
    return ""


def determine_lead_athlete_status(status: str, has_score: bool) -> Tuple[str, str]:
    """Determine lead athlete status and styling"""
    if not has_score:
        return "", "📄"
    
    if "Qualified" in status or "✓✓" in status:
        return "qualified", "✅"
    elif "Eliminated" in status or "✗" in status:
        return "eliminated", "❌"
    elif "Podium" in status and "No Podium" not in status and "Contention" not in status:
        return "podium-position", "🏆"
    elif "Podium Contention" in status or "Contention" in status:
        return "podium-contention", "⚠️"
    elif "No Podium" in status:
        return "no-podium", "❌"
    else:
        return "", "📄"


def get_lead_position_emoji(rank: any, has_score: bool, card_class: str, status_emoji: str) -> str:
    """Get position emoji for lead athletes"""
    rank_num = DataProcessor.safe_numeric_conversion(rank)
    if rank_num > 0:
        return status_emoji if has_score and card_class else f"#{rank_num}"
    return "📄"


def format_worst_finish(worst_finish: any, has_score: bool) -> str:
    """Format worst finish display"""
    if not has_score or worst_finish in ['N/A', '', None] or pd.isna(worst_finish):
        return ""
    
    worst_finish_clean = DataProcessor.clean_text(str(worst_finish))
    return f" | Worst Finish: {worst_finish_clean}" if worst_finish_clean and worst_finish_clean != '-' else ""


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"🚫 Application Error: {e}")
        st.markdown("Please refresh the page or contact support if the issue persists.")
        
        with st.expander("🔧 Debug Information"):
            st.code(f"Error: {e}")
            st.code(f"Time: {datetime.now()}")
            import traceback
            st.code(traceback.format_exc()), na=False)) &      # Remove "25+" style entries
            (~df['Name'].apply(is_placeholder_athlete))
        ]
        
        # Second pass: If we have rank information, use it to filter properly
        if 'Current Rank' in filtered_df.columns:
            filtered_df['temp_rank'] = pd.to_numeric(filtered_df['Current Rank'], errors='coerce')
            
            # Keep only rows with valid ranks within expected range
            ranked_df = filtered_df[
                (filtered_df['temp_rank'].notna()) & 
                (filtered_df['temp_rank'] >= 1) & 
                (filtered_df['temp_rank'] <= expected_max)
            ]
            
            if len(ranked_df) > 0:
                # Sort by rank and take only the expected number
                ranked_df = ranked_df.sort_values('temp_rank').head(expected_max)
                filtered_df = ranked_df.drop('temp_rank', axis=1)
            else:
                # If no valid ranks, fall back to manual filtering
                filtered_df = manual_athlete_filter(filtered_df, expected_max)
        else:
            # No rank column available, use manual filtering
            filtered_df = manual_athlete_filter(filtered_df, expected_max)
        
        # Third pass: Additional validation for lead competitions
        if "Lead" in competition_name:
            filtered_df = validate_lead_athletes(filtered_df, expected_max)
        
        logger.info(f"Filtered to {len(filtered_df)} athletes for {competition_name} (expected: {expected_max})")
        return filtered_df
        
    except Exception as e:
        logger.error(f"Error filtering athletes for {competition_name}: {e}")
        # Fallback to basic filtering with count limit
        basic_filtered = df[
            df['Name'].notna() & 
            (df['Name'] != '') &
            (~df['Name'].astype(str).str.contains('Hold for', na=False))
        ].head(expected_max)
        return basic_filtered


def manual_athlete_filter(df: pd.DataFrame, expected_max: int) -> pd.DataFrame:
    """Manually filter athletes when rank information is not reliable"""
    # Look for patterns that indicate real athlete names vs reference data
    potential_athletes = []
    
    for idx, row in df.iterrows():
        name = str(row.get('Name', '')).strip()
        
        # Skip if name looks like reference data
        if any(keyword in name.lower() for keyword in [
            'hold', 'min', 'max', 'qualification', 'threshold', 'zone', 'top',
            'points', 'score', 'rank', 'position', 'place', 'finish'
        ]):
            continue
        
        # Skip if name is too short or looks like a number/code
        if len(name) < 3 or name.isdigit() or not any(c.isalpha() for c in name):
            continue
        
        # Look for typical athlete name patterns (First Last or similar)
        name_parts = name.split()
        if len(name_parts) >= 2 and all(part.isalpha() or part.replace('.', '').isalpha() for part in name_parts):
            potential_athletes.append(idx)
        elif len(name_parts) == 1 and len(name) > 4 and name.isalpha():
            # Single names that are long enough and all letters
            potential_athletes.append(idx)
    
    # Return the filtered dataframe, limited to expected count
    return df.loc[potential_athletes[:expected_max]]


def validate_lead_athletes(df: pd.DataFrame, expected_max: int) -> pd.DataFrame:
    """Additional validation specifically for lead competitions"""
    if len(df) <= expected_max:
        return df
    
    # For lead competitions, prioritize athletes with actual climbing data
    scored_athletes = df[df['Manual Score'].notna() & (df['Manual Score'] != '')].copy()
    unscored_athletes = df[df['Manual Score'].isna() | (df['Manual Score'] == '')].copy()
    
    # Combine scored athletes first, then fill with unscored up to limit
    result_df = scored_athletes.copy()
    remaining_slots = expected_max - len(scored_athletes)
    
    if remaining_slots > 0 and len(unscored_athletes) > 0:
        result_df = pd.concat([result_df, unscored_athletes.head(remaining_slots)], ignore_index=True)
    
    return result_df.head(expected_max)


def is_placeholder_athlete(name: str) -> bool:
    """Check if name is a placeholder like 'Athlete 1', 'Athlete 23', etc."""
    name_str = str(name).strip()
    if name_str.startswith('Athlete '):
        remaining = name_str[8:].strip()
        return remaining.isdigit()
    return False


def display_qualification_thresholds(qualification_info: Dict[str, str]):
    """Display qualification thresholds if available"""
    if qualification_info:
        threshold_items = []
        threshold_mapping = {
            'Hold for 1st': ('🥇 1st', '#FFD700'),
            'Hold for 2nd': ('🥈 2nd', '#C0C0C0'),
            'Hold for 3rd': ('🥉 3rd', '#CD7F32'),
            'Hold to Qualify': ('✅ Qualify', '#28a745'),
            'Min to Qualify': ('⚠️ Min', '#ffc107')
        }
        
        for key, value in qualification_info.items():
            if key in threshold_mapping:
                label, color = threshold_mapping[key]
                threshold_items.append(f'<span style="color: {color}; font-weight: bold;">{label}: {value}</span>')
        
        if threshold_items:
            st.markdown(f"""
            <div class="threshold-card">
                <h5>🎯 Qualification Thresholds</h5>
                {' | '.join(threshold_items)}
            </div>
            """, unsafe_allow_html=True)


def display_lead_athletes(active_df: pd.DataFrame, qualification_info: Dict[str, str]):
    """Display lead competition athletes with enhanced formatting"""
    # Sort by rank if available
    try:
        if 'Current Rank' in active_df.columns:
            active_df['Current Rank'] = pd.to_numeric(active_df['Current Rank'], errors='coerce')
            active_df = active_df.sort_values('Current Rank', ascending=True).reset_index(drop=True)
    except Exception as e:
        logger.warning(f"Could not sort by rank: {e}")
    
    # Display athlete cards
    for _, row in active_df.iterrows():
        name = DataProcessor.clean_text(str(row.get('Name', 'Unknown')))
        score = row.get('Manual Score', 'N/A')
        rank = row.get('Current Rank', 'N/A')
        status = DataProcessor.clean_text(str(row.get('Status', 'Unknown')))
        worst_finish = row.get('Worst Finish', 'N/A')
        
        # Determine if athlete has a score
        has_score = score not in ['N/A', '', None] and not pd.isna(score)
        
        # Create threshold display for athletes without scores
        threshold_display = create_threshold_display(has_score, qualification_info)
        
        # Determine card styling
        card_class, status_emoji = determine_lead_athlete_status(status, has_score)
        
        # Set position emoji
        position_emoji = get_lead_position_emoji(rank, has_score, card_class, status_emoji)
        
        # Format displays
        score_display = score if has_score else "Awaiting Result"
        worst_finish_display = format_worst_finish(worst_finish, has_score)
        
        # Create athlete card
        st.markdown(f"""
        <div class="athlete-row {card_class}">
            <strong>{position_emoji} #{rank} - {name}</strong><br>
            <small>Score: {score_display} | Status: {status}{worst_finish_display}</small>{threshold_display}
        </div>
        """, unsafe_allow_html=True)


def create_threshold_display(has_score: bool, qualification_info: Dict[str, str]) -> str:
    """Create threshold display for athletes without scores"""
    if has_score or not qualification_info:
        return ""
    
    thresholds = []
    for key, value in qualification_info.items():
        if key == 'Hold for 1st':
            thresholds.append(f'🥇 1st: {value}')
        elif key == 'Hold for 2nd':
            thresholds.append(f'🥈 2nd: {value}')
        elif key == 'Hold for 3rd':
            thresholds.append(f'🥉 3rd: {value}')
        elif key in ['Hold to Qualify', 'Min to Qualify']:
            thresholds.append(f'🎯 Target: {value}')
    
    if thresholds:
        return f"<br><div class='targets'><strong>Targets:</strong> {' | '.join(thresholds)}</div>"
    return ""


def determine_lead_athlete_status(status: str, has_score: bool) -> Tuple[str, str]:
    """Determine lead athlete status and styling"""
    if not has_score:
        return "", "📄"
    
    if "Qualified" in status or "✓✓" in status:
        return "qualified", "✅"
    elif "Eliminated" in status or "✗" in status:
        return "eliminated", "❌"
    elif "Podium" in status and "No Podium" not in status and "Contention" not in status:
        return "podium-position", "🏆"
    elif "Podium Contention" in status or "Contention" in status:
        return "podium-contention", "⚠️"
    elif "No Podium" in status:
        return "no-podium", "❌"
    else:
        return "", "📄"


def get_lead_position_emoji(rank: any, has_score: bool, card_class: str, status_emoji: str) -> str:
    """Get position emoji for lead athletes"""
    rank_num = DataProcessor.safe_numeric_conversion(rank)
    if rank_num > 0:
        return status_emoji if has_score and card_class else f"#{rank_num}"
    return "📄"


def format_worst_finish(worst_finish: any, has_score: bool) -> str:
    """Format worst finish display"""
    if not has_score or worst_finish in ['N/A', '', None] or pd.isna(worst_finish):
        return ""
    
    worst_finish_clean = DataProcessor.clean_text(str(worst_finish))
    return f" | Worst Finish: {worst_finish_clean}" if worst_finish_clean and worst_finish_clean != '-' else ""


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"🚫 Application Error: {e}")
        st.markdown("Please refresh the page or contact support if the issue persists.")
        
        with st.expander("🔧 Debug Information"):
            st.code(f"Error: {e}")
            st.code(f"Time: {datetime.now()}")
            import traceback
            st.code(traceback.format_exc()),                # Decimal numbers
        r'^\d+\+


def display_qualification_thresholds(qualification_info: Dict[str, str]):
    """Display qualification thresholds if available"""
    if qualification_info:
        threshold_items = []
        threshold_mapping = {
            'Hold for 1st': ('🥇 1st', '#FFD700'),
            'Hold for 2nd': ('🥈 2nd', '#C0C0C0'),
            'Hold for 3rd': ('🥉 3rd', '#CD7F32'),
            'Hold to Qualify': ('✅ Qualify', '#28a745'),
            'Min to Qualify': ('⚠️ Min', '#ffc107')
        }
        
        for key, value in qualification_info.items():
            if key in threshold_mapping:
                label, color = threshold_mapping[key]
                threshold_items.append(f'<span style="color: {color}; font-weight: bold;">{label}: {value}</span>')
        
        if threshold_items:
            st.markdown(f"""
            <div class="threshold-card">
                <h5>🎯 Qualification Thresholds</h5>
                {' | '.join(threshold_items)}
            </div>
            """, unsafe_allow_html=True)


def display_lead_athletes(active_df: pd.DataFrame, qualification_info: Dict[str, str]):
    """Display lead competition athletes with enhanced formatting"""
    # Sort by rank if available
    try:
        if 'Current Rank' in active_df.columns:
            active_df['Current Rank'] = pd.to_numeric(active_df['Current Rank'], errors='coerce')
            active_df = active_df.sort_values('Current Rank', ascending=True).reset_index(drop=True)
    except Exception as e:
        logger.warning(f"Could not sort by rank: {e}")
    
    # Display athlete cards
    for _, row in active_df.iterrows():
        name = DataProcessor.clean_text(str(row.get('Name', 'Unknown')))
        score = row.get('Manual Score', 'N/A')
        rank = row.get('Current Rank', 'N/A')
        status = DataProcessor.clean_text(str(row.get('Status', 'Unknown')))
        worst_finish = row.get('Worst Finish', 'N/A')
        
        # Determine if athlete has a score
        has_score = score not in ['N/A', '', None] and not pd.isna(score)
        
        # Create threshold display for athletes without scores
        threshold_display = create_threshold_display(has_score, qualification_info)
        
        # Determine card styling
        card_class, status_emoji = determine_lead_athlete_status(status, has_score)
        
        # Set position emoji
        position_emoji = get_lead_position_emoji(rank, has_score, card_class, status_emoji)
        
        # Format displays
        score_display = score if has_score else "Awaiting Result"
        worst_finish_display = format_worst_finish(worst_finish, has_score)
        
        # Create athlete card
        st.markdown(f"""
        <div class="athlete-row {card_class}">
            <strong>{position_emoji} #{rank} - {name}</strong><br>
            <small>Score: {score_display} | Status: {status}{worst_finish_display}</small>{threshold_display}
        </div>
        """, unsafe_allow_html=True)


def create_threshold_display(has_score: bool, qualification_info: Dict[str, str]) -> str:
    """Create threshold display for athletes without scores"""
    if has_score or not qualification_info:
        return ""
    
    thresholds = []
    for key, value in qualification_info.items():
        if key == 'Hold for 1st':
            thresholds.append(f'🥇 1st: {value}')
        elif key == 'Hold for 2nd':
            thresholds.append(f'🥈 2nd: {value}')
        elif key == 'Hold for 3rd':
            thresholds.append(f'🥉 3rd: {value}')
        elif key in ['Hold to Qualify', 'Min to Qualify']:
            thresholds.append(f'🎯 Target: {value}')
    
    if thresholds:
        return f"<br><div class='targets'><strong>Targets:</strong> {' | '.join(thresholds)}</div>"
    return ""


def determine_lead_athlete_status(status: str, has_score: bool) -> Tuple[str, str]:
    """Determine lead athlete status and styling"""
    if not has_score:
        return "", "📄"
    
    if "Qualified" in status or "✓✓" in status:
        return "qualified", "✅"
    elif "Eliminated" in status or "✗" in status:
        return "eliminated", "❌"
    elif "Podium" in status and "No Podium" not in status and "Contention" not in status:
        return "podium-position", "🏆"
    elif "Podium Contention" in status or "Contention" in status:
        return "podium-contention", "⚠️"
    elif "No Podium" in status:
        return "no-podium", "❌"
    else:
        return "", "📄"


def get_lead_position_emoji(rank: any, has_score: bool, card_class: str, status_emoji: str) -> str:
    """Get position emoji for lead athletes"""
    rank_num = DataProcessor.safe_numeric_conversion(rank)
    if rank_num > 0:
        return status_emoji if has_score and card_class else f"#{rank_num}"
    return "📄"


def format_worst_finish(worst_finish: any, has_score: bool) -> str:
    """Format worst finish display"""
    if not has_score or worst_finish in ['N/A', '', None] or pd.isna(worst_finish):
        return ""
    
    worst_finish_clean = DataProcessor.clean_text(str(worst_finish))
    return f" | Worst Finish: {worst_finish_clean}" if worst_finish_clean and worst_finish_clean != '-' else ""


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"🚫 Application Error: {e}")
        st.markdown("Please refresh the page or contact support if the issue persists.")
        
        with st.expander("🔧 Debug Information"):
            st.code(f"Error: {e}")
            st.code(f"Time: {datetime.now()}")
            import traceback
            st.code(traceback.format_exc()), na=False)) &  # Remove pure numbers
            (~df['Name'].astype(str).str.match(r'^\d+\+


def is_placeholder_athlete(name: str) -> bool:
    """Check if name is a placeholder like 'Athlete 1', 'Athlete 23', etc."""
    name_str = str(name).strip()
    if name_str.startswith('Athlete '):
        remaining = name_str[8:].strip()
        return remaining.isdigit()
    return False


def display_qualification_thresholds(qualification_info: Dict[str, str]):
    """Display qualification thresholds if available"""
    if qualification_info:
        threshold_items = []
        threshold_mapping = {
            'Hold for 1st': ('🥇 1st', '#FFD700'),
            'Hold for 2nd': ('🥈 2nd', '#C0C0C0'),
            'Hold for 3rd': ('🥉 3rd', '#CD7F32'),
            'Hold to Qualify': ('✅ Qualify', '#28a745'),
            'Min to Qualify': ('⚠️ Min', '#ffc107')
        }
        
        for key, value in qualification_info.items():
            if key in threshold_mapping:
                label, color = threshold_mapping[key]
                threshold_items.append(f'<span style="color: {color}; font-weight: bold;">{label}: {value}</span>')
        
        if threshold_items:
            st.markdown(f"""
            <div class="threshold-card">
                <h5>🎯 Qualification Thresholds</h5>
                {' | '.join(threshold_items)}
            </div>
            """, unsafe_allow_html=True)


def display_lead_athletes(active_df: pd.DataFrame, qualification_info: Dict[str, str]):
    """Display lead competition athletes with enhanced formatting"""
    # Sort by rank if available
    try:
        if 'Current Rank' in active_df.columns:
            active_df['Current Rank'] = pd.to_numeric(active_df['Current Rank'], errors='coerce')
            active_df = active_df.sort_values('Current Rank', ascending=True).reset_index(drop=True)
    except Exception as e:
        logger.warning(f"Could not sort by rank: {e}")
    
    # Display athlete cards
    for _, row in active_df.iterrows():
        name = DataProcessor.clean_text(str(row.get('Name', 'Unknown')))
        score = row.get('Manual Score', 'N/A')
        rank = row.get('Current Rank', 'N/A')
        status = DataProcessor.clean_text(str(row.get('Status', 'Unknown')))
        worst_finish = row.get('Worst Finish', 'N/A')
        
        # Determine if athlete has a score
        has_score = score not in ['N/A', '', None] and not pd.isna(score)
        
        # Create threshold display for athletes without scores
        threshold_display = create_threshold_display(has_score, qualification_info)
        
        # Determine card styling
        card_class, status_emoji = determine_lead_athlete_status(status, has_score)
        
        # Set position emoji
        position_emoji = get_lead_position_emoji(rank, has_score, card_class, status_emoji)
        
        # Format displays
        score_display = score if has_score else "Awaiting Result"
        worst_finish_display = format_worst_finish(worst_finish, has_score)
        
        # Create athlete card
        st.markdown(f"""
        <div class="athlete-row {card_class}">
            <strong>{position_emoji} #{rank} - {name}</strong><br>
            <small>Score: {score_display} | Status: {status}{worst_finish_display}</small>{threshold_display}
        </div>
        """, unsafe_allow_html=True)


def create_threshold_display(has_score: bool, qualification_info: Dict[str, str]) -> str:
    """Create threshold display for athletes without scores"""
    if has_score or not qualification_info:
        return ""
    
    thresholds = []
    for key, value in qualification_info.items():
        if key == 'Hold for 1st':
            thresholds.append(f'🥇 1st: {value}')
        elif key == 'Hold for 2nd':
            thresholds.append(f'🥈 2nd: {value}')
        elif key == 'Hold for 3rd':
            thresholds.append(f'🥉 3rd: {value}')
        elif key in ['Hold to Qualify', 'Min to Qualify']:
            thresholds.append(f'🎯 Target: {value}')
    
    if thresholds:
        return f"<br><div class='targets'><strong>Targets:</strong> {' | '.join(thresholds)}</div>"
    return ""


def determine_lead_athlete_status(status: str, has_score: bool) -> Tuple[str, str]:
    """Determine lead athlete status and styling"""
    if not has_score:
        return "", "📄"
    
    if "Qualified" in status or "✓✓" in status:
        return "qualified", "✅"
    elif "Eliminated" in status or "✗" in status:
        return "eliminated", "❌"
    elif "Podium" in status and "No Podium" not in status and "Contention" not in status:
        return "podium-position", "🏆"
    elif "Podium Contention" in status or "Contention" in status:
        return "podium-contention", "⚠️"
    elif "No Podium" in status:
        return "no-podium", "❌"
    else:
        return "", "📄"


def get_lead_position_emoji(rank: any, has_score: bool, card_class: str, status_emoji: str) -> str:
    """Get position emoji for lead athletes"""
    rank_num = DataProcessor.safe_numeric_conversion(rank)
    if rank_num > 0:
        return status_emoji if has_score and card_class else f"#{rank_num}"
    return "📄"


def format_worst_finish(worst_finish: any, has_score: bool) -> str:
    """Format worst finish display"""
    if not has_score or worst_finish in ['N/A', '', None] or pd.isna(worst_finish):
        return ""
    
    worst_finish_clean = DataProcessor.clean_text(str(worst_finish))
    return f" | Worst Finish: {worst_finish_clean}" if worst_finish_clean and worst_finish_clean != '-' else ""


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"🚫 Application Error: {e}")
        st.markdown("Please refresh the page or contact support if the issue persists.")
        
        with st.expander("🔧 Debug Information"):
            st.code(f"Error: {e}")
            st.code(f"Time: {datetime.now()}")
            import traceback
            st.code(traceback.format_exc()), na=False)) &      # Remove "25+" style entries
            (~df['Name'].apply(is_placeholder_athlete))
        ]
        
        # Second pass: If we have rank information, use it to filter properly
        if 'Current Rank' in filtered_df.columns:
            filtered_df['temp_rank'] = pd.to_numeric(filtered_df['Current Rank'], errors='coerce')
            
            # Keep only rows with valid ranks within expected range
            ranked_df = filtered_df[
                (filtered_df['temp_rank'].notna()) & 
                (filtered_df['temp_rank'] >= 1) & 
                (filtered_df['temp_rank'] <= expected_max)
            ]
            
            if len(ranked_df) > 0:
                # Sort by rank and take only the expected number
                ranked_df = ranked_df.sort_values('temp_rank').head(expected_max)
                filtered_df = ranked_df.drop('temp_rank', axis=1)
            else:
                # If no valid ranks, fall back to manual filtering
                filtered_df = manual_athlete_filter(filtered_df, expected_max)
        else:
            # No rank column available, use manual filtering
            filtered_df = manual_athlete_filter(filtered_df, expected_max)
        
        # Third pass: Additional validation for lead competitions
        if "Lead" in competition_name:
            filtered_df = validate_lead_athletes(filtered_df, expected_max)
        
        logger.info(f"Filtered to {len(filtered_df)} athletes for {competition_name} (expected: {expected_max})")
        return filtered_df
        
    except Exception as e:
        logger.error(f"Error filtering athletes for {competition_name}: {e}")
        # Fallback to basic filtering with count limit
        basic_filtered = df[
            df['Name'].notna() & 
            (df['Name'] != '') &
            (~df['Name'].astype(str).str.contains('Hold for', na=False))
        ].head(expected_max)
        return basic_filtered


def manual_athlete_filter(df: pd.DataFrame, expected_max: int) -> pd.DataFrame:
    """Manually filter athletes when rank information is not reliable"""
    # Look for patterns that indicate real athlete names vs reference data
    potential_athletes = []
    
    for idx, row in df.iterrows():
        name = str(row.get('Name', '')).strip()
        
        # Skip if name looks like reference data
        if any(keyword in name.lower() for keyword in [
            'hold', 'min', 'max', 'qualification', 'threshold', 'zone', 'top',
            'points', 'score', 'rank', 'position', 'place', 'finish'
        ]):
            continue
        
        # Skip if name is too short or looks like a number/code
        if len(name) < 3 or name.isdigit() or not any(c.isalpha() for c in name):
            continue
        
        # Look for typical athlete name patterns (First Last or similar)
        name_parts = name.split()
        if len(name_parts) >= 2 and all(part.isalpha() or part.replace('.', '').isalpha() for part in name_parts):
            potential_athletes.append(idx)
        elif len(name_parts) == 1 and len(name) > 4 and name.isalpha():
            # Single names that are long enough and all letters
            potential_athletes.append(idx)
    
    # Return the filtered dataframe, limited to expected count
    return df.loc[potential_athletes[:expected_max]]


def validate_lead_athletes(df: pd.DataFrame, expected_max: int) -> pd.DataFrame:
    """Additional validation specifically for lead competitions"""
    if len(df) <= expected_max:
        return df
    
    # For lead competitions, prioritize athletes with actual climbing data
    scored_athletes = df[df['Manual Score'].notna() & (df['Manual Score'] != '')].copy()
    unscored_athletes = df[df['Manual Score'].isna() | (df['Manual Score'] == '')].copy()
    
    # Combine scored athletes first, then fill with unscored up to limit
    result_df = scored_athletes.copy()
    remaining_slots = expected_max - len(scored_athletes)
    
    if remaining_slots > 0 and len(unscored_athletes) > 0:
        result_df = pd.concat([result_df, unscored_athletes.head(remaining_slots)], ignore_index=True)
    
    return result_df.head(expected_max)


def is_placeholder_athlete(name: str) -> bool:
    """Check if name is a placeholder like 'Athlete 1', 'Athlete 23', etc."""
    name_str = str(name).strip()
    if name_str.startswith('Athlete '):
        remaining = name_str[8:].strip()
        return remaining.isdigit()
    return False


def display_qualification_thresholds(qualification_info: Dict[str, str]):
    """Display qualification thresholds if available"""
    if qualification_info:
        threshold_items = []
        threshold_mapping = {
            'Hold for 1st': ('🥇 1st', '#FFD700'),
            'Hold for 2nd': ('🥈 2nd', '#C0C0C0'),
            'Hold for 3rd': ('🥉 3rd', '#CD7F32'),
            'Hold to Qualify': ('✅ Qualify', '#28a745'),
            'Min to Qualify': ('⚠️ Min', '#ffc107')
        }
        
        for key, value in qualification_info.items():
            if key in threshold_mapping:
                label, color = threshold_mapping[key]
                threshold_items.append(f'<span style="color: {color}; font-weight: bold;">{label}: {value}</span>')
        
        if threshold_items:
            st.markdown(f"""
            <div class="threshold-card">
                <h5>🎯 Qualification Thresholds</h5>
                {' | '.join(threshold_items)}
            </div>
            """, unsafe_allow_html=True)


def display_lead_athletes(active_df: pd.DataFrame, qualification_info: Dict[str, str]):
    """Display lead competition athletes with enhanced formatting"""
    # Sort by rank if available
    try:
        if 'Current Rank' in active_df.columns:
            active_df['Current Rank'] = pd.to_numeric(active_df['Current Rank'], errors='coerce')
            active_df = active_df.sort_values('Current Rank', ascending=True).reset_index(drop=True)
    except Exception as e:
        logger.warning(f"Could not sort by rank: {e}")
    
    # Display athlete cards
    for _, row in active_df.iterrows():
        name = DataProcessor.clean_text(str(row.get('Name', 'Unknown')))
        score = row.get('Manual Score', 'N/A')
        rank = row.get('Current Rank', 'N/A')
        status = DataProcessor.clean_text(str(row.get('Status', 'Unknown')))
        worst_finish = row.get('Worst Finish', 'N/A')
        
        # Determine if athlete has a score
        has_score = score not in ['N/A', '', None] and not pd.isna(score)
        
        # Create threshold display for athletes without scores
        threshold_display = create_threshold_display(has_score, qualification_info)
        
        # Determine card styling
        card_class, status_emoji = determine_lead_athlete_status(status, has_score)
        
        # Set position emoji
        position_emoji = get_lead_position_emoji(rank, has_score, card_class, status_emoji)
        
        # Format displays
        score_display = score if has_score else "Awaiting Result"
        worst_finish_display = format_worst_finish(worst_finish, has_score)
        
        # Create athlete card
        st.markdown(f"""
        <div class="athlete-row {card_class}">
            <strong>{position_emoji} #{rank} - {name}</strong><br>
            <small>Score: {score_display} | Status: {status}{worst_finish_display}</small>{threshold_display}
        </div>
        """, unsafe_allow_html=True)


def create_threshold_display(has_score: bool, qualification_info: Dict[str, str]) -> str:
    """Create threshold display for athletes without scores"""
    if has_score or not qualification_info:
        return ""
    
    thresholds = []
    for key, value in qualification_info.items():
        if key == 'Hold for 1st':
            thresholds.append(f'🥇 1st: {value}')
        elif key == 'Hold for 2nd':
            thresholds.append(f'🥈 2nd: {value}')
        elif key == 'Hold for 3rd':
            thresholds.append(f'🥉 3rd: {value}')
        elif key in ['Hold to Qualify', 'Min to Qualify']:
            thresholds.append(f'🎯 Target: {value}')
    
    if thresholds:
        return f"<br><div class='targets'><strong>Targets:</strong> {' | '.join(thresholds)}</div>"
    return ""


def determine_lead_athlete_status(status: str, has_score: bool) -> Tuple[str, str]:
    """Determine lead athlete status and styling"""
    if not has_score:
        return "", "📄"
    
    if "Qualified" in status or "✓✓" in status:
        return "qualified", "✅"
    elif "Eliminated" in status or "✗" in status:
        return "eliminated", "❌"
    elif "Podium" in status and "No Podium" not in status and "Contention" not in status:
        return "podium-position", "🏆"
    elif "Podium Contention" in status or "Contention" in status:
        return "podium-contention", "⚠️"
    elif "No Podium" in status:
        return "no-podium", "❌"
    else:
        return "", "📄"


def get_lead_position_emoji(rank: any, has_score: bool, card_class: str, status_emoji: str) -> str:
    """Get position emoji for lead athletes"""
    rank_num = DataProcessor.safe_numeric_conversion(rank)
    if rank_num > 0:
        return status_emoji if has_score and card_class else f"#{rank_num}"
    return "📄"


def format_worst_finish(worst_finish: any, has_score: bool) -> str:
    """Format worst finish display"""
    if not has_score or worst_finish in ['N/A', '', None] or pd.isna(worst_finish):
        return ""
    
    worst_finish_clean = DataProcessor.clean_text(str(worst_finish))
    return f" | Worst Finish: {worst_finish_clean}" if worst_finish_clean and worst_finish_clean != '-' else ""


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"🚫 Application Error: {e}")
        st.markdown("Please refresh the page or contact support if the issue persists.")
        
        with st.expander("🔧 Debug Information"):
            st.code(f"Error: {e}")
            st.code(f"Time: {datetime.now()}")
            import traceback
            st.code(traceback.format_exc()),                   # "25+"
        r'^tbd$|^tba


def display_qualification_thresholds(qualification_info: Dict[str, str]):
    """Display qualification thresholds if available"""
    if qualification_info:
        threshold_items = []
        threshold_mapping = {
            'Hold for 1st': ('🥇 1st', '#FFD700'),
            'Hold for 2nd': ('🥈 2nd', '#C0C0C0'),
            'Hold for 3rd': ('🥉 3rd', '#CD7F32'),
            'Hold to Qualify': ('✅ Qualify', '#28a745'),
            'Min to Qualify': ('⚠️ Min', '#ffc107')
        }
        
        for key, value in qualification_info.items():
            if key in threshold_mapping:
                label, color = threshold_mapping[key]
                threshold_items.append(f'<span style="color: {color}; font-weight: bold;">{label}: {value}</span>')
        
        if threshold_items:
            st.markdown(f"""
            <div class="threshold-card">
                <h5>🎯 Qualification Thresholds</h5>
                {' | '.join(threshold_items)}
            </div>
            """, unsafe_allow_html=True)


def display_lead_athletes(active_df: pd.DataFrame, qualification_info: Dict[str, str]):
    """Display lead competition athletes with enhanced formatting"""
    # Sort by rank if available
    try:
        if 'Current Rank' in active_df.columns:
            active_df['Current Rank'] = pd.to_numeric(active_df['Current Rank'], errors='coerce')
            active_df = active_df.sort_values('Current Rank', ascending=True).reset_index(drop=True)
    except Exception as e:
        logger.warning(f"Could not sort by rank: {e}")
    
    # Display athlete cards
    for _, row in active_df.iterrows():
        name = DataProcessor.clean_text(str(row.get('Name', 'Unknown')))
        score = row.get('Manual Score', 'N/A')
        rank = row.get('Current Rank', 'N/A')
        status = DataProcessor.clean_text(str(row.get('Status', 'Unknown')))
        worst_finish = row.get('Worst Finish', 'N/A')
        
        # Determine if athlete has a score
        has_score = score not in ['N/A', '', None] and not pd.isna(score)
        
        # Create threshold display for athletes without scores
        threshold_display = create_threshold_display(has_score, qualification_info)
        
        # Determine card styling
        card_class, status_emoji = determine_lead_athlete_status(status, has_score)
        
        # Set position emoji
        position_emoji = get_lead_position_emoji(rank, has_score, card_class, status_emoji)
        
        # Format displays
        score_display = score if has_score else "Awaiting Result"
        worst_finish_display = format_worst_finish(worst_finish, has_score)
        
        # Create athlete card
        st.markdown(f"""
        <div class="athlete-row {card_class}">
            <strong>{position_emoji} #{rank} - {name}</strong><br>
            <small>Score: {score_display} | Status: {status}{worst_finish_display}</small>{threshold_display}
        </div>
        """, unsafe_allow_html=True)


def create_threshold_display(has_score: bool, qualification_info: Dict[str, str]) -> str:
    """Create threshold display for athletes without scores"""
    if has_score or not qualification_info:
        return ""
    
    thresholds = []
    for key, value in qualification_info.items():
        if key == 'Hold for 1st':
            thresholds.append(f'🥇 1st: {value}')
        elif key == 'Hold for 2nd':
            thresholds.append(f'🥈 2nd: {value}')
        elif key == 'Hold for 3rd':
            thresholds.append(f'🥉 3rd: {value}')
        elif key in ['Hold to Qualify', 'Min to Qualify']:
            thresholds.append(f'🎯 Target: {value}')
    
    if thresholds:
        return f"<br><div class='targets'><strong>Targets:</strong> {' | '.join(thresholds)}</div>"
    return ""


def determine_lead_athlete_status(status: str, has_score: bool) -> Tuple[str, str]:
    """Determine lead athlete status and styling"""
    if not has_score:
        return "", "📄"
    
    if "Qualified" in status or "✓✓" in status:
        return "qualified", "✅"
    elif "Eliminated" in status or "✗" in status:
        return "eliminated", "❌"
    elif "Podium" in status and "No Podium" not in status and "Contention" not in status:
        return "podium-position", "🏆"
    elif "Podium Contention" in status or "Contention" in status:
        return "podium-contention", "⚠️"
    elif "No Podium" in status:
        return "no-podium", "❌"
    else:
        return "", "📄"


def get_lead_position_emoji(rank: any, has_score: bool, card_class: str, status_emoji: str) -> str:
    """Get position emoji for lead athletes"""
    rank_num = DataProcessor.safe_numeric_conversion(rank)
    if rank_num > 0:
        return status_emoji if has_score and card_class else f"#{rank_num}"
    return "📄"


def format_worst_finish(worst_finish: any, has_score: bool) -> str:
    """Format worst finish display"""
    if not has_score or worst_finish in ['N/A', '', None] or pd.isna(worst_finish):
        return ""
    
    worst_finish_clean = DataProcessor.clean_text(str(worst_finish))
    return f" | Worst Finish: {worst_finish_clean}" if worst_finish_clean and worst_finish_clean != '-' else ""


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"🚫 Application Error: {e}")
        st.markdown("Please refresh the page or contact support if the issue persists.")
        
        with st.expander("🔧 Debug Information"):
            st.code(f"Error: {e}")
            st.code(f"Time: {datetime.now()}")
            import traceback
            st.code(traceback.format_exc()), na=False)) &  # Remove pure numbers
            (~df['Name'].astype(str).str.match(r'^\d+\+


def is_placeholder_athlete(name: str) -> bool:
    """Check if name is a placeholder like 'Athlete 1', 'Athlete 23', etc."""
    name_str = str(name).strip()
    if name_str.startswith('Athlete '):
        remaining = name_str[8:].strip()
        return remaining.isdigit()
    return False


def display_qualification_thresholds(qualification_info: Dict[str, str]):
    """Display qualification thresholds if available"""
    if qualification_info:
        threshold_items = []
        threshold_mapping = {
            'Hold for 1st': ('🥇 1st', '#FFD700'),
            'Hold for 2nd': ('🥈 2nd', '#C0C0C0'),
            'Hold for 3rd': ('🥉 3rd', '#CD7F32'),
            'Hold to Qualify': ('✅ Qualify', '#28a745'),
            'Min to Qualify': ('⚠️ Min', '#ffc107')
        }
        
        for key, value in qualification_info.items():
            if key in threshold_mapping:
                label, color = threshold_mapping[key]
                threshold_items.append(f'<span style="color: {color}; font-weight: bold;">{label}: {value}</span>')
        
        if threshold_items:
            st.markdown(f"""
            <div class="threshold-card">
                <h5>🎯 Qualification Thresholds</h5>
                {' | '.join(threshold_items)}
            </div>
            """, unsafe_allow_html=True)


def display_lead_athletes(active_df: pd.DataFrame, qualification_info: Dict[str, str]):
    """Display lead competition athletes with enhanced formatting"""
    # Sort by rank if available
    try:
        if 'Current Rank' in active_df.columns:
            active_df['Current Rank'] = pd.to_numeric(active_df['Current Rank'], errors='coerce')
            active_df = active_df.sort_values('Current Rank', ascending=True).reset_index(drop=True)
    except Exception as e:
        logger.warning(f"Could not sort by rank: {e}")
    
    # Display athlete cards
    for _, row in active_df.iterrows():
        name = DataProcessor.clean_text(str(row.get('Name', 'Unknown')))
        score = row.get('Manual Score', 'N/A')
        rank = row.get('Current Rank', 'N/A')
        status = DataProcessor.clean_text(str(row.get('Status', 'Unknown')))
        worst_finish = row.get('Worst Finish', 'N/A')
        
        # Determine if athlete has a score
        has_score = score not in ['N/A', '', None] and not pd.isna(score)
        
        # Create threshold display for athletes without scores
        threshold_display = create_threshold_display(has_score, qualification_info)
        
        # Determine card styling
        card_class, status_emoji = determine_lead_athlete_status(status, has_score)
        
        # Set position emoji
        position_emoji = get_lead_position_emoji(rank, has_score, card_class, status_emoji)
        
        # Format displays
        score_display = score if has_score else "Awaiting Result"
        worst_finish_display = format_worst_finish(worst_finish, has_score)
        
        # Create athlete card
        st.markdown(f"""
        <div class="athlete-row {card_class}">
            <strong>{position_emoji} #{rank} - {name}</strong><br>
            <small>Score: {score_display} | Status: {status}{worst_finish_display}</small>{threshold_display}
        </div>
        """, unsafe_allow_html=True)


def create_threshold_display(has_score: bool, qualification_info: Dict[str, str]) -> str:
    """Create threshold display for athletes without scores"""
    if has_score or not qualification_info:
        return ""
    
    thresholds = []
    for key, value in qualification_info.items():
        if key == 'Hold for 1st':
            thresholds.append(f'🥇 1st: {value}')
        elif key == 'Hold for 2nd':
            thresholds.append(f'🥈 2nd: {value}')
        elif key == 'Hold for 3rd':
            thresholds.append(f'🥉 3rd: {value}')
        elif key in ['Hold to Qualify', 'Min to Qualify']:
            thresholds.append(f'🎯 Target: {value}')
    
    if thresholds:
        return f"<br><div class='targets'><strong>Targets:</strong> {' | '.join(thresholds)}</div>"
    return ""


def determine_lead_athlete_status(status: str, has_score: bool) -> Tuple[str, str]:
    """Determine lead athlete status and styling"""
    if not has_score:
        return "", "📄"
    
    if "Qualified" in status or "✓✓" in status:
        return "qualified", "✅"
    elif "Eliminated" in status or "✗" in status:
        return "eliminated", "❌"
    elif "Podium" in status and "No Podium" not in status and "Contention" not in status:
        return "podium-position", "🏆"
    elif "Podium Contention" in status or "Contention" in status:
        return "podium-contention", "⚠️"
    elif "No Podium" in status:
        return "no-podium", "❌"
    else:
        return "", "📄"


def get_lead_position_emoji(rank: any, has_score: bool, card_class: str, status_emoji: str) -> str:
    """Get position emoji for lead athletes"""
    rank_num = DataProcessor.safe_numeric_conversion(rank)
    if rank_num > 0:
        return status_emoji if has_score and card_class else f"#{rank_num}"
    return "📄"


def format_worst_finish(worst_finish: any, has_score: bool) -> str:
    """Format worst finish display"""
    if not has_score or worst_finish in ['N/A', '', None] or pd.isna(worst_finish):
        return ""
    
    worst_finish_clean = DataProcessor.clean_text(str(worst_finish))
    return f" | Worst Finish: {worst_finish_clean}" if worst_finish_clean and worst_finish_clean != '-' else ""


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"🚫 Application Error: {e}")
        st.markdown("Please refresh the page or contact support if the issue persists.")
        
        with st.expander("🔧 Debug Information"):
            st.code(f"Error: {e}")
            st.code(f"Time: {datetime.now()}")
            import traceback
            st.code(traceback.format_exc()), na=False)) &      # Remove "25+" style entries
            (~df['Name'].apply(is_placeholder_athlete))
        ]
        
        # Second pass: If we have rank information, use it to filter properly
        if 'Current Rank' in filtered_df.columns:
            filtered_df['temp_rank'] = pd.to_numeric(filtered_df['Current Rank'], errors='coerce')
            
            # Keep only rows with valid ranks within expected range
            ranked_df = filtered_df[
                (filtered_df['temp_rank'].notna()) & 
                (filtered_df['temp_rank'] >= 1) & 
                (filtered_df['temp_rank'] <= expected_max)
            ]
            
            if len(ranked_df) > 0:
                # Sort by rank and take only the expected number
                ranked_df = ranked_df.sort_values('temp_rank').head(expected_max)
                filtered_df = ranked_df.drop('temp_rank', axis=1)
            else:
                # If no valid ranks, fall back to manual filtering
                filtered_df = manual_athlete_filter(filtered_df, expected_max)
        else:
            # No rank column available, use manual filtering
            filtered_df = manual_athlete_filter(filtered_df, expected_max)
        
        # Third pass: Additional validation for lead competitions
        if "Lead" in competition_name:
            filtered_df = validate_lead_athletes(filtered_df, expected_max)
        
        logger.info(f"Filtered to {len(filtered_df)} athletes for {competition_name} (expected: {expected_max})")
        return filtered_df
        
    except Exception as e:
        logger.error(f"Error filtering athletes for {competition_name}: {e}")
        # Fallback to basic filtering with count limit
        basic_filtered = df[
            df['Name'].notna() & 
            (df['Name'] != '') &
            (~df['Name'].astype(str).str.contains('Hold for', na=False))
        ].head(expected_max)
        return basic_filtered


def manual_athlete_filter(df: pd.DataFrame, expected_max: int) -> pd.DataFrame:
    """Manually filter athletes when rank information is not reliable"""
    # Look for patterns that indicate real athlete names vs reference data
    potential_athletes = []
    
    for idx, row in df.iterrows():
        name = str(row.get('Name', '')).strip()
        
        # Skip if name looks like reference data
        if any(keyword in name.lower() for keyword in [
            'hold', 'min', 'max', 'qualification', 'threshold', 'zone', 'top',
            'points', 'score', 'rank', 'position', 'place', 'finish'
        ]):
            continue
        
        # Skip if name is too short or looks like a number/code
        if len(name) < 3 or name.isdigit() or not any(c.isalpha() for c in name):
            continue
        
        # Look for typical athlete name patterns (First Last or similar)
        name_parts = name.split()
        if len(name_parts) >= 2 and all(part.isalpha() or part.replace('.', '').isalpha() for part in name_parts):
            potential_athletes.append(idx)
        elif len(name_parts) == 1 and len(name) > 4 and name.isalpha():
            # Single names that are long enough and all letters
            potential_athletes.append(idx)
    
    # Return the filtered dataframe, limited to expected count
    return df.loc[potential_athletes[:expected_max]]


def validate_lead_athletes(df: pd.DataFrame, expected_max: int) -> pd.DataFrame:
    """Additional validation specifically for lead competitions"""
    if len(df) <= expected_max:
        return df
    
    # For lead competitions, prioritize athletes with actual climbing data
    scored_athletes = df[df['Manual Score'].notna() & (df['Manual Score'] != '')].copy()
    unscored_athletes = df[df['Manual Score'].isna() | (df['Manual Score'] == '')].copy()
    
    # Combine scored athletes first, then fill with unscored up to limit
    result_df = scored_athletes.copy()
    remaining_slots = expected_max - len(scored_athletes)
    
    if remaining_slots > 0 and len(unscored_athletes) > 0:
        result_df = pd.concat([result_df, unscored_athletes.head(remaining_slots)], ignore_index=True)
    
    return result_df.head(expected_max)


def is_placeholder_athlete(name: str) -> bool:
    """Check if name is a placeholder like 'Athlete 1', 'Athlete 23', etc."""
    name_str = str(name).strip()
    if name_str.startswith('Athlete '):
        remaining = name_str[8:].strip()
        return remaining.isdigit()
    return False


def display_qualification_thresholds(qualification_info: Dict[str, str]):
    """Display qualification thresholds if available"""
    if qualification_info:
        threshold_items = []
        threshold_mapping = {
            'Hold for 1st': ('🥇 1st', '#FFD700'),
            'Hold for 2nd': ('🥈 2nd', '#C0C0C0'),
            'Hold for 3rd': ('🥉 3rd', '#CD7F32'),
            'Hold to Qualify': ('✅ Qualify', '#28a745'),
            'Min to Qualify': ('⚠️ Min', '#ffc107')
        }
        
        for key, value in qualification_info.items():
            if key in threshold_mapping:
                label, color = threshold_mapping[key]
                threshold_items.append(f'<span style="color: {color}; font-weight: bold;">{label}: {value}</span>')
        
        if threshold_items:
            st.markdown(f"""
            <div class="threshold-card">
                <h5>🎯 Qualification Thresholds</h5>
                {' | '.join(threshold_items)}
            </div>
            """, unsafe_allow_html=True)


def display_lead_athletes(active_df: pd.DataFrame, qualification_info: Dict[str, str]):
    """Display lead competition athletes with enhanced formatting"""
    # Sort by rank if available
    try:
        if 'Current Rank' in active_df.columns:
            active_df['Current Rank'] = pd.to_numeric(active_df['Current Rank'], errors='coerce')
            active_df = active_df.sort_values('Current Rank', ascending=True).reset_index(drop=True)
    except Exception as e:
        logger.warning(f"Could not sort by rank: {e}")
    
    # Display athlete cards
    for _, row in active_df.iterrows():
        name = DataProcessor.clean_text(str(row.get('Name', 'Unknown')))
        score = row.get('Manual Score', 'N/A')
        rank = row.get('Current Rank', 'N/A')
        status = DataProcessor.clean_text(str(row.get('Status', 'Unknown')))
        worst_finish = row.get('Worst Finish', 'N/A')
        
        # Determine if athlete has a score
        has_score = score not in ['N/A', '', None] and not pd.isna(score)
        
        # Create threshold display for athletes without scores
        threshold_display = create_threshold_display(has_score, qualification_info)
        
        # Determine card styling
        card_class, status_emoji = determine_lead_athlete_status(status, has_score)
        
        # Set position emoji
        position_emoji = get_lead_position_emoji(rank, has_score, card_class, status_emoji)
        
        # Format displays
        score_display = score if has_score else "Awaiting Result"
        worst_finish_display = format_worst_finish(worst_finish, has_score)
        
        # Create athlete card
        st.markdown(f"""
        <div class="athlete-row {card_class}">
            <strong>{position_emoji} #{rank} - {name}</strong><br>
            <small>Score: {score_display} | Status: {status}{worst_finish_display}</small>{threshold_display}
        </div>
        """, unsafe_allow_html=True)


def create_threshold_display(has_score: bool, qualification_info: Dict[str, str]) -> str:
    """Create threshold display for athletes without scores"""
    if has_score or not qualification_info:
        return ""
    
    thresholds = []
    for key, value in qualification_info.items():
        if key == 'Hold for 1st':
            thresholds.append(f'🥇 1st: {value}')
        elif key == 'Hold for 2nd':
            thresholds.append(f'🥈 2nd: {value}')
        elif key == 'Hold for 3rd':
            thresholds.append(f'🥉 3rd: {value}')
        elif key in ['Hold to Qualify', 'Min to Qualify']:
            thresholds.append(f'🎯 Target: {value}')
    
    if thresholds:
        return f"<br><div class='targets'><strong>Targets:</strong> {' | '.join(thresholds)}</div>"
    return ""


def determine_lead_athlete_status(status: str, has_score: bool) -> Tuple[str, str]:
    """Determine lead athlete status and styling"""
    if not has_score:
        return "", "📄"
    
    if "Qualified" in status or "✓✓" in status:
        return "qualified", "✅"
    elif "Eliminated" in status or "✗" in status:
        return "eliminated", "❌"
    elif "Podium" in status and "No Podium" not in status and "Contention" not in status:
        return "podium-position", "🏆"
    elif "Podium Contention" in status or "Contention" in status:
        return "podium-contention", "⚠️"
    elif "No Podium" in status:
        return "no-podium", "❌"
    else:
        return "", "📄"


def get_lead_position_emoji(rank: any, has_score: bool, card_class: str, status_emoji: str) -> str:
    """Get position emoji for lead athletes"""
    rank_num = DataProcessor.safe_numeric_conversion(rank)
    if rank_num > 0:
        return status_emoji if has_score and card_class else f"#{rank_num}"
    return "📄"


def format_worst_finish(worst_finish: any, has_score: bool) -> str:
    """Format worst finish display"""
    if not has_score or worst_finish in ['N/A', '', None] or pd.isna(worst_finish):
        return ""
    
    worst_finish_clean = DataProcessor.clean_text(str(worst_finish))
    return f" | Worst Finish: {worst_finish_clean}" if worst_finish_clean and worst_finish_clean != '-' else ""


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"🚫 Application Error: {e}")
        st.markdown("Please refresh the page or contact support if the issue persists.")
        
        with st.expander("🔧 Debug Information"):
            st.code(f"Error: {e}")
            st.code(f"Time: {datetime.now()}")
            import traceback
            st.code(traceback.format_exc()),               # To be determined/announced
        r'^n\/a$|^na


def display_qualification_thresholds(qualification_info: Dict[str, str]):
    """Display qualification thresholds if available"""
    if qualification_info:
        threshold_items = []
        threshold_mapping = {
            'Hold for 1st': ('🥇 1st', '#FFD700'),
            'Hold for 2nd': ('🥈 2nd', '#C0C0C0'),
            'Hold for 3rd': ('🥉 3rd', '#CD7F32'),
            'Hold to Qualify': ('✅ Qualify', '#28a745'),
            'Min to Qualify': ('⚠️ Min', '#ffc107')
        }
        
        for key, value in qualification_info.items():
            if key in threshold_mapping:
                label, color = threshold_mapping[key]
                threshold_items.append(f'<span style="color: {color}; font-weight: bold;">{label}: {value}</span>')
        
        if threshold_items:
            st.markdown(f"""
            <div class="threshold-card">
                <h5>🎯 Qualification Thresholds</h5>
                {' | '.join(threshold_items)}
            </div>
            """, unsafe_allow_html=True)


def display_lead_athletes(active_df: pd.DataFrame, qualification_info: Dict[str, str]):
    """Display lead competition athletes with enhanced formatting"""
    # Sort by rank if available
    try:
        if 'Current Rank' in active_df.columns:
            active_df['Current Rank'] = pd.to_numeric(active_df['Current Rank'], errors='coerce')
            active_df = active_df.sort_values('Current Rank', ascending=True).reset_index(drop=True)
    except Exception as e:
        logger.warning(f"Could not sort by rank: {e}")
    
    # Display athlete cards
    for _, row in active_df.iterrows():
        name = DataProcessor.clean_text(str(row.get('Name', 'Unknown')))
        score = row.get('Manual Score', 'N/A')
        rank = row.get('Current Rank', 'N/A')
        status = DataProcessor.clean_text(str(row.get('Status', 'Unknown')))
        worst_finish = row.get('Worst Finish', 'N/A')
        
        # Determine if athlete has a score
        has_score = score not in ['N/A', '', None] and not pd.isna(score)
        
        # Create threshold display for athletes without scores
        threshold_display = create_threshold_display(has_score, qualification_info)
        
        # Determine card styling
        card_class, status_emoji = determine_lead_athlete_status(status, has_score)
        
        # Set position emoji
        position_emoji = get_lead_position_emoji(rank, has_score, card_class, status_emoji)
        
        # Format displays
        score_display = score if has_score else "Awaiting Result"
        worst_finish_display = format_worst_finish(worst_finish, has_score)
        
        # Create athlete card
        st.markdown(f"""
        <div class="athlete-row {card_class}">
            <strong>{position_emoji} #{rank} - {name}</strong><br>
            <small>Score: {score_display} | Status: {status}{worst_finish_display}</small>{threshold_display}
        </div>
        """, unsafe_allow_html=True)


def create_threshold_display(has_score: bool, qualification_info: Dict[str, str]) -> str:
    """Create threshold display for athletes without scores"""
    if has_score or not qualification_info:
        return ""
    
    thresholds = []
    for key, value in qualification_info.items():
        if key == 'Hold for 1st':
            thresholds.append(f'🥇 1st: {value}')
        elif key == 'Hold for 2nd':
            thresholds.append(f'🥈 2nd: {value}')
        elif key == 'Hold for 3rd':
            thresholds.append(f'🥉 3rd: {value}')
        elif key in ['Hold to Qualify', 'Min to Qualify']:
            thresholds.append(f'🎯 Target: {value}')
    
    if thresholds:
        return f"<br><div class='targets'><strong>Targets:</strong> {' | '.join(thresholds)}</div>"
    return ""


def determine_lead_athlete_status(status: str, has_score: bool) -> Tuple[str, str]:
    """Determine lead athlete status and styling"""
    if not has_score:
        return "", "📄"
    
    if "Qualified" in status or "✓✓" in status:
        return "qualified", "✅"
    elif "Eliminated" in status or "✗" in status:
        return "eliminated", "❌"
    elif "Podium" in status and "No Podium" not in status and "Contention" not in status:
        return "podium-position", "🏆"
    elif "Podium Contention" in status or "Contention" in status:
        return "podium-contention", "⚠️"
    elif "No Podium" in status:
        return "no-podium", "❌"
    else:
        return "", "📄"


def get_lead_position_emoji(rank: any, has_score: bool, card_class: str, status_emoji: str) -> str:
    """Get position emoji for lead athletes"""
    rank_num = DataProcessor.safe_numeric_conversion(rank)
    if rank_num > 0:
        return status_emoji if has_score and card_class else f"#{rank_num}"
    return "📄"


def format_worst_finish(worst_finish: any, has_score: bool) -> str:
    """Format worst finish display"""
    if not has_score or worst_finish in ['N/A', '', None] or pd.isna(worst_finish):
        return ""
    
    worst_finish_clean = DataProcessor.clean_text(str(worst_finish))
    return f" | Worst Finish: {worst_finish_clean}" if worst_finish_clean and worst_finish_clean != '-' else ""


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"🚫 Application Error: {e}")
        st.markdown("Please refresh the page or contact support if the issue persists.")
        
        with st.expander("🔧 Debug Information"):
            st.code(f"Error: {e}")
            st.code(f"Time: {datetime.now()}")
            import traceback
            st.code(traceback.format_exc()), na=False)) &  # Remove pure numbers
            (~df['Name'].astype(str).str.match(r'^\d+\+


def is_placeholder_athlete(name: str) -> bool:
    """Check if name is a placeholder like 'Athlete 1', 'Athlete 23', etc."""
    name_str = str(name).strip()
    if name_str.startswith('Athlete '):
        remaining = name_str[8:].strip()
        return remaining.isdigit()
    return False


def display_qualification_thresholds(qualification_info: Dict[str, str]):
    """Display qualification thresholds if available"""
    if qualification_info:
        threshold_items = []
        threshold_mapping = {
            'Hold for 1st': ('🥇 1st', '#FFD700'),
            'Hold for 2nd': ('🥈 2nd', '#C0C0C0'),
            'Hold for 3rd': ('🥉 3rd', '#CD7F32'),
            'Hold to Qualify': ('✅ Qualify', '#28a745'),
            'Min to Qualify': ('⚠️ Min', '#ffc107')
        }
        
        for key, value in qualification_info.items():
            if key in threshold_mapping:
                label, color = threshold_mapping[key]
                threshold_items.append(f'<span style="color: {color}; font-weight: bold;">{label}: {value}</span>')
        
        if threshold_items:
            st.markdown(f"""
            <div class="threshold-card">
                <h5>🎯 Qualification Thresholds</h5>
                {' | '.join(threshold_items)}
            </div>
            """, unsafe_allow_html=True)


def display_lead_athletes(active_df: pd.DataFrame, qualification_info: Dict[str, str]):
    """Display lead competition athletes with enhanced formatting"""
    # Sort by rank if available
    try:
        if 'Current Rank' in active_df.columns:
            active_df['Current Rank'] = pd.to_numeric(active_df['Current Rank'], errors='coerce')
            active_df = active_df.sort_values('Current Rank', ascending=True).reset_index(drop=True)
    except Exception as e:
        logger.warning(f"Could not sort by rank: {e}")
    
    # Display athlete cards
    for _, row in active_df.iterrows():
        name = DataProcessor.clean_text(str(row.get('Name', 'Unknown')))
        score = row.get('Manual Score', 'N/A')
        rank = row.get('Current Rank', 'N/A')
        status = DataProcessor.clean_text(str(row.get('Status', 'Unknown')))
        worst_finish = row.get('Worst Finish', 'N/A')
        
        # Determine if athlete has a score
        has_score = score not in ['N/A', '', None] and not pd.isna(score)
        
        # Create threshold display for athletes without scores
        threshold_display = create_threshold_display(has_score, qualification_info)
        
        # Determine card styling
        card_class, status_emoji = determine_lead_athlete_status(status, has_score)
        
        # Set position emoji
        position_emoji = get_lead_position_emoji(rank, has_score, card_class, status_emoji)
        
        # Format displays
        score_display = score if has_score else "Awaiting Result"
        worst_finish_display = format_worst_finish(worst_finish, has_score)
        
        # Create athlete card
        st.markdown(f"""
        <div class="athlete-row {card_class}">
            <strong>{position_emoji} #{rank} - {name}</strong><br>
            <small>Score: {score_display} | Status: {status}{worst_finish_display}</small>{threshold_display}
        </div>
        """, unsafe_allow_html=True)


def create_threshold_display(has_score: bool, qualification_info: Dict[str, str]) -> str:
    """Create threshold display for athletes without scores"""
    if has_score or not qualification_info:
        return ""
    
    thresholds = []
    for key, value in qualification_info.items():
        if key == 'Hold for 1st':
            thresholds.append(f'🥇 1st: {value}')
        elif key == 'Hold for 2nd':
            thresholds.append(f'🥈 2nd: {value}')
        elif key == 'Hold for 3rd':
            thresholds.append(f'🥉 3rd: {value}')
        elif key in ['Hold to Qualify', 'Min to Qualify']:
            thresholds.append(f'🎯 Target: {value}')
    
    if thresholds:
        return f"<br><div class='targets'><strong>Targets:</strong> {' | '.join(thresholds)}</div>"
    return ""


def determine_lead_athlete_status(status: str, has_score: bool) -> Tuple[str, str]:
    """Determine lead athlete status and styling"""
    if not has_score:
        return "", "📄"
    
    if "Qualified" in status or "✓✓" in status:
        return "qualified", "✅"
    elif "Eliminated" in status or "✗" in status:
        return "eliminated", "❌"
    elif "Podium" in status and "No Podium" not in status and "Contention" not in status:
        return "podium-position", "🏆"
    elif "Podium Contention" in status or "Contention" in status:
        return "podium-contention", "⚠️"
    elif "No Podium" in status:
        return "no-podium", "❌"
    else:
        return "", "📄"


def get_lead_position_emoji(rank: any, has_score: bool, card_class: str, status_emoji: str) -> str:
    """Get position emoji for lead athletes"""
    rank_num = DataProcessor.safe_numeric_conversion(rank)
    if rank_num > 0:
        return status_emoji if has_score and card_class else f"#{rank_num}"
    return "📄"


def format_worst_finish(worst_finish: any, has_score: bool) -> str:
    """Format worst finish display"""
    if not has_score or worst_finish in ['N/A', '', None] or pd.isna(worst_finish):
        return ""
    
    worst_finish_clean = DataProcessor.clean_text(str(worst_finish))
    return f" | Worst Finish: {worst_finish_clean}" if worst_finish_clean and worst_finish_clean != '-' else ""


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"🚫 Application Error: {e}")
        st.markdown("Please refresh the page or contact support if the issue persists.")
        
        with st.expander("🔧 Debug Information"):
            st.code(f"Error: {e}")
            st.code(f"Time: {datetime.now()}")
            import traceback
            st.code(traceback.format_exc()), na=False)) &      # Remove "25+" style entries
            (~df['Name'].apply(is_placeholder_athlete))
        ]
        
        # Second pass: If we have rank information, use it to filter properly
        if 'Current Rank' in filtered_df.columns:
            filtered_df['temp_rank'] = pd.to_numeric(filtered_df['Current Rank'], errors='coerce')
            
            # Keep only rows with valid ranks within expected range
            ranked_df = filtered_df[
                (filtered_df['temp_rank'].notna()) & 
                (filtered_df['temp_rank'] >= 1) & 
                (filtered_df['temp_rank'] <= expected_max)
            ]
            
            if len(ranked_df) > 0:
                # Sort by rank and take only the expected number
                ranked_df = ranked_df.sort_values('temp_rank').head(expected_max)
                filtered_df = ranked_df.drop('temp_rank', axis=1)
            else:
                # If no valid ranks, fall back to manual filtering
                filtered_df = manual_athlete_filter(filtered_df, expected_max)
        else:
            # No rank column available, use manual filtering
            filtered_df = manual_athlete_filter(filtered_df, expected_max)
        
        # Third pass: Additional validation for lead competitions
        if "Lead" in competition_name:
            filtered_df = validate_lead_athletes(filtered_df, expected_max)
        
        logger.info(f"Filtered to {len(filtered_df)} athletes for {competition_name} (expected: {expected_max})")
        return filtered_df
        
    except Exception as e:
        logger.error(f"Error filtering athletes for {competition_name}: {e}")
        # Fallback to basic filtering with count limit
        basic_filtered = df[
            df['Name'].notna() & 
            (df['Name'] != '') &
            (~df['Name'].astype(str).str.contains('Hold for', na=False))
        ].head(expected_max)
        return basic_filtered


def manual_athlete_filter(df: pd.DataFrame, expected_max: int) -> pd.DataFrame:
    """Manually filter athletes when rank information is not reliable"""
    # Look for patterns that indicate real athlete names vs reference data
    potential_athletes = []
    
    for idx, row in df.iterrows():
        name = str(row.get('Name', '')).strip()
        
        # Skip if name looks like reference data
        if any(keyword in name.lower() for keyword in [
            'hold', 'min', 'max', 'qualification', 'threshold', 'zone', 'top',
            'points', 'score', 'rank', 'position', 'place', 'finish'
        ]):
            continue
        
        # Skip if name is too short or looks like a number/code
        if len(name) < 3 or name.isdigit() or not any(c.isalpha() for c in name):
            continue
        
        # Look for typical athlete name patterns (First Last or similar)
        name_parts = name.split()
        if len(name_parts) >= 2 and all(part.isalpha() or part.replace('.', '').isalpha() for part in name_parts):
            potential_athletes.append(idx)
        elif len(name_parts) == 1 and len(name) > 4 and name.isalpha():
            # Single names that are long enough and all letters
            potential_athletes.append(idx)
    
    # Return the filtered dataframe, limited to expected count
    return df.loc[potential_athletes[:expected_max]]


def validate_lead_athletes(df: pd.DataFrame, expected_max: int) -> pd.DataFrame:
    """Additional validation specifically for lead competitions"""
    if len(df) <= expected_max:
        return df
    
    # For lead competitions, prioritize athletes with actual climbing data
    scored_athletes = df[df['Manual Score'].notna() & (df['Manual Score'] != '')].copy()
    unscored_athletes = df[df['Manual Score'].isna() | (df['Manual Score'] == '')].copy()
    
    # Combine scored athletes first, then fill with unscored up to limit
    result_df = scored_athletes.copy()
    remaining_slots = expected_max - len(scored_athletes)
    
    if remaining_slots > 0 and len(unscored_athletes) > 0:
        result_df = pd.concat([result_df, unscored_athletes.head(remaining_slots)], ignore_index=True)
    
    return result_df.head(expected_max)


def is_placeholder_athlete(name: str) -> bool:
    """Check if name is a placeholder like 'Athlete 1', 'Athlete 23', etc."""
    name_str = str(name).strip()
    if name_str.startswith('Athlete '):
        remaining = name_str[8:].strip()
        return remaining.isdigit()
    return False


def display_qualification_thresholds(qualification_info: Dict[str, str]):
    """Display qualification thresholds if available"""
    if qualification_info:
        threshold_items = []
        threshold_mapping = {
            'Hold for 1st': ('🥇 1st', '#FFD700'),
            'Hold for 2nd': ('🥈 2nd', '#C0C0C0'),
            'Hold for 3rd': ('🥉 3rd', '#CD7F32'),
            'Hold to Qualify': ('✅ Qualify', '#28a745'),
            'Min to Qualify': ('⚠️ Min', '#ffc107')
        }
        
        for key, value in qualification_info.items():
            if key in threshold_mapping:
                label, color = threshold_mapping[key]
                threshold_items.append(f'<span style="color: {color}; font-weight: bold;">{label}: {value}</span>')
        
        if threshold_items:
            st.markdown(f"""
            <div class="threshold-card">
                <h5>🎯 Qualification Thresholds</h5>
                {' | '.join(threshold_items)}
            </div>
            """, unsafe_allow_html=True)


def display_lead_athletes(active_df: pd.DataFrame, qualification_info: Dict[str, str]):
    """Display lead competition athletes with enhanced formatting"""
    # Sort by rank if available
    try:
        if 'Current Rank' in active_df.columns:
            active_df['Current Rank'] = pd.to_numeric(active_df['Current Rank'], errors='coerce')
            active_df = active_df.sort_values('Current Rank', ascending=True).reset_index(drop=True)
    except Exception as e:
        logger.warning(f"Could not sort by rank: {e}")
    
    # Display athlete cards
    for _, row in active_df.iterrows():
        name = DataProcessor.clean_text(str(row.get('Name', 'Unknown')))
        score = row.get('Manual Score', 'N/A')
        rank = row.get('Current Rank', 'N/A')
        status = DataProcessor.clean_text(str(row.get('Status', 'Unknown')))
        worst_finish = row.get('Worst Finish', 'N/A')
        
        # Determine if athlete has a score
        has_score = score not in ['N/A', '', None] and not pd.isna(score)
        
        # Create threshold display for athletes without scores
        threshold_display = create_threshold_display(has_score, qualification_info)
        
        # Determine card styling
        card_class, status_emoji = determine_lead_athlete_status(status, has_score)
        
        # Set position emoji
        position_emoji = get_lead_position_emoji(rank, has_score, card_class, status_emoji)
        
        # Format displays
        score_display = score if has_score else "Awaiting Result"
        worst_finish_display = format_worst_finish(worst_finish, has_score)
        
        # Create athlete card
        st.markdown(f"""
        <div class="athlete-row {card_class}">
            <strong>{position_emoji} #{rank} - {name}</strong><br>
            <small>Score: {score_display} | Status: {status}{worst_finish_display}</small>{threshold_display}
        </div>
        """, unsafe_allow_html=True)


def create_threshold_display(has_score: bool, qualification_info: Dict[str, str]) -> str:
    """Create threshold display for athletes without scores"""
    if has_score or not qualification_info:
        return ""
    
    thresholds = []
    for key, value in qualification_info.items():
        if key == 'Hold for 1st':
            thresholds.append(f'🥇 1st: {value}')
        elif key == 'Hold for 2nd':
            thresholds.append(f'🥈 2nd: {value}')
        elif key == 'Hold for 3rd':
            thresholds.append(f'🥉 3rd: {value}')
        elif key in ['Hold to Qualify', 'Min to Qualify']:
            thresholds.append(f'🎯 Target: {value}')
    
    if thresholds:
        return f"<br><div class='targets'><strong>Targets:</strong> {' | '.join(thresholds)}</div>"
    return ""


def determine_lead_athlete_status(status: str, has_score: bool) -> Tuple[str, str]:
    """Determine lead athlete status and styling"""
    if not has_score:
        return "", "📄"
    
    if "Qualified" in status or "✓✓" in status:
        return "qualified", "✅"
    elif "Eliminated" in status or "✗" in status:
        return "eliminated", "❌"
    elif "Podium" in status and "No Podium" not in status and "Contention" not in status:
        return "podium-position", "🏆"
    elif "Podium Contention" in status or "Contention" in status:
        return "podium-contention", "⚠️"
    elif "No Podium" in status:
        return "no-podium", "❌"
    else:
        return "", "📄"


def get_lead_position_emoji(rank: any, has_score: bool, card_class: str, status_emoji: str) -> str:
    """Get position emoji for lead athletes"""
    rank_num = DataProcessor.safe_numeric_conversion(rank)
    if rank_num > 0:
        return status_emoji if has_score and card_class else f"#{rank_num}"
    return "📄"


def format_worst_finish(worst_finish: any, has_score: bool) -> str:
    """Format worst finish display"""
    if not has_score or worst_finish in ['N/A', '', None] or pd.isna(worst_finish):
        return ""
    
    worst_finish_clean = DataProcessor.clean_text(str(worst_finish))
    return f" | Worst Finish: {worst_finish_clean}" if worst_finish_clean and worst_finish_clean != '-' else ""


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"🚫 Application Error: {e}")
        st.markdown("Please refresh the page or contact support if the issue persists.")
        
        with st.expander("🔧 Debug Information"):
            st.code(f"Error: {e}")
            st.code(f"Time: {datetime.now()}")
            import traceback
            st.code(traceback.format_exc()),               # Not available
        r'^hold\s+\d+',               # "Hold 25"
        r'^zone\s+\d+',               # "Zone 40"
        r'^top\s+\d+',                # "Top 50"
        r'qualification|threshold',    # Reference text
        r'worst|best|average',        # Statistical text
        r'points|score|rank',         # Score-related text
    ]
    
    # Check against patterns
    import re
    for pattern in placeholder_patterns:
        if re.match(pattern, name_str):
            return True
    
    # Check for very short names (likely not real names)
    if len(name_str) < 3:
        return True
    
    # Check if name contains no letters (likely not a real name)
    if not any(c.isalpha() for c in name_str):
        return True
    
    return False


def display_qualification_thresholds(qualification_info: Dict[str, str]):
    """Display qualification thresholds if available"""
    if qualification_info:
        threshold_items = []
        threshold_mapping = {
            'Hold for 1st': ('🥇 1st', '#FFD700'),
            'Hold for 2nd': ('🥈 2nd', '#C0C0C0'),
            'Hold for 3rd': ('🥉 3rd', '#CD7F32'),
            'Hold to Qualify': ('✅ Qualify', '#28a745'),
            'Min to Qualify': ('⚠️ Min', '#ffc107')
        }
        
        for key, value in qualification_info.items():
            if key in threshold_mapping:
                label, color = threshold_mapping[key]
                threshold_items.append(f'<span style="color: {color}; font-weight: bold;">{label}: {value}</span>')
        
        if threshold_items:
            st.markdown(f"""
            <div class="threshold-card">
                <h5>🎯 Qualification Thresholds</h5>
                {' | '.join(threshold_items)}
            </div>
            """, unsafe_allow_html=True)


def display_lead_athletes(active_df: pd.DataFrame, qualification_info: Dict[str, str]):
    """Display lead competition athletes with enhanced formatting"""
    # Sort by rank if available
    try:
        if 'Current Rank' in active_df.columns:
            active_df['Current Rank'] = pd.to_numeric(active_df['Current Rank'], errors='coerce')
            active_df = active_df.sort_values('Current Rank', ascending=True).reset_index(drop=True)
    except Exception as e:
        logger.warning(f"Could not sort by rank: {e}")
    
    # Display athlete cards
    for _, row in active_df.iterrows():
        name = DataProcessor.clean_text(str(row.get('Name', 'Unknown')))
        score = row.get('Manual Score', 'N/A')
        rank = row.get('Current Rank', 'N/A')
        status = DataProcessor.clean_text(str(row.get('Status', 'Unknown')))
        worst_finish = row.get('Worst Finish', 'N/A')
        
        # Determine if athlete has a score
        has_score = score not in ['N/A', '', None] and not pd.isna(score)
        
        # Create threshold display for athletes without scores
        threshold_display = create_threshold_display(has_score, qualification_info)
        
        # Determine card styling
        card_class, status_emoji = determine_lead_athlete_status(status, has_score)
        
        # Set position emoji
        position_emoji = get_lead_position_emoji(rank, has_score, card_class, status_emoji)
        
        # Format displays
        score_display = score if has_score else "Awaiting Result"
        worst_finish_display = format_worst_finish(worst_finish, has_score)
        
        # Create athlete card
        st.markdown(f"""
        <div class="athlete-row {card_class}">
            <strong>{position_emoji} #{rank} - {name}</strong><br>
            <small>Score: {score_display} | Status: {status}{worst_finish_display}</small>{threshold_display}
        </div>
        """, unsafe_allow_html=True)


def create_threshold_display(has_score: bool, qualification_info: Dict[str, str]) -> str:
    """Create threshold display for athletes without scores"""
    if has_score or not qualification_info:
        return ""
    
    thresholds = []
    for key, value in qualification_info.items():
        if key == 'Hold for 1st':
            thresholds.append(f'🥇 1st: {value}')
        elif key == 'Hold for 2nd':
            thresholds.append(f'🥈 2nd: {value}')
        elif key == 'Hold for 3rd':
            thresholds.append(f'🥉 3rd: {value}')
        elif key in ['Hold to Qualify', 'Min to Qualify']:
            thresholds.append(f'🎯 Target: {value}')
    
    if thresholds:
        return f"<br><div class='targets'><strong>Targets:</strong> {' | '.join(thresholds)}</div>"
    return ""


def determine_lead_athlete_status(status: str, has_score: bool) -> Tuple[str, str]:
    """Determine lead athlete status and styling"""
    if not has_score:
        return "", "📄"
    
    if "Qualified" in status or "✓✓" in status:
        return "qualified", "✅"
    elif "Eliminated" in status or "✗" in status:
        return "eliminated", "❌"
    elif "Podium" in status and "No Podium" not in status and "Contention" not in status:
        return "podium-position", "🏆"
    elif "Podium Contention" in status or "Contention" in status:
        return "podium-contention", "⚠️"
    elif "No Podium" in status:
        return "no-podium", "❌"
    else:
        return "", "📄"


def get_lead_position_emoji(rank: any, has_score: bool, card_class: str, status_emoji: str) -> str:
    """Get position emoji for lead athletes"""
    rank_num = DataProcessor.safe_numeric_conversion(rank)
    if rank_num > 0:
        return status_emoji if has_score and card_class else f"#{rank_num}"
    return "📄"


def format_worst_finish(worst_finish: any, has_score: bool) -> str:
    """Format worst finish display"""
    if not has_score or worst_finish in ['N/A', '', None] or pd.isna(worst_finish):
        return ""
    
    worst_finish_clean = DataProcessor.clean_text(str(worst_finish))
    return f" | Worst Finish: {worst_finish_clean}" if worst_finish_clean and worst_finish_clean != '-' else ""


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"🚫 Application Error: {e}")
        st.markdown("Please refresh the page or contact support if the issue persists.")
        
        with st.expander("🔧 Debug Information"):
            st.code(f"Error: {e}")
            st.code(f"Time: {datetime.now()}")
            import traceback
            st.code(traceback.format_exc()), na=False)) &  # Remove pure numbers
            (~df['Name'].astype(str).str.match(r'^\d+\+


def is_placeholder_athlete(name: str) -> bool:
    """Check if name is a placeholder like 'Athlete 1', 'Athlete 23', etc."""
    name_str = str(name).strip()
    if name_str.startswith('Athlete '):
        remaining = name_str[8:].strip()
        return remaining.isdigit()
    return False


def display_qualification_thresholds(qualification_info: Dict[str, str]):
    """Display qualification thresholds if available"""
    if qualification_info:
        threshold_items = []
        threshold_mapping = {
            'Hold for 1st': ('🥇 1st', '#FFD700'),
            'Hold for 2nd': ('🥈 2nd', '#C0C0C0'),
            'Hold for 3rd': ('🥉 3rd', '#CD7F32'),
            'Hold to Qualify': ('✅ Qualify', '#28a745'),
            'Min to Qualify': ('⚠️ Min', '#ffc107')
        }
        
        for key, value in qualification_info.items():
            if key in threshold_mapping:
                label, color = threshold_mapping[key]
                threshold_items.append(f'<span style="color: {color}; font-weight: bold;">{label}: {value}</span>')
        
        if threshold_items:
            st.markdown(f"""
            <div class="threshold-card">
                <h5>🎯 Qualification Thresholds</h5>
                {' | '.join(threshold_items)}
            </div>
            """, unsafe_allow_html=True)


def display_lead_athletes(active_df: pd.DataFrame, qualification_info: Dict[str, str]):
    """Display lead competition athletes with enhanced formatting"""
    # Sort by rank if available
    try:
        if 'Current Rank' in active_df.columns:
            active_df['Current Rank'] = pd.to_numeric(active_df['Current Rank'], errors='coerce')
            active_df = active_df.sort_values('Current Rank', ascending=True).reset_index(drop=True)
    except Exception as e:
        logger.warning(f"Could not sort by rank: {e}")
    
    # Display athlete cards
    for _, row in active_df.iterrows():
        name = DataProcessor.clean_text(str(row.get('Name', 'Unknown')))
        score = row.get('Manual Score', 'N/A')
        rank = row.get('Current Rank', 'N/A')
        status = DataProcessor.clean_text(str(row.get('Status', 'Unknown')))
        worst_finish = row.get('Worst Finish', 'N/A')
        
        # Determine if athlete has a score
        has_score = score not in ['N/A', '', None] and not pd.isna(score)
        
        # Create threshold display for athletes without scores
        threshold_display = create_threshold_display(has_score, qualification_info)
        
        # Determine card styling
        card_class, status_emoji = determine_lead_athlete_status(status, has_score)
        
        # Set position emoji
        position_emoji = get_lead_position_emoji(rank, has_score, card_class, status_emoji)
        
        # Format displays
        score_display = score if has_score else "Awaiting Result"
        worst_finish_display = format_worst_finish(worst_finish, has_score)
        
        # Create athlete card
        st.markdown(f"""
        <div class="athlete-row {card_class}">
            <strong>{position_emoji} #{rank} - {name}</strong><br>
            <small>Score: {score_display} | Status: {status}{worst_finish_display}</small>{threshold_display}
        </div>
        """, unsafe_allow_html=True)


def create_threshold_display(has_score: bool, qualification_info: Dict[str, str]) -> str:
    """Create threshold display for athletes without scores"""
    if has_score or not qualification_info:
        return ""
    
    thresholds = []
    for key, value in qualification_info.items():
        if key == 'Hold for 1st':
            thresholds.append(f'🥇 1st: {value}')
        elif key == 'Hold for 2nd':
            thresholds.append(f'🥈 2nd: {value}')
        elif key == 'Hold for 3rd':
            thresholds.append(f'🥉 3rd: {value}')
        elif key in ['Hold to Qualify', 'Min to Qualify']:
            thresholds.append(f'🎯 Target: {value}')
    
    if thresholds:
        return f"<br><div class='targets'><strong>Targets:</strong> {' | '.join(thresholds)}</div>"
    return ""


def determine_lead_athlete_status(status: str, has_score: bool) -> Tuple[str, str]:
    """Determine lead athlete status and styling"""
    if not has_score:
        return "", "📄"
    
    if "Qualified" in status or "✓✓" in status:
        return "qualified", "✅"
    elif "Eliminated" in status or "✗" in status:
        return "eliminated", "❌"
    elif "Podium" in status and "No Podium" not in status and "Contention" not in status:
        return "podium-position", "🏆"
    elif "Podium Contention" in status or "Contention" in status:
        return "podium-contention", "⚠️"
    elif "No Podium" in status:
        return "no-podium", "❌"
    else:
        return "", "📄"


def get_lead_position_emoji(rank: any, has_score: bool, card_class: str, status_emoji: str) -> str:
    """Get position emoji for lead athletes"""
    rank_num = DataProcessor.safe_numeric_conversion(rank)
    if rank_num > 0:
        return status_emoji if has_score and card_class else f"#{rank_num}"
    return "📄"


def format_worst_finish(worst_finish: any, has_score: bool) -> str:
    """Format worst finish display"""
    if not has_score or worst_finish in ['N/A', '', None] or pd.isna(worst_finish):
        return ""
    
    worst_finish_clean = DataProcessor.clean_text(str(worst_finish))
    return f" | Worst Finish: {worst_finish_clean}" if worst_finish_clean and worst_finish_clean != '-' else ""


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"🚫 Application Error: {e}")
        st.markdown("Please refresh the page or contact support if the issue persists.")
        
        with st.expander("🔧 Debug Information"):
            st.code(f"Error: {e}")
            st.code(f"Time: {datetime.now()}")
            import traceback
            st.code(traceback.format_exc()), na=False)) &      # Remove "25+" style entries
            (~df['Name'].apply(is_placeholder_athlete))
        ]
        
        # Second pass: If we have rank information, use it to filter properly
        if 'Current Rank' in filtered_df.columns:
            filtered_df['temp_rank'] = pd.to_numeric(filtered_df['Current Rank'], errors='coerce')
            
            # Keep only rows with valid ranks within expected range
            ranked_df = filtered_df[
                (filtered_df['temp_rank'].notna()) & 
                (filtered_df['temp_rank'] >= 1) & 
                (filtered_df['temp_rank'] <= expected_max)
            ]
            
            if len(ranked_df) > 0:
                # Sort by rank and take only the expected number
                ranked_df = ranked_df.sort_values('temp_rank').head(expected_max)
                filtered_df = ranked_df.drop('temp_rank', axis=1)
            else:
                # If no valid ranks, fall back to manual filtering
                filtered_df = manual_athlete_filter(filtered_df, expected_max)
        else:
            # No rank column available, use manual filtering
            filtered_df = manual_athlete_filter(filtered_df, expected_max)
        
        # Third pass: Additional validation for lead competitions
        if "Lead" in competition_name:
            filtered_df = validate_lead_athletes(filtered_df, expected_max)
        
        logger.info(f"Filtered to {len(filtered_df)} athletes for {competition_name} (expected: {expected_max})")
        return filtered_df
        
    except Exception as e:
        logger.error(f"Error filtering athletes for {competition_name}: {e}")
        # Fallback to basic filtering with count limit
        basic_filtered = df[
            df['Name'].notna() & 
            (df['Name'] != '') &
            (~df['Name'].astype(str).str.contains('Hold for', na=False))
        ].head(expected_max)
        return basic_filtered


def manual_athlete_filter(df: pd.DataFrame, expected_max: int) -> pd.DataFrame:
    """Manually filter athletes when rank information is not reliable"""
    # Look for patterns that indicate real athlete names vs reference data
    potential_athletes = []
    
    for idx, row in df.iterrows():
        name = str(row.get('Name', '')).strip()
        
        # Skip if name looks like reference data
        if any(keyword in name.lower() for keyword in [
            'hold', 'min', 'max', 'qualification', 'threshold', 'zone', 'top',
            'points', 'score', 'rank', 'position', 'place', 'finish'
        ]):
            continue
        
        # Skip if name is too short or looks like a number/code
        if len(name) < 3 or name.isdigit() or not any(c.isalpha() for c in name):
            continue
        
        # Look for typical athlete name patterns (First Last or similar)
        name_parts = name.split()
        if len(name_parts) >= 2 and all(part.isalpha() or part.replace('.', '').isalpha() for part in name_parts):
            potential_athletes.append(idx)
        elif len(name_parts) == 1 and len(name) > 4 and name.isalpha():
            # Single names that are long enough and all letters
            potential_athletes.append(idx)
    
    # Return the filtered dataframe, limited to expected count
    return df.loc[potential_athletes[:expected_max]]


def validate_lead_athletes(df: pd.DataFrame, expected_max: int) -> pd.DataFrame:
    """Additional validation specifically for lead competitions"""
    if len(df) <= expected_max:
        return df
    
    # For lead competitions, prioritize athletes with actual climbing data
    scored_athletes = df[df['Manual Score'].notna() & (df['Manual Score'] != '')].copy()
    unscored_athletes = df[df['Manual Score'].isna() | (df['Manual Score'] == '')].copy()
    
    # Combine scored athletes first, then fill with unscored up to limit
    result_df = scored_athletes.copy()
    remaining_slots = expected_max - len(scored_athletes)
    
    if remaining_slots > 0 and len(unscored_athletes) > 0:
        result_df = pd.concat([result_df, unscored_athletes.head(remaining_slots)], ignore_index=True)
    
    return result_df.head(expected_max)


def is_placeholder_athlete(name: str) -> bool:
    """Check if name is a placeholder like 'Athlete 1', 'Athlete 23', etc."""
    name_str = str(name).strip()
    if name_str.startswith('Athlete '):
        remaining = name_str[8:].strip()
        return remaining.isdigit()
    return False


def display_qualification_thresholds(qualification_info: Dict[str, str]):
    """Display qualification thresholds if available"""
    if qualification_info:
        threshold_items = []
        threshold_mapping = {
            'Hold for 1st': ('🥇 1st', '#FFD700'),
            'Hold for 2nd': ('🥈 2nd', '#C0C0C0'),
            'Hold for 3rd': ('🥉 3rd', '#CD7F32'),
            'Hold to Qualify': ('✅ Qualify', '#28a745'),
            'Min to Qualify': ('⚠️ Min', '#ffc107')
        }
        
        for key, value in qualification_info.items():
            if key in threshold_mapping:
                label, color = threshold_mapping[key]
                threshold_items.append(f'<span style="color: {color}; font-weight: bold;">{label}: {value}</span>')
        
        if threshold_items:
            st.markdown(f"""
            <div class="threshold-card">
                <h5>🎯 Qualification Thresholds</h5>
                {' | '.join(threshold_items)}
            </div>
            """, unsafe_allow_html=True)


def display_lead_athletes(active_df: pd.DataFrame, qualification_info: Dict[str, str]):
    """Display lead competition athletes with enhanced formatting"""
    # Sort by rank if available
    try:
        if 'Current Rank' in active_df.columns:
            active_df['Current Rank'] = pd.to_numeric(active_df['Current Rank'], errors='coerce')
            active_df = active_df.sort_values('Current Rank', ascending=True).reset_index(drop=True)
    except Exception as e:
        logger.warning(f"Could not sort by rank: {e}")
    
    # Display athlete cards
    for _, row in active_df.iterrows():
        name = DataProcessor.clean_text(str(row.get('Name', 'Unknown')))
        score = row.get('Manual Score', 'N/A')
        rank = row.get('Current Rank', 'N/A')
        status = DataProcessor.clean_text(str(row.get('Status', 'Unknown')))
        worst_finish = row.get('Worst Finish', 'N/A')
        
        # Determine if athlete has a score
        has_score = score not in ['N/A', '', None] and not pd.isna(score)
        
        # Create threshold display for athletes without scores
        threshold_display = create_threshold_display(has_score, qualification_info)
        
        # Determine card styling
        card_class, status_emoji = determine_lead_athlete_status(status, has_score)
        
        # Set position emoji
        position_emoji = get_lead_position_emoji(rank, has_score, card_class, status_emoji)
        
        # Format displays
        score_display = score if has_score else "Awaiting Result"
        worst_finish_display = format_worst_finish(worst_finish, has_score)
        
        # Create athlete card
        st.markdown(f"""
        <div class="athlete-row {card_class}">
            <strong>{position_emoji} #{rank} - {name}</strong><br>
            <small>Score: {score_display} | Status: {status}{worst_finish_display}</small>{threshold_display}
        </div>
        """, unsafe_allow_html=True)


def create_threshold_display(has_score: bool, qualification_info: Dict[str, str]) -> str:
    """Create threshold display for athletes without scores"""
    if has_score or not qualification_info:
        return ""
    
    thresholds = []
    for key, value in qualification_info.items():
        if key == 'Hold for 1st':
            thresholds.append(f'🥇 1st: {value}')
        elif key == 'Hold for 2nd':
            thresholds.append(f'🥈 2nd: {value}')
        elif key == 'Hold for 3rd':
            thresholds.append(f'🥉 3rd: {value}')
        elif key in ['Hold to Qualify', 'Min to Qualify']:
            thresholds.append(f'🎯 Target: {value}')
    
    if thresholds:
        return f"<br><div class='targets'><strong>Targets:</strong> {' | '.join(thresholds)}</div>"
    return ""


def determine_lead_athlete_status(status: str, has_score: bool) -> Tuple[str, str]:
    """Determine lead athlete status and styling"""
    if not has_score:
        return "", "📄"
    
    if "Qualified" in status or "✓✓" in status:
        return "qualified", "✅"
    elif "Eliminated" in status or "✗" in status:
        return "eliminated", "❌"
    elif "Podium" in status and "No Podium" not in status and "Contention" not in status:
        return "podium-position", "🏆"
    elif "Podium Contention" in status or "Contention" in status:
        return "podium-contention", "⚠️"
    elif "No Podium" in status:
        return "no-podium", "❌"
    else:
        return "", "📄"


def get_lead_position_emoji(rank: any, has_score: bool, card_class: str, status_emoji: str) -> str:
    """Get position emoji for lead athletes"""
    rank_num = DataProcessor.safe_numeric_conversion(rank)
    if rank_num > 0:
        return status_emoji if has_score and card_class else f"#{rank_num}"
    return "📄"


def format_worst_finish(worst_finish: any, has_score: bool) -> str:
    """Format worst finish display"""
    if not has_score or worst_finish in ['N/A', '', None] or pd.isna(worst_finish):
        return ""
    
    worst_finish_clean = DataProcessor.clean_text(str(worst_finish))
    return f" | Worst Finish: {worst_finish_clean}" if worst_finish_clean and worst_finish_clean != '-' else ""


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"🚫 Application Error: {e}")
        st.markdown("Please refresh the page or contact support if the issue persists.")
        
        with st.expander("🔧 Debug Information"):
            st.code(f"Error: {e}")
            st.code(f"Time: {datetime.now()}")
            import traceback
            st.code(traceback.format_exc())
