import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from lib.database import get_fields

columns = get_fields('records')

sns.set_style('whitegrid')

def plot_metric_over_time(db_data, metric, user_name):
    """
    Plots a selected metric over time.

    :param db_data: list of tuples
    :param metric: str
    :param user_name: str
    """
    # convert the data to a pandas dataframe

    df = pd.DataFrame(db_data, columns=["id"] + columns)
    
    plt.figure(figsize=(12, 6))

    # We only want to display the date, not the time on the axis
    # We convert the date to a datetime object

    times = pd.to_datetime(df['date'])
    
    if metric in ['sentiment', 'mood']:
        sns.lineplot(x=times, y=df[metric], marker='o',label=metric.capitalize())
        plt.ylabel(f'{metric.capitalize()} score')
        plt.title(f'{metric.capitalize()} over time for {user_name}')

    elif metric in ['well_being', 'energy', 'productivity']:
        # we want to plot all at the same time
        sns.lineplot(x=times, y=df['well_being'], marker='o', label='Well-being')
        sns.lineplot(x=times, y=df['energy'], marker='o', label='Energy')
        sns.lineplot(x=times, y=df['productivity'], marker='o', label='Productivity')
        plt.ylabel('Score')
        plt.title(f'Well-being, Energy, and Productivity over time for {user_name}')

    plt.xticks(rotation=45)
    plt.xlabel('Time')
    plt.grid(True)

    image_name = f'plots/{metric}_over_time.png'

    plt.savefig(image_name)

    return image_name