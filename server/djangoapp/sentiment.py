"""Small, reusable sentiment-analysis helper."""

from textblob import TextBlob


def analyze_sentiment(text):
    """Return a label plus TextBlob polarity/subjectivity scores."""
    blob = TextBlob(text or "")
    polarity = round(float(blob.sentiment.polarity), 4)
    subjectivity = round(float(blob.sentiment.subjectivity), 4)

    if polarity > 0.1:
        label = "positive"
    elif polarity < -0.1:
        label = "negative"
    else:
        label = "neutral"

    return {
        "sentiment": label,
        "polarity_score": polarity,
        "subjectivity_score": subjectivity,
    }
