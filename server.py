#!/usr/local/bin/python3

# Std Library Imports
import pickle
from random import choices
import sys
import string

# Project Imports
from entities import Member, MemberID, Piece, PieceID, buildModels

sympeeps: dict[MemberID, Member]
pieces: dict[PieceID, Piece]

"""Paginated list of Sympoh Members"""
def Names():
    for i, el in enumerate(sympeeps):
        print(el, end=', ')
        if i % 10 == 4:
            print()
        if i % 10 == 9:
            if input() == 'x':
                return
            print('----------------------------------')
            

"""List of all the pieces"""
def Pieces():
    for id, obj in pieces.items():
        print(f'{id}: {obj.choreographers}')

def addRemove(command, mID: MemberID, pID: PieceID):
    mID = mID.title()
    if mID not in sympeeps:
        print('Member does not exist')
        return
    if pID not in pieces:
        print('Piece with id does not esxist')
        return
    if command == 'Add':
        return add(mID, pID)
    if command == 'Remove':
        return remove(mID, pID)

def add(mID: MemberID, pID: PieceID):
    # global sympeeps, pieces
    member = sympeeps[mID]
    if pID in member.actual:
        print(f'{mID} already in {pID}')
        return
    member.actual.add(pID) # TODO: confirm global
    piece = pieces[pID]
    piece.actual.add(mID)

def remove(mID: MemberID, pID: PieceID):
    try:
        member = sympeeps[mID]
        member.actual.remove(pID) # TODO: confirm global
        piece = pieces[pID]
        piece.actual.remove(mID)
    except KeyError:
        print(f'{mID} not in cast {pID}')
        return

def viewPiece(pieceID: PieceID):
    print(pieces.get(pieceID, 'No such piece'))

def viewMember(mID: MemberID):
    print(sympeeps.get(mID, 'Member does not exist'))

def Clear():
    for member in sympeeps.values():
        member.actual.clear()
    for piece in pieces.values():
        piece.actual.clear()
    
def PlaceK(k: int):
    assert 0 < k <= len(pieces)
    Clear()
    for mID, member in sympeeps.items():
        add(mID, member.prefs[k])

def proccessInput(args: str):
    if not args.strip(): # Empty list
        return
    command, _, args = args.partition(' ')
    command = command.capitalize()
    if command == 'Names':
        Names()
    elif command == 'Pieces':
        Pieces()
    elif command in ['Add', 'Remove']:
        try:
            # args = ['first last', pieceID]
            addRemove(command, *args.rsplit(maxsplit=1))
        except TypeError: # missing args
            print(f"Bad {command}, missing args")
    elif command == 'View':
        try:
            if args.isdigit():
                viewPiece(args)
            else:
                viewMember(args.title())
        except TypeError:
            print(f"Bad View, missing args")
    elif command == 'Placek':
        if len(args) != 1 or not args[0].isdigit():
            print('Bad PlaceK args')
            return
        k = int(args[0])
        PlaceK(k)
    elif command == 'Clear':
        if input("Clear the current experiment? (type 'Yes')") == 'Yes':
            Clear()
    else:
        print('Invalid Command')
        return

if __name__ == '__main__':
    try: # open file
        with open(sys.argv[1], 'rb') as f:
            sympeeps, pieces = pickle.load(f)
        # TODO: confirm that this updates global state.
    except IndexError or FileNotFoundError: # If no file given or given file doesn't exist 
        # build model from scratch
        print('Initializing New Dataset')
        sympeeps, pieces = buildModels()
    try:
        while 1:
            proccessInput(input('* : '))
    except KeyboardInterrupt: # on exit
        pass
        # save to a new file with random suffix to avoid overwrite of other experiments
    while 1:
        try:
            filepath = 'data' 
            suffix = ''.join(choices(string.ascii_uppercase, k=4))
            with open(f'{filepath}/{suffix}.pkl', 'xb') as d,\
            open(f'{filepath}/names.{suffix}.txt', 'w') as n,\
            open(f'{filepath}/casts.{suffix}.txt', 'w') as c:
                pickle.dump((sympeeps, pieces), d)
                for x in sympeeps:
                    n.write(f'{x}\n')
                for x in pieces.values():
                    c.write(f'{x.id, x.choreographers}\n')
            print('State saved, Suffix is', suffix)
            break
        except FileExistsError:
            continue