# We'll use the popular VADER library for sentiment analysis
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class SentimentAnalyzerTool:
    """
    A tool to analyze the sentiment of a given text.
    """
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
        print("[SentimentAnalyzerTool] Initialized.")

    def run(self, text: str):
        """
        Analyzes the sentiment of the text.

        Args:
            text (str): The text to analyze.

        Returns:
            dict: A dictionary containing the sentiment scores (pos, neu, neg, compound).
                  The 'compound' score is the most useful metric (-1 to 1).
        """
        if not text:
            return {"pos": 0.0, "neu": 1.0, "neg": 0.0, "compound": 0.0}
            
        sentiment_dict = self.analyzer.polarity_scores(text)
        return sentiment_dict