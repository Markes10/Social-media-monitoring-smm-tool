import random
from datetime import datetime, timedelta

# Simulated audience activity data
activity_hours = {
    "Monday": [9, 12, 18, 21],
    "Tuesday": [10, 13, 19, 20],
    "Wednesday": [11, 14, 20, 22],
    "Thursday": [9, 12, 18, 21],
    "Friday": [10, 13, 19, 22],
    "Saturday": [12, 15, 20, 23],
    "Sunday": [14, 16, 21, 22]
}

def suggest_post_time():
    """Suggests the best time to post based on audience activity."""
    
    day = datetime.today().strftime("%A")  # Get current day
    best_hours = activity_hours.get(day, [12, 18])  # Default to 12 PM and 6 PM if no data
    
    recommended_hour = random.choice(best_hours)  # Pick a random peak hour
    recommended_time = datetime.today().replace(hour=recommended_hour, minute=0, second=0)
    
    return {
        "best_time": recommended_time.strftime("%Y-%m-%d %H:%M:%S"),
        "recommendation": f"Schedule your post at {recommended_time.strftime('%I:%M %p')} for maximum engagement."
    }

# Example usage:
# print(suggest_post_time())
