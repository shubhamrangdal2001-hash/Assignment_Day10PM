# analyze_text.py
# Part D - AI-Augmented Task: Text Analyzer Module
#
# Prompt used:
# "Write a Python module with a function called analyze_text(text: str, **options)
# that accepts any text and keyword arguments for options (count_words=True,
# count_sentences=True, find_longest_word=True, sentiment_simple=True).
# Each option enables a different analysis. Use *args and **kwargs, add type hints
# and Google-style docstrings. Return a dict with all requested analyses."


# ==============================================================
# SECTION 1: AI's Output (as received, lightly formatted)
# ==============================================================

def analyze_text_ai_version(text: str, **options) -> dict:
    """Analyze the given text based on the options provided.

    Args:
        text: Input text to analyze.
        **options: Keyword arguments to enable specific analyses:
            count_words (bool): Count total words. Default True.
            count_sentences (bool): Count sentences. Default True.
            find_longest_word (bool): Find longest word. Default True.
            sentiment_simple (bool): Simple positive/negative sentiment. Default True.

    Returns:
        A dict containing results of each enabled analysis.
    """
    results = {}

    if not text:
        return results

    if options.get('count_words', True):
        results['word_count'] = len(text.split())

    if options.get('count_sentences', True):
        import re
        results['sentence_count'] = len(re.split(r'[.!?]+', text.strip()))

    if options.get('find_longest_word', True):
        words = text.split()
        results['longest_word'] = max(words, key=len) if words else ''

    if options.get('sentiment_simple', True):
        positive_words = ['good', 'great', 'excellent', 'happy', 'love', 'wonderful']
        negative_words = ['bad', 'terrible', 'horrible', 'sad', 'hate', 'awful']
        lower = text.lower()
        pos = sum(1 for w in positive_words if w in lower)
        neg = sum(1 for w in negative_words if w in lower)
        if pos > neg:
            results['sentiment'] = 'positive'
        elif neg > pos:
            results['sentiment'] = 'negative'
        else:
            results['sentiment'] = 'neutral'

    return results


# ==============================================================
# AI Output Evaluation Notes (written by student)
# ==============================================================
#
# Q: Does it properly use **kwargs?
#    Yes, options.get() is used correctly for each feature flag.
#
# Q: Are type hints correct?
#    Mostly yes. Return type hint dict is fine, though dict[str, Any] would be
#    more precise. No type hint for individual option values (bool assumed).
#
# Q: Does it handle edge cases (empty text, no options)?
#    Partially. Empty text returns {} early. But "no options" still runs all
#    analyses because defaults are True — could surprise users who pass nothing.
#
# Q: Is the docstring useful?
#    It lists parameters but doesn't describe what each key in the result dict
#    looks like. Could be more specific about return structure.
#
# Q: Single Responsibility?
#    No — one function is doing 4 different jobs. It's a monolithic function.
#    Better to split each analysis into its own small function.
#
# Improvements made in the version below:
# - Split each analysis into a dedicated helper function
# - Improved edge case handling (punctuation stripped from words)
# - Empty text returns a dict with a clear message, not just {}
# - Docstrings describe return value structure more clearly


# ==============================================================
# SECTION 2: Improved Version
# ==============================================================

import re
from typing import Any


def _count_words(text: str) -> int:
    """Count words in text, ignoring extra whitespace.

    Args:
        text: Input string.

    Returns:
        Number of words as an integer.
    """
    words = text.split()
    return len(words)


def _count_sentences(text: str) -> int:
    """Count sentences split by '.', '!', or '?'.

    Args:
        text: Input string.

    Returns:
        Number of sentences as an integer.
    """
    parts = re.split(r'[.!?]+', text.strip())
    # Remove empty strings from trailing punctuation
    sentences = [p for p in parts if p.strip()]
    return len(sentences)


def _find_longest_word(text: str) -> str:
    """Find the longest word in the text (ignores punctuation).

    Args:
        text: Input string.

    Returns:
        The longest word as a string, or '' if no words found.
    """
    # Strip punctuation from each word before comparing
    words = re.findall(r"[a-zA-Z']+", text)
    if not words:
        return ''
    return max(words, key=len)


def _simple_sentiment(text: str) -> str:
    """Determine simple sentiment: positive, negative, or neutral.

    Args:
        text: Input string.

    Returns:
        One of 'positive', 'negative', or 'neutral'.
    """
    positive_words = {'good', 'great', 'excellent', 'happy', 'love', 'wonderful', 'amazing'}
    negative_words = {'bad', 'terrible', 'horrible', 'sad', 'hate', 'awful', 'dreadful'}

    lower_words = set(re.findall(r'\b\w+\b', text.lower()))
    pos_count = len(lower_words & positive_words)
    neg_count = len(lower_words & negative_words)

    if pos_count > neg_count:
        return 'positive'
    elif neg_count > pos_count:
        return 'negative'
    return 'neutral'


def analyze_text(text: str, **options) -> dict[str, Any]:
    """Analyze text with modular options for different analyses.

    Each option flag controls which analysis is included in the result.
    All options default to True so calling without kwargs runs everything.

    Args:
        text: The input text to analyze.
        **options: Optional feature flags:
            count_words (bool): Include word count. Default True.
            count_sentences (bool): Include sentence count. Default True.
            find_longest_word (bool): Include longest word. Default True.
            sentiment_simple (bool): Include simple sentiment label. Default True.

    Returns:
        A dict with analysis results, for example:
        {
            'word_count': 12,
            'sentence_count': 2,
            'longest_word': 'wonderful',
            'sentiment': 'positive'
        }
        Returns {'error': 'Empty text provided'} if text is empty or whitespace.

    Example:
        >>> analyze_text("I love Python!", count_words=True, sentiment_simple=True)
        {'word_count': 3, 'sentiment': 'positive'}
    """
    if not text or not text.strip():
        return {'error': 'Empty text provided'}

    results: dict[str, Any] = {}

    if options.get('count_words', True):
        results['word_count'] = _count_words(text)

    if options.get('count_sentences', True):
        results['sentence_count'] = _count_sentences(text)

    if options.get('find_longest_word', True):
        results['longest_word'] = _find_longest_word(text)

    if options.get('sentiment_simple', True):
        results['sentiment'] = _simple_sentiment(text)

    return results


# --- Demo when run directly ---
if __name__ == "__main__":
    sample = "Python is a wonderful language. I love writing clean code! It makes me happy."

    print("=== Full Analysis ===")
    print(analyze_text(sample))

    print("\n=== Only Word Count + Sentiment ===")
    print(analyze_text(sample, count_words=True, sentiment_simple=True,
                        count_sentences=False, find_longest_word=False))

    print("\n=== Empty Text Edge Case ===")
    print(analyze_text(""))

    print("\n=== No Options Passed (all default True) ===")
    print(analyze_text("This is a bad and horrible day."))

    print("\n=== AI Version for Comparison ===")
    print(analyze_text_ai_version(sample))
