word_counter = {}

raw_input = input("Enter a long sentence or paragraph > ")
raw_input = raw_input.title().split()

if not raw_input:
    print("You didn't type anything!")

else:
    for word in raw_input:
        if word in word_counter.keys():
            word_counter[word] += 1
        else:
            word_counter[word] = 1

    # Find the biggest repeated word
    biggest_word = max(word_counter, key = lambda k: word_counter[k])
    print(f"You type {biggest_word} {word_counter[biggest_word]} times.")
