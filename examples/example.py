from typing import List, Dict

def calculate_word_frequencies(text: str) -> Dict[str, int]:
    """
    Calculate the frequency of each word in the given text.
    
    Args:
        text: Input text to analyze
        
    Returns:
        Dictionary with words as keys and their frequencies as values
    """
    words = text.lower().split()
    frequencies: Dict[str, int] = {}
    
    for word in words:
        if word in frequencies:
            frequencies[word] += 1
        else:
            frequencies[word] = 1
            
    return frequencies

def get_most_common_words(frequencies: Dict[str, int], n: int) -> List[str]:
    """
    Get the n most frequently occurring words.
    
    Args:
        frequencies: Dictionary of word frequencies
        n: Number of top words to return
        
    Returns:
        List of the n most common words
    """
    sorted_words = sorted(
        frequencies.items(),
        key=lambda x: (-x[1], x[0])
    )
    return [word for word, _ in sorted_words[:n]]

# Example usage
if __name__ == "__main__":
    sample_text = "the quick brown fox jumps over the lazy dog"
    freq = calculate_word_frequencies(sample_text)
    top_words = get_most_common_words(freq, 3)
    print(f"Top 3 most common words: {top_words}") 