# Get two words from the user 
word1 = input("Enter the first word: ") 
word2 = input("Enter the second word: ") 

# Normalize the words: remove spaces and make lowercase 
word1 = word1.replace(" ", "").lower() 
word2 = word2.replace(" ", "").lower() 

def sort_word(word) -> str:
    sorted_word = {}
    for char in word:
        sorted_word[char] = sorted_word.get(char, 0) + 1
    return sorted_word

# Compare the sorted lists 
if sort_word(word1) == sort_word(word2): 
    print("These words are anagrams!") 
    
else:
    print("These words are NOT anagrams.")
