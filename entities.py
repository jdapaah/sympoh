"""Entities used in the Project, including a member (cast member, human)
 and a piece (collection of members, associated choreographers)"""
import string
from random import choice, choices
import csv


MemberID = str # Name
PieceID   = str # Piece Number

class Member:
    id: MemberID
    num_want: int
    prefs: list[PieceID] # ordered list, 0-padded
    actual: set[PieceID]

    def __init__(self, id, num_want, prefs) -> None:
        self.id = id
        self.nw = num_want
        self.prefs = prefs
        self.actual = set()

    def __str__(self) -> str:
        return f'{self.id}\n\tPieces: {self.actual}'
    
class Piece:
    # member key rather than object to avoid circular import
    id: PieceID
    choreographers: str
    num_want: tuple[int, int] # range
    actual: set[MemberID]
    # prefs: set[MemberID] # TODO: pain
     
    def __init__(self, id, chor, num_want) -> None:
        self.id = id
        self.nw = num_want
        self.choreographers = chor
        self.actual = set()
    
    def __str__(self) -> str:
        return f'{self.id}\n\tChoreographers: {self.choreographers}\n\tMembers: {self.actual}'
    
    def overlap(self, other):
        return self.actual & other.actual
    
def buildModels():
    members: dict[MemberID, Member] = {}
    piece_map: dict[str, Piece] = {}

    with open('anon-rankings.csv') as r, open('male-names.txt') as b,\
        open('female-names.txt') as g, open('last-names.txt') as l:
        ln = l.readlines()
        fn = b.readlines() + g.readlines()
        memberIDs = set()
        pieceIDs = set()
        reader = csv.reader(r)
        next(reader) # skip the header    
        for line in reader: # for each line in dataset (casting request)
            while (memberID := f'{choice(fn).strip()} {choice(ln).strip()}') in memberIDs:
                continue
            memberIDs.add(memberID)
            prefs = [None] # null padding to make top-k easier to understand
            for piece in line[2:]: # generate list of preferences, generating piece objs along the way
                # note that `piece` string is the choreographer names
                if not piece: # if empty (did not assign a piece to rank i)
                    continue # should be break but i dont trust the data to be contiguous
                if piece not in piece_map: # if new piece
                    # generate new piece id
                    while (pieceID:=''.join(choices(string.digits, k=2))) in pieceIDs:
                        continue
                    pieceIDs.add(pieceID)
                    pieceNum = piece[piece.find("(")+1:piece.find(")")]
                    # generate a new piece obj
                    piece_map[piece] = Piece(id=pieceNum, chor=piece[4:],
                                            num_want=(8, 12)) # create piece obj

                prefs.append(piece_map[piece].id) # add to members prefs
            member = Member(id=memberID, num_want=int(line[1]),
                            prefs=prefs)
            members[memberID] = member
    return members, {obj.id: obj for obj in piece_map.values()}