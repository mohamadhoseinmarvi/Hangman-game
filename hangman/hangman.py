
import random
import string

WORDLIST_FILENAME = "words.txt"

responses = [
    "I am thinking of a word that is {0} letters long",
    "Congratulations, you won!",
    "Your total score for this game is: {0}",
    "Sorry, you ran out of guesses. The word was: {0}",
    "You have {0} guesses left.",
    "Available letters: {0}",
    "Good guess: {0}",
    "Oops! That letter is not in my word: {0}",
    "Oops! You've already guessed that letter: {0}",
]

def choose_random_word(wordlist):
    return random.choice(wordlist)


def load_words():
    print(f'Loading word list from file: {WORDLIST_FILENAME}')
    word_file = open(WORDLIST_FILENAME,"r")
    read_file = word_file.read()
    wordlist = read_file.split(" ")
    print(f"{len(wordlist)} words loaded.")

    return wordlist


def is_word_guessed(word, letters_guessed):

    is_my_word_guessed = False
    if (all(x in letters_guessed for x in list(word))):
        is_my_word_guessed = True
    return is_my_word_guessed


def get_guessed_word(word, letters_guessed):

    guessed_string = " "
    for letter in word:
        if letter.lower() in letters_guessed:
            print(letter,end="")
        else:
            print("_",end= " ")


def get_remaining_letters(letters_guessed):

    letters = list(string.ascii_lowercase)
    for letter in letters_guessed:
        if letter in letters:
            letters.remove(letter)

    print(f"Available letters: {''.join(letters)}")


def hangman(word):

    print("I am thinking of a word that is {0} letters long".format(len(word)))

    while True:
        try:
            letters_guessed = []
            vowel = ["a", "e", "i", "o", "u"]
            tries = 11
            score = 0
            while tries > 0:
                print(f"You have {tries} guesses left.")
                get_remaining_letters(letters_guessed)
                guess = str(input("Please guess a letter: ")).lower()

                while guess[0] in letters_guessed:

                    print(f"Oops! You've already guessed that letter: {get_guessed_word(word, letters_guessed)}")
                    print()
                    print("-------------")
                    guess = str(input("Please guess a letter: ")).lower()

                if guess[0] not in word:

                    if guess in vowel:
                        tries = tries - 2
                    else:
                        tries = tries - 1

                letters_guessed.append(guess[0])
                if guess[0] in word:
                    print("Good guess:", end=" ")
                    get_guessed_word(word, letters_guessed)
                else:
                    print("Oops! That letter is not in my word: ", end=" ")
                    get_guessed_word(word, letters_guessed)

                print()
                print("-------------------")

                word_is_guessed_or_not = is_word_guessed(word, letters_guessed)
                if word_is_guessed_or_not == True:

                    unique_char = set(word)
                    score = tries * len(unique_char)
                    print("Congratulations, you won")
                    print(f"Your total score for this game is: {score}")
                    break
            if tries == 0:

                print(f"Sorry, you ran out of guesses. The word was: {word}")
                exit()
            return score
        except IndexError:
            pass

def scoreboard():

    try:
        file = open("scores.txt", 'r')
        readthefile = file.readlines()
        sorted_data = sorted(readthefile, reverse=True)
        print("Score       " + " Name")
        print("--------------------------")
        for line in range(3):
            print(str(sorted_data[line]))
        file.close()
    except IndexError:
        pass

def high_score():

    list_all = []
    with open("scores.txt", "r") as f:
        for line in f:
            list_all = line.split(" ")
    return list_all


def update_scoreboard(name,score):

    file = open("scores.txt", 'a')
    file.write("\n"+(str(score))+"          " + (name) )
    print("OK, your score has been saved. ")
    file.close()

def score_decision_controller_main():
    word = choose_random_word(wordlist)
    name = str(input("What is your name: "))
    highscore_list = []
    final_score=hangman(word)

    highscore_list = high_score()
    if final_score !=0:
                if highscore_list[0] != "\n" and len(highscore_list) != 0:
                    if int(final_score) > int(highscore_list[0]):

                        print("A new personal best!")
                        while True:
                            decision_save = str(input("Would you like to save your score(y/n): ")).lower()
                            if decision_save != "y" and decision_save != "n":
                                pass
                            elif decision_save == "y":
                                update_scoreboard(name, final_score)
                                game_decision_controller_main()
                                break
                            elif decision_save == "n":
                                game_decision_controller_main()
                                break
                    elif int(final_score) < int(highscore_list[0]) or int(final_score) == int(highscore_list[0]):

                        while True:
                            decision_save = str(input("Would you like to save your score(y/n): ")).lower()
                            if decision_save != "y" and decision_save != "n":
                                pass
                            elif decision_save == "y":
                                update_scoreboard(name, final_score)
                                game_decision_controller_main()
                                break
                            elif decision_save == "n":
                                game_decision_controller_main()
                                break


def game_decision_controller_main():
    what_to_do = str(input("Do you want to Play (p) view the leaderboard (l) or quit (q): ")).lower()
    if what_to_do=='p':
        score_decision_controller_main()
        while True:
            what_to_do_next = str(input("Would you like to play (p) or view the leaderboard (l): ")).lower()
            if what_to_do_next=='p':
                score_decision_controller_main()
            elif what_to_do_next=='l':
                scoreboard()
    elif what_to_do=='l':
        scoreboard()
        while True:
            what_to_do_next = str(input("Would you like to play (p) or view the leaderboard (l): ")).lower()
            if what_to_do_next=='p':
                score_decision_controller_main()
            elif what_to_do_next=='l':

                scoreboard()
    elif what_to_do=='q':

        print("Thanks, for playing goodbye!")
        exit()

if __name__ == "__main__":
    wordlist = load_words()
    print("Welcome to Hangman")
    game_decision_controller_main()
