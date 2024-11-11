from typing import Dict
import pandas as pd
import requests
import streamlit as st
from time import sleep, time
from datetime import datetime, timedelta
from collections import deque
import os
from ratelimiting import RateLimiter

def scrapetheweb(query: str, column: str, filtered_df: pd.DataFrame, export_format: str = 'excel') -> None:
    """
    Enhanced scraping function with built-in rate limiting
    """
    # Initialize rate limiter
    rate_limiter = RateLimiter(max_per_second=1, max_per_day=100)
    
    # SERP API Configuration
    SERP_API_KEY = os.getenv('SERP_API_KEY')
    SERP_API_URL = "https://api.serpapi.com/search"
    
    def search_serp(company_name: str) -> Dict:
        # Wait if needed based on rate limits
        rate_limiter.wait_if_needed()
        
        search_query = query.format(company=company_name)
        params = {
            "api_key": SERP_API_KEY,
            "engine": "google",
            "q": search_query,
            "num": 10,
            "gl": "us"
        }
        
        try:
            response = requests.get(SERP_API_URL, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error searching for {company_name}: {str(e)}")
            return None
