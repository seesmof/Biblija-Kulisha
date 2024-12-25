from dataclasses import dataclass


@dataclass
class BibleReference:
    Book:str
    Chapter:int
    Verse:int

@dataclass
class ChangeEntry(BibleReference):
    Mistake:str
    Correction:str
    Reason:str

@dataclass
class TypoEntry(BibleReference):
    Contents:str