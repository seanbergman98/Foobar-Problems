def isBetter(next_sol, sol):

    #Method to check if a given set of saved bunnies is better than another set of saved bunnies, with both sets already ordered

    if len(next_sol) > len(sol):
        return True
    elif len(sol) > len(next_sol):
        return False
    
    for i in range(len(next_sol)):

        if next_sol[i] < sol[i]:
            return True
        elif sol[i] < next_sol[i]:
            return False
    
    return False

def saveBunnies(shortest_edges, current_location, saved_bunnies, remaining_bunnies, time_remaining):
    
    solution = saved_bunnies[:]

    #Iterate through all possible paths we can take
    for next_bunny in remaining_bunnies:

        #Check to see if we can rescue this bunny
        if shortest_edges[current_location][next_bunny + 1] + shortest_edges[next_bunny + 1][len(shortest_edges) - 1] <= time_remaining:
            
            next_saved_bunnies = saved_bunnies[:]
            next_saved_bunnies.append(next_bunny)
            next_saved_bunnies.sort()

            next_remaining_bunnies = remaining_bunnies[:]
            next_remaining_bunnies.remove(next_bunny)

            next_time_remaining = time_remaining - shortest_edges[current_location][next_bunny + 1]

            next_solution = saveBunnies(shortest_edges, next_bunny + 1, next_saved_bunnies, next_remaining_bunnies, next_time_remaining)

        else:
            next_solution = saved_bunnies[:]

        if isBetter(next_solution, solution):
            solution = next_solution[:]

    return solution
        





def isShorterPath(predecessor_node_dist, final_node_dist, edge_dist):

    #Check whether the path to vertex 2 through vertex 1 is a shorter path than the current shortest path

    if predecessor_node_dist == 'inf':
        return False
    elif final_node_dist == 'inf':
        return True

    elif (predecessor_node_dist + edge_dist) < final_node_dist:
        return True
    else:
        return False


def bellmanFord(times, source):

    #Return the array of shortest path times from the node source to each other node

    shortest_dist = ['inf']*len(times)

    #The shortest distance from the source node to itself should just be 0
    shortest_dist[source] = 0

    #The index i is never referenced, just used to provide the number of nodes - 1 iterations
    for i in range(len(times) - 1):


        #Iterate through all edges between nodes
        for j in range(len(times)):

            for k in range(len(times[j])):
                    
                if isShorterPath(shortest_dist[j], shortest_dist[k], times[j][k]):
                    
                    shortest_dist[k] = shortest_dist[j] + times[j][k]
    
    #The above algorithm should give us our array of shortest path times from the source node to each other node, provided no
    #negative cycles exist

    #Lastly, check to see if any negative cycles do exist by checking to see if any distances can still be made shorter
    for j in range(len(times)):

        for k in range(len(times[j])):

            if j != k:

                if isShorterPath(shortest_dist[j], shortest_dist[k], times[j][k]):
                    return [-1] * len(times)

    return shortest_dist


def solution(times, times_limit):

    num_bunnies = len(times) - 2

    shortest_dist = []

    for i in range(len(times)):
        
        next_row = bellmanFord(times,i)

        #If there exists any negative cycle, we can run this cycle for as long as we need to save all the bunnies
        if next_row == [-1]*len(times):
            return list(range(num_bunnies))

        shortest_dist.append(next_row)

    saved_bunnies = []
    remaining_bunnies = list(range(num_bunnies))
    
    saved_bunnies = saveBunnies(shortest_dist, 0, saved_bunnies, remaining_bunnies, times_limit)

    return saved_bunnies

