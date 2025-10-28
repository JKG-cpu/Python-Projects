import re

class Compression:
    def generate_key(self, text: str, top_n: int = 5) -> dict:
        word_amounts = {}
        # Split text into words (keep punctuation separate)
        words = re.findall(r"\w+|[^\w\s]", text.lower())

        # Count word frequencies
        for word in words:
            word_amounts[word] = word_amounts.get(word, 0) + 1

        # Get top N most frequent words
        sorted_words = sorted(word_amounts.items(), key=lambda x: x[1], reverse=True)
        biggest_words = [word for word, _ in sorted_words[:top_n]]

        # Assign short codes
        key = {word: str(i+1) for i, word in enumerate(biggest_words)}
        return key

    def compress_text(self, text: str, amount: int = 5) -> str:
        key = self.generate_key(text, amount)
        words = re.findall(r"\w+|[^\w\s]", text.lower())

        # Replace words using key
        compressed_words = [key.get(word, word) for word in words]
        compressed_text = " ".join(compressed_words)
        return compressed_text, key

if __name__ == '__main__':
    text_to_compress = ("The rain fell and fell, falling softly, softly, softly on the rooftops. "
                        "The wind whispered and whispered, whispering through the trees, "
                        "through the branches, through the leaves. Lights blinked and blinked, "
                        "blinking in the distance, blinking in the darkness. People walked and walked, "
                        "walking slowly, slowly, slowly down the streets, down the avenues, down the alleys. "
                        "And the city hummed, hummed, hummed, alive and alive, alive and awake, awake in the night, "
                        "awake in the quiet, awake in the endless, endless, endless rhythm of itself.")

    compressed_text, key = Compression().compress_text(text_to_compress, 10)
    print("Compressed Text:\n", compressed_text)
    print("\nCompression Key:\n", key)
