import csv, place


def apsp(g):
    '''All-Pairs Shortest Paths using the Floyd-Warshall algorithm.'''
    '''DO NOT CHANGE'''

    INFINITE = 2 ** 63 - 1  # a really big number (the biggest int for a 64-bit machine)

    # Initialize paths with paths for adjacent nodes
    paths = [[0 for j in range(len(g))] for i in range(len(g))]
    for i in range(len(g)):
        for j in range(len(g)):
            if g[i][j] != 0:
                paths[i][j] = [i, j]  # if two places are already adjacent then assign an initial path to them
            elif i != j:  # i == j means this is the same place so distance is zero
                g[i][j] = INFINITE  # replacing zero by an "infinite" value
                # zero earlier meant that two places are not connected, now it will mean that they are not connected
                # initially, meaning that are "very-very" far ("virtually", for the sake of initialization)

    # apsp computation - floyd-warshall algorithm
    for k in range(len(g)):  # (for each) vertex k, to compare if i--k + k--j is shorter than i--j computed so far
        for i in range(len(g)):  # (for each) vertex i of our interest
            for j in range(len(g)):  # (for each) vertex j, to get the computed distance so far (between i and j)
                if g[i][j] > g[i][k] + g[k][j]:  # determining if there is a shorter path (as per the above comment)
                    g[i][j] = g[i][k] + g[k][j]  # updating the path-length value if there is a shorter path

                    # updating the path itself if there is a shorter path
                    paths[i][j] = paths[i][k][:]
                    paths[i][j].extend(paths[k][j][1:])

    # if a pair of places are still at infinite distance,
    # then assign them 0, to declare that they are not connected
    for i in range(len(g)):
        for j in range(len(g)):
            if g[i][j] == INFINITE:
                g[i][j] = 0

    return g, paths


def open_file():
    ''' Opens the file and checks directory if a file is there if not displays error message'''
    file = True
    while file == True:  # Creates initial boolean to tell if file is correct
        txt = input('Enter the file name: ')
        try:  # initates loop to check if true
            fp = open(txt)
            return fp
        except FileNotFoundError:  # creates a invalid output if filenotfound error pops up
            print('\nFile not found.! Try again.')


def read_file(fp):
    '''DocString'''
    reader = csv.reader(fp)
    fp.readline()
    row_list = []
    for i in fp:
        if i[-1:] == '\n':
            row = i[:-1].split(',')
        else:
            row = i.split(',')
        if row[2] == '':
            rows = (row[0], row[1], 0)
        else:
            rows = (row[0], row[1], int(row[2]))

        row_list.append(rows)
    fp.close()
    return row_list


def adjacency_matrix(L):
    '''DocString'''
    places_set = set()
    for i in L:
        places_set.add(i[0])
        places_set.add(i[1])
    places_set = sorted(places_set)
    places_lst = places_set
    g = []
    for i in range(len(places_lst)):
        n = len(places_lst)
        g.append([0] * n)
    for x in L:
        city1 = places_lst.index(x[0])
        city2 = places_lst.index(x[1])
        g[city2][city1] = x[2]
        g[city1][city2] = x[2]
    return places_lst, g


def make_objects(places_lst, g):
    '''DocString'''
    id = dict()
    name = dict()
    g,paths = apsp(g)
    count = -1
    for i in places_lst:
        count += 1
        a_place = place.Place(i,str(count))
        a_place.set_distances(g)
        a_place.set_paths(paths)
        name[i] = a_place
        id[count] = a_place
    return name, id


def main():
    BANNER = '\nBegin the search!'
    fp = open_file()
    master_list = read_file(fp)
    places_lst, g = adjacency_matrix(master_list)
SUBMITTED BY
Chris Swiecicki
CREATED AT
12/8/2021 11:57 PM
DUE DATE
12/8/2021 11:59 PM

LATE DAYS
1 (50%/day)
SUBMISSION HISTORY
    name,id = make_objects(places_lst, g)
    print(BANNER)
    usr_inp = input("Enter starting place, enter 'q' to quit: ")
    route_lst = []
    route_lst.append(usr_inp)

    while usr_inp != 'q' or 'Q':
        while usr_inp not in places_lst:
            print('This place is not in the list!')
            usr_inp = input("Enter starting place, enter 'q' to quit: ")

        if usr_inp in places_lst:

            next_dest = input('Enter next destination, enter "end" to exit: ')
            if next_dest == 'q' or 'Q':
                break
            if next_dest not in places_lst:
                print('This destination is not valid or is the same as the previous destination!')
                next_dest = input('Enter next destination, enter "end" to exit: ')
            elif next_dest == route_lst[:-1]:
                print('This destination is not valid or is the same as the previous destination!')
                next_dest = input('Enter next destination, enter "end" to exit: ')
            while next_dest != 'end':
                if next_dest not in places_lst:
                    print('This destination is not valid or is the same as the previous destination!')
                    next_dest = input('Enter next destination, enter "end" to exit: ')
                elif next_dest == route_lst[:-1]:
                    print('This destination is not valid or is the same as the previous destination!')
                    next_dest = input('Enter next destination, enter "end" to exit: ')
                else:
                    route_lst.append(next_dest)
                    next_dest = input('Enter next destination, enter "end" to exit: ')
        count = -1
        distance = 0
        error = False
        path_taken = []
        errors = []
        for i in route_lst[:-1]:
            count += 1
            destination = route_lst[count + 1]
            dest_index = name[destination].get_index()
            path = name[route_lst[count]].get_path(dest_index)
            if path != 0:
                path_distance = name[route_lst[count]].get_distance(dest_index)
                distance += path_distance
                path_taken.append(path)
            elif path == 0:
                error_tup = (route_lst[count],destination)
                errors.append(error_tup)
                error = True
        if error == True:
            for y in errors:
                print('places {} and {} are not connected.'.format(error_tup[0],error_tup[1]))
                errors.pop(0)
                error = False

        else:
            print("Your route is:")
            places = []
            for z,t in enumerate(path_taken):
                if z != 0:
                    places += t[1:]
                else:
                    places += t
            for l in places:
                city = id[l].get_name()
                print("     {}".format(city))
            print("Total distance = {}".format(str(distance)))
        print(BANNER)
        route_lst = []
    print('Thanks for using the software')


if __name__ == '__main__':
    main()
