class SearchEngine:
    def __init__(self, indexer):
        self.indexer = indexer

    def print_word(self, word):
        word = word.lower()
        if word in self.indexer.index:
            data = self.indexer.index[word]
            print(f"\nInverted index for '{word}':")
            for url, positions in data.items():
                frequency = len(positions)
                print(f"  -> {url} | Frequency: {frequency} | Positions: {positions}")
        else:
            print(f"Word '{word}' not found in the index.")

    def find_phrase(self, phrase):
        words = phrase.lower().split()
        if not words:
            return

        url_sets = []
        for word in words:
            if word in self.indexer.index:
                # Add the set of URLs where this word appears
                url_sets.append(set(self.indexer.index[word].keys()))
            else:
                print(f"No pages found containing the word '{word}'.")
                return

        # Perform an intersection to find URLs that contain ALL words in the phrase
        common_urls = set.intersection(*url_sets)

        if common_urls:
            print(f"\nFound {len(common_urls)} page(s) containing '{phrase}':")
            for url in common_urls:
                print(f"  -> {url}")
        else:
            print(f"No single page found containing all words in '{phrase}'.")