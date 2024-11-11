from datetime import datetime
from enum import Enum
from threading import Lock
import itertools

# MatchStatus Enum
class MatchStatus(Enum):
    SCHEDULED = "SCHEDULED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    ABANDONED = "ABANDONED"


# Ball Class
class Ball:
    def __init__(self, ball_number, bowler, batsman, result):
        self.ball_number = ball_number
        self.bowler = bowler
        self.batsman = batsman
        self.result = result

    def get_ball_number(self):
        return self.ball_number

    def get_batsman(self):
        return self.batsman

    def get_bowler(self):
        return self.bowler

    def get_result(self):
        return self.result


# Player Class
class Player:
    def __init__(self, id, name, role):
        self.id = id
        self.name = name
        self.role = role


# Team Class
class Team:
    def __init__(self, id, name, players):
        self.id = id
        self.name = name
        self.players = players


# Match Class
class Match:
    def __init__(self, id, title, venue, start_time, teams):
        self.id = id
        self.title = title
        self.venue = venue
        self.start_time = start_time
        self.teams = teams
        self.status = MatchStatus.SCHEDULED

    def get_id(self):
        return self.id

    def set_status(self, status):
        self.status = status

    def get_title(self):
        return self.title


# Scorecard Class
class Scorecard:
    def __init__(self, id, match):
        self.id = id
        self.match = match
        self.team_scores = {}
        self.innings = []

    def update_score(self, team_id, score):
        self.team_scores[team_id] = score

    def add_innings(self, innings):
        self.innings.append(innings)

    def get_id(self):
        return self.id

    def get_match(self):
        return self.match

    def get_team_scores(self):
        return self.team_scores

    def get_innings(self):
        return self.innings


# Innings Class
class Innings:
    def __init__(self, id, batting_team_id, bowling_team_id):
        self.id = id
        self.batting_team_id = batting_team_id
        self.bowling_team_id = bowling_team_id
        self.overs = []

    def add_over(self, over):
        self.overs.append(over)

    def get_id(self):
        return self.id

    def get_overs(self):
        return self.overs

    def get_batting_team_id(self):
        return self.batting_team_id

    def get_bowling_team_id(self):
        return self.bowling_team_id


# Over Class
class Over:
    def __init__(self, over_number):
        self.over_number = over_number
        self.balls = []

    def add_ball(self, ball):
        self.balls.append(ball)

    def get_over_number(self):
        return self.over_number

    def get_balls(self):
        return self.balls


# Cricinfo System Classes

# MatchService Class
class MatchService:
    _instance = None
    _lock = Lock()

    def __init__(self):
        self.matches = {}

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
        return cls._instance

    def add_match(self, match):
        self.matches[match.get_id()] = match

    def get_match(self, match_id):
        return self.matches.get(match_id)

    def get_all_matches(self):
        return list(self.matches.values())

    def update_match_status(self, match_id, status):
        match = self.get_match(match_id)
        if match:
            match.set_status(status)


# ScorecardService Class
class ScorecardService:
    _instance = None
    _lock = Lock()

    def __init__(self):
        self.scorecards = {}
        self.scorecard_id_counter = itertools.count(1)

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
        return cls._instance

    def create_scorecard(self, match):
        scorecard_id = self._generate_scorecard_id(match.get_id())
        scorecard = Scorecard(scorecard_id, match)
        self.scorecards[scorecard_id] = scorecard

    def get_scorecard(self, scorecard_id):
        return self.scorecards.get(scorecard_id)

    def update_score(self, scorecard_id, team_id, score):
        scorecard = self.get_scorecard(scorecard_id)
        if scorecard:
            scorecard.update_score(team_id, score)

    def add_innings(self, scorecard_id, innings):
        scorecard = self.get_scorecard(scorecard_id)
        if scorecard:
            scorecard.add_innings(innings)

    def _generate_scorecard_id(self, match_id):
        scorecard_id = next(self.scorecard_id_counter)
        return f"SC-{match_id}-{scorecard_id:04d}"


# CricinfoSystem Class
class CricinfoSystem:
    def __init__(self):
        self.match_service = MatchService.get_instance()
        self.scorecard_service = ScorecardService.get_instance()

    def add_match(self, match):
        self.match_service.add_match(match)

    def get_match(self, match_id):
        return self.match_service.get_match(match_id)

    def get_all_matches(self):
        return self.match_service.get_all_matches()

    def update_match_status(self, match_id, status):
        self.match_service.update_match_status(match_id, status)

    def create_scorecard(self, match):
        self.scorecard_service.create_scorecard(match)

    def get_scorecard(self, scorecard_id):
        return self.scorecard_service.get_scorecard(scorecard_id)

    def update_score(self, scorecard_id, team_id, score):
        self.scorecard_service.update_score(scorecard_id, team_id, score)

    def add_innings(self, scorecard_id, innings):
        self.scorecard_service.add_innings(scorecard_id, innings)


# CricinfoDemo Class
class CricinfoDemo:
    @staticmethod
    def run():
        # Create teams
        team1_players = [
            Player("P101", "Player 1", "Batsman"),
            Player("P102", "Player 2", "Bowler"),
            Player("P103", "Player 3", "All-rounder")
        ]
        team2_players = [
            Player("P201", "Player 4", "Batsman"),
            Player("P202", "Player 5", "Bowler"),
            Player("P203", "Player 6", "All-rounder")
        ]
        team1 = Team("T1", "Team 1", team1_players)
        team2 = Team("T2", "Team 2", team2_players)
        teams = [team1, team2]

        # Create a match
        match = Match("M001", "Match 1", "Venue 1", datetime.now(), teams)

        # Create Cricinfo system
        cricinfo_system = CricinfoSystem()

        # Add the match to the system
        cricinfo_system.add_match(match)

        # Create a scorecard for the match
        cricinfo_system.create_scorecard(match)

        # Get the scorecard
        scorecard_id = "SC-M001-0001"
        scorecard = cricinfo_system.get_scorecard(scorecard_id)

        # Update scores
        cricinfo_system.update_score(scorecard_id, "T1", 100)
        cricinfo_system.update_score(scorecard_id, "T2", 75)

        # Create innings
        innings1 = Innings("I1", "T1", "T2")
        innings2 = Innings("I2", "T2", "T1")

        # Add overs to innings
        over1 = Over(1)
        over1.add_ball(Ball(1, "P202", "P101", "4"))
        over1.add_ball(Ball(2, "P202", "P101", "6"))
        innings1.add_over(over1)

        over2 = Over(2)
        over2.add_ball(Ball(1, "P102", "P201", "1"))
        over2.add_ball(Ball(2, "P102", "P201", "0"))
        innings1.add_over(over2)

        # Add innings to the scorecard
        cricinfo_system.add_innings(scorecard_id, innings1)
        cricinfo_system.add_innings(scorecard_id, innings2)

        # Get the updated scorecard
        updated_scorecard = cricinfo_system.get_scorecard(scorecard_id)

        # Display the scorecard
        print("Scorecard ID:", updated_scorecard.get_id())
        print("Match:", updated_scorecard.get_match().get_title())
        print("Team Scores:")
        for team_id, score in updated_scorecard.get_team_scores().items():
            print(f"{team_id}: {score}")
        print("Innings:")
        for innings in updated_scorecard.get_innings():
            print("Innings ID:", innings.get_id())
            print("Batting Team:", innings.get_batting_team_id())
            print("Bowling Team:", innings.get_bowling_team_id())
            print("Overs:")
            for over in innings.get_overs():
                print("Over", over.get_over_number())
                for ball in over.get_balls():
                    print(f"Ball {ball.get_ball_number()}: {ball.get_bowler()} to {ball.get_batsman()} - {ball.get_result()}")
                print()


# Run the Demo
if __name__ == "__main__":
    CricinfoDemo.run()
