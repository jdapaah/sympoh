#!/usr/local/bin/python3
import csv
from sys import argv

# TODO: update the 13 to account for cycle 4
def ind_stats(row):
    def clean(temp):
        for i in range(0,4,2): # sess
            temp[i] = int(temp[i]) # convert sess to
        for i in range(1,4,2): # company
            temp[i] = int(bool(temp[i])) # convert sess to
        return temp
    cycles = [ clean(row[start:start+4]) for start in range(1, 13, 5) ]
    
    stats = {}
    stats['number of sess'] = sum([sum(c[0::2]) for c in cycles])
    stats['number of companies'] = sum([sum(c[1::2]) for c in cycles])
    stats['cycle raw data'] = cycles
    return stats

def main():
    try:
        f = open(argv[1])
    except (FileNotFoundError, IndexError):
        f = open('raw-sess.csv')

    reader = csv.reader(f)
    reader.__next__() # header
    reader.__next__() # header
    database = {}
    for row in reader:
        database[row[0]] = ind_stats(row)
    while 1:
        try:
            key = input("Member: ") 
            if key.title().startswith(("*Top", '*Bottom')):
                try:
                    k = int(key.split()[-1])
                except ValueError:
                    print('no number given')
                top = key.title().startswith("**Top")
                ranked = sorted(database, key=lambda mem: database[mem]['number of sess'], reverse=top)[:k]
                print({t: database[t]['number of sess'] for t in ranked})
            else:
                for k, v in database[key].items():
                    print(f"{k}: {v}")
        except KeyError:
            print('Misspelled Name/ Not found')
        except KeyboardInterrupt:
            break
    f.close()

if __name__ == '__main__':
    main()
