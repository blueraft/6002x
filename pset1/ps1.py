###########################
# 6.00.2x Problem Set 1: Space Cows

from ps1_partition import get_partitions
import time
import operator

#================================
# Part A: Transporting Space Cows
#================================

def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """

    cow_dict = dict()

    f = open(filename, 'r')

    for line in f:
        line_data = line.split(',')
        cow_dict[line_data[0]] = int(line_data[1])
    return cow_dict


# Problem 1
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """

    sorted_cows = sorted(cows.items(), key=operator.itemgetter(1), reverse = True)
    trips = []
    while len(sorted_cows) > 0:
        trip = []
        i = 0
        templimit = limit
        j = 0
        length = len(sorted_cows)
        while j < length:
            cow = sorted_cows[j]
            if cow[1] <= templimit:
                trip.append(cow[0])
                templimit = templimit - cow[1]
                sorted_cows.pop(j)
                j -= 1
                length -= 1
                if len(sorted_cows) == 1:
                    if sorted_cows[0][1] <= templimit:
                        trip.append(sorted_cows[0][0])
                        sorted_cows.pop(j)
                        length -= 1
                        j += 1
            j += 1
        i += 1
        trips.append(trip)

        if i == 50:
            break
    return (trips)


# Problem 2
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """

    sorted_cows = sorted(cows.items(), key=operator.itemgetter(1), reverse = True)
    sorted_cows = [x[0] for x in sorted_cows]
    cow_weights = []
    for cow_sets in (get_partitions(cows)):
        for cow_set in cow_sets:
            total_weight = 0
            for cow in cow_set:
                total_weight += cows[cow]
            if total_weight > limit:
                pass
            else:
                cow_weights.append((cow_set,total_weight))

    sorted_weights = sorted(cow_weights, key=operator.itemgetter(1),reverse = True)
    sorted_weights = [x[0] for x in sorted_weights]
    trips = []
    i =0
    lenght = len(sorted_cows)
    while lenght >= i:
        current_cow = sorted_weights[0]
        sorted_cows = [x for x in sorted_cows if x not in current_cow]
        trips.append(sorted_weights[0])
        for cow in current_cow:
            sorted_weights = [x for x in sorted_weights if cow not in x]
        if len(sorted_cows) == 0:
            break
        i+= 1

    return trips
