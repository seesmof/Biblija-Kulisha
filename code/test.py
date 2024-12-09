from dataclasses import dataclass


@dataclass
class Change:
    Book: str
    Chapter: int
    Verse: int
    Mistake: str
    Correction: str
    Reason: str


example = "GEN|3|21|коли б|колиб|Extra space"
change_usage = Change(*example.split("|"))
print(change_usage)
