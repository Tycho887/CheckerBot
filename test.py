import lib.database as db
from lib.plotting import plot_metric_over_time

message = "I had a great day at work today. I'm feeling a bit tired but happy that I completed my project."

# Analyse the message

metrics = {'sentiment': 0.5, 
           'mood': 0.75, 
           'key_topics': ['Work', 'tiredness', 'happiness', 'project completion'], 
           'well_being': 8, 
           'energy': 6, 
           'productivity': 9}

#analyse_message_with_LLM(message)

# Connect to the database

db.add_user(123456, "John")

# Add the record to the database

db.add_data_to_records(123456, metrics, message)

# Plot the score vs. date

print(db.get_records_for_user(123456))

plot_metric_over_time(db.get_records_for_user(123456), 'energy', "John")