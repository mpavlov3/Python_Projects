import random

game_results = []
print('H A N G M A N')

while True:
    game_start = input('"Type "play" to play the game, "results" to show the scoreboard, and "exit" to quit".')
    key = random.choice(['python', 'java', 'swift', 'javascript'])
    display = '-' * len(key)
    if game_start == "play":
        i = 0
        used_letters = []
        while i < 8:
            print()
            print(display)
            letter = input('Input a letter: ')
            if len(letter) != 1:
                print("Please, input a single letter.")
            elif letter in key:
                counter = 0
                for x in key:
                    if x == letter:
                        display = display[:counter] + letter + display[counter + 1:]
                    counter += 1
                if letter in used_letters:
                    print("You've already guessed this letter.")
                used_letters.append(letter)
            else:
                if letter.isalpha() is False:
                    print("Please, enter a lowercase letter from the English alphabet.")
                elif letter.isupper() is True:
                    print("Please, enter a lowercase letter from the English alphabet.")
                elif letter in used_letters:
                    print("You've already guessed this letter.")
                else:
                    print("That letter doesn't appear in the word.")
                    i += 1
                    used_letters.append(letter)
            if display == key:
                print(f"You guessed the word {key}!")
                print('You survived!')
                game_results.append('You survived!')
                break

        else:
            print("You lost!")
            game_results.append("You lost!")
    elif game_start == "results":
        print("You lost: " + str(game_results.count("You lost!")) + ' times.')
        print("You won: " + str(game_results.count("You survived!")) + ' times.')
    elif game_start == "exit":
        break
