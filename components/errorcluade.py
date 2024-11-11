
'''import streamlit as st
from typing import Optional, Union, Dict, Any
import pandas as pd
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
import requests
import time
from enum import Enum

class ErrorSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"

class AppError:
    def __init__(self, message: str, severity: ErrorSeverity, suggestions: list[str] = None):
        self.message = message
        self.severity = severity
        self.suggestions = suggestions or []
        self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

class ErrorHandler:
    def __init__(self):
        if 'errors' not in st.session_state:
            st.session_state.errors = []
    
    def add_error(self, error: AppError):
        """Add an error to the session state and display it"""
        st.session_state.errors.append(error)
        self._display_error(error)
    
    def _display_error(self, error: AppError):
        """Display an error using appropriate Streamlit components"""
        if error.severity == ErrorSeverity.ERROR:
            with st.error(error.message):
                if error.suggestions:
                    st.write("Suggestions to resolve:")
                    for suggestion in error.suggestions:
                        st.markdown(f"- {suggestion}")
        elif error.severity == ErrorSeverity.WARNING:
            with st.warning(error.message):
                if error.suggestions:
                    st.write("Suggestions:")
                    for suggestion in error.suggestions:
                        st.markdown(f"- {suggestion}")
        else:
            with st.info(error.message):
                if error.suggestions:
                    for suggestion in error.suggestions:
                        st.markdown(f"- {suggestion}")
    
    def clear_errors(self):
        """Clear all errors from the session state"""
        st.session_state.errors = []
    
    def handle_file_upload_error(self, e: Exception) -> None:
        """Handle errors related to file uploads"""
        if isinstance(e, pd.errors.EmptyDataError):
            self.add_error(AppError(
                "The uploaded file is empty.",
                ErrorSeverity.ERROR,
                ["Please upload a file containing data",
                 "Check if the file was corrupted during upload"]
            ))
        elif isinstance(e, pd.errors.ParserError):
            self.add_error(AppError(
                "Unable to parse the uploaded file.",
                ErrorSeverity.ERROR,
                ["Ensure the file is a valid CSV",
                 "Check for special characters in the column headers",
                 "Verify the file encoding (UTF-8 recommended)"]
            ))
        else:
            self.add_error(AppError(
                f"An error occurred while uploading the file: {str(e)}",
                ErrorSeverity.ERROR,
                ["Try uploading the file again",
                 "Ensure the file isn't corrupted"]
            ))

    def handle_google_sheets_error(self, e: Exception) -> None:
        """Handle Google Sheets API related errors"""
        if isinstance(e, HttpError):
            if e.resp.status == 403:
                self.add_error(AppError(
                    "Access denied to Google Sheet.",
                    ErrorSeverity.ERROR,
                    ["Verify that you have sharing permissions for this sheet",
                     "Check if your Google Sheets API credentials are valid",
                     "Ensure the sheet is not restricted"]
                ))
            elif e.resp.status == 404:
                self.add_error(AppError(
                    "Google Sheet not found.",
                    ErrorSeverity.ERROR,
                    ["Verify the Sheet ID is correct",
                     "Make sure the sheet hasn't been deleted"]
                ))
        else:
            self.add_error(AppError(
                f"An error occurred with Google Sheets: {str(e)}",
                ErrorSeverity.ERROR,
                ["Check your internet connection",
                 "Verify your Google Sheets API credentials"]
            ))

    def handle_api_error(self, e: Exception, api_name: str) -> None:
        """Handle errors from external APIs (Search API, LLM API)"""
        if isinstance(e, requests.exceptions.RequestException):
            if isinstance(e, requests.exceptions.ConnectionError):
                self.add_error(AppError(
                    f"Unable to connect to {api_name}.",
                    ErrorSeverity.ERROR,
                    ["Check your internet connection",
                     "Verify the API endpoint is correct",
                     "Check if the service is down"]
                ))
            elif isinstance(e, requests.exceptions.Timeout):
                self.add_error(AppError(
                    f"{api_name} request timed out.",
                    ErrorSeverity.WARNING,
                    ["Try again with a smaller batch of data",
                     "Check your internet connection speed"]
                ))
            elif isinstance(e, requests.exceptions.TooManyRedirects):
                self.add_error(AppError(
                    f"Too many redirects while accessing {api_name}.",
                    ErrorSeverity.ERROR,
                    ["Check if the API endpoint is correct",
                     "Verify your API credentials"]
                ))
        else:
            self.add_error(AppError(
                f"An error occurred while accessing {api_name}: {str(e)}",
                ErrorSeverity.ERROR,
                ["Check your API key",
                 "Verify you haven't exceeded API rate limits"]
            ))

    def handle_data_processing_error(self, e: Exception, context: str) -> None:
        """Handle errors during data processing"""
        self.add_error(AppError(
            f"Error processing data during {context}: {str(e)}",
            ErrorSeverity.ERROR,
            ["Try with a smaller dataset",
             "Check if your data contains the required columns",
             "Verify the data format matches the expected format"]
        ))

    def show_rate_limit_warning(self, api_name: str, remaining_quota: int):
        """Display warning when approaching API rate limits"""
        if remaining_quota < 100:
            self.add_error(AppError(
                f"Running low on {api_name} API quota (remaining: {remaining_quota})",
                ErrorSeverity.WARNING,
                ["Consider upgrading your API plan",
                 "Process remaining data in smaller batches",
                 "Wait for quota reset"]
            ))

def create_error_handler():
    """Factory function to create or retrieve the error handler"""
    if 'error_handler' not in st.session_state:
        st.session_state.error_handler = ErrorHandler()
    return st.session_state.error_handler

# Usage example wrapper function
def safe_operation(operation_func):
    """Decorator for safely executing operations with error handling"""
    def wrapper(*args, **kwargs):
        error_handler = create_error_handler()
        try:
            return operation_func(*args, **kwargs)
        except Exception as e:
            error_handler.handle_api_error(e, operation_func.__name__)
            return None
    return wrapper

    '''