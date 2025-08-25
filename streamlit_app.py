with col2:
        st.markdown(f'''
        <div class="metric-card">
            <h4>🔴 Live</h4>
            <h2>{overview_metrics["live"]}</h2>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="metric-card">
            <h4>✅ Completed</h4>
            <h2>{overview_metrics["completed"]}</h2>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown(f'''
        <div class="metric-card">
            <h4>📄 Upcoming</h4>
            <h2>{overview_metrics["upcoming"]}</h2>
        </div>
        ''', unsafe_allow_html=True)
    
    # Display results
    st.markdown("### 📊 Live Results")
    
    if len(filtered_competitions) > 1:
        # Create tabs for multiple competitions
        tab_names = list(filtered_competitions.keys())
        tabs = st.tabs(tab_names)
        
        for i, (comp_name, url) in enumerate(filtered_competitions.items()):
            with tabs[i]:
                display_competition_results(comp_name, url)
    else:
        # Single competition view
        comp_name, url = list(filtered_competitions.items())[0]
        display_competition_results(comp_name, url)
    
    # Enhanced footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**⛰️ IFSC World Championships 2025**")
    with col2:
        st.markdown("**📊 Real-time Results**")
    with col3:
        st.markdown(f"**🔄 Auto-refresh: {'ON' if st.session_state.auto_refresh_enabled else 'OFF'}**")
    
    # Auto-refresh logic
    if st.session_state.auto_refresh_enabled:
        time_since_last = (datetime.now() - st.session_state.last_refresh).total_seconds()
        if time_since_last >= Config.AUTO_REFRESH_INTERVAL:
            st.session_state.last_refresh = datetime.now()
            st.rerun()


def get_filtered_competitions(competition_type: str, gender_filter: str, round_filter: str) -> Dict[str, str]:
    """Get filtered competitions based on user selection"""
    filtered_competitions = {}
    
    for name, url in Config.SHEETS_URLS.items():
        include = True
        
        if competition_type != "All" and competition_type.lower() not in name.lower():
            include = False
        
        if gender_filter != "All" and gender_filter.lower() not in name.lower():
            include = False
                
        if round_filter != "All" and round_filter.lower() not in name.lower():
            include = False
        
        if include:
            filtered_competitions[name] = url
    
    return filtered_competitions


def calculate_overview_metrics(filtered_competitions: Dict[str, str]) -> Dict[str, int]:
    """Calculate overview metrics for all competitions"""
    metrics = {"total": 0, "live": 0, "completed": 0, "upcoming": 0}
    
    for comp_name, url in filtered_competitions.items():
        try:
            df = DataLoader.load_sheet_data(url)
            status, _ = CompetitionStatusDetector.get_competition_status(df, comp_name)
            metrics["total"] += 1
            metrics[status] += 1
        except Exception as e:
            logger.warning(f"Error calculating metrics for {comp_name}: {e}")
            metrics["total"] += 1
            metrics["upcoming"] += 1
    
    return metrics


def display_competition_results(comp_name: str, url: str):
    """Display results for a single competition"""
    with st.spinner(f"Loading {comp_name}..."):
        df = DataLoader.load_sheet_data(url)
    
    current_time = datetime.now().strftime("%H:%M:%S")
    st.caption(f"📡 Last updated: {current_time}")
    
    if "Boulder" in comp_name:
        display_boulder_results(df, comp_name)
    elif "Lead" in comp_name:
        display_lead_results(df, comp_name)
    else:
        if not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.markdown('<div class="error-card">⚠️ No data available</div>', unsafe_allow_html=True)


def display_boulder_results(df: pd.DataFrame, competition_name: str):
    """Enhanced boulder competition results display"""
    status, status_emoji = CompetitionStatusDetector.get_competition_status(df, competition_name)
    status_class = f"badge-{status}"
    
    st.markdown(f"""
    ### 🪨 {competition_name} 
    <span class="status-badge {status_class}">{status_emoji} {status.upper()}</span>
    """, unsafe_allow_html=True)
    
    if df.empty:
        st.markdown('<div class="error-card">⚠️ No data available for this competition</div>', unsafe_allow_html=True)
        return
    
    # Validate required columns
    required_cols = ['Athlete Name', 'Current Position/Rank']
    is_valid, issues = DataProcessor.validate_dataframe(df, required_cols)
    
    if not is_valid:
        st.markdown(f'<div class="error-card">⚠️ Data validation failed: {"; ".join(issues)}</div>', unsafe_allow_html=True)
        with st.expander("🔍 Raw Data"):
            st.dataframe(df, use_container_width=True, hide_index=True)
        return
    
    # Display enhanced metrics
    display_enhanced_metrics(df, competition_name)
    
    st.markdown("#### 📋 Current Standings")
    
    # Find the total score column
    score_col = next((col for col in df.columns if 'Total Score' in str(col)), None)
    
    # Sort and prepare data
    df_sorted = df.copy()
    
    # Convert rank to numeric
    if 'Current Position/Rank' in df.columns:
        df_sorted['Current Position/Rank'] = pd.to_numeric(df_sorted['Current Position/Rank'], errors='coerce')
    
    # Convert score to numeric if available
    if score_col is not None:
        df_sorted[score_col] = pd.to_numeric(df_sorted[score_col], errors='coerce')
    
    # Sort by position
    try:
        if 'Current Position/Rank' in df_sorted.columns:
            df_sorted = df_sorted.sort_values('Current Position/Rank', ascending=True).reset_index(drop=True)
        elif score_col is not None:
            df_sorted = df_sorted.sort_values(score_col, ascending=False).reset_index(drop=True)
    except Exception as e:
        logger.warning(f"Could not sort data: {e}")
        df_sorted = df.copy()
    
    # Display results with enhanced athlete cards
    display_boulder_athlete_cards(df_sorted, score_col, competition_name)


def display_boulder_athlete_cards(df_sorted: pd.DataFrame, score_col: Optional[str], competition_name: str):
    """Display enhanced athlete cards for boulder competitions"""
    
    for idx, row in df_sorted.iterrows():
        if pd.isna(row.get('Athlete Name')) or row.get('Athlete Name') == '':
            continue
            
        rank = row.get('Current Position/Rank', 'N/A')
        athlete = DataProcessor.clean_text(str(row.get('Athlete Name', 'Unknown')))
        total_score = row.get(score_col, 'N/A') if score_col else 'N/A'
        
        # Calculate boulder completion
        boulder_info = calculate_boulder_completion(row)
        
        # Determine athlete status and styling
        card_class, position_emoji = determine_athlete_status(
            rank, total_score, boulder_info, competition_name
        )
        
        # Create strategy display if applicable
        strategy_display = create_strategy_display(row, boulder_info, competition_name)
        
        # Create the athlete card
        create_athlete_card(
            position_emoji, athlete, total_score, boulder_info, 
            strategy_display, card_class
        )


def calculate_boulder_completion(row: pd.Series) -> Dict[str, any]:
    """Calculate boulder completion information for an athlete"""
    boulder_scores = []
    completed_boulders = 0
    
    for i in range(1, 5):
        col_name = f'Boulder {i} Score (0-25)'
        if col_name in row.index:
            score = row.get(col_name, '-')
            if pd.notna(score) and str(score) != '-' and str(score) != '':
                boulder_scores.append(f"B{i}: {score}")
                completed_boulders += 1
            else:
                boulder_scores.append(f"B{i}: -")
    
    boulder_display = " | ".join(boulder_scores) if boulder_scores else "No boulder data"
    
    # Check for worst finish information
    worst_finish_display = ""
    if completed_boulders == 4:
        worst_finish_col = next((
            col for col in row.index 
            if 'worst' in str(col).lower() and 'finish' in str(col).lower()
        ), None)
        
        if worst_finish_col:
            worst_finish = row.get(worst_finish_col, 'N/A')
            if worst_finish not in ['N/A', '', None] and not pd.isna(worst_finish):
                worst_finish_clean = DataProcessor.clean_text(str(worst_finish))
                if worst_finish_clean and worst_finish_clean != '-':
                    worst_finish_display = f" | Worst Finish: {worst_finish_clean}"
    
    return {
        'boulder_scores': boulder_scores,
        'completed_boulders': completed_boulders,
        'boulder_display': boulder_display,
        'worst_finish_display': worst_finish_display
    }


def determine_athlete_status(rank: any, total_score: any, boulder_info: Dict, competition_name: str) -> Tuple[str, str]:
    """Determine athlete status and appropriate styling"""
    card_class = ""
    position_emoji = ""
    
    try:
        rank_num = DataProcessor.safe_numeric_conversion(rank)
        completed_boulders = boulder_info['completed_boulders']
        worst_finish_display = boulder_info['worst_finish_display']
        
        # Extract worst finish number if available
        worst_finish_num = None
        if worst_finish_display:
            try:
                worst_parts = worst_finish_display.split("Worst Finish: ")
                if len(worst_parts) > 1:
                    worst_finish_num = float(worst_parts[1])
            except:
                pass
        
        # Apply status logic based on completion and competition type
        if completed_boulders == 4 or (total_score not in ['N/A', '', None] and not pd.isna(total_score)):
            if "Final" in competition_name:
                card_class, position_emoji = determine_final_status(rank_num, worst_finish_num, completed_boulders)
            elif "Semis" in competition_name:
                card_class, position_emoji = determine_semis_status(rank_num, worst_finish_num, completed_boulders)
            else:
                card_class, position_emoji = determine_general_status(rank_num)
        
        # Fallback for rank display
        if not position_emoji and rank_num > 0:
            position_emoji = f"#{rank_num}"
            
    except Exception as e:
        logger.warning(f"Error determining athlete status: {e}")
        rank_num = DataProcessor.safe_numeric_conversion(rank)
        if rank_num > 0:
            position_emoji = f"#{rank_num}"
    
    return card_class, position_emoji


def determine_final_status(rank_num: float, worst_finish_num: Optional[float], completed_boulders: int) -> Tuple[str, str]:
    """Determine status for final competitions"""
    if worst_finish_num and worst_finish_num <= 3:
        return "podium-position", "🏆"
    elif rank_num <= 3 and completed_boulders < 4:
        return "podium-contention", "⚠️"
    elif rank_num > 3:
        if completed_boulders < 4:
            return "podium-contention", "⚠️"
        else:
            return "no-podium", "❌"
    else:
        return "podium-contention", "⚠️"


def determine_semis_status(rank_num: float, worst_finish_num: Optional[float], completed_boulders: int) -> Tuple[str, str]:
    """Determine status for semifinals"""
    if worst_finish_num and worst_finish_num <= 8:
        return "qualified", "✅"
    elif rank_num <= 8 or completed_boulders < 4:
        return "podium-contention", "⚠️"
    else:
        return "eliminated", "❌"


def determine_general_status(rank_num: float) -> Tuple[str, str]:
    """Determine status for general competitions"""
    if rank_num <= 3:
        emoji = "🥇" if rank_num == 1 else "🥈" if rank_num == 2 else "🥉"
        return "podium-position", emoji
    elif rank_num <= 8:
        return "qualified", "✅"
    else:
        return "eliminated", "❌"


def create_strategy_display(row: pd.Series, boulder_info: Dict, competition_name: str) -> str:
    """Create strategy display for boulder competitions"""
    strategy_display = ""
    completed_boulders = boulder_info['completed_boulders']
    
    if ("Semis" in competition_name or "Final" in competition_name) and completed_boulders == 3:
        strategy_cols = {}
        for col in row.index:
            col_str = str(col)
            if '1st Place Strategy' in col_str:
                strategy_cols['1st'] = col
            elif '2nd Place Strategy' in col_str:
                strategy_cols['2nd'] = col
            elif '3rd Place Strategy' in col_str:
                strategy_cols['3rd'] = col
            elif 'Points Needed for Top 8' in col_str:
                strategy_cols['top8'] = col
        
        if strategy_cols:
            strategies = []
            for place, col in strategy_cols.items():
                strategy_value = row.get(col, '')
                if strategy_value and str(strategy_value) not in ['', 'nan', 'N/A']:
                    strategy_clean = DataProcessor.clean_text(str(strategy_value))
                    if strategy_clean:
                        if place == '1st':
                            strategies.append(f"🥇 1st: {strategy_clean}")
                        elif place == '2nd':
                            strategies.append(f"🥈 2nd: {strategy_clean}")
                        elif place == '3rd':
                            strategies.append(f"🥉 3rd: {strategy_clean}")
                        elif place == 'top8' and "Semis" in competition_name:
                            strategies.append(f"🎯 Top 8: {strategy_clean}")
            
            if strategies:
                comp_type = "Final" if "Final" in competition_name else "Semi"
                strategy_display = f"<br><div class='targets'><strong>{comp_type} Strategy:</strong> {' | '.join(strategies)}</div>"
    
    return strategy_display


def create_athlete_card(position_emoji: str, athlete: str, total_score: any, 
                       boulder_info: Dict, strategy_display: str, card_class: str):
    """Create and display an athlete card"""
    completed_boulders = boulder_info['completed_boulders']
    boulder_display = boulder_info['boulder_display']
    worst_finish_display = boulder_info['worst_finish_display']
    
    # Create detail text based on completion status
    if completed_boulders == 4:
        detail_text = f"Total: {total_score} | {boulder_display}{worst_finish_display}"
    elif completed_boulders == 3:
        detail_text = f"Total: {total_score} | {boulder_display} | 1 boulder remaining"
    else:
        detail_text = f"Total: {total_score} | {boulder_display} | Progress: {completed_boulders}/4"
    
    st.markdown(f"""
    <div class="athlete-row {card_class}">
        <strong>{position_emoji} - {athlete}</strong><br>
        <small>{detail_text}</small>{strategy_display}
    </div>
    """, unsafe_allow_html=True)


def display_lead_results(df: pd.DataFrame, competition_name: str):
    """Enhanced lead competition results display"""
    status, status_emoji = CompetitionStatusDetector.get_competition_status(df, competition_name)
    status_class = f"badge-{status}"
    
    st.markdown(f"""
    ### 🧗‍♀️ {competition_name}
    <span class="status-badge {status_class}">{status_emoji} {status.upper()}</span>
    """, unsafe_allow_html=True)
    
    if df.empty:
        st.markdown('<div class="error-card">⚠️ No data available for this competition</div>', unsafe_allow_html=True)
        return
    
    if 'Name' not in df.columns:
        st.markdown('<div class="error-card">⚠️ Name column not found in data</div>', unsafe_allow_html=True)
        return
    
    # Extract qualification info and filter active athletes
    qualification_info = extract_qualification_info(df)
    active_df = filter_active_athletes(df, competition_name)
    
    # Display enhanced metrics
    display_enhanced_metrics(active_df, competition_name)
    
    st.markdown("#### 📋 Current Standings")
    
    # Show qualification thresholds
    display_qualification_thresholds(qualification_info)
    
    # Sort and display athletes
    display_lead_athletes(active_df, qualification_info)


def extract_qualification_info(df: pd.DataFrame) -> Dict[str, str]:
    """Extract qualification threshold information from dataframe"""
    qualification_info = {}
    try:
        threshold_cols = ['Hold for 1st', 'Hold for 2nd', 'Hold for 3rd', 'Hold to Qualify', 'Min to Qualify']
        for _, row in df.iterrows():
            if pd.isna(row.get('Name')) or row.get('Name') == '':
                continue
            for col in threshold_cols:
                if col in df.columns and pd.notna(row.get(col)):
                    qualification_info[col] = DataProcessor.clean_text(str(row.get(col)))
    except Exception as e:
        logger.warning(f"Error extracting qualification thresholds: {e}")
    return qualification_info


def filter_active_athletes(df: pd.DataFrame, competition_name: str) -> pd.DataFrame:
    """Filter out reference rows to get only active athletes with proper count limits"""
    try:
        # Determine expected athlete count based on competition type
        expected_max = 24 if "Semis" in competition_name else 8 if "Final" in competition_name else 50
        
        # First pass: Remove obvious non-athlete rows
        filtered_df = df[
            df['Name'].notna() & 
            (df['Name'] != '') & 
            (~df['Name'].astype(str).str.isdigit()) &
            (~df['Name'].astype(str).str.contains('Hold for|Min to|Qualification|Threshold|Zone|Top|TBD|TBA', na=False, case=False)) &
            (~df['Name'].astype(str).str.startswith(('Hold', 'Min', '#', 'Athlete '), na=False)) &
            (~df['Name'].astype(str).str.match(r'^\d+\.?\d*import streamlit as st
import pandas as pd
import requests
from io import StringIO
import time
from datetime import datetime, timedelta
import logging
import re
import os
from typing import Dict, Tuple, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure the page
st.set_page_config(
    page_title="🧗‍♂️ IFSC 2025 World Championships",
    page_icon="🧗‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with better mobile responsiveness
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        text-align: center;
        padding: 2rem 1rem;
        background: linear-gradient(135deg, #ff6b6b, #4ecdc4, #45b7d1);
        color: white;
        margin-bottom: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        animation: fadeIn 1s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Responsive athlete cards */
    .athlete-row {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 12px;
        font-weight: 500;
        border: 2px solid transparent;
        box-shadow: 0 3px 8px rgba(0,0,0,0.12);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .athlete-row:hover {
        transform: translateY(-3px) scale(1.01);
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    }
    
    .athlete-row strong {
        font-size: 1.1rem;
        display: block;
        margin-bottom: 0.5rem;
        text-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    .athlete-row small {
        font-size: 0.9rem;
        opacity: 0.9;
        line-height: 1.4;
    }
    
    .athlete-row .targets {
        background-color: rgba(0, 0, 0, 0.15);
        padding: 0.6rem 0.8rem;
        border-radius: 8px;
        margin-top: 0.6rem;
        display: inline-block;
        font-weight: 600;
        border: 2px solid rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(5px);
        font-size: 0.85rem;
    }
    
    /* Status-based styling */
    .podium-position {
        background: linear-gradient(135deg, #d4edda, #c3e6cb) !important;
        border: 2px solid #28a745 !important;
        color: #155724 !important;
    }
    
    .podium-position .targets {
        background-color: rgba(40, 167, 69, 0.25) !important;
        color: #155724 !important;
        border: 2px solid #28a745 !important;
    }
    
    .qualified {
        background: linear-gradient(135deg, #d4edda, #c3e6cb);
        border: 2px solid #28a745;
        color: #155724;
    }
    
    .podium-contention {
        background: linear-gradient(135deg, #fff3cd, #ffeaa7);
        border: 2px solid #ffc107;
        color: #856404;
    }
    
    .eliminated, .no-podium {
        background: linear-gradient(135deg, #f8d7da, #f1b0b7);
        border: 2px solid #dc3545;
        color: #721c24;
    }
    
    .awaiting-result {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        border: 2px solid #6c757d;
        color: #495057;
    }
    
    /* Enhanced metric cards */
    .metric-card {
        background: linear-gradient(135deg, white, #f8f9fa);
        padding: 1.5rem 1rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        text-align: center;
        color: #333333;
        border: 1px solid #e9ecef;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .metric-card h4 {
        color: #666666;
        margin-bottom: 0.8rem;
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-card h2 {
        color: #333333;
        margin: 0;
        font-size: 1.6rem;
        font-weight: bold;
        text-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-left: 0.5rem;
    }
    
    .badge-live {
        background: linear-gradient(45deg, #ff4757, #ff6b6b);
        color: white;
        animation: pulse 2s infinite;
    }
    
    .badge-completed {
        background: linear-gradient(45deg, #2ed573, #7bed9f);
        color: white;
    }
    
    .badge-upcoming {
        background: linear-gradient(45deg, #ffa502, #ff6348);
        color: white;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    /* Threshold and error cards */
    .threshold-card {
        background: linear-gradient(135deg, #e3f2fd, #bbdefb);
        border: 2px solid #2196f3;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        color: #0d47a1;
    }
    
    .error-card {
        background: linear-gradient(135deg, #ffebee, #ffcdd2);
        border: 2px solid #f44336;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        color: #c62828;
    }
    
    /* Progress bar */
    .progress-bar {
        width: 100%;
        height: 6px;
        background-color: #e9ecef;
        border-radius: 3px;
        margin: 0.5rem 0;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #28a745, #20c997);
        border-radius: 3px;
        transition: width 0.3s ease;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .metric-card {
            padding: 1rem 0.5rem;
        }
        
        .metric-card h2 {
            font-size: 1.4rem;
        }
        
        .athlete-row {
            padding: 0.8rem;
        }
        
        .athlete-row strong {
            font-size: 1rem;
        }
        
        .athlete-row .targets {
            font-size: 0.8rem;
            padding: 0.5rem 0.6rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Configuration with enhanced settings
class Config:
    CACHE_TTL = 30
    AUTO_REFRESH_INTERVAL = 60
    MAX_RETRIES = 3
    REQUEST_TIMEOUT = 15
    MAX_ATHLETES_DISPLAY = 50
    
    # Google Sheets URLs
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

class DataProcessor:
    """Enhanced data processing utilities"""
    
    @staticmethod
    def safe_numeric_conversion(value, default=0) -> float:
        """Safely convert value to numeric with proper error handling"""
        try:
            if pd.isna(value) or value == '' or value is None:
                return default
            return pd.to_numeric(value, errors='coerce')
        except Exception as e:
            logger.warning(f"Error converting {value} to numeric: {e}")
            return default

    @staticmethod
    def clean_text(text) -> str:
        """Enhanced text cleaning with better Unicode handling"""
        if not isinstance(text, str):
            return str(text) if text is not None else ""
        
        try:
            # Better Unicode handling
            cleaned = text.encode('utf-8', 'ignore').decode('utf-8')
            # Remove extra whitespace
            cleaned = ' '.join(cleaned.split())
            # Remove common problematic characters
            cleaned = re.sub(r'[^\w\s\-\.\,\(\)]+', '', cleaned)
            return cleaned.strip()
        except Exception as e:
            logger.warning(f"Error cleaning text '{text}': {e}")
            return str(text) if text is not None else ""

    @staticmethod
    def validate_dataframe(df: pd.DataFrame, expected_columns: List[str]) -> Tuple[bool, List[str]]:
        """Enhanced DataFrame validation"""
        if df.empty:
            return False, ["DataFrame is empty"]
        
        issues = []
        missing_cols = [col for col in expected_columns if col not in df.columns]
        
        if missing_cols:
            issues.append(f"Missing columns: {', '.join(missing_cols)}")
        
        # Check for minimum data requirements
        if len(df) < 1:
            issues.append("Insufficient data rows")
        
        return len(issues) == 0, issues

class CompetitionStatusDetector:
    """Enhanced competition status detection"""
    
    @staticmethod
    def get_competition_status(df: pd.DataFrame, competition_name: str) -> Tuple[str, str]:
        """Determine competition status with improved logic"""
        if df.empty:
            return "upcoming", "📄"
        
        try:
            if "Boulder" in competition_name:
                return CompetitionStatusDetector._get_boulder_status(df)
            elif "Lead" in competition_name:
                return CompetitionStatusDetector._get_lead_status(df)
        except Exception as e:
            logger.warning(f"Error determining status for {competition_name}: {e}")
        
        return "upcoming", "📄"
    
    @staticmethod
    def _get_boulder_status(df: pd.DataFrame) -> Tuple[str, str]:
        """Determine boulder competition status"""
        score_cols = [col for col in df.columns if 'Score' in str(col)]
        if not score_cols:
            return "upcoming", "📄"
        
        has_scores = df[score_cols].notna().any().any()
        if not has_scores:
            return "upcoming", "📄"
        
        total_athletes = len(df[df.iloc[:, 0].notna() & (df.iloc[:, 0] != '')])
        completed_athletes = len(df[df[score_cols].notna().any(axis=1)])
        
        completion_rate = completed_athletes / max(total_athletes, 1)
        
        if completion_rate >= 0.9:
            return "completed", "✅"
        elif completion_rate >= 0.1:
            return "live", "🔴"
        else:
            return "upcoming", "📄"
    
    @staticmethod
    def _get_lead_status(df: pd.DataFrame) -> Tuple[str, str]:
        """Determine lead competition status"""
        if 'Manual Score' not in df.columns:
            return "upcoming", "📄"
        
        has_scores = df['Manual Score'].notna().any()
        if not has_scores:
            return "upcoming", "📄"
        
        total_athletes = len(df[df['Name'].notna() & (df['Name'] != '')])
        completed_athletes = len(df[df['Manual Score'].notna()])
        
        completion_rate = completed_athletes / max(total_athletes, 1)
        
        if completion_rate >= 0.9:
            return "completed", "✅"
        elif completion_rate >= 0.1:
            return "live", "🔴"
        else:
            return "upcoming", "📄"

class DataLoader:
    """Enhanced data loading with better error handling and caching"""
    
    @staticmethod
    @st.cache_data(ttl=Config.CACHE_TTL, show_spinner=False)
    def load_sheet_data(url: str, retries: int = 0) -> pd.DataFrame:
        """Load data from Google Sheets with enhanced error handling"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/csv,text/plain,*/*',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive'
            }
            
            response = requests.get(
                url, 
                timeout=Config.REQUEST_TIMEOUT,
                headers=headers,
                stream=True
            )
            response.raise_for_status()
            
            # Read CSV data with better encoding handling
            csv_data = StringIO(response.text)
            df = pd.read_csv(csv_data, encoding='utf-8', low_memory=False)
            
            # Enhanced data cleaning
            df = DataLoader._clean_dataframe(df)
            
            logger.info(f"Successfully loaded data: {len(df)} rows, {len(df.columns)} columns")
            return df
            
        except requests.RequestException as e:
            error_msg = f"Network error: {str(e)}"
            logger.error(error_msg)
            
            if retries < Config.MAX_RETRIES:
                logger.info(f"Retrying... attempt {retries + 1}")
                time.sleep(2 ** retries)
                return DataLoader.load_sheet_data(url, retries + 1)
            
            st.error(f"🚫 {error_msg}")
            return pd.DataFrame()
            
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            st.error(f"🚫 {error_msg}")
            return pd.DataFrame()
    
    @staticmethod
    def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """Enhanced DataFrame cleaning"""
        # Remove completely empty rows
        df = df.dropna(how='all')
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Remove unnamed columns
        unnamed_cols = [col for col in df.columns if str(col).startswith('Unnamed')]
        df = df.drop(columns=unnamed_cols, errors='ignore')
        
        # Clean text data
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].apply(DataProcessor.clean_text)
        
        return df

class MetricsCalculator:
    """Enhanced metrics calculation"""
    
    @staticmethod
    def calculate_boulder_metrics(df: pd.DataFrame) -> Dict[str, any]:
        """Calculate boulder competition metrics"""
        try:
            total_athletes = len(df[df['Athlete Name'].notna() & (df['Athlete Name'] != '')])
            
            boulder_cols = [col for col in df.columns if 'Boulder' in str(col) and 'Score' in str(col)]
            completed_problems = sum(df[col].notna().sum() for col in boulder_cols) if boulder_cols else 0
            
            # Find total score column
            score_col = next((col for col in df.columns if 'Total Score' in str(col)), None)
            
            avg_score = 0
            if score_col:
                numeric_scores = pd.to_numeric(df[score_col], errors='coerce')
                avg_score = numeric_scores.mean() if not numeric_scores.isna().all() else 0
            
            # Find leader
            leader = "TBD"
            if 'Current Position/Rank' in df.columns:
                try:
                    leader_mask = pd.to_numeric(df['Current Position/Rank'], errors='coerce') == 1
                    if leader_mask.any():
                        leader = DataProcessor.clean_text(df.loc[leader_mask, 'Athlete Name'].iloc[0])
                except:
                    pass
            
            return {
                'total_athletes': total_athletes,
                'completed_problems': completed_problems,
                'avg_score': avg_score,
                'leader': leader
            }
        except Exception as e:
            logger.error(f"Error calculating boulder metrics: {e}")
            return {'total_athletes': 0, 'completed_problems': 0, 'avg_score': 0, 'leader': 'TBD'}
    
    @staticmethod
    def calculate_lead_metrics(df: pd.DataFrame) -> Dict[str, any]:
        """Calculate lead competition metrics"""
        try:
            # Filter active athletes
            active_df = df[
                df['Name'].notna() & 
                (df['Name'] != '') & 
                (~df['Name'].astype(str).str.contains('Hold for', na=False)) &
                (~df['Name'].astype(str).str.contains('Min to', na=False))
            ]
            
            total_athletes = len(active_df)
            completed = len(active_df[active_df['Manual Score'].notna() & (active_df['Manual Score'] != '')])
            
            # Calculate average score
            avg_score = 0
            if 'Manual Score' in active_df.columns:
                scores = pd.to_numeric(active_df['Manual Score'], errors='coerce')
                avg_score = scores.mean() if not scores.isna().all() else 0
            
            # Find leader
            leader = "TBD"
            if 'Current Rank' in active_df.columns:
                try:
                    leader_idx = pd.to_numeric(active_df['Current Rank'], errors='coerce') == 1
                    if leader_idx.any():
                        leader = DataProcessor.clean_text(active_df.loc[leader_idx, 'Name'].iloc[0])
                except:
                    pass
            
            return {
                'total_athletes': total_athletes,
                'completed': completed,
                'avg_score': avg_score,
                'leader': leader
            }
        except Exception as e:
            logger.error(f"Error calculating lead metrics: {e}")
            return {'total_athletes': 0, 'completed': 0, 'avg_score': 0, 'leader': 'TBD'}

def display_enhanced_metrics(df: pd.DataFrame, competition_name: str):
    """Display enhanced metrics with progress indicators"""
    col1, col2, col3, col4 = st.columns(4)
    
    if "Boulder" in competition_name:
        metrics = MetricsCalculator.calculate_boulder_metrics(df)
        
        with col1:
            st.markdown(f'''
            <div class="metric-card">
                <h4>👥 Athletes</h4>
                <h2>{metrics["total_athletes"]}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''
            <div class="metric-card">
                <h4>🧗‍♂️ Problems Completed</h4>
                <h2>{metrics["completed_problems"]}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'''
            <div class="metric-card">
                <h4>📊 Avg Score</h4>
                <h2>{metrics["avg_score"]:.1f}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        with col4:
            st.markdown(f'''
            <div class="metric-card">
                <h4>🥇 Leader</h4>
                <h2>{metrics["leader"][:15]}{"..." if len(metrics["leader"]) > 15 else ""}</h2>
            </div>
            ''', unsafe_allow_html=True)
    
    elif "Lead" in competition_name:
        metrics = MetricsCalculator.calculate_lead_metrics(df)
        
        with col1:
            st.markdown(f'''
            <div class="metric-card">
                <h4>👥 Athletes</h4>
                <h2>{metrics["total_athletes"]}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            completion_rate = (metrics["completed"] / max(metrics["total_athletes"], 1)) * 100
            st.markdown(f'''
            <div class="metric-card">
                <h4>✅ Completed</h4>
                <h2>{metrics["completed"]}</h2>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {completion_rate}%"></div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'''
            <div class="metric-card">
                <h4>📊 Avg Score</h4>
                <h2>{metrics["avg_score"]:.1f}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        with col4:
            st.markdown(f'''
            <div class="metric-card">
                <h4>🥇 Leader</h4>
                <h2>{metrics["leader"][:15]}{"..." if len(metrics["leader"]) > 15 else ""}</h2>
            </div>
            ''', unsafe_allow_html=True)

def is_placeholder_athlete(name: str) -> bool:
    """Check if name is a placeholder or reference entry"""
    name_str = str(name).strip().lower()
    
    # Check for "Athlete X" pattern first
    if name_str.startswith('athlete '):
        remaining = name_str[8:].strip()
        if remaining.isdigit():
            return True
    
    placeholder_patterns = [
        r'^n/a$|^na$',                # Not available
        r'^athlete\s+\d+',            # "Athlete 1", "Athlete 23"
        r'^climber\s+\d+',            # "Climber 1", "Climber 23"  
        r'^competitor\s+\d+',         # "Competitor 1"
        r'^\d+$',                     # Just numbers
        r'^\d+\.\d+$',                # Decimal numbers
        r'^\d+\+$',                   # "25+"
        r'^tbd$|^tba$',               # To be determined/announced
        r'^n\/a$|^na$',               # Not available
        r'^hold\s+\d+',               # "Hold 25"
        r'^zone\s+\d+',               # "Zone 40"
        r'^top\s+\d+',                # "Top 50"
        r'qualification|threshold',    # Reference text
        r'worst|best|average',        # Statistical text
        r'points|score|rank',         # Score-related text
    ]
    
    # Check against patterns
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

def main():
    """Enhanced main application function"""
    
    # Initialize session state
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = datetime.now()
    if 'auto_refresh_enabled' not in st.session_state:
        st.session_state.auto_refresh_enabled = True
    if 'selected_competitions' not in st.session_state:
        st.session_state.selected_competitions = []
    
    # Enhanced header
    st.markdown("""
    <div class="main-header">
        <h1>🧗‍♂️ IFSC 2025 World Championships</h1>
        <h3>Live Competition Results Dashboard</h3>
        <p style="margin: 0; opacity: 0.9;">Real-time climbing competition tracking</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced sidebar
    st.sidebar.title("🎯 Dashboard Controls")
    
    # Auto-refresh section
    with st.sidebar.expander("🔄 Refresh Settings", expanded=True):
        auto_refresh = st.checkbox(
            "Enable Auto-Refresh", 
            value=st.session_state.auto_refresh_enabled,
            help=f"Updates every {Config.AUTO_REFRESH_INTERVAL}s"
        )
        st.session_state.auto_refresh_enabled = auto_refresh
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh", type="primary", use_container_width=True):
                st.cache_data.clear()
                st.session_state.last_refresh = datetime.now()
                st.success("✅ Refreshed!")
                time.sleep(0.5)
                st.rerun()
        
        with col2:
            if st.button("🗑️ Clear Cache", use_container_width=True):
                st.cache_data.clear()
                st.success("✅ Cache cleared!")
        
        # Show refresh status
        time_since = (datetime.now() - st.session_state.last_refresh).seconds
        st.caption(f"🕐 Last refresh: {time_since}s ago")
    
    # Competition filters
    with st.sidebar.expander("🎯 Competition Filters", expanded=True):
        competition_type = st.selectbox(
            "⛰️ Discipline",
            ["All", "Boulder", "Lead"],
            help="Filter by climbing discipline"
        )
        
        gender_filter = st.selectbox(
            "👤 Gender",
            ["All", "Male", "Female"],
            help="Filter by gender category"
        )
        
        round_filter = st.selectbox(
            "🎯 Round",
            ["All", "Semis", "Final"],
            help="Filter by competition round"
        )
    
    # Filter competitions
    filtered_competitions = get_filtered_competitions(competition_type, gender_filter, round_filter)
    
    if not filtered_competitions:
        st.markdown("""
        <div class="error-card">
            <h3>⚠️ No Competitions Found</h3>
            <p>No competitions match your current filters. Please adjust your selection.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Competition overview
    st.markdown("### 🚀 Competition Overview")
    
    # Calculate overview metrics with progress
    overview_metrics = calculate_overview_metrics(filtered_competitions)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <h4>🏆 Total</h4>
            <h2>{overview_metrics["total"]}</h2>
        </div>
        ''', unsafe_allow_html=True)
    
    , na=False)) &
            (~df['Name'].astype(str).str.match(r'^\d+\+import streamlit as st
import pandas as pd
import requests
from io import StringIO
import time
from datetime import datetime, timedelta
import logging
import re
import os
from typing import Dict, Tuple, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure the page
st.set_page_config(
    page_title="🧗‍♂️ IFSC 2025 World Championships",
    page_icon="🧗‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with better mobile responsiveness
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        text-align: center;
        padding: 2rem 1rem;
        background: linear-gradient(135deg, #ff6b6b, #4ecdc4, #45b7d1);
        color: white;
        margin-bottom: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        animation: fadeIn 1s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Responsive athlete cards */
    .athlete-row {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 12px;
        font-weight: 500;
        border: 2px solid transparent;
        box-shadow: 0 3px 8px rgba(0,0,0,0.12);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .athlete-row:hover {
        transform: translateY(-3px) scale(1.01);
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    }
    
    .athlete-row strong {
        font-size: 1.1rem;
        display: block;
        margin-bottom: 0.5rem;
        text-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    .athlete-row small {
        font-size: 0.9rem;
        opacity: 0.9;
        line-height: 1.4;
    }
    
    .athlete-row .targets {
        background-color: rgba(0, 0, 0, 0.15);
        padding: 0.6rem 0.8rem;
        border-radius: 8px;
        margin-top: 0.6rem;
        display: inline-block;
        font-weight: 600;
        border: 2px solid rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(5px);
        font-size: 0.85rem;
    }
    
    /* Status-based styling */
    .podium-position {
        background: linear-gradient(135deg, #d4edda, #c3e6cb) !important;
        border: 2px solid #28a745 !important;
        color: #155724 !important;
    }
    
    .podium-position .targets {
        background-color: rgba(40, 167, 69, 0.25) !important;
        color: #155724 !important;
        border: 2px solid #28a745 !important;
    }
    
    .qualified {
        background: linear-gradient(135deg, #d4edda, #c3e6cb);
        border: 2px solid #28a745;
        color: #155724;
    }
    
    .podium-contention {
        background: linear-gradient(135deg, #fff3cd, #ffeaa7);
        border: 2px solid #ffc107;
        color: #856404;
    }
    
    .eliminated, .no-podium {
        background: linear-gradient(135deg, #f8d7da, #f1b0b7);
        border: 2px solid #dc3545;
        color: #721c24;
    }
    
    .awaiting-result {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        border: 2px solid #6c757d;
        color: #495057;
    }
    
    /* Enhanced metric cards */
    .metric-card {
        background: linear-gradient(135deg, white, #f8f9fa);
        padding: 1.5rem 1rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        text-align: center;
        color: #333333;
        border: 1px solid #e9ecef;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .metric-card h4 {
        color: #666666;
        margin-bottom: 0.8rem;
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-card h2 {
        color: #333333;
        margin: 0;
        font-size: 1.6rem;
        font-weight: bold;
        text-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-left: 0.5rem;
    }
    
    .badge-live {
        background: linear-gradient(45deg, #ff4757, #ff6b6b);
        color: white;
        animation: pulse 2s infinite;
    }
    
    .badge-completed {
        background: linear-gradient(45deg, #2ed573, #7bed9f);
        color: white;
    }
    
    .badge-upcoming {
        background: linear-gradient(45deg, #ffa502, #ff6348);
        color: white;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    /* Threshold and error cards */
    .threshold-card {
        background: linear-gradient(135deg, #e3f2fd, #bbdefb);
        border: 2px solid #2196f3;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        color: #0d47a1;
    }
    
    .error-card {
        background: linear-gradient(135deg, #ffebee, #ffcdd2);
        border: 2px solid #f44336;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        color: #c62828;
    }
    
    /* Progress bar */
    .progress-bar {
        width: 100%;
        height: 6px;
        background-color: #e9ecef;
        border-radius: 3px;
        margin: 0.5rem 0;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #28a745, #20c997);
        border-radius: 3px;
        transition: width 0.3s ease;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .metric-card {
            padding: 1rem 0.5rem;
        }
        
        .metric-card h2 {
            font-size: 1.4rem;
        }
        
        .athlete-row {
            padding: 0.8rem;
        }
        
        .athlete-row strong {
            font-size: 1rem;
        }
        
        .athlete-row .targets {
            font-size: 0.8rem;
            padding: 0.5rem 0.6rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Configuration with enhanced settings
class Config:
    CACHE_TTL = 30
    AUTO_REFRESH_INTERVAL = 60
    MAX_RETRIES = 3
    REQUEST_TIMEOUT = 15
    MAX_ATHLETES_DISPLAY = 50
    
    # Google Sheets URLs
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

class DataProcessor:
    """Enhanced data processing utilities"""
    
    @staticmethod
    def safe_numeric_conversion(value, default=0) -> float:
        """Safely convert value to numeric with proper error handling"""
        try:
            if pd.isna(value) or value == '' or value is None:
                return default
            return pd.to_numeric(value, errors='coerce')
        except Exception as e:
            logger.warning(f"Error converting {value} to numeric: {e}")
            return default

    @staticmethod
    def clean_text(text) -> str:
        """Enhanced text cleaning with better Unicode handling"""
        if not isinstance(text, str):
            return str(text) if text is not None else ""
        
        try:
            # Better Unicode handling
            cleaned = text.encode('utf-8', 'ignore').decode('utf-8')
            # Remove extra whitespace
            cleaned = ' '.join(cleaned.split())
            # Remove common problematic characters
            cleaned = re.sub(r'[^\w\s\-\.\,\(\)]+', '', cleaned)
            return cleaned.strip()
        except Exception as e:
            logger.warning(f"Error cleaning text '{text}': {e}")
            return str(text) if text is not None else ""

    @staticmethod
    def validate_dataframe(df: pd.DataFrame, expected_columns: List[str]) -> Tuple[bool, List[str]]:
        """Enhanced DataFrame validation"""
        if df.empty:
            return False, ["DataFrame is empty"]
        
        issues = []
        missing_cols = [col for col in expected_columns if col not in df.columns]
        
        if missing_cols:
            issues.append(f"Missing columns: {', '.join(missing_cols)}")
        
        # Check for minimum data requirements
        if len(df) < 1:
            issues.append("Insufficient data rows")
        
        return len(issues) == 0, issues

class CompetitionStatusDetector:
    """Enhanced competition status detection"""
    
    @staticmethod
    def get_competition_status(df: pd.DataFrame, competition_name: str) -> Tuple[str, str]:
        """Determine competition status with improved logic"""
        if df.empty:
            return "upcoming", "📄"
        
        try:
            if "Boulder" in competition_name:
                return CompetitionStatusDetector._get_boulder_status(df)
            elif "Lead" in competition_name:
                return CompetitionStatusDetector._get_lead_status(df)
        except Exception as e:
            logger.warning(f"Error determining status for {competition_name}: {e}")
        
        return "upcoming", "📄"
    
    @staticmethod
    def _get_boulder_status(df: pd.DataFrame) -> Tuple[str, str]:
        """Determine boulder competition status"""
        score_cols = [col for col in df.columns if 'Score' in str(col)]
        if not score_cols:
            return "upcoming", "📄"
        
        has_scores = df[score_cols].notna().any().any()
        if not has_scores:
            return "upcoming", "📄"
        
        total_athletes = len(df[df.iloc[:, 0].notna() & (df.iloc[:, 0] != '')])
        completed_athletes = len(df[df[score_cols].notna().any(axis=1)])
        
        completion_rate = completed_athletes / max(total_athletes, 1)
        
        if completion_rate >= 0.9:
            return "completed", "✅"
        elif completion_rate >= 0.1:
            return "live", "🔴"
        else:
            return "upcoming", "📄"
    
    @staticmethod
    def _get_lead_status(df: pd.DataFrame) -> Tuple[str, str]:
        """Determine lead competition status"""
        if 'Manual Score' not in df.columns:
            return "upcoming", "📄"
        
        has_scores = df['Manual Score'].notna().any()
        if not has_scores:
            return "upcoming", "📄"
        
        total_athletes = len(df[df['Name'].notna() & (df['Name'] != '')])
        completed_athletes = len(df[df['Manual Score'].notna()])
        
        completion_rate = completed_athletes / max(total_athletes, 1)
        
        if completion_rate >= 0.9:
            return "completed", "✅"
        elif completion_rate >= 0.1:
            return "live", "🔴"
        else:
            return "upcoming", "📄"

class DataLoader:
    """Enhanced data loading with better error handling and caching"""
    
    @staticmethod
    @st.cache_data(ttl=Config.CACHE_TTL, show_spinner=False)
    def load_sheet_data(url: str, retries: int = 0) -> pd.DataFrame:
        """Load data from Google Sheets with enhanced error handling"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/csv,text/plain,*/*',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive'
            }
            
            response = requests.get(
                url, 
                timeout=Config.REQUEST_TIMEOUT,
                headers=headers,
                stream=True
            )
            response.raise_for_status()
            
            # Read CSV data with better encoding handling
            csv_data = StringIO(response.text)
            df = pd.read_csv(csv_data, encoding='utf-8', low_memory=False)
            
            # Enhanced data cleaning
            df = DataLoader._clean_dataframe(df)
            
            logger.info(f"Successfully loaded data: {len(df)} rows, {len(df.columns)} columns")
            return df
            
        except requests.RequestException as e:
            error_msg = f"Network error: {str(e)}"
            logger.error(error_msg)
            
            if retries < Config.MAX_RETRIES:
                logger.info(f"Retrying... attempt {retries + 1}")
                time.sleep(2 ** retries)
                return DataLoader.load_sheet_data(url, retries + 1)
            
            st.error(f"🚫 {error_msg}")
            return pd.DataFrame()
            
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            st.error(f"🚫 {error_msg}")
            return pd.DataFrame()
    
    @staticmethod
    def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """Enhanced DataFrame cleaning"""
        # Remove completely empty rows
        df = df.dropna(how='all')
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Remove unnamed columns
        unnamed_cols = [col for col in df.columns if str(col).startswith('Unnamed')]
        df = df.drop(columns=unnamed_cols, errors='ignore')
        
        # Clean text data
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].apply(DataProcessor.clean_text)
        
        return df

class MetricsCalculator:
    """Enhanced metrics calculation"""
    
    @staticmethod
    def calculate_boulder_metrics(df: pd.DataFrame) -> Dict[str, any]:
        """Calculate boulder competition metrics"""
        try:
            total_athletes = len(df[df['Athlete Name'].notna() & (df['Athlete Name'] != '')])
            
            boulder_cols = [col for col in df.columns if 'Boulder' in str(col) and 'Score' in str(col)]
            completed_problems = sum(df[col].notna().sum() for col in boulder_cols) if boulder_cols else 0
            
            # Find total score column
            score_col = next((col for col in df.columns if 'Total Score' in str(col)), None)
            
            avg_score = 0
            if score_col:
                numeric_scores = pd.to_numeric(df[score_col], errors='coerce')
                avg_score = numeric_scores.mean() if not numeric_scores.isna().all() else 0
            
            # Find leader
            leader = "TBD"
            if 'Current Position/Rank' in df.columns:
                try:
                    leader_mask = pd.to_numeric(df['Current Position/Rank'], errors='coerce') == 1
                    if leader_mask.any():
                        leader = DataProcessor.clean_text(df.loc[leader_mask, 'Athlete Name'].iloc[0])
                except:
                    pass
            
            return {
                'total_athletes': total_athletes,
                'completed_problems': completed_problems,
                'avg_score': avg_score,
                'leader': leader
            }
        except Exception as e:
            logger.error(f"Error calculating boulder metrics: {e}")
            return {'total_athletes': 0, 'completed_problems': 0, 'avg_score': 0, 'leader': 'TBD'}
    
    @staticmethod
    def calculate_lead_metrics(df: pd.DataFrame) -> Dict[str, any]:
        """Calculate lead competition metrics"""
        try:
            # Filter active athletes
            active_df = df[
                df['Name'].notna() & 
                (df['Name'] != '') & 
                (~df['Name'].astype(str).str.contains('Hold for', na=False)) &
                (~df['Name'].astype(str).str.contains('Min to', na=False))
            ]
            
            total_athletes = len(active_df)
            completed = len(active_df[active_df['Manual Score'].notna() & (active_df['Manual Score'] != '')])
            
            # Calculate average score
            avg_score = 0
            if 'Manual Score' in active_df.columns:
                scores = pd.to_numeric(active_df['Manual Score'], errors='coerce')
                avg_score = scores.mean() if not scores.isna().all() else 0
            
            # Find leader
            leader = "TBD"
            if 'Current Rank' in active_df.columns:
                try:
                    leader_idx = pd.to_numeric(active_df['Current Rank'], errors='coerce') == 1
                    if leader_idx.any():
                        leader = DataProcessor.clean_text(active_df.loc[leader_idx, 'Name'].iloc[0])
                except:
                    pass
            
            return {
                'total_athletes': total_athletes,
                'completed': completed,
                'avg_score': avg_score,
                'leader': leader
            }
        except Exception as e:
            logger.error(f"Error calculating lead metrics: {e}")
            return {'total_athletes': 0, 'completed': 0, 'avg_score': 0, 'leader': 'TBD'}

def display_enhanced_metrics(df: pd.DataFrame, competition_name: str):
    """Display enhanced metrics with progress indicators"""
    col1, col2, col3, col4 = st.columns(4)
    
    if "Boulder" in competition_name:
        metrics = MetricsCalculator.calculate_boulder_metrics(df)
        
        with col1:
            st.markdown(f'''
            <div class="metric-card">
                <h4>👥 Athletes</h4>
                <h2>{metrics["total_athletes"]}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''
            <div class="metric-card">
                <h4>🧗‍♂️ Problems Completed</h4>
                <h2>{metrics["completed_problems"]}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'''
            <div class="metric-card">
                <h4>📊 Avg Score</h4>
                <h2>{metrics["avg_score"]:.1f}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        with col4:
            st.markdown(f'''
            <div class="metric-card">
                <h4>🥇 Leader</h4>
                <h2>{metrics["leader"][:15]}{"..." if len(metrics["leader"]) > 15 else ""}</h2>
            </div>
            ''', unsafe_allow_html=True)
    
    elif "Lead" in competition_name:
        metrics = MetricsCalculator.calculate_lead_metrics(df)
        
        with col1:
            st.markdown(f'''
            <div class="metric-card">
                <h4>👥 Athletes</h4>
                <h2>{metrics["total_athletes"]}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            completion_rate = (metrics["completed"] / max(metrics["total_athletes"], 1)) * 100
            st.markdown(f'''
            <div class="metric-card">
                <h4>✅ Completed</h4>
                <h2>{metrics["completed"]}</h2>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {completion_rate}%"></div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'''
            <div class="metric-card">
                <h4>📊 Avg Score</h4>
                <h2>{metrics["avg_score"]:.1f}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        with col4:
            st.markdown(f'''
            <div class="metric-card">
                <h4>🥇 Leader</h4>
                <h2>{metrics["leader"][:15]}{"..." if len(metrics["leader"]) > 15 else ""}</h2>
            </div>
            ''', unsafe_allow_html=True)

def is_placeholder_athlete(name: str) -> bool:
    """Check if name is a placeholder or reference entry"""
    name_str = str(name).strip().lower()
    
    # Check for "Athlete X" pattern first
    if name_str.startswith('athlete '):
        remaining = name_str[8:].strip()
        if remaining.isdigit():
            return True
    
    placeholder_patterns = [
        r'^n/a$|^na$',                # Not available
        r'^athlete\s+\d+',            # "Athlete 1", "Athlete 23"
        r'^climber\s+\d+',            # "Climber 1", "Climber 23"  
        r'^competitor\s+\d+',         # "Competitor 1"
        r'^\d+$',                     # Just numbers
        r'^\d+\.\d+$',                # Decimal numbers
        r'^\d+\+$',                   # "25+"
        r'^tbd$|^tba$',               # To be determined/announced
        r'^n\/a$|^na$',               # Not available
        r'^hold\s+\d+',               # "Hold 25"
        r'^zone\s+\d+',               # "Zone 40"
        r'^top\s+\d+',                # "Top 50"
        r'qualification|threshold',    # Reference text
        r'worst|best|average',        # Statistical text
        r'points|score|rank',         # Score-related text
    ]
    
    # Check against patterns
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

def main():
    """Enhanced main application function"""
    
    # Initialize session state
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = datetime.now()
    if 'auto_refresh_enabled' not in st.session_state:
        st.session_state.auto_refresh_enabled = True
    if 'selected_competitions' not in st.session_state:
        st.session_state.selected_competitions = []
    
    # Enhanced header
    st.markdown("""
    <div class="main-header">
        <h1>🧗‍♂️ IFSC 2025 World Championships</h1>
        <h3>Live Competition Results Dashboard</h3>
        <p style="margin: 0; opacity: 0.9;">Real-time climbing competition tracking</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced sidebar
    st.sidebar.title("🎯 Dashboard Controls")
    
    # Auto-refresh section
    with st.sidebar.expander("🔄 Refresh Settings", expanded=True):
        auto_refresh = st.checkbox(
            "Enable Auto-Refresh", 
            value=st.session_state.auto_refresh_enabled,
            help=f"Updates every {Config.AUTO_REFRESH_INTERVAL}s"
        )
        st.session_state.auto_refresh_enabled = auto_refresh
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh", type="primary", use_container_width=True):
                st.cache_data.clear()
                st.session_state.last_refresh = datetime.now()
                st.success("✅ Refreshed!")
                time.sleep(0.5)
                st.rerun()
        
        with col2:
            if st.button("🗑️ Clear Cache", use_container_width=True):
                st.cache_data.clear()
                st.success("✅ Cache cleared!")
        
        # Show refresh status
        time_since = (datetime.now() - st.session_state.last_refresh).seconds
        st.caption(f"🕐 Last refresh: {time_since}s ago")
    
    # Competition filters
    with st.sidebar.expander("🎯 Competition Filters", expanded=True):
        competition_type = st.selectbox(
            "⛰️ Discipline",
            ["All", "Boulder", "Lead"],
            help="Filter by climbing discipline"
        )
        
        gender_filter = st.selectbox(
            "👤 Gender",
            ["All", "Male", "Female"],
            help="Filter by gender category"
        )
        
        round_filter = st.selectbox(
            "🎯 Round",
            ["All", "Semis", "Final"],
            help="Filter by competition round"
        )
    
    # Filter competitions
    filtered_competitions = get_filtered_competitions(competition_type, gender_filter, round_filter)
    
    if not filtered_competitions:
        st.markdown("""
        <div class="error-card">
            <h3>⚠️ No Competitions Found</h3>
            <p>No competitions match your current filters. Please adjust your selection.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Competition overview
    st.markdown("### 🚀 Competition Overview")
    
    # Calculate overview metrics with progress
    overview_metrics = calculate_overview_metrics(filtered_competitions)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <h4>🏆 Total</h4>
            <h2>{overview_metrics["total"]}</h2>
        </div>
        ''', unsafe_allow_html=True)
    
    , na=False)) &
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
            st.code(traceback.format_exc())import streamlit as st
import pandas as pd
import requests
from io import StringIO
import time
from datetime import datetime, timedelta
import logging
import re
import os
from typing import Dict, Tuple, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure the page
st.set_page_config(
    page_title="🧗‍♂️ IFSC 2025 World Championships",
    page_icon="🧗‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with better mobile responsiveness
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        text-align: center;
        padding: 2rem 1rem;
        background: linear-gradient(135deg, #ff6b6b, #4ecdc4, #45b7d1);
        color: white;
        margin-bottom: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        animation: fadeIn 1s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Responsive athlete cards */
    .athlete-row {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 12px;
        font-weight: 500;
        border: 2px solid transparent;
        box-shadow: 0 3px 8px rgba(0,0,0,0.12);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .athlete-row:hover {
        transform: translateY(-3px) scale(1.01);
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    }
    
    .athlete-row strong {
        font-size: 1.1rem;
        display: block;
        margin-bottom: 0.5rem;
        text-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    .athlete-row small {
        font-size: 0.9rem;
        opacity: 0.9;
        line-height: 1.4;
    }
    
    .athlete-row .targets {
        background-color: rgba(0, 0, 0, 0.15);
        padding: 0.6rem 0.8rem;
        border-radius: 8px;
        margin-top: 0.6rem;
        display: inline-block;
        font-weight: 600;
        border: 2px solid rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(5px);
        font-size: 0.85rem;
    }
    
    /* Status-based styling */
    .podium-position {
        background: linear-gradient(135deg, #d4edda, #c3e6cb) !important;
        border: 2px solid #28a745 !important;
        color: #155724 !important;
    }
    
    .podium-position .targets {
        background-color: rgba(40, 167, 69, 0.25) !important;
        color: #155724 !important;
        border: 2px solid #28a745 !important;
    }
    
    .qualified {
        background: linear-gradient(135deg, #d4edda, #c3e6cb);
        border: 2px solid #28a745;
        color: #155724;
    }
    
    .podium-contention {
        background: linear-gradient(135deg, #fff3cd, #ffeaa7);
        border: 2px solid #ffc107;
        color: #856404;
    }
    
    .eliminated, .no-podium {
        background: linear-gradient(135deg, #f8d7da, #f1b0b7);
        border: 2px solid #dc3545;
        color: #721c24;
    }
    
    .awaiting-result {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        border: 2px solid #6c757d;
        color: #495057;
    }
    
    /* Enhanced metric cards */
    .metric-card {
        background: linear-gradient(135deg, white, #f8f9fa);
        padding: 1.5rem 1rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        text-align: center;
        color: #333333;
        border: 1px solid #e9ecef;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .metric-card h4 {
        color: #666666;
        margin-bottom: 0.8rem;
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-card h2 {
        color: #333333;
        margin: 0;
        font-size: 1.6rem;
        font-weight: bold;
        text-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-left: 0.5rem;
    }
    
    .badge-live {
        background: linear-gradient(45deg, #ff4757, #ff6b6b);
        color: white;
        animation: pulse 2s infinite;
    }
    
    .badge-completed {
        background: linear-gradient(45deg, #2ed573, #7bed9f);
        color: white;
    }
    
    .badge-upcoming {
        background: linear-gradient(45deg, #ffa502, #ff6348);
        color: white;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    /* Threshold and error cards */
    .threshold-card {
        background: linear-gradient(135deg, #e3f2fd, #bbdefb);
        border: 2px solid #2196f3;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        color: #0d47a1;
    }
    
    .error-card {
        background: linear-gradient(135deg, #ffebee, #ffcdd2);
        border: 2px solid #f44336;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        color: #c62828;
    }
    
    /* Progress bar */
    .progress-bar {
        width: 100%;
        height: 6px;
        background-color: #e9ecef;
        border-radius: 3px;
        margin: 0.5rem 0;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #28a745, #20c997);
        border-radius: 3px;
        transition: width 0.3s ease;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .metric-card {
            padding: 1rem 0.5rem;
        }
        
        .metric-card h2 {
            font-size: 1.4rem;
        }
        
        .athlete-row {
            padding: 0.8rem;
        }
        
        .athlete-row strong {
            font-size: 1rem;
        }
        
        .athlete-row .targets {
            font-size: 0.8rem;
            padding: 0.5rem 0.6rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Configuration with enhanced settings
class Config:
    CACHE_TTL = 30
    AUTO_REFRESH_INTERVAL = 60
    MAX_RETRIES = 3
    REQUEST_TIMEOUT = 15
    MAX_ATHLETES_DISPLAY = 50
    
    # Google Sheets URLs
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

class DataProcessor:
    """Enhanced data processing utilities"""
    
    @staticmethod
    def safe_numeric_conversion(value, default=0) -> float:
        """Safely convert value to numeric with proper error handling"""
        try:
            if pd.isna(value) or value == '' or value is None:
                return default
            return pd.to_numeric(value, errors='coerce')
        except Exception as e:
            logger.warning(f"Error converting {value} to numeric: {e}")
            return default

    @staticmethod
    def clean_text(text) -> str:
        """Enhanced text cleaning with better Unicode handling"""
        if not isinstance(text, str):
            return str(text) if text is not None else ""
        
        try:
            # Better Unicode handling
            cleaned = text.encode('utf-8', 'ignore').decode('utf-8')
            # Remove extra whitespace
            cleaned = ' '.join(cleaned.split())
            # Remove common problematic characters
            cleaned = re.sub(r'[^\w\s\-\.\,\(\)]+', '', cleaned)
            return cleaned.strip()
        except Exception as e:
            logger.warning(f"Error cleaning text '{text}': {e}")
            return str(text) if text is not None else ""

    @staticmethod
    def validate_dataframe(df: pd.DataFrame, expected_columns: List[str]) -> Tuple[bool, List[str]]:
        """Enhanced DataFrame validation"""
        if df.empty:
            return False, ["DataFrame is empty"]
        
        issues = []
        missing_cols = [col for col in expected_columns if col not in df.columns]
        
        if missing_cols:
            issues.append(f"Missing columns: {', '.join(missing_cols)}")
        
        # Check for minimum data requirements
        if len(df) < 1:
            issues.append("Insufficient data rows")
        
        return len(issues) == 0, issues

class CompetitionStatusDetector:
    """Enhanced competition status detection"""
    
    @staticmethod
    def get_competition_status(df: pd.DataFrame, competition_name: str) -> Tuple[str, str]:
        """Determine competition status with improved logic"""
        if df.empty:
            return "upcoming", "📄"
        
        try:
            if "Boulder" in competition_name:
                return CompetitionStatusDetector._get_boulder_status(df)
            elif "Lead" in competition_name:
                return CompetitionStatusDetector._get_lead_status(df)
        except Exception as e:
            logger.warning(f"Error determining status for {competition_name}: {e}")
        
        return "upcoming", "📄"
    
    @staticmethod
    def _get_boulder_status(df: pd.DataFrame) -> Tuple[str, str]:
        """Determine boulder competition status"""
        score_cols = [col for col in df.columns if 'Score' in str(col)]
        if not score_cols:
            return "upcoming", "📄"
        
        has_scores = df[score_cols].notna().any().any()
        if not has_scores:
            return "upcoming", "📄"
        
        total_athletes = len(df[df.iloc[:, 0].notna() & (df.iloc[:, 0] != '')])
        completed_athletes = len(df[df[score_cols].notna().any(axis=1)])
        
        completion_rate = completed_athletes / max(total_athletes, 1)
        
        if completion_rate >= 0.9:
            return "completed", "✅"
        elif completion_rate >= 0.1:
            return "live", "🔴"
        else:
            return "upcoming", "📄"
    
    @staticmethod
    def _get_lead_status(df: pd.DataFrame) -> Tuple[str, str]:
        """Determine lead competition status"""
        if 'Manual Score' not in df.columns:
            return "upcoming", "📄"
        
        has_scores = df['Manual Score'].notna().any()
        if not has_scores:
            return "upcoming", "📄"
        
        total_athletes = len(df[df['Name'].notna() & (df['Name'] != '')])
        completed_athletes = len(df[df['Manual Score'].notna()])
        
        completion_rate = completed_athletes / max(total_athletes, 1)
        
        if completion_rate >= 0.9:
            return "completed", "✅"
        elif completion_rate >= 0.1:
            return "live", "🔴"
        else:
            return "upcoming", "📄"

class DataLoader:
    """Enhanced data loading with better error handling and caching"""
    
    @staticmethod
    @st.cache_data(ttl=Config.CACHE_TTL, show_spinner=False)
    def load_sheet_data(url: str, retries: int = 0) -> pd.DataFrame:
        """Load data from Google Sheets with enhanced error handling"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/csv,text/plain,*/*',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive'
            }
            
            response = requests.get(
                url, 
                timeout=Config.REQUEST_TIMEOUT,
                headers=headers,
                stream=True
            )
            response.raise_for_status()
            
            # Read CSV data with better encoding handling
            csv_data = StringIO(response.text)
            df = pd.read_csv(csv_data, encoding='utf-8', low_memory=False)
            
            # Enhanced data cleaning
            df = DataLoader._clean_dataframe(df)
            
            logger.info(f"Successfully loaded data: {len(df)} rows, {len(df.columns)} columns")
            return df
            
        except requests.RequestException as e:
            error_msg = f"Network error: {str(e)}"
            logger.error(error_msg)
            
            if retries < Config.MAX_RETRIES:
                logger.info(f"Retrying... attempt {retries + 1}")
                time.sleep(2 ** retries)
                return DataLoader.load_sheet_data(url, retries + 1)
            
            st.error(f"🚫 {error_msg}")
            return pd.DataFrame()
            
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            st.error(f"🚫 {error_msg}")
            return pd.DataFrame()
    
    @staticmethod
    def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """Enhanced DataFrame cleaning"""
        # Remove completely empty rows
        df = df.dropna(how='all')
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Remove unnamed columns
        unnamed_cols = [col for col in df.columns if str(col).startswith('Unnamed')]
        df = df.drop(columns=unnamed_cols, errors='ignore')
        
        # Clean text data
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].apply(DataProcessor.clean_text)
        
        return df

class MetricsCalculator:
    """Enhanced metrics calculation"""
    
    @staticmethod
    def calculate_boulder_metrics(df: pd.DataFrame) -> Dict[str, any]:
        """Calculate boulder competition metrics"""
        try:
            total_athletes = len(df[df['Athlete Name'].notna() & (df['Athlete Name'] != '')])
            
            boulder_cols = [col for col in df.columns if 'Boulder' in str(col) and 'Score' in str(col)]
            completed_problems = sum(df[col].notna().sum() for col in boulder_cols) if boulder_cols else 0
            
            # Find total score column
            score_col = next((col for col in df.columns if 'Total Score' in str(col)), None)
            
            avg_score = 0
            if score_col:
                numeric_scores = pd.to_numeric(df[score_col], errors='coerce')
                avg_score = numeric_scores.mean() if not numeric_scores.isna().all() else 0
            
            # Find leader
            leader = "TBD"
            if 'Current Position/Rank' in df.columns:
                try:
                    leader_mask = pd.to_numeric(df['Current Position/Rank'], errors='coerce') == 1
                    if leader_mask.any():
                        leader = DataProcessor.clean_text(df.loc[leader_mask, 'Athlete Name'].iloc[0])
                except:
                    pass
            
            return {
                'total_athletes': total_athletes,
                'completed_problems': completed_problems,
                'avg_score': avg_score,
                'leader': leader
            }
        except Exception as e:
            logger.error(f"Error calculating boulder metrics: {e}")
            return {'total_athletes': 0, 'completed_problems': 0, 'avg_score': 0, 'leader': 'TBD'}
    
    @staticmethod
    def calculate_lead_metrics(df: pd.DataFrame) -> Dict[str, any]:
        """Calculate lead competition metrics"""
        try:
            # Filter active athletes
            active_df = df[
                df['Name'].notna() & 
                (df['Name'] != '') & 
                (~df['Name'].astype(str).str.contains('Hold for', na=False)) &
                (~df['Name'].astype(str).str.contains('Min to', na=False))
            ]
            
            total_athletes = len(active_df)
            completed = len(active_df[active_df['Manual Score'].notna() & (active_df['Manual Score'] != '')])
            
            # Calculate average score
            avg_score = 0
            if 'Manual Score' in active_df.columns:
                scores = pd.to_numeric(active_df['Manual Score'], errors='coerce')
                avg_score = scores.mean() if not scores.isna().all() else 0
            
            # Find leader
            leader = "TBD"
            if 'Current Rank' in active_df.columns:
                try:
                    leader_idx = pd.to_numeric(active_df['Current Rank'], errors='coerce') == 1
                    if leader_idx.any():
                        leader = DataProcessor.clean_text(active_df.loc[leader_idx, 'Name'].iloc[0])
                except:
                    pass
            
            return {
                'total_athletes': total_athletes,
                'completed': completed,
                'avg_score': avg_score,
                'leader': leader
            }
        except Exception as e:
            logger.error(f"Error calculating lead metrics: {e}")
            return {'total_athletes': 0, 'completed': 0, 'avg_score': 0, 'leader': 'TBD'}

def display_enhanced_metrics(df: pd.DataFrame, competition_name: str):
    """Display enhanced metrics with progress indicators"""
    col1, col2, col3, col4 = st.columns(4)
    
    if "Boulder" in competition_name:
        metrics = MetricsCalculator.calculate_boulder_metrics(df)
        
        with col1:
            st.markdown(f'''
            <div class="metric-card">
                <h4>👥 Athletes</h4>
                <h2>{metrics["total_athletes"]}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''
            <div class="metric-card">
                <h4>🧗‍♂️ Problems Completed</h4>
                <h2>{metrics["completed_problems"]}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'''
            <div class="metric-card">
                <h4>📊 Avg Score</h4>
                <h2>{metrics["avg_score"]:.1f}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        with col4:
            st.markdown(f'''
            <div class="metric-card">
                <h4>🥇 Leader</h4>
                <h2>{metrics["leader"][:15]}{"..." if len(metrics["leader"]) > 15 else ""}</h2>
            </div>
            ''', unsafe_allow_html=True)
    
    elif "Lead" in competition_name:
        metrics = MetricsCalculator.calculate_lead_metrics(df)
        
        with col1:
            st.markdown(f'''
            <div class="metric-card">
                <h4>👥 Athletes</h4>
                <h2>{metrics["total_athletes"]}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            completion_rate = (metrics["completed"] / max(metrics["total_athletes"], 1)) * 100
            st.markdown(f'''
            <div class="metric-card">
                <h4>✅ Completed</h4>
                <h2>{metrics["completed"]}</h2>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {completion_rate}%"></div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'''
            <div class="metric-card">
                <h4>📊 Avg Score</h4>
                <h2>{metrics["avg_score"]:.1f}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        with col4:
            st.markdown(f'''
            <div class="metric-card">
                <h4>🥇 Leader</h4>
                <h2>{metrics["leader"][:15]}{"..." if len(metrics["leader"]) > 15 else ""}</h2>
            </div>
            ''', unsafe_allow_html=True)

def is_placeholder_athlete(name: str) -> bool:
    """Check if name is a placeholder or reference entry"""
    name_str = str(name).strip().lower()
    
    # Check for "Athlete X" pattern first
    if name_str.startswith('athlete '):
        remaining = name_str[8:].strip()
        if remaining.isdigit():
            return True
    
    placeholder_patterns = [
        r'^n/a$|^na$',                # Not available
        r'^athlete\s+\d+',            # "Athlete 1", "Athlete 23"
        r'^climber\s+\d+',            # "Climber 1", "Climber 23"  
        r'^competitor\s+\d+',         # "Competitor 1"
        r'^\d+$',                     # Just numbers
        r'^\d+\.\d+$',                # Decimal numbers
        r'^\d+\+$',                   # "25+"
        r'^tbd$|^tba$',               # To be determined/announced
        r'^n\/a$|^na$',               # Not available
        r'^hold\s+\d+',               # "Hold 25"
        r'^zone\s+\d+',               # "Zone 40"
        r'^top\s+\d+',                # "Top 50"
        r'qualification|threshold',    # Reference text
        r'worst|best|average',        # Statistical text
        r'points|score|rank',         # Score-related text
    ]
    
    # Check against patterns
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

def main():
    """Enhanced main application function"""
    
    # Initialize session state
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = datetime.now()
    if 'auto_refresh_enabled' not in st.session_state:
        st.session_state.auto_refresh_enabled = True
    if 'selected_competitions' not in st.session_state:
        st.session_state.selected_competitions = []
    
    # Enhanced header
    st.markdown("""
    <div class="main-header">
        <h1>🧗‍♂️ IFSC 2025 World Championships</h1>
        <h3>Live Competition Results Dashboard</h3>
        <p style="margin: 0; opacity: 0.9;">Real-time climbing competition tracking</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced sidebar
    st.sidebar.title("🎯 Dashboard Controls")
    
    # Auto-refresh section
    with st.sidebar.expander("🔄 Refresh Settings", expanded=True):
        auto_refresh = st.checkbox(
            "Enable Auto-Refresh", 
            value=st.session_state.auto_refresh_enabled,
            help=f"Updates every {Config.AUTO_REFRESH_INTERVAL}s"
        )
        st.session_state.auto_refresh_enabled = auto_refresh
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh", type="primary", use_container_width=True):
                st.cache_data.clear()
                st.session_state.last_refresh = datetime.now()
                st.success("✅ Refreshed!")
                time.sleep(0.5)
                st.rerun()
        
        with col2:
            if st.button("🗑️ Clear Cache", use_container_width=True):
                st.cache_data.clear()
                st.success("✅ Cache cleared!")
        
        # Show refresh status
        time_since = (datetime.now() - st.session_state.last_refresh).seconds
        st.caption(f"🕐 Last refresh: {time_since}s ago")
    
    # Competition filters
    with st.sidebar.expander("🎯 Competition Filters", expanded=True):
        competition_type = st.selectbox(
            "⛰️ Discipline",
            ["All", "Boulder", "Lead"],
            help="Filter by climbing discipline"
        )
        
        gender_filter = st.selectbox(
            "👤 Gender",
            ["All", "Male", "Female"],
            help="Filter by gender category"
        )
        
        round_filter = st.selectbox(
            "🎯 Round",
            ["All", "Semis", "Final"],
            help="Filter by competition round"
        )
    
    # Filter competitions
    filtered_competitions = get_filtered_competitions(competition_type, gender_filter, round_filter)
    
    if not filtered_competitions:
        st.markdown("""
        <div class="error-card">
            <h3>⚠️ No Competitions Found</h3>
            <p>No competitions match your current filters. Please adjust your selection.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Competition overview
    st.markdown("### 🚀 Competition Overview")
    
    # Calculate overview metrics with progress
    overview_metrics = calculate_overview_metrics(filtered_competitions)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <h4>🏆 Total</h4>
            <h2>{overview_metrics["total"]}</h2>
        </div>
        ''', unsafe_allow_html=True)
