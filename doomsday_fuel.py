from fractions import Fraction
from math import gcd

def zeroes(m,n):

    #Create an m x n array of zeroes

    A = []
    
    for i in range(m):
        A.append([0]*n)

    return A

def subtract_Rows(r1, r2):
    
    #Returns the difference of the array r1 minus the array r2
    #subtracted element-wise
    
    diff = r1[:]
    
    for i in range(len(diff)):
        diff[i] -= r2[i]
        
    return diff
        
def solve(A,b):
    
    #Solves the augmented matrix A|b for the terminal probability
    #distributions starting from each of the non-terminal states
    
    this_A = A[:]
    this_b = b[:]
        
    #Proceed column by column
    for i in range(len(this_A)):
            
        #Check to see if the pivot is equal to 0, and swap two
        #rows if so
        if this_A[i][i] == 0:
                
            for j in range(i+1, len(this_A)):
                
                if this_A[j][i] != 0:
                    bufferRow_A = this_A[i]
                    this_A[i] = this_A[j]
                    this_A[j] = bufferRow_A
                    
                    bufferRow_b = b[i]
                    this_b[i] = this_b[j]
                    this_b[j] = bufferRow_b
                    
                    break
        
        #Change the pivot to 1 by multiplying the entire row    
        
        bufferConstant = Fraction(this_A[i][i].denominator, this_A[i][i].numerator)
        
        this_A[i] = [x*bufferConstant for x in this_A[i] ]
        this_b[i] = [x*bufferConstant for x in this_b[i] ]
        
        #Subtract multiples of the ith row from each of the lower
        #rows to produce leading zeroes
        for j in range(i+1, len(this_A)):
            
            bufferConstant = this_A[j][i]
            
            this_A[j] = subtract_Rows(this_A[j], [x*bufferConstant for x in this_A[i] ])
            this_b[j] = subtract_Rows(this_b[j], [x*bufferConstant for x in this_b[i] ])
        
    #Now erase all non-zero entries above our pivots
    for i in reversed(range(len(this_A))):
            
        for j in reversed(range(i)):
            
            bufferConstant = this_A[j][i]
            
            this_A[j] = subtract_Rows(this_A[j], [x * bufferConstant for x in this_A[i] ])
            this_b[j] = subtract_Rows(this_b[j], [x * bufferConstant for x in this_b[i] ])
            
    return this_b[0]       
    
    
def solution(m):
    
    #Create our transition matrix P by converting the input matrix m
    #into a matrix where the element P[i][j] represents the transition
    #probability of the matter going from state i to state j
    
    #The array terminalStates keeps track of our terminal states
    terminalStates = []
    P = zeroes(len(m),len(m))
    
    for i in range(len(m)):
        
        if m[i] == [0]*len(m):
            
            #Add the index i to our list of terminal states, and
            #reformat the ith row for creating our transition
            #matrix P
            terminalStates.append(i)
            m[i][i] = 1
        
        for j in range(len(m)):
            
            P[i][j] = Fraction(m[i][j], sum(m[i]))
    
    #Check to see if the initial state 0 is a terminal state
    if 0 in terminalStates:
        finalProb = [0]*len(terminalStates)
        finalProb[0] = 1
        finalProb.append(1)
        
        return finalProb
    
    A = zeroes(len(m)-len(terminalStates), len(m) - len(terminalStates))
    b = zeroes(len(m) - len(terminalStates), len(m))
    
    rowIndex = 0
    for i in range(len(m)):
        
        if i not in terminalStates:
            
            columnIndex = 0
            for j in range(len(m)):
                
                if j not in terminalStates:
                    
                    if j == i:
                        A[rowIndex][columnIndex] = 1 - P[i][j]
                    else:
                        A[rowIndex][columnIndex] = -P[i][j]
                    
                    columnIndex += 1
                    
                else:
                    b[rowIndex][j] = P[i][j]
            
            rowIndex += 1
            
    finalProb = solve(A,b)
    
    finalProb = [finalProb[x] for x in terminalStates]
    
    lcm = finalProb[0].denominator
    for i in range(1,len(finalProb)):
        lcm = (lcm*finalProb[i].denominator)//gcd(lcm,finalProb[i].denominator)
    
    finalProb = [x.numerator*lcm//x.denominator for x in finalProb]
    finalProb.append(lcm)
    
    ans = [0]*len(terminalStates)
    
    ans[0] = 1
    ans.append(1)
    
    print(ans)

    return ans
