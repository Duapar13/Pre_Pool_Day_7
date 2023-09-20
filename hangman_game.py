import random

word_list = ["hangman"]

def choose_word(word_list):
    return random.choice(word_list)

def initialize_game():
    word_to_guess = choose_word(word_list)
    guessed_letters = []
    attempts = 6  

    return word_to_guess, guessed_letters, attempts

def display_word(word, guessed_letters):
    display = ""
    for letter in word:
        if letter in guessed_letters:
            display += letter
        else:
            display += "_"
    return display

def play_hangman():
    print("Welcome to Hangman!")
    word_to_guess, guessed_letters, attempts = initialize_game()

    while attempts > 0:
        print("\nAttempts left:", attempts)
        current_display = display_word(word_to_guess, guessed_letters)
        print("Current word:", current_display)

        guess = input("Guess a letter or the whole word: ").lower()

        if len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters:
                print("You've already guessed that letter.")
            elif guess in word_to_guess:
                print("Good guess!")
                guessed_letters.append(guess)
            else:
                print("Incorrect guess.")
                guessed_letters.append(guess)
                attempts -= 1
        elif len(guess) == len(word_to_guess) and guess.isalpha():
            if guess == word_to_guess:
                print("Congratulations! You've guessed the word:", word_to_guess)
                break
            else:
                print("Incorrect guess.")
                attempts -= 1
        else:
            print("Invalid input. Please enter a single letter or the entire word.")

    if attempts == 0:
        print("Sorry, you've run out of attempts. The word was:", word_to_guess)

play_hangman()
