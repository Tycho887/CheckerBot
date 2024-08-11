import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from lib.database import get_fields, get_last_n_records_for_user, get_user_name
from lib.utility.functions import convert_sentiment, convert_mood
import logging

sns.set_style('whitegrid')

def plot_metric_over_time(user_id, metric, days=30):
    """
    Plots selected metrics over time for a given user.

    :param user_id: int
    :param metric: str
    :param days: int
    :return: str, path to the saved plot image
    """
    assert isinstance(user_id, int), "User ID should be an integer."
    assert isinstance(metric, str), "Metric should be a string."

    user_name = get_user_name(user_id)

    # Fetch records and convert to DataFrame
    metrics_list = ['sentiment', 'mood', 'well_being', 'energy', 'productivity', 'score']
    
    df = pd.DataFrame(get_last_n_records_for_user(user_id, limit=days), columns=["id"] + get_fields('records'))
    
    if df.empty:
        logging.error(f"No data available for user {user_id} and metric {metric}")
        return None

    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'])

    if metric == 'all':
        fig, axs = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle(f'Metrics Over Time for {user_name}', fontsize=16)

        # Plot Mood
        sns.lineplot(x=df['date'], y=convert_mood(df['mood']), ax=axs[0, 0], marker='o', label='Mood')
        axs[0, 0].set_title('Mood')
        axs[0, 0].set_ylabel('Mood Score')
        axs[0, 0].set_yticks([0.0, 0.25, 0.5, 0.75, 1.0])
        axs[0, 0].set_yticklabels(["Very Bad", "Bad", "Neutral", "Good", "Very Good"])

        # Plot Sentiment
        sns.lineplot(x=df['date'], y=convert_sentiment(df['sentiment']), ax=axs[0, 1], marker='o', label='Sentiment')
        axs[0, 1].set_title('Sentiment')
        axs[0, 1].set_ylabel('Sentiment Score')
        axs[0, 1].set_yticks([-1.0, -0.5, 0, 0.5, 1.0])
        axs[0, 1].set_yticklabels(["Very Negative", "Negative", "Neutral", "Positive", "Very Positive"])

        # Plot Well-being, Energy, and Productivity
        axs[1, 0].plot(df['date'], df['well_being'], marker='o', label='Well-being')
        axs[1, 0].plot(df['date'], df['energy'], marker='o', label='Energy')
        axs[1, 0].plot(df['date'], df['productivity'], marker='o', label='Productivity')
        axs[1, 0].set_title('Well-being, Energy, and Productivity')
        axs[1, 0].set_ylabel('Score')
        axs[1, 0].legend()

        # Plot Weighted sum score
        sns.lineplot(x=df['date'], y=df['score'], ax=axs[1, 1], marker='o', label='Weighted Sum Score')
        axs[1, 1].set_title('Weighted Sum Score')
        axs[1, 1].set_ylabel('Weighted Sum Score')

        for ax in axs.flat:
            ax.set_xlabel('Time')
            ax.tick_params(axis='x', rotation=45)
            ax.grid(True)

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])

        # Save the plot
        image_name = f'plots/all_metrics_over_time.png'
        plt.savefig(image_name)
        plt.close()

        return image_name

    else:
        plt.figure(figsize=(12, 6))

        # Handle different metrics
        if metric == 'sentiment':
            sns.lineplot(x=df['date'], y=convert_sentiment(df[metric]), marker='o', label=metric.capitalize())
            plt.yticks([-1.0, -0.5, 0, 0.5, 1.0], ["Very Negative", "Negative", "Neutral", "Positive", "Very Positive"])
            y_label = f'{metric.capitalize()} Score'
            title = f'{metric.capitalize()} Over Time for {user_name}'

        elif metric == 'mood':
            sns.lineplot(x=df['date'], y=convert_mood(df[metric]), marker='o', label=metric.capitalize())
            plt.yticks([0.0, 0.25, 0.5, 0.75, 1.0], ["Very Bad", "Bad", "Neutral", "Good", "Very Good"])
            y_label = f'{metric.capitalize()} Score'
            title = f'{metric.capitalize()} Over Time for {user_name}'

        elif metric in ['well_being', 'energy', 'productivity']:
            sns.lineplot(x=df['date'], y=df[metric], marker='o', label=metric.replace("_", " ").capitalize())
            plt.ylim((0,10))
            y_label = f'{metric.replace("_", " ").capitalize()} Score'
            title = f'{metric.replace("_", " ").capitalize()} Over Time for {user_name}'

        elif metric == 'score':
            sns.lineplot(x=df['date'], y=df['score'], marker='o', label='Weighted sum score')
            plt.ylim((0,100))
            y_label = 'Weighted sum Score'
            title = f"Weighted sum score over time for {user_name}"
        else:
            logging.error(f"Invalid metric passed to visualizer: {metric}")
            return None

        # Final touches on the plot
        plt.ylabel(y_label)
        plt.title(title)
        plt.xticks(rotation=45)
        plt.xlabel('Time')
        plt.grid(True)
        plt.legend()

        # Save the plot
        image_name = f'plots/{metric}_over_time.png'
        plt.savefig(image_name)
        plt.close()

        return image_name
