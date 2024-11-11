from time import sleep, time
from datetime import datetime, timedelta
from collections import deque

class RateLimiter:
    """
    Custom rate limiter using deque for tracking requests
    """
    def __init__(self, max_per_second=1, max_per_day=100):
        self.max_per_second = max_per_second
        self.max_per_day = max_per_day
        self.seconds_tracker = deque(maxlen=max_per_second)
        self.daily_tracker = deque(maxlen=max_per_day)
    
    def wait_if_needed(self):
        """
        Check limits and wait if necessary
        """
        now = time()
        current_datetime = datetime.now()
        
        # Clean old entries from daily tracker
        while self.daily_tracker and \
              (current_datetime - self.daily_tracker[0]).total_seconds() > 86400:  # 24 hours
            self.daily_tracker.popleft()
        
        # Clean old entries from seconds tracker
        while self.seconds_tracker and now - self.seconds_tracker[0] > 1:
            self.seconds_tracker.popleft()
        
        # Check daily limit
        if len(self.daily_tracker) >= self.max_per_day:
            oldest = self.daily_tracker[0]
            sleep_time = 86400 - (current_datetime - oldest).total_seconds()
            if sleep_time > 0:
                sleep(sleep_time)
        
        # Check per-second limit
        if len(self.seconds_tracker) >= self.max_per_second:
            sleep_time = 1 - (now - self.seconds_tracker[0])
            if sleep_time > 0:
                sleep(sleep_time)
        
        # Log the request
        self.seconds_tracker.append(now)
        self.daily_tracker.append(current_datetime)

'''class RateLimiter:
    def __init__(self, max_per_second=1, max_per_day=100):
        self.max_per_second = max_per_second
        self.max_per_day = max_per_day
        self.seconds_tracker = deque(maxlen=max_per_second)
        self.daily_tracker = deque(maxlen=max_per_day)
    
    def wait_if_needed(self):
        now = time()
        current_datetime = datetime.now()
        
        # Clean old entries
        while self.daily_tracker and \
              (current_datetime - self.daily_tracker[0]).total_seconds() > 86400:
            self.daily_tracker.popleft()
        
        while self.seconds_tracker and now - self.seconds_tracker[0] > 1:
            self.seconds_tracker.popleft()
        
        # Check limits and wait if needed
        if len(self.daily_tracker) >= self.max_per_day:
            oldest = self.daily_tracker[0]
            sleep_time = 86400 - (current_datetime - oldest).total_seconds()
            if sleep_time > 0:
                sleep(sleep_time)
        
        if len(self.seconds_tracker) >= self.max_per_second:
            sleep_time = 1 - (now - self.seconds_tracker[0])
            if sleep_time > 0:
                sleep(sleep_time)
        
        # Log the request
        self.seconds_tracker.append(now)
        self.daily_tracker.append(current_datetime)
'''