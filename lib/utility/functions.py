import numpy as np
import sqlite3


def normalize_score(score, min_val, max_val):
    return (score - min_val) / (max_val - min_val)

def calculate_composite_score(metrics, weights=None):
    """
    Calculate a composite score based on the given metrics.
    
    :param metrics: A dictionary containing the metrics.
    :param weights: A dictionary containing the weights for each metric.
    :return: A composite score.
    """
    
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