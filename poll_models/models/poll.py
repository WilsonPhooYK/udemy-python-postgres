from dataclasses import dataclass
from connection_pool import get_connection
from models.option import Option
import database

@dataclass
class Poll:
    title: str
    owner: str
    id: int = 0
    
    def __repr__(self) -> str:
        return f"Poll({self.title!r}, {self.owner!r}, {self.id!r})"
    
    def save(self):
        with get_connection() as connection:
            new_poll_id = database.create_poll(connection, self.title, self.owner)
            self.id = new_poll_id
        
    def add_option(self, option_text: str):
        Option(option_text, self.id).save()
        
        
    @property
    def options(self) -> list[Option]:
        with get_connection() as connection:
            options = database.get_poll_options(connection, self.id)
        
        return [Option(option[1], option[2], option[0]) for option in options]
    
    @property
    def options_spread(self) -> list[database.OptionSpread]:
        with get_connection() as connection:
            spreads = database.get_options_spread_in_poll(connection, self.id)
            return spreads
    
    @classmethod
    def get(cls, poll_id: int) -> "Poll":
        with get_connection() as connection:
            poll = database.get_poll(connection, poll_id)
            return cls(poll[1], poll[2], poll[0])
    
    @classmethod
    def all(cls) -> list["Poll"]:
        with get_connection() as connection:
            polls = database.get_polls(connection)
            return [cls(poll[1], poll[2], poll[0]) for poll in polls]
        
    @classmethod
    def get_polls_and_votes(cls) -> list[database.OptionSpread]:
        with get_connection() as connection:
            polls_and_votes = database.get_polls_and_votes(connection)
            return polls_and_votes
    
    
    @classmethod
    def latest(cls) -> "Poll":
        with get_connection() as connection:
            poll = database.get_latest_poll(connection)
            return cls(poll[1], poll[2], poll[0])
        