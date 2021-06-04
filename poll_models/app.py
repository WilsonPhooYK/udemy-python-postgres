from datetime import datetime
import random
import matplotlib.pyplot as plt

import pytz
import database
import charts
from models.option import Option
from models.poll import Poll
from connection_pool import get_connection


DATABASE_PROMPT = "Enter the DATABASE_URI value or leave empty to load from .env file: "
MENU_PROMPT = """-- Menu --

1) Create new poll
2) List open polls
3) Vote on a poll
4) Show poll votes
5) Select a random winner from a poll option
6) Chart Polls
7) Chart All Polls
8) Exit

Enter your choice: """
NEW_OPTION_PROMPT = "Enter new option text (or leave empty to stop adding options): "
CHART_POLL_PROMPT = "Select the poll id to create a pie chart of the vote percentages (Enter 'q' to quit): "

def prompt_create_poll():
    poll_title = input("Enter poll title: ")
    poll_owner = input("Enter poll owner: ")
    poll = Poll(poll_title, poll_owner)
    poll.save()

    while (new_option := input(NEW_OPTION_PROMPT)):
        poll.add_option(new_option)

def list_open_polls():
    for poll in Poll.all():
        print(f"{poll.id}: {poll.title} (created by {poll.owner})")


def prompt_vote_poll():
    poll_id = int(input("Enter poll would you like to vote on: "))
    
    _print_poll_options(Poll.get(poll_id).options)

    option_id = int(input("Enter option you'd like to vote for: "))
    username = input("Enter the username you'd like to vote as: ")
    
    Option.get(option_id).vote(username)


def _print_poll_options(options: list[Option]):
    for option in options:
        print(f"{option.id}: {option.text}")


def show_poll_votes():
    poll_id = int(input("Enter poll you would like to see votes for: "))
    options = Poll.get(poll_id).options
    votes_per_option = [len(option.votes) for option in options]
    total_votes = sum(votes_per_option)
    
    try:
        for option, votes in zip(options, votes_per_option):
            percentage = votes / total_votes * 100.0
            print(f"{option.text} got {votes} votes ({percentage:.2f}% of total)")
    except ZeroDivisionError:
        print("No votes cast for this poll yet.")
        
    vote_log = input("Would you like to see the vote log? (y/N)")
    
    if vote_log == "y":
        _print_votes_for_options(options)


def _print_votes_for_options(options: list[Option]):
    for option in options:
        print(f"-- {option.text}")
        for vote in option.votes:
            naive_datetime = datetime.utcfromtimestamp(vote[2])
            utc_date = pytz.utc.localize(naive_datetime)
            local_date = utc_date.astimezone(pytz.timezone("Asia/Singapore")).strftime("%Y-%m-%d %H:%M")
            print(f"\t {vote[0]} on {local_date}")
    
def randomize_poll_winner():
    poll_id = int(input("Enter poll you'd like to pick a winner for: "))
    _print_poll_options(Poll.get(poll_id).options)

    option_id = int(input("Enter which is the winning option, we'll pick a random winner from voters: "))
    votes = Option.get(option_id).votes
    winner = random.choice(votes)
    print(f"The randomly selected winner is {winner[0]}.")
    
def chart_polls():
    while (selected_poll := input(CHART_POLL_PROMPT) != 'q'):
        options_spread = Poll.get(int(selected_poll)).options_spread
        # Draw pie chart here
        _ = charts.create_pie_chart(options_spread)
        plt.show()
        
def chart_all_polls():
    options_spread = Poll.get_polls_and_votes()
    # Draw pie chart here
    _ = charts.create_bar_chart(options_spread)
    plt.show()


MENU_OPTIONS = {
    "1": prompt_create_poll,
    "2": list_open_polls,
    "3": prompt_vote_poll,
    "4": show_poll_votes,
    "5": randomize_poll_winner,
    "6": chart_polls,
    "7": chart_all_polls
}


def menu():
    with get_connection() as connection:
        database.create_tables(connection)

    while (selection := input(MENU_PROMPT)) != "8":
        try:
            MENU_OPTIONS[selection]()
        except KeyError:
            print("Invalid input selected. Please try again.")


menu()
