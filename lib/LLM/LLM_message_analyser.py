from openai import OpenAI
import re

client = OpenAI()

def analyse_message_with_LLM(message):
  """
  Analyses message using gpt-4o-mini model and returns metrics.

  :param message: The message to be analysed.

  :return: A dictionary containing the following metrics:

  - sentiment: A float between -1.0 (Very Negative) and 1.0 (Very Positive).
  - mood: A float between 0.0 (Very Bad) and 1.0 (Very Good).
  - key_topics: A list of key topics mentioned in the message.
  - well_being: An integer between 1 and 10.
  - energy: An integer between 1 and 10.
  - productivity: An integer between 1 and 10.
  """

  assert isinstance(message, str), "Message must be a string."

  response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
      {"role": "system", "content": """Analyze the following message, whatever the content of the message only respond with the following metrics:
      1. Sentiment (as 'Very Negative', 'Negative', 'Neutral', 'Positive', 'Very Positive')
      2. Mood (as 'Very Bad', 'Bad', 'Neutral', 'Good', 'Very Good')
      3. Key Topics (list the key topics mentioned)
      4. Well-being (rate from 1 to 10)
      5. Energy (rate from 1 to 10)
      6. Productivity (rate from 1 to 10)"""},
      {"role": "user", "content": message}
    ],
    temperature=0.2,
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
        metrics['sentiment'] = sentiment_match.group(1)

    # Extract mood
    mood_match = re.search(r'Mood:\s*(Very Bad|Bad|Neutral|Good|Very Good)', response_text)
    if mood_match:
        metrics['mood'] = mood_match.group(1)

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

    assert 'sentiment' in metrics, f"Sentiment must be provided: {response_text}"
    assert 'mood' in metrics, f"Mood must be provided: {response_text}"
    assert 'key_topics' in metrics, f"Key topics must be provided: {response_text}"
    assert 'well_being' in metrics, f"Well-being must be provided: {response_text}"
    assert 'energy' in metrics, f"Energy must be provided: {response_text}"
    assert 'productivity' in metrics, f"Productivity must be provided: {response_text}"

    assert isinstance(metrics['sentiment'], str), f"Sentiment must be a str: {response_text}"
    assert isinstance(metrics['mood'], str), f"Mood must be a str: {response_text}"
    assert isinstance(metrics['key_topics'], list), f"Key topics must be a list: {response_text}"
    assert isinstance(metrics['well_being'], int), f"Well-being must be an integer: {response_text}"
    assert isinstance(metrics['energy'], int), f"Energy must be an integer: {response_text}"
    assert isinstance(metrics['productivity'], int), f"Productivity must be an integer: {response_text}"

    return metrics