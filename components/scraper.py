import logging
from typing import Dict, List, Optional
import pandas as pd
import requests
import streamlit as st
from time import sleep, time
from datetime import datetime, timedelta
from collections import deque
import os
from ratelimiting import RateLimiter

def scrapetheweb(
    query_template: str,
    column_name: str,
    filtered_df: pd.DataFrame,
    export_format: str = 'excel',
    db_name: str = 'search_results.db',
    export_path: str = 'export_results'
) -> Dict[str, List[str]]:
    """
    Returns:
        Dict containing lists of scraped results and export file paths
    """
    
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('scraping.log'),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
    
    # Validate inputs
    if column_name not in filtered_df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame")
    if '{value}' not in query_template:
        raise ValueError("Query template must contain {value} placeholder")
    
    # Initialize rate limiter
    rate_limiter = RateLimiter(max_per_second=1, max_per_day=15)
    
    # SERP API setup
    SERP_API_KEY = os.getenv('SERP_API_KEY')
    if not SERP_API_KEY:
        raise ValueError("SERP_API_KEY not found in environment variables")
    
    SERP_API_URL = "https://api.serpapi.com/search"
    
    def handle_api_errors(err: Exception, value: str):
        """Handles API errors by logging and displaying a message in Streamlit."""
        logger.error(f"Error searching for '{value}': {str(err)}")
        st.error(f"An error occurred while searching for '{value}': {str(err)}")

    def search_serp(value: str) -> Optional[Dict]:
        rate_limiter.wait_if_needed()
        
        # Replace placeholder in query template
        search_query = query_template.format(value=value)
        
        params = {
            "api_key": SERP_API_KEY,
            "engine": "google",
            "q": search_query,
            "num": 10,
            "gl": "us"
        }
        
        try:
            response = requests.get(SERP_API_URL, params=params)
            response.raise_for_status()  # Raises HTTPError for bad responses
            return response.json()
        
        except requests.RequestException as e:
            handle_api_errors(e, value)
            return None


            