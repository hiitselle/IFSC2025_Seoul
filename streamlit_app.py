import streamlit as st
import pandas as pd
import requests
from io import StringIO
import time
from datetime import datetime, timedelta
import logging
import re
import os
import unicodedata
from typing import Dict, Tuple, List, Optional, Any, Callable
import hashlib
import hmac
from collections import defaultdict, deque
from functools import wraps
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from scipy import stats
from concurrent.futures import ThreadPoolExecutor
import json

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

# Enhanced CSS with better mobile responsiveness and all improvements
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
    
    /* Status-based styling - FIXED */
    .athlete-row.podium-position {
        background: linear-gradient(135deg, #d4edda, #c3e6cb) !important;
        border: 2px solid #28a745 !important;
        color: #155724 !important;
    }
    
    .athlete-row.qualified {
        background: linear-gradient(135deg, #d4edda, #c3e6cb) !important;
        border: 2px solid #28a745 !important;
        color: #155724 !important;
    }
    
    .athlete-row.podium-contention {
        background: linear-gradient(135deg, #fff3cd, #ffeaa7) !important;
        border: 2px solid #ffc107 !important;
        color: #856404 !important;
    }
    
    .athlete-row.eliminated,
    .athlete-row.no-podium {
        background: linear-gradient(135deg, #f8d7da, #f1b0b7) !important;
        border: 2px solid #dc3545 !important;
        color: #721c24 !important;
    }
    
    .athlete-row.awaiting-result {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef) !important;
        border: 2px solid #6c757d !important;
        color: #495057 !important;
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
    
    /* Live notifications */
    .live-notification {
        position: fixed;
        top: 20px;
        right: 20px;
        background: #17a2b8;
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        z-index: 9999;
        animation: slideIn 0.5s ease-out;
        max-width: 300px;
        word-wrap: break-word;
    }
    
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 1.5rem !important;
        }
        .main-header h3 {
            font-size: 1.2rem !important;
        }
        .metric-card {
            padding: 0.8rem 0.5rem !important;
        }
        .metric-card h4 {
            font-size: 0.8rem !important;
        }
        .metric-card h2 {
            font-size: 1.3rem !important;
        }
        .athlete-row {
            padding: 0.6rem !important;
            margin: 0.3rem 0 !important;
        }
        .athlete-row strong {
            font-size: 0.9rem !important;
        }
        .athlete-row small {
            font-size: 0.8rem !important;
        }
    }
    
    /* Touch-friendly buttons */
    @media (hover: none) and (pointer: coarse) {
        .athlete-row:hover {
            transform: none !important;
        }
        button {
            min-height: 44px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Enhanced configuration with security settings
class Config:
    CACHE_TTL = 30
    AUTO_REFRESH_INTERVAL = 60
    MAX_RETRIES = 3
    REQUEST_TIMEOUT = 15
    MAX_ATHLETES_DISPLAY = 50
    
    # Performance settings
    CONCURRENT_REQUESTS = True
    BATCH_SIZE = 4
    MEMORY_LIMIT_MB = 100
    
    # Security settings
    ENABLE_RATE_LIMITING = True
    MAX_REQUESTS_PER_MINUTE = 30
    MAX_CONCURRENT_CONNECTIONS = 5
    ENABLE_REQUEST_SIGNING = True
    
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

class SecurityManager:
    """Enhanced security management for the application"""
    
    # Whitelist of allowed domains for data fetching
    ALLOWED_DOMAINS = {
        'docs.google.com',
        'sheets.googleapis.com',
        'drive.google.com'
    }
    
    # Maximum data size limits
    MAX_CSV_SIZE_MB = 10
    MAX_DATAFRAME_ROWS = 10000
    MAX_DATAFRAME_COLUMNS = 100
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate that URL is from allowed domains"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            
            # Remove www. prefix if present
            if domain.startswith('www.'):
                domain = domain[4:]
            
            return domain in SecurityManager.ALLOWED_DOMAINS
            
        except Exception as e:
            logger.warning(f"URL validation failed for {url}: {e}")
            return False
    
    @staticmethod
    def sanitize_input(input_str: str) -> str:
        """Sanitize user input to prevent injection attacks"""
        if not isinstance(input_str, str):
            return str(input_str)
        
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>"\';\\]', '', input_str)
        
        # Limit length
        sanitized = sanitized[:1000]
        
        # Remove multiple spaces
        sanitized = re.sub(r'\s+', ' ', sanitized).strip()
        
        return sanitized
    
    @staticmethod
    def validate_dataframe_size(df: pd.DataFrame) -> Tuple[bool, str]:
        """Validate DataFrame size limits"""
        if df.empty:
            return True, "DataFrame is empty"
        
        # Check row count
        if len(df) > SecurityManager.MAX_DATAFRAME_ROWS:
            return False, f"DataFrame has {len(df)} rows, maximum allowed is {SecurityManager.MAX_DATAFRAME_ROWS}"
        
        # Check column count
        if len(df.columns) > SecurityManager.MAX_DATAFRAME_COLUMNS:
            return False, f"DataFrame has {len(df.columns)} columns, maximum allowed is {SecurityManager.MAX_DATAFRAME_COLUMNS}"
        
        # Check memory usage
        memory_mb = df.memory_usage(deep=True).sum() / 1024 / 1024
        if memory_mb > SecurityManager.MAX_CSV_SIZE_MB:
            return False, f"DataFrame uses {memory_mb:.1f}MB, maximum allowed is {SecurityManager.MAX_CSV_SIZE_MB}MB"
        
        return True, "DataFrame size is acceptable"

class RateLimiter:
    """Rate limiting system to prevent abuse"""
    
    def __init__(self):
        self.requests = defaultdict(deque)  # IP -> deque of timestamps
        self.blocked_ips = set()
        self.block_duration = 300  # 5 minutes
        self.blocked_until = {}
    
    def is_rate_limited(self, identifier: str, max_requests: int = 60, 
                       time_window: int = 60) -> Tuple[bool, int]:
        """
        Check if identifier is rate limited
        Returns: (is_limited, time_until_reset)
        """
        current_time = time.time()
        
        # Check if currently blocked
        if identifier in self.blocked_until:
            if current_time < self.blocked_until[identifier]:
                remaining = int(self.blocked_until[identifier] - current_time)
                return True, remaining
            else:
                # Block expired
                del self.blocked_until[identifier]
                self.blocked_ips.discard(identifier)
        
        # Clean old requests
        request_queue = self.requests[identifier]
        while request_queue and request_queue[0] < current_time - time_window:
            request_queue.popleft()
        
        # Check rate limit
        if len(request_queue) >= max_requests:
            # Block the identifier
            self.blocked_ips.add(identifier)
            self.blocked_until[identifier] = current_time + self.block_duration
            return True, self.block_duration
        
        # Add current request
        request_queue.append(current_time)
        return False, 0
    
    def get_rate_limit_status(self, identifier: str, max_requests: int = 60, 
                            time_window: int = 60) -> Dict[str, any]:
        """Get current rate limit status for identifier"""
        current_time = time.time()
        request_queue = self.requests[identifier]
        
        # Clean old requests
        while request_queue and request_queue[0] < current_time - time_window:
            request_queue.popleft()
        
        remaining_requests = max(0, max_requests - len(request_queue))
        reset_time = int(current_time + time_window)
        
        return {
            'remaining_requests': remaining_requests,
            'reset_time': reset_time,
            'is_blocked': identifier in self.blocked_ips,
            'block_remaining': max(0, int(self.blocked_until.get(identifier, 0) - current_time))
        }

class SecureDataLoader:
    """Enhanced DataLoader with security features"""
    
    def __init__(self):
        self.rate_limiter = RateLimiter()
        self.security_manager = SecurityManager()
    
    @staticmethod
    def get_client_identifier() -> str:
        """Get client identifier for rate limiting"""
        # In Streamlit Cloud, we can use session state as identifier
        if 'client_id' not in st.session_state:
            st.session_state.client_id = hashlib.md5(
                f"{time.time()}:{id(st.session_state)}".encode()
            ).hexdigest()
        return st.session_state.client_id
    
    @st.cache_data(ttl=Config.CACHE_TTL, show_spinner=False)
    def load_sheet_data_secure(_self, url: str, retries: int = 0) -> pd.DataFrame:
        """Securely load sheet data with rate limiting and validation"""
        client_id = _self.get_client_identifier()
        
        # Check rate limiting
        is_limited, wait_time = _self.rate_limiter.is_rate_limited(client_id, max_requests=30, time_window=60)
        if is_limited:
            st.error(f"🚫 Rate limit exceeded. Please wait {wait_time} seconds before trying again.")
            return pd.DataFrame()
        
        # Validate URL
        if not _self.security_manager.validate_url(url):
            st.error("🚫 Access denied: URL not in allowed domains list.")
            return pd.DataFrame()
        
        try:
            # Enhanced request headers with security
            current_timestamp = int(time.time())
            
            headers = {
                'User-Agent': 'IFSC-Climbing-Dashboard/1.0',
                'Accept': 'text/csv,application/csv,text/plain',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=30',
                'Referer': 'https://ifsc-climbing-dashboard.streamlit.app'
            }
            
            # Make request with timeout and size limits
            response = requests.get(
                url, 
                timeout=Config.REQUEST_TIMEOUT,
                headers=headers,
                stream=True
            )
            response.raise_for_status()
            
            # Check content size before processing
            content_length = response.headers.get('content-length')
            if content_length and int(content_length) > _self.security_manager.MAX_CSV_SIZE_MB * 1024 * 1024:
                raise ValueError(f"Response too large: {content_length} bytes")
            
            # Read content with size limit
            content = ""
            total_size = 0
            max_size = _self.security_manager.MAX_CSV_SIZE_MB * 1024 * 1024
            
            for chunk in response.iter_content(chunk_size=8192, decode_unicode=True):
                if chunk:
                    total_size += len(chunk.encode('utf-8'))
                    if total_size > max_size:
                        raise ValueError(f"Response exceeded maximum size of {_self.security_manager.MAX_CSV_SIZE_MB}MB")
                    content += chunk
            
            # Process CSV data
            csv_data = StringIO(content)
            df = pd.read_csv(
                csv_data, 
                encoding='utf-8', 
                low_memory=False,
                dtype=str,
                na_values=['', 'N/A', 'TBD', 'TBA'],
                nrows=_self.security_manager.MAX_DATAFRAME_ROWS  # Limit rows
            )
            
            # Validate DataFrame size
            is_valid, message = _self.security_manager.validate_dataframe_size(df)
            if not is_valid:
                logger.warning(f"Data size warning: {message}")
                # Truncate if necessary
                if len(df) > _self.security_manager.MAX_DATAFRAME_ROWS:
                    df = df.head(_self.security_manager.MAX_DATAFRAME_ROWS)
            
            # Clean and sanitize data
            df = _self._clean_and_sanitize_dataframe(df)
            
            logger.info(f"Securely loaded data: {len(df)} rows, {len(df.columns)} columns")
            return df
            
        except requests.RequestException as e:
            error_msg = f"Network error: {str(e)}"
            logger.error(error_msg)
            
            if retries < Config.MAX_RETRIES:
                wait_time = 2 ** retries
                logger.info(f"Retrying in {wait_time}s... attempt {retries + 1}")
                time.sleep(wait_time)
                return _self.load_sheet_data_secure(url, retries + 1)
            
            return pd.DataFrame()
            
        except ValueError as e:
            logger.error(f"Data validation error: {str(e)}")
            return pd.DataFrame()
            
        except Exception as e:
            logger.error(f"Unexpected error loading data: {e}")
            return pd.DataFrame()
    
    def _clean_and_sanitize_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and sanitize DataFrame with security considerations"""
        # Basic cleaning
        df = df.dropna(how='all')
        
        # Sanitize column names
        df.columns = [self.security_manager.sanitize_input(str(col)) for col in df.columns]
        
        # Remove unnamed columns
        columns_to_keep = [col for col in df.columns if not str(col).startswith('Unnamed')]
        df = df[columns_to_keep]
        
        # Sanitize text data
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype(str).apply(self.security_manager.sanitize_input)
        
        return df

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

class CompetitionAnalytics:
    """Advanced analytics for competition data"""
    
    @staticmethod
    def calculate_performance_trends(df: pd.DataFrame, competition_name: str) -> Dict[str, Any]:
        """Calculate performance trends and statistics"""
        analytics = {
            'total_athletes': 0,
            'completion_rate': 0,
            'average_performance': 0,
            'performance_distribution': [],
            'difficulty_analysis': {},
            'progression_insights': []
        }
        
        try:
            if "Boulder" in competition_name:
                analytics.update(CompetitionAnalytics._analyze_boulder_performance(df))
            elif "Lead" in competition_name:
                analytics.update(CompetitionAnalytics._analyze_lead_performance(df))
                
        except Exception as e:
            logger.error(f"Error calculating analytics for {competition_name}: {e}")
            
        return analytics
    
    @staticmethod
    def _analyze_boulder_performance(df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze boulder competition performance"""
        analytics = {}
        
        try:
            # Find boulder score columns
            boulder_cols = [col for col in df.columns if 'Boulder' in str(col) and 'Score' in str(col)]
            
            if not boulder_cols or df.empty:
                return analytics
            
            # Calculate completion rates per boulder
            boulder_completion = {}
            boulder_avg_scores = {}
            
            for col in boulder_cols:
                boulder_num = col.split()[1] if len(col.split()) > 1 else col
                numeric_scores = pd.to_numeric(df[col], errors='coerce')
                
                # Completion rate (non-zero scores)
                completed = (numeric_scores > 0).sum()
                total_attempts = numeric_scores.notna().sum()
                completion_rate = completed / max(total_attempts, 1) * 100
                
                boulder_completion[f'Boulder {boulder_num}'] = completion_rate
                boulder_avg_scores[f'Boulder {boulder_num}'] = numeric_scores.mean() if not numeric_scores.isna().all() else 0
            
            # Overall performance metrics
            total_score_col = next((col for col in df.columns if 'Total Score' in str(col)), None)
            if total_score_col:
                total_scores = pd.to_numeric(df[total_score_col], errors='coerce')
                valid_scores = total_scores.dropna()
                
                analytics.update({
                    'boulder_completion_rates': boulder_completion,
                    'boulder_avg_scores': boulder_avg_scores,
                    'total_athletes': len(df),
                    'average_score': valid_scores.mean() if len(valid_scores) > 0 else 0,
                    'score_std': valid_scores.std() if len(valid_scores) > 0 else 0,
                    'score_range': [valid_scores.min(), valid_scores.max()] if len(valid_scores) > 0 else [0, 0],
                    'performance_distribution': valid_scores.tolist() if len(valid_scores) > 0 else []
                })
            
            # Identify most/least difficult boulders
            if boulder_completion:
                easiest_boulder = max(boulder_completion.items(), key=lambda x: x[1])
                hardest_boulder = min(boulder_completion.items(), key=lambda x: x[1])
                
                analytics['difficulty_analysis'] = {
                    'easiest_boulder': f"{easiest_boulder[0]} ({easiest_boulder[1]:.1f}% completion)",
                    'hardest_boulder': f"{hardest_boulder[0]} ({hardest_boulder[1]:.1f}% completion)",
                    'difficulty_spread': max(boulder_completion.values()) - min(boulder_completion.values())
                }
            
        except Exception as e:
            logger.error(f"Error in boulder performance analysis: {e}")
        
        return analytics
    
    @staticmethod
    def _analyze_lead_performance(df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze lead competition performance"""
        analytics = {}
        
        try:
            if 'Manual Score' not in df.columns:
                return analytics
            
            # Filter active athletes
            active_df = df[
                df['Name'].notna() & 
                (df['Name'] != '') & 
                (~df['Name'].astype(str).str.contains('Hold for', na=False))
            ]
            
            scores = pd.to_numeric(active_df['Manual Score'], errors='coerce')
            valid_scores = scores.dropna()
            
            if len(valid_scores) == 0:
                return analytics
            
            # Performance metrics
            analytics.update({
                'total_athletes': len(active_df),
                'completed_athletes': len(valid_scores),
                'completion_rate': len(valid_scores) / len(active_df) * 100,
                'average_score': valid_scores.mean(),
                'median_score': valid_scores.median(),
                'score_std': valid_scores.std(),
                'score_range': [valid_scores.min(), valid_scores.max()],
                'performance_distribution': valid_scores.tolist()
            })
            
            # Performance categories
            if len(valid_scores) >= 3:
                q25, q75 = valid_scores.quantile([0.25, 0.75])
                analytics['performance_categories'] = {
                    'top_performers': (valid_scores >= q75).sum(),
                    'middle_performers': ((valid_scores >= q25) & (valid_scores < q75)).sum(),
                    'lower_performers': (valid_scores < q25).sum()
                }
            
        except Exception as e:
            logger.error(f"Error in lead performance analysis: {e}")
        
        return analytics

class VisualizationEngine:
    """Create visualizations for competition data"""
    
    @staticmethod
    def create_performance_charts(analytics: Dict[str, Any], competition_name: str) -> List[go.Figure]:
        """Create performance visualization charts"""
        charts = []
        
        try:
            if "Boulder" in competition_name:
                charts.extend(VisualizationEngine._create_boulder_charts(analytics, competition_name))
            elif "Lead" in competition_name:
                charts.extend(VisualizationEngine._create_lead_charts(analytics, competition_name))
                
        except Exception as e:
            logger.error(f"Error creating charts for {competition_name}: {e}")
        
        return charts
    
    @staticmethod
    def _create_boulder_charts(analytics: Dict[str, Any], competition_name: str) -> List[go.Figure]:
        """Create boulder-specific charts"""
        charts = []
        
        try:
            # Boulder completion rates chart
            if 'boulder_completion_rates' in analytics:
                completion_rates = analytics['boulder_completion_rates']
                
                fig = go.Figure(data=[
                    go.Bar(
                        x=list(completion_rates.keys()),
                        y=list(completion_rates.values()),
                        marker_color=['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4'],
                        text=[f'{rate:.1f}%' for rate in completion_rates.values()],
                        textposition='auto'
                    )
                ])
                
                fig.update_layout(
                    title=f'{competition_name} - Boulder Completion Rates',
                    xaxis_title='Boulder',
                    yaxis_title='Completion Rate (%)',
                    template='plotly_white',
                    height=400
                )
                
                charts.append(fig)
            
            # Performance distribution histogram
            if 'performance_distribution' in analytics and analytics['performance_distribution']:
                scores = analytics['performance_distribution']
                
                fig = go.Figure(data=[
                    go.Histogram(
                        x=scores,
                        nbinsx=15,
                        marker_color='#4ecdc4',
                        opacity=0.7
                    )
                ])
                
                fig.update_layout(
                    title=f'{competition_name} - Score Distribution',
                    xaxis_title='Total Score',
                    yaxis_title='Number of Athletes',
                    template='plotly_white',
                    height=400
                )
                
                charts.append(fig)
            
        except Exception as e:
            logger.error(f"Error creating boulder charts: {e}")
        
        return charts
    
    @staticmethod
    def _create_lead_charts(analytics: Dict[str, Any], competition_name: str) -> List[go.Figure]:
        """Create lead-specific charts"""
        charts = []
        
        try:
            # Performance categories pie chart
            if 'performance_categories' in analytics:
                categories = analytics['performance_categories']
                
                fig = go.Figure(data=[
                    go.Pie(
                        labels=['Top Performers', 'Middle Performers', 'Lower Performers'],
                        values=[categories['top_performers'], categories['middle_performers'], categories['lower_performers']],
                        marker_colors=['#28a745', '#ffc107', '#dc3545'],
                        hole=0.4
                    )
                ])
                
                fig.update_layout(
                    title=f'{competition_name} - Performance Categories',
                    template='plotly_white',
                    height=400
                )
                
                charts.append(fig)
            
            # Score distribution
            if 'performance_distribution' in analytics and analytics['performance_distribution']:
                scores = analytics['performance_distribution']
                
                # Box plot
                fig = go.Figure()
                
                fig.add_trace(go.Box(
                    y=scores,
                    name='Scores',
                    marker_color='#45b7d1',
                    boxmean='sd'
                ))
                
                fig.update_layout(
                    title=f'{competition_name} - Score Distribution',
                    yaxis_title='Score',
                    template='plotly_white',
                    height=400
                )
                
                charts.append(fig)
            
        except Exception as e:
            logger.error(f"Error creating lead charts: {e}")
        
        return charts

class InsightGenerator:
    """Generate insights from competition data"""
    
    @staticmethod
    def generate_insights(analytics: Dict[str, Any], competition_name: str) -> List[str]:
        """Generate human-readable insights from analytics"""
        insights = []
        
        try:
            if "Boulder" in competition_name:
                insights.extend(InsightGenerator._generate_boulder_insights(analytics, competition_name))
            elif "Lead" in competition_name:
                insights.extend(InsightGenerator._generate_lead_insights(analytics, competition_name))
            
        except Exception as e:
            logger.error(f"Error generating insights for {competition_name}: {e}")
        
        return insights
    
    @staticmethod
    def _generate_boulder_insights(analytics: Dict[str, Any], competition_name: str) -> List[str]:
        """Generate boulder-specific insights"""
        insights = []
        
        try:
            # Difficulty analysis
            if 'difficulty_analysis' in analytics:
                difficulty = analytics['difficulty_analysis']
                if 'easiest_boulder' in difficulty and 'hardest_boulder' in difficulty:
                    insights.append(f"🎯 **Boulder Difficulty**: {difficulty['easiest_boulder']} was the easiest, while {difficulty['hardest_boulder']} proved most challenging.")
                
                if 'difficulty_spread' in difficulty:
                    spread = difficulty['difficulty_spread']
                    if spread > 40:
                        insights.append(f"⚡ **Route Setting**: Large difficulty spread ({spread:.1f}%) indicates varied problem difficulty.")
                    elif spread < 15:
                        insights.append(f"🎯 **Route Setting**: Consistent difficulty across problems ({spread:.1f}% spread).")
            
            # Performance insights
            if 'average_score' in analytics and 'score_std' in analytics:
                avg_score = analytics['average_score']
                std_score = analytics['score_std']
                
                if std_score > 0:
                    cv = std_score / avg_score * 100  # Coefficient of variation
                    if cv > 30:
                        insights.append(f"📊 **Performance Spread**: High score variation ({cv:.1f}%) suggests competitive field with clear skill gaps.")
                    elif cv < 15:
                        insights.append(f"🏁 **Close Competition**: Low score variation ({cv:.1f}%) indicates very competitive field.")
            
            # Completion rate analysis
            if 'boulder_completion_rates' in analytics:
                rates = list(analytics['boulder_completion_rates'].values())
                if rates:
                    avg_completion = sum(rates) / len(rates)
                    if avg_completion > 70:
                        insights.append(f"✅ **High Success Rate**: Average {avg_completion:.1f}% completion suggests achievable difficulty level.")
                    elif avg_completion < 30:
                        insights.append(f"💪 **Challenging Set**: Average {avg_completion:.1f}% completion indicates very difficult problems.")
            
        except Exception as e:
            logger.error(f"Error generating boulder insights: {e}")
        
        return insights
    
    @staticmethod
    def _generate_lead_insights(analytics: Dict[str, Any], competition_name: str) -> List[str]:
        """Generate lead-specific insights"""
        insights = []
        
        try:
            # Completion rate insights
            if 'completion_rate' in analytics:
                completion_rate = analytics['completion_rate']
                if completion_rate > 80:
                    insights.append(f"🚀 **Competition Progress**: {completion_rate:.1f}% of athletes have completed their climbs - competition nearly finished!")
                elif completion_rate > 50:
                    insights.append(f"⏳ **Competition Progress**: {completion_rate:.1f}% completed - competition is well underway.")
                elif completion_rate > 20:
                    insights.append(f"🏁 **Early Stage**: {completion_rate:.1f}% completed - competition is in early stages.")
            
            # Performance spread analysis
            if 'average_score' in analytics and 'score_std' in analytics and 'score_range' in analytics:
                avg_score = analytics['average_score']
                std_score = analytics['score_std']
                score_range = analytics['score_range']
                
                range_span = score_range[1] - score_range[0]
                if range_span > 30 and std_score > 0:
                    insights.append(f"📈 **Score Distribution**: Wide scoring range ({score_range[0]:.1f}-{score_range[1]:.1f}) shows varied performance levels.")
                
                if std_score > 10:
                    insights.append(f"⚡ **Competitive Spread**: High score variation ({std_score:.1f}) indicates significant performance differences.")
            
            # Performance categories
            if 'performance_categories' in analytics:
                categories = analytics['performance_categories']
                total = sum(categories.values())
                if total > 0:
                    top_pct = categories['top_performers'] / total * 100
                    if top_pct < 20:
                        insights.append(f"🏆 **Elite Performance**: Only {top_pct:.0f}% of athletes in top performance tier - highly competitive field.")
                    elif top_pct > 35:
                        insights.append(f"📊 **Accessible Route**: {top_pct:.0f}% in top tier suggests route is achievable for skilled climbers.")
            
        except Exception as e:
            logger.error(f"Error generating lead insights: {e}")
        
        return insights

# FIXED ATHLETE STATUS DETERMINATION - Key fix for worst finish logic
def determine_athlete_status_enhanced(rank: any, total_score: any, boulder_info: Dict, 
                                    competition_name: str, row_data: pd.Series = None) -> Tuple[str, str]:
    """Enhanced athlete status determination with FIXED worst finish logic"""
    try:
        rank_num = DataProcessor.safe_numeric_conversion(rank)
        completed_boulders = boulder_info.get('completed_boulders', 0)
        
        # If no valid rank, return awaiting result
        if rank_num <= 0:
            return "awaiting-result", "⏳"
        
        # Boulder Semifinals logic - FIXED for worst finish
        if "Boulder" in competition_name and "Semis" in competition_name:
            if completed_boulders < 4:
                # Still competing - yellow for everyone still climbing
                return "podium-contention", "⚠️"
            else:
                # All 4 boulders completed - check position and worst finish
                if rank_num <= 8:
                    # Look for worst finish in row data
                    worst_finish_num = None
                    
                    if row_data is not None:
                        # Try to find worst finish column
                        worst_finish_col = next((
                            col for col in row_data.index 
                            if 'worst' in str(col).lower() and 'finish' in str(col).lower()
                        ), None)
                        
                        if worst_finish_col:
                            worst_finish_value = row_data.get(worst_finish_col)
                            if pd.notna(worst_finish_value) and str(worst_finish_value) not in ['', 'N/A', '-']:
                                try:
                                    worst_finish_num = float(str(worst_finish_value).strip())
                                except (ValueError, TypeError):
                                    worst_finish_num = None
                    
                    # CRITICAL LOGIC: If in top 8 but worst finish > 8, show yellow (could be eliminated)
                    if worst_finish_num is not None and worst_finish_num > 8:
                        return "podium-contention", "⚠️"  # Yellow - at risk of elimination
                    else:
                        return "qualified", "✅"  # Green - safely qualified
                else:
                    return "eliminated", "❌"  # Red - eliminated
        
        # Boulder Finals logic
        elif "Boulder" in competition_name and "Final" in competition_name:
            if completed_boulders < 4:
                if rank_num <= 3 and completed_boulders >= 2:
                    return "podium-position", "🏆"
                else:
                    return "podium-contention", "⚠️"
            else:
                if rank_num <= 3:
                    return "podium-position", "🏆"
                else:
                    return "no-podium", "❌"
        
        # Lead competitions logic
        elif "Lead" in competition_name:
            if "Semis" in competition_name:
                if rank_num <= 8:
                    return "qualified", "✅"
                else:
                    return "eliminated", "❌"
            elif "Final" in competition_name:
                if rank_num <= 3:
                    return "podium-position", "🏆"
                else:
                    return "no-podium", "❌"
        
        # Default fallback
        if rank_num <= 3:
            return "podium-position", "🏆"
        elif rank_num <= 8:
            return "qualified", "✅"
        else:
            return "eliminated", "❌"
            
    except Exception as e:
        logger.warning(f"Error determining status: {e}")
        return "awaiting-result", "⏳"

def determine_lead_athlete_status(status: str, has_score: bool, rank: any = None) -> Tuple[str, str]:
    """Enhanced lead athlete status determination"""
    if not has_score:
        return "awaiting-result", "📄"
    
    # Convert rank for additional context
    rank_num = DataProcessor.safe_numeric_conversion(rank) if rank else 0
    status_lower = str(status).lower()
    
    # Priority-based status determination
    if "podium" in status_lower and "no podium" not in status_lower:
        return "podium-position", "🏆"
    elif "qualified" in status_lower:
        return "qualified", "✅"
    elif "eliminated" in status_lower:
        return "eliminated", "❌"
    elif "no podium" in status_lower:
        return "no-podium", "❌"
    elif "contention" in status_lower:
        return "podium-contention", "⚠️"
    
    # Fallback to rank-based determination
    if rank_num > 0:
        if rank_num <= 3:
            return "podium-position", "🏆"
        elif rank_num <= 8:
            return "qualified", "✅"
        else:
            return "eliminated", "❌"
    
    return "podium-contention", "📊"

def calculate_boulder_completion_enhanced(row: pd.Series) -> Dict[str, any]:
    """Enhanced boulder completion calculation with worst finish handling"""
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
    
    # Enhanced worst finish handling
    worst_finish_display = ""
    worst_finish_value = None
    
    if completed_boulders == 4:
        worst_finish_col = next((
            col for col in row.index 
            if 'worst' in str(col).lower() and 'finish' in str(col).lower()
        ), None)
        
        if worst_finish_col:
            worst_finish_raw = row.get(worst_finish_col, 'N/A')
            if worst_finish_raw not in ['N/A', '', None] and not pd.isna(worst_finish_raw):
                worst_finish_clean = DataProcessor.clean_text(str(worst_finish_raw))
                if worst_finish_clean and worst_finish_clean != '-':
                    worst_finish_display = f" | Worst Finish: {worst_finish_clean}"
                    # Store numeric value for logic
                    try:
                        worst_finish_value = float(worst_finish_clean)
                    except (ValueError, TypeError):
                        worst_finish_value = None
    
    return {
        'boulder_scores': boulder_scores,
        'completed_boulders': completed_boulders,
        'boulder_display': boulder_display,
        'worst_finish_display': worst_finish_display,
        'worst_finish_numeric': worst_finish_value  # NEW: numeric value for logic
    }

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

def create_athlete_card_enhanced(position_emoji: str, athlete: str, total_score: any, 
                               boulder_info: Dict, strategy_display: str, card_class: str):
    """Create and display an enhanced athlete card"""
    completed_boulders = boulder_info['completed_boulders']
    boulder_display = boulder_info['boulder_display']
    worst_finish_display = boulder_info['worst_finish_display']
    
    # Ensure card_class is never empty
    if not card_class or card_class.strip() == "":
        card_class = "awaiting-result"
    
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
