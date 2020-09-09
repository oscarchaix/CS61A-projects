"""Typing test implementation"""

from utils import *
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    lst = []
    for i in paragraphs:
        if select(i):
            lst.append(i)
    if k < len(lst):
        return lst[k]
    else:
        return ''
    # END PROBLEM 1

def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM
    def helper_function(paragraph):
        my_list = []
        modified_paragraph = split(remove_punctuation(lower(paragraph)))
        for i in topic:
            if i in modified_paragraph:
                my_list.append(1)
            my_list.append(0)
        return sum(my_list) > 0
    return helper_function
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    result = []
    if len(typed_words) > len(reference_words):
        for i in range(len(reference_words)):
            if typed_words[i] == reference_words[i]:
                result.append(100/len(typed_words))
            else:
                result.append(0)
    else:
        for i in range(len(typed_words)):
            if typed_words[i] == reference_words[i]:
                result.append(100/len(typed_words))
            else:
                result.append(0)
    return float(sum(result))
    # END PROBLEM 3

def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    return (len(typed)/5)*(60/elapsed)
    # END PROBLEM 4

def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    if user_word in valid_words:
        return user_word
    else:
        lst = {i:diff_function(user_word,valid_words[i],limit) for i in range(len(valid_words))}
        if diff_function(user_word,valid_words[min(lst, key=lst.get)],limit) <= limit:
            return valid_words[min(lst, key=lst.get)]
        else:
            return user_word
    # END PROBLEM 5

def swap_diff(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    if len(start) == 0 or len(goal) == 0:
        return 0

    elif limit < 0:
        return 0

    elif len(start) == len(goal):
        if start[len(start)-1] != goal[len(goal)-1]:
            return 1 + swap_diff(start[:len(start)-1],goal[:len(goal)-1],limit-1)
        else:
            return 0 + swap_diff(start[:len(start)-1],goal[:len(goal)-1],limit)

    else:
        diff = abs(len(goal)-len(start))
        if start[min(len(start),len(goal))-1] != goal[min(len(start),len(goal))-1]:
            return diff + 1 + swap_diff(start[:min(len(start),len(goal))-1],goal[:min(len(start),len(goal))-1],limit-1-diff)
        else:
            return diff + 0 + swap_diff(start[:min(len(start),len(goal))-1],goal[:min(len(start),len(goal))-1],limit-diff)
    # END PROBLEM 6


def edit_diff(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""

    if start == goal: # Fill in the condition
        # BEGIN
        return 0
        # END

    elif not start or not goal: # Feel free to remove or add additional cases
    # BEGIN
        return max(len(start),len(goal))
    # END

    elif limit < 0:
        return 0

    elif start[:1] == goal[:1]:
        return edit_diff(start[1:],goal[1:],limit)

    else:
        add_diff = edit_diff(start[1:],goal,limit-1) + 1
        remove_diff = edit_diff(start,goal[1:],limit-1) + 1
        substitute_diff = edit_diff(start[1:],goal[1:],limit-1) + 1
        return min(add_diff,remove_diff,substitute_diff)



def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'




###########
# Phase 3 #
###########


def report_progress(typed, prompt, id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    total = 0
    for i in range(len(typed)):
        if typed[i] == prompt[i]:
            total += 1
        else:
            break
    frac_corr = total / len(prompt)
    send({'id':id,'progress':frac_corr})
    return frac_corr
    # END PROBLEM 8


def fastest_words_report(word_times):
    """Return a text description of the fastest words typed by each player."""
    fastest = fastest_words(word_times)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def fastest_words(word_times, margin=1e-5):
    """A list of which words each player typed fastest."""
    n_players = len(word_times)
    n_words = len(word_times[0]) - 1
    assert all(len(times) == n_words + 1 for times in word_times)
    assert margin > 0
    # BEGIN PROBLEM 9
    all_words = [word(wt) for wt in word_times[0]][1:]

    def time_spent_typing_word(i,player):
        "The time it took player to type word i"
        return elapsed_time(word_times[player][i+1]) - elapsed_time(word_times[player][i])

    all_times_for_every_word =  []
    for w in range(n_words):
        all_times_for_every_word += [[time_spent_typing_word(w, p) for p in range(n_players)]]

    min_times = []
    for element in all_times_for_every_word:
        min_times.append(min(element))

    final_lst = []
    for player in range(n_players):
        final_lst += [[all_words[i] for i in range(len(all_words)) if all_times_for_every_word[i][player] <= (min_times[i] + margin)]]
    return final_lst

    # END PROBLEM 9


def word_time(word, elapsed_time):
    """A data abstrction for the elapsed time that a player finished a word."""
    return [word, elapsed_time]


def word(word_time):
    """An accessor function for the word of a word_time."""
    return word_time[0]


def elapsed_time(word_time):
    """An accessor function for the elapsed time of a word_time."""
    return word_time[1]


enable_multiplayer = False  # Change to True when you


##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)
