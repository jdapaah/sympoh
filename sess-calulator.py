import csv

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

def general_stats(database):
    pass

def main():
    f = open('sess.csv')
    reader = csv.reader(f)
    reader.__next__() # header
    reader.__next__() # header
    database = {}
    for row in reader:
        database[row[0]] = ind_stats(row)
    while 1:
        try:
            print(k, v for database[input("Member: ")].items())
        except KeyError:
            print('Misspelled Name/ Not found')
    f.close()

if __name__ == '__main__':
    main()
