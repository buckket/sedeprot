"""
    sedeprot
    ~~~~~~~~
    
    A self-enforcing protocol for collaborative decision-making
    
    Based on a proposal by erlehmann and Katharin Tai:
    http://daten.dieweltistgarnichtso.net/tmp/docs/collaborative-decision-making.html
    
    :copyright: (c) 2017 by buckket.
    :license: GPLv3+, see LICENSE for more details.
"""

__version__ = "1.0.0"


class DuplicateError(Exception):
    pass


class AlreadyVotedError(Exception):
    pass


class Participant:
    def __init__(self, name):
        """A participant in the decision-making process."""
        self.name = name
        self.votes = []

    def add_vote(self, value):
        """Appends a new value to the participant's acceptable choices."""
        if value not in self.votes:
            self.votes.append(value)
        else:
            raise DuplicateError

    def get_score(self, value):
        """Returns the position of the value in the participant's choices list."""
        return self.votes.index(value)

    def has_voted(self, round_number):
        """Checks if the participant has already voted in the specified round."""
        return len(self.votes) > round_number


class DecisionProcess:
    def __init__(self, participants, valid_answers=None):
        """A DecisionProcess oversees all participants, is able to check if consent is reached and acts as a gateway to 
        append new incoming votes to the respective participants whilst doing the error checking.
        
        Example session:
            >>> from sedeprot import *
            >>> dp = DecisionProcess(participants=["a", "b"])
            >>> dp.add_vote("a", "foo")
            >>> dp.check_consent()
            (0, None, None)
            >>> dp.add_vote("b", "bar")
            >>> dp.check_consent()
            (1, None, None)
            >>> dp.add_vote("a", "bar")
            >>> dp.check_consent()
            (1, None, None)
            >>> dp.add_vote("b", "foo")
            >>> dp.check_consent()
            (1, 1, ['bar', 'foo'])
        """
        self.participants = {name: Participant(name) for name in participants}
        self.valid_answers = valid_answers
        self.round = 0

    def add_vote(self, name, value):
        """Appends a new value to the specified participant's acceptable choices.
        Raises KeyError, ValueError, AlreadyVotedError, DuplicateError.
        """
        if name not in self.participants.keys():
            raise KeyError

        if self.valid_answers and value not in self.valid_answers:
            raise ValueError

        if self.participants[name].has_voted(self.round):
            raise AlreadyVotedError

        self.participants[name].add_vote(value)

    def get_votes(self, name=None):
        """Returns a dict with all participants and their submitted choices.
        
        Examples:
            - {'a': [], 'b': [], 'c': []}
            - {'a': ['foo', 'bar'], 'b': ['bar', 'baz']}
        """
        if name:
            return {name: self.participants[name].votes}
        else:
            return {k: v.votes for k, v, in self.participants.items()}

    def check_consent(self):
        """Checks if consent is reached and returns a tuple consisting of round, score and a list of winning values.
        If consent is not reached a new round is started and more votes can be cast. In this case it returns the new
        round number and None for score as well as the winning values.
        
        Has to be called every time after a new vote has been added to the list.
        
        Examples:
            - (0, None, None)
            - (1, 1, ['foo', 'bar'])
            - (3, 4, ['bz'])
        """
        if all([participant.has_voted(self.round) for participant in self.participants.values()]):
            intersection = set.intersection(*[set(v.votes) for k, v in self.participants.items()])
            if intersection:
                result = {}
                for ivalue in intersection:
                    result[ivalue] = sum([participant.get_score(ivalue) for participant in self.participants.values()])
                lowest_score = min(result.values())
                best_solution = [k for k in result if result[k] == lowest_score]
                return self.round, lowest_score, best_solution
            else:
                self.round += 1
        return self.round, None, None
