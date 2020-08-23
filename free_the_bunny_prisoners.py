def swap(dist, n1, n2):

    #Swaps all instances of the key n1 for instances of the key n2 in the key distribution dist while maintaing numerical
    #left to right order in each row

    swapped_dist = [x[:] for x in dist]

    for i in range(len(swapped_dist)):

        for j in range(len(swapped_dist[i])):

            if swapped_dist[i][j] == n1:

                swapped_dist[i][j] = n2

            elif swapped_dist[i][j] == n2:
                
                swapped_dist[i][j] = n1

    for i in range(len(swapped_dist)):
        swapped_dist[i].sort()

    return swapped_dist

def least(dist):

    #Rearranges the key distribution dist into the lexicographically least equivalent distribution

    #Create a duplicate of the input dist
    leastDist = [x[:] for x in dist]
    
    #Minimize dist iterating first through rows
    for i in range(len(leastDist)):
        
        nextKey = 0

        #Then iterating through columns
        for j in range(len(leastDist[i])):

            while nextKey < leastDist[i][j]:

                canSwap = True

                #Check that swapping the values of the next least key and the current entry will not affect the least ordering
                #of the above rows
                for k in range(i):
                    
                    if (nextKey in leastDist[k]) ^ (leastDist[i][j] in leastDist[k]):
                        canSwap = False
                        break
                
                if canSwap:
                    leastDist = swap(leastDist, nextKey, leastDist[i][j])
                    break
                else:
                    nextKey += 1

            nextKey = leastDist[i][j] + 1

    return leastDist







def numKeys(dist):

    #Returns the number of distinct keys for given key distribution

    distinctKeys = []
    count = 0

    for x in dist:

        for y in x:

            if y not in distinctKeys:
                distinctKeys.append(y)
                count += 1
            
    return count



def keyDistribution(num_buns, num_required):
    
    dist = []

    #Base cases if the # of required bunnies is 0 or the # of required bunnies is equal to the total # of bunnies
    if num_required == 0:
        for i in range(num_buns):
            dist.append([])
        return dist

    elif num_buns == num_required:
        for i in range(num_buns):
            dist.append([i])

        return dist

    dist1 = keyDistribution(num_buns - 1, num_required - 1)
    dist2 = keyDistribution(num_buns - 1, num_required)

    dist1_keys = numKeys(dist1)
    dist2_keys = numKeys(dist2)

    #Add to the keys in dist2 such that dist1 and dist2 have no common keys
    for i in range(len(dist2)):
        for j in range(len(dist2[i])):
            dist2[i][j] = dist2[i][j] + dist1_keys
    
    for i in range(num_buns - 1):
        dist.append(list( set(dist1[i]) | set(dist2[i])))

    dist.append([i for i in range(dist1_keys, dist1_keys + dist2_keys)])

    dist = least(dist)

    return dist
    

def solution(num_buns, num_required):

    keyDist = keyDistribution(num_buns, num_required)

    return keyDist
