from openai import OpenAI
import re

client = OpenAI()

def analyse_message_with_LLM(message):

  assert isinstance(message, str), "Message must be a string."

  response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
      {"role": "system", "content": """Analyze the following message and provide the following metrics:
      1. Sentiment (as 'Very Negative', 'Negative', 'Neutral', 'Positive', 'Very Positive')
      2. Mood (as 'Very Bad', 'Bad', 'Neutral', 'Good', 'Very Good')
      3. Key Topics (list the key topics mentioned)
      4. Well-being (rate from 1 to 10)
      5. Energy (rate from 1 to 10)
      6. Productivity (rate from 1 to 10)"""},
      {"role": "user", "content": message}
    ],
    temperature=0.5,
    max_tokens=150
  )
  return parse_llm_response(response.choices[0].message.content)


def parse_llm_response(response_text):
    """
    Parses the LLM response and converts it into a structured dictionary.

    :param response_text: The raw text response from the LLM.
    :return: A dictionary with parsed metrics.
    """

    metrics = {}

    # Extract sentiment
    sentiment_match = re.search(r'Sentiment:\s*(Very Negative|Negative|Neutral|Positive|Very Positive)', response_text)
    if sentiment_match:
        sentiment_text = sentiment_match.group(1)
        metrics['sentiment'] = convert_sentiment(sentiment_text)

    # Extract mood
    mood_match = re.search(r'Mood:\s*(Very Bad|Bad|Neutral|Good|Very Good)', response_text)
    if mood_match:
        mood_text = mood_match.group(1)
        metrics['mood'] = convert_mood(mood_text)

    # Extract key topics
    topics_match = re.search(r'Key Topics:\s*(.*)', response_text)
    if topics_match:
        metrics['key_topics'] = [topic.strip() for topic in topics_match.group(1).split(',')]

    # Extract well-being, energy, productivity
    well_being_match = re.search(r'Well-being:\s*(\d+)', response_text)
    energy_match = re.search(r'Energy:\s*(\d+)', response_text)
    productivity_match = re.search(r'Productivity:\s*(\d+)', response_text)

    if well_being_match:
        metrics['well_being'] = int(well_being_match.group(1))
    if energy_match:
        metrics['energy'] = int(energy_match.group(1))
    if productivity_match:
        metrics['productivity'] = int(productivity_match.group(1))

    assert 'sentiment' in metrics, "Sentiment must be provided."
    assert 'mood' in metrics, "Mood must be provided."
    assert 'key_topics' in metrics, "Key topics must be provided."
    assert 'well_being' in metrics, "Well-being must be provided."
    assert 'energy' in metrics, "Energy must be provided."
    assert 'productivity' in metrics, "Productivity must be provided."

    assert isinstance(metrics['sentiment'], float), "Sentiment must be a float."
    assert isinstance(metrics['mood'], float), "Mood must be a float."
    assert isinstance(metrics['key_topics'], list), "Key topics must be a list."
    assert isinstance(metrics['well_being'], int), "Well-being must be an integer."
    assert isinstance(metrics['energy'], int), "Energy must be an integer."
    assert isinstance(metrics['productivity'], int), "Productivity must be an integer."

    return metrics

def convert_sentiment(sentiment_text):
    mapping = {
        "Very Negative": -1.0,
        "Negative": -0.5,
        "Neutral": 0.0,
        "Positive": 0.5,
        "Very Positive": 1.0,
    }
    return mapping.get(sentiment_text, 0.0)

def convert_mood(mood_text):
    mapping = {
        "Very Bad": 0.0,
        "Bad": 0.25,
        "Neutral": 0.5,
        "Good": 0.75,
        "Very Good": 1.0,
    }
    return mapping.get(mood_text, 0.5)

print(analyse_message_with_LLM("I had a great day at work today. I'm feeling a bit tired but happy that I completed my project."))

