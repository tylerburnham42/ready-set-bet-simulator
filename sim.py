import random
from typing import Dict
import matplotlib.pyplot as plt

class Horse:
    def __init__(self, name="", boost=0, position=0):
        self.position = position
        self.boost=boost
        self.name = name

    def __lt__(self, obj):
        return self.position < obj.position

    def __gt__(self, obj):
        return self.position > obj.position

    def __le__(self, obj):
        return self.position <= obj.position

    def __ge__(self, obj):
        return self.position >= obj.position

    def __eq__(self, obj):
        return self.position == obj.position

    def __repr__(self):
        return f'{self.name}: {self.position}'

def get_roll() -> int:
    """ Gets The Sum of 2 Six Sided Dice Rolls. """
    return random.randint(1, 6) + random.randint(1, 6)

def setup_horses() -> Dict[int, Horse]:
    """ Get the dictionary of horses used to simulate the race. """
    horse_dict = {}
    two_and_three = Horse(name='Horse 02/03', boost=3)
    horse_dict[2] = two_and_three
    horse_dict[3] = two_and_three

    horse_dict[4] = Horse(name='Horse 04', boost=3)
    horse_dict[5] = Horse(name='Horse 05', boost=2)
    horse_dict[6] = Horse(name='Horse 06', boost=1)
    horse_dict[7] = Horse(name='Horse 07', boost=0)
    horse_dict[8] = Horse(name='Horse 08', boost=1)
    horse_dict[9] = Horse(name='Horse 09', boost=2)
    horse_dict[10] = Horse(name='Horse 10', boost=3)

    eleven_and_twelve = Horse(name='Horse 11/12', boost=3)
    horse_dict[11] = eleven_and_twelve
    horse_dict[12] = eleven_and_twelve
    return horse_dict

def run_race():
    """ Runs a full race and returns the winner. """
    winner = 0
    previous_num = 0
    horse_dict = setup_horses()
    while(not winner):
        # Roll a Random Number and update the position of the horse
        current_num = get_roll()
        horse_dict[current_num].position += 1

        # Boost the horse on consecutive rolls.
        if current_num == previous_num:
            horse_dict[current_num].position += horse_dict[current_num].boost
            # Clear the previous number on doubles so triples will not trigger.
            previous_num = 0

        previous_num = current_num

        # If the race is run mark the winner.
        if horse_dict[current_num].position >= 15:
            winner = horse_dict[current_num].name

    place = [winner]
    show = [winner]
    place_num = -1
    show_num = -1

    del horse_dict[2]
    del horse_dict[12]
    ordered_horses = sorted(horse_dict.values(), reverse=True)
    winner_found = False
    tie_second = False
    for horse in ordered_horses:
        # Skip the Winner We already know it.
        if horse.position >= 15:
            continue

        # If the place number is still the default this is second place.
        if place_num == -1:
            place_num = horse.position
            place.append(horse.name)
            show.append(horse.name)
            continue

        # If tied for second place continue to mark that.
        if place_num == horse.position:
            place.append(horse.name)
            show.append(horse.name)
            tie_second = True
            continue

        # If there was a tie and the new number is not that skip it
        if tie_second:
            break

                # If the place number is still the default this is second place.
        if show_num == -1:
            show_num = horse.position
            show.append(horse.name)
            continue

        # If tied for second place continue to mark that.
        if show_num == horse.position:
            show.append(horse.name)
            tie_second = True
            continue

        else:
            break

    #print(ordered_horses)
    return winner, place, show

def make_plot(results, name):

    names, values = zip(*results)

    fig = plt.figure(figsize = (10, 5))

    # creating the bar plot
    plt.bar(names, values, color ='maroon',
            width = 0.4)

    plt.xlabel("Horses")
    plt.ylabel(f"Number of {name}s")
    plt.title(f"Simulating {name} Percentage in Ready Set Bet.")
    plt.show()

if __name__ == "__main__":
    winners = {}
    places = {}
    shows = {}
    total = 100000
    for i in range(total):
        winner_result, place_result, show_result = run_race()
        if winner_result in winners:
            winners[winner_result] += 1
        else:
            winners[winner_result] = 1

        for place in place_result:
            if place in places:
                places[place] += 1
            else:
                places[place] = 1

        for show in show_result:
            if show in shows:
                shows[show] += 1
            else:
                shows[show] = 1

    winners = sorted(winners.items())
    total_places = sum(places.values())
    places = sorted(places.items())
    total_shows = sum(shows.values())
    shows = sorted(shows.items())
    print("Win %")
    print(f"Total Races: {total}")
    for name, value in winners:
        print(f'{name} - {value/total:.4f}')

    print(f"Total Places: {total_places}")
    print("Place %")
    for name, value in places:
        print(f'{name} - {value/total_places:.4f}')

    print(f"Total Shows: {total_shows}")
    print("Show %")
    for name, value in shows:
        print(f'{name} - {value/total_shows:.4f}')

    make_plot(winners, "Win")
    make_plot(places, "Place")
    make_plot(shows, "Show")
