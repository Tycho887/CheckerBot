import numpy as np
import pandas as pd

def normalize_score(score, min_val, max_val):
    return (score - min_val) / (max_val - min_val)


def convert_sentiment(sentiment):
    """
    Convert the sentiment string to a numerical value.
    
    :param sentiment: A string representing the sentiment.
    :return: A numerical value representing the sentiment.
    """
    sentiment_mapping = {
        "Very Negative": -1.0,
        "Negative": -0.5,
        "Neutral": 0,
        "Positive": 0.5,
        "Very Positive": 1.0
    }
    if isinstance(sentiment, str):
        return sentiment_mapping.get(sentiment, 0.5)
    elif isinstance(sentiment, pd.Series):
        return sentiment.apply(lambda x: sentiment_mapping.get(x, 0.5))
    else:
        return 0.5

def convert_mood(mood):
    """
    Convert the mood string to a numerical value.
    
    :param mood: A string representing the mood.
    :return: A numerical value representing the mood.
    """
    mood_mapping = {
        "Very Bad": 0.0,
        "Bad": 0.25,
        "Neutral": 0.5,
        "Good": 0.75,
        "Very Good": 1.0
    }
    if isinstance(mood, str):
        return mood_mapping.get(mood, 0.5)
    elif isinstance(mood, pd.Series):
        return mood.apply(lambda x: mood_mapping.get(x, 0.5))
    else:
        return 0.5

def calculate_composite_score(metrics, weights=None):
    """
    Calculate a composite score based on the given metrics.
    
    :param metrics: A dictionary containing the metrics.
    :param weights: A dictionary containing the weights for each metric.
    :return: A composite score.
    """
    assert len(metrics) == 6, "Metrics should contain 5 values: sentiment, mood, well-being, energy, and productivity."

    
    # Default weights if none provided
    if weights is None:
        weights = {
            "sentiment": 1.0,
            "mood": 1.0,
            "well_being": 1.0,
            "energy": 1.0,
            "productivity": 1.0
        }
    
    # Normalize well-being, energy, and productivity (0-1 scale)
    metrics['well_being'] = normalize_score(metrics['well_being'], 1, 10)
    metrics['energy'] = normalize_score(metrics['energy'], 1, 10)
    metrics['productivity'] = normalize_score(metrics['productivity'], 1, 10)
    metrics['mood'] = convert_mood(metrics['mood'])
    metrics['sentiment'] = convert_sentiment(metrics['sentiment'])

    # Calculate the composite score
    composite_score = (
        metrics['sentiment'] * weights['sentiment'] +
        metrics['mood'] * weights['mood'] +
        metrics['well_being'] * weights['well_being'] +
        metrics['energy'] * weights['energy'] +
        metrics['productivity'] * weights['productivity']
    )
    
    # Normalize the composite score to be between 0 and 1
    max_possible_score = sum(weights.values())
    composite_score_normalized = composite_score / max_possible_score
    
    return composite_score_normalized