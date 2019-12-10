import random
import time
import csv
import datetime


# function that reads capitals and their corresponding countries from a .csv file:
def import_capital_list(cities_list_file):
    with open(cities_list_file, encoding='ISO-8859-1') as capital_and_countries_file:
        reader=csv.reader(capital_and_countries_file, delimiter='|')
        country_list, capital_list = zip(*reader)
        capital_list = list(capital_list)
        country_list = list(country_list)
    capital_and_countries_file.close()
    return country_list, capital_list

# function responsible for drawing the hangman, depending on lives left


def draw_hangman(lives_left):
    if lives_left == 0:
        print('________\n|/      |\n|      (_)\n|      \|/\n|       |\n|      / \ \n|\n|___')
    elif lives_left == 1:
        print('________\n|/      |\n|      (_)\n|      \|/\n|       |\n|      /   \n|\n|___')
    elif lives_left == 2:
        print('________\n|/      |\n|      (_)\n|      \|/\n|       |\n|          \n|\n|___')
    elif lives_left == 3:
        print('________\n|/      |\n|      (_)\n|      \| \n|       |\n|          \n|\n|___')
    elif lives_left == 4:
        print('________\n|/      |\n|      (_)\n|       | \n|       |\n|          \n|\n|___')
    elif lives_left == 5:
        print('________\n|/      |\n|      (_)\n|         \n|        \n|          \n|\n|___')
    elif lives_left == 6:
        print('________\n|/      |\n|         \n|         \n|        \n|          \n|\n|___')


play = True
while play:
    #define variables and set their default values
    picking_category = 1
    game_on = 0
    guesses_left = 6
    letter_index = 0
    capital_letters_set = {''}
    wrong_letters = {''}
    guess_count = 0
    capital_list = []
    country_list = []
    rand_number = 0
    hint_prompted = 0
    first_letter_hint = 0
    start_time = time.time()
    now = datetime.datetime.now()

    while picking_category == 1:
        #read high score list from file, each column into separate list
        try:
            with open('hangman_score.csv', newline='') as f:
                score_reader=csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
                sortedlist = sorted(score_reader, key=lambda data_entry: float(data_entry[1]))
                while len(sortedlist) > 10:
                    sortedlist.pop()
                name_list, score_list, guess_count_list, date_list, time_list, capital_guessed = zip(*sortedlist)      
        except:
            name_list = []
            score_list = []
            guess_count_list = []
            date_list = []
            time_list = []
            capital_guessed = []
        finally:
            #print 10 best records from current high score sheet
            print('Best scores:')
            print('Name  Score    Guesses     Date        Time      Guessed capital')
            for order in range(0, len(name_list)):
                print(name_list[order], end = '')
                print('  ',end = '')
                print(score_list[order], end = '')
                print('  ',end = '')
                print(guess_count_list[order], end = '')
                print('          ',end = '')
                print(date_list[order], end = '')
                print('  ',end = '')
                print(time_list[order], end = '')
                print('  ',end = '')
                print(str(capital_guessed[order]))
                print('')

        #pick the continent of capital-country pair
        category_pick = input('Pick a continent: \n-E for Europe \n-Am for Americas \n-As for Asia \n-Af for Africa \n-O for Oceania \n-W for whole world. \n')
        if category_pick.lower() == 'e':
            country_list, capital_list = import_capital_list('Europe_capitals.txt')
            picking_category = 0
            game_on = 1
        elif category_pick.lower() == 'am':
            country_list, capital_list = import_capital_list('America_capitals.txt')
            picking_category = 0
            game_on = 1
        elif category_pick.lower() == 'as':
            country_list, capital_list = import_capital_list('Asia_capitals.txt')
            picking_category = 0
            game_on = 1
        elif category_pick.lower() == 'af':
            country_list, capital_list = import_capital_list('Africa_capitals.txt')
            picking_category = 0
            game_on = 1
        elif category_pick.lower() == 'o':
            country_list, capital_list = import_capital_list('Oceania_capitals.txt')
            picking_category = 0
            game_on = 1
        elif category_pick.lower() == 'w':
            country_list, capital_list = import_capital_list('Countries_and_capitals.txt')
            picking_category = 0
            game_on = 1
        else:
            print('Pick again.\n')
    #generate random number and use it to pick two elements from both country and capital lists, that way we're sure they are corresponding
    rand_number = random.randrange(0,len(capital_list))
    selected_capital = capital_list[rand_number]
    selected_country = country_list[rand_number]
    start_time = time.time() #start the timer
    hidden_capital = selected_capital  #create copy of the capital to replace its letters with dashes
    #loop responsible for swapping each letter of the capital into dashes
    for letter in selected_capital:
        if letter.isalpha():
            capital_letters_set.add(letter.lower())
                    
            hidden_capital = hidden_capital.replace(letter,'_')
    draw_hangman(6) #draw empty gallows
    
    print(hidden_capital)

    #print(selected_capital)       #uncomment to enable cheat

    while game_on == 1:
        guess_count += 1
        player_guess = input('Guess a letter: ')
        if player_guess.lower() == selected_capital.lower():
            elapsed_time = time.time() - start_time     #calculate elapsed time
            rounded_time = "{0:.2f}".format(elapsed_time)
            print('Correct! Nice job!')
            if float(rounded_time) < float(score_list[9]):   #save the result on high score list if the result is better than the 10th record
                print("Impressive! What's your name? You'll be remembered forever! Well, at least until a better player arrives. \n")
                high_score_name = input("What's your name? \n")
                with open('hangman_score.csv', mode='a', newline= '') as file:     
                    score_writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                    score_writer.writerow([high_score_name, str(rounded_time),str(guess_count),str(now.date()),str(now.time()),selected_capital])
            print('Congratulations! You guessed the answer in ' + rounded_time +' seconds!\n' + 'You managed to do it in ' + str(guess_count) + ' guesses.')
            play_again = str(input('Type Y to play again. '))
            if play_again.lower() == 'y':
                break
            game_on = 0
            play = False

        elif player_guess.lower() in capital_letters_set and len(player_guess)>0: 
            capital_letters_set.remove(player_guess.lower())
            print('You guessed '+ player_guess +' correctly!')

            for letter in selected_capital: #put the correct letter to the dashed word at the corresponding place
                
                if letter.lower() == player_guess.lower():
                    hidden_capital = hidden_capital[:letter_index] + selected_capital[letter_index] + hidden_capital[letter_index + 1:]
                letter_index +=1

        else:   #what's being desplayed when user inputs wrong answer
            if len(player_guess) >= 2:
                print('You took the shot but you missed. -2 chances.')
                guesses_left -= 2
            else:
                print('Wrong')
                guesses_left -= 1
                wrong_letters.add(player_guess)

        draw_hangman(guesses_left)
        print(hidden_capital)
        print('Chances left:' + str(guesses_left))
        print('Not-in-word letters:' + str(wrong_letters))
        letter_index = 0

        if guesses_left < 1:
            print(f'You have lost. The capital was {selected_capital}')
            play_again = str(input('Type Y to play again. '))
            if play_again.lower() == 'y':
                break
            game_on = 0
            play = False

        if guesses_left == 2 and first_letter_hint == 0:   #while on 2 chances left, player gets the first letter of the word as the hint
            print(f'It starts with {selected_capital[0]}')
            first_letter_hint = 1

        if guesses_left == 1 and hint_prompted == 0:   #while on 1 chance left, player gets a hint about the city's country
            print(f"Oops, only 2 chances left... Here, take this hint: \nIt's the capital of {selected_country}.")
            hint_prompted = 1


        if capital_letters_set == {''}:
            elapsed_time = time.time() - start_time #calculate elapsed time based on current time and time saved at the start of the game
            rounded_time = "{0:.2f}".format(elapsed_time)
            # save the score
            if float(rounded_time) < float(score_list[9]):
                print("Impressive! What's your name? You'll be remembered forever! Well, at least until a better player arrives. \n")
                high_score_name = input("What's your name? \n")
                # save score into .csv file
                with open('hangman_score.csv', mode='a', newline= '') as file:
                    score_writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    score_writer.writerow([high_score_name, str(rounded_time),str(guess_count),str(now.date()),str(now.time()),selected_capital])
            print('Congratulations! You guessed the answer in ' + rounded_time +' seconds!\n' + 'You managed to do it in ' + str(guess_count) + ' guesses.')
            play_again = str(input('Type Y to play again. '))
            if play_again.lower() == 'y':
                break
            game_on = 0
            play = False
        
    