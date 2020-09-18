#######
# File: Homework2_drb160130.py
# Author: Dorian Benitez (drb160130)
# Date: 9/6/2020 
# Purpose: CS 4395.001 - Homework 2 (Word Guessing Game)
#######

import sys
import nltk
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import random


# Function to preprocess the raw text
def preprocessing(raw):
    # Tokenize the lowercase raw text
    tokens = word_tokenize(raw.lower())

    # Store the stopwords
    stop_words = set(stopwords.words('english'))

    # Reduce the tokens to only those that are alpha, not in the NLTK stopword list, and have length > 5
    tokens = [t for t in tokens if t.isalpha() and t not in stop_words and len(t) > 5]

    # Lemmatize the tokens and use set() to make a list of unique lemmas
    unique_lemmas = sorted(list(set([WordNetLemmatizer().lemmatize(r) for r in tokens])))

    # Do POS tagging on the unique lemmas and print the first 20 tagged items
    lemmas_unique_tags = nltk.pos_tag(unique_lemmas)

    # Create a list of only those lemmas that are nouns
    noun_lemmas = list([x[0] for x in lemmas_unique_tags if x[1].startswith("N")])

    # Print the number of tokens and the number of nouns
    # Calculate the lexical diversity of the tokenized text and output it
    print('\nNumber of Tokens:', len(tokens))
    print('\nNumber of Nouns:', len(noun_lemmas))
    print("\nLexical diversity: %.2f" % (len(unique_lemmas) / (len(tokens))))
    print('\nFirst 20 Tagged Items:', lemmas_unique_tags[:20])

    return tokens, noun_lemmas


# Guessing game function
def guessing_game(list):
    # Give the user 5 points to start with
    user_score = 5

    # Randomly choose one of the 50 words in the top 50 list
    random_word_from_list = random.choice(list)[0]
    is_in_word = []
    guessed_letter = []

    print("\n\nScore: ", user_score, "\n")

    for element in random_word_from_list:
        print('_', end=" ")

    # The game ends when the total user score is negative
    while user_score > -1:
        user_letter_input = input('\n\nPlease enter a letter: ').lower()

        # The user is prompted to retry with a proper value
        if not user_letter_input.isalpha() and user_letter_input != "!":
            print("\nType a valid letter, please!")

        # The user is prompted to retry if they entered a duplicate letter
        elif user_letter_input in guessed_letter:
            print("\nYou already tried this letter, try again!")

        # The game ends when the user enters ‘!’
        elif user_letter_input != "!":
            # Populate a list that holds all user guesses
            guessed_letter.append(user_letter_input)

            # If the letter is in the word, fill in all matching letter _ with the letter and add 1 point to the user score
            if user_letter_input in random_word_from_list:
                user_score += 1
                is_in_word.append(user_letter_input)
                print("\nThis letter IS in the word")

            # If the letter is not in the word, subtract 1 from the user score and print message
            else:
                print("\nThis letter is NOT in the word")
                user_score -= 1

            # Update and print the current state of the game
            count = 0
            for element in random_word_from_list:
                if element in is_in_word:
                    print(element, end=" ")
                    count += 1
                else:
                    print('_', end=" ")

            # Right or wrong, give user feedback on their score for this word after each guess
            print("\nScore:", user_score)

            # Game ends if the user guesses the word correctly
            if count == len(random_word_from_list):
                # Ask the user if they want to play again
                play_again_decision = input("\n\nCongrats, you won!!! Play again? (Y/N) ")
                if play_again_decision.lower() == "y":
                    guessing_game(list)
                else:
                    print("\nThank you for playing!")
                    sys.exit(0)

        else:
            print("\nThank you for playing!")
            sys.exit(0)

    # Keep a cumulative total score and end the game if it is negative
    print("\n\nYou lost by score...the word was:", random_word_from_list)

    # Ask the user if they want to play again
    play_again_decision = input("\nPlay again? (Y/N) ")
    if play_again_decision.lower() == "y":
        guessing_game(list)
    else:
        print("\nThank you for playing!")
        sys.exit(0)


if __name__ == '__main__':
    # Send the filename to the main program in a system argument.
    # If no system arg is present, print an error message and exit the program.
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        print('Input file: ', input_file)

        with open('anat19.txt', 'r') as f:
            raw_text = f.read()

        tokens, noun_lemmas = preprocessing(raw_text)
        common_list = []

        # Dictionary of {noun:count of noun in tokens} items from the nouns and tokens lists
        counts = {t: tokens.count(t) for t in noun_lemmas}

        # Sort the dictionary by count and print the 50 most common words and their counts
        # Save these words to a list because they will be used in the guessing game
        sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        print("50 most common words:")
        for i in range(50):
            common_list.append(sorted_counts[i])
            print(sorted_counts[i])

        # Start a guessing game with the list of 50 words
        guessing_game(common_list)
    else:
        print('File name missing')
