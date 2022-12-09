import copy
import os
import colorama
import networkx as nx
import matplotlib.pyplot as plt; plt.ion
import netgraph



"""
easy
row1=[" "," ","3"," ","2"," ","6"," "," "]
row2=["9"," "," ","3"," ","5"," "," ","1"]
row3=[" "," ","1","8"," ","6","4"," "," "]
row4=[" "," ","8","1"," ","2","9"," "," "]
row5=["7"," "," "," "," "," "," "," ","8"]
row6=[" "," ","6","7"," ","8","2"," "," "]
row7=[" "," ","2","6"," ","9","5"," "," "]
row8=["8"," "," ","2"," ","3"," "," ","9"]
row9=[" "," ","5"," ","1"," ","3"," "," "]

AI?
"""
row1=[" "," "," ","7"," "," ","8"," "," "]
row2=[" "," ","6"," "," "," "," ","3","1"]
row3=[" ","4"," "," "," ","2"," "," "," "]
row4=[" ","2","4"," ","7"," "," "," "," "]
row5=[" ","1"," "," ","3"," "," ","8"," "]
row6=[" "," "," "," ","6"," ","2","9"," "]
row7=[" "," "," ","8"," "," "," ","7"," "]
row8=["8","6"," "," "," "," ","5"," "," "]
row9=[" "," ","2"," "," ","6"," "," "," "]

"""
expert
row1=[" "," ","5","6"," ","2"," "," "," "]
row2=["7"," "," ","8","1"," ","4"," "," "]
row3=[" "," "," "," "," "," ","5","6"," "]
row4=[" ","4","9"," "," "," "," "," "," "]
row5=["8"," "," "," "," "," "," "," ","7"]
row6=[" "," "," "," ","5","1"," "," "," "]
row7=[" "," "," ","9","4"," ","8"," ","2"]
row8=["3"," ","6","1"," "," "," "," "," "]
row9=[" "," "," "," "," "," "," "," "," "]
"""
rows=[row1,row2,row3,row4,row5,row6,row7,row8,row9]
potentialSolutions=copy.deepcopy(rows)


colorama.init()
def put_cursor(x,y):
    print ("\x1b[{};{}H".format(y+1,x+1))

def clear():
    print ("\x1b[2J")

def printGrid():
    #print("\n\n")
    #os.system('clear')
    put_cursor(0,0)
    for i in range(9):
        if i%3==0:
            print("-"*13)
        for j in range(9):
                if j%3==0:
                    print("|", end="")
                print(rows[i][j], end="")

        print("|")
    print("-"*13)

def rowContainsNumber(row, number):
    return number in row

def columnContainsNumber(colNumber, number):
    for row in rows:
        if row[colNumber]==number:
            return True

    return False

def squareContainsNumber(rowNumber, colNumber, number):
    baseRow=((rowNumber//3)*3)
    baseCol=((colNumber//3)*3)
    rowsInSquare=[rows[baseRow], rows[baseRow+1],rows[baseRow+2]]
    colsInSquare=[baseCol, baseCol+1, baseCol+2]
    for row in rowsInSquare:
        for col in colsInSquare:
            if row[col] == number:
                return True
    return False


def gridComplete():
    for row in rows:
        if " " in row:
            return False
    print("solved!")
    return True

def simpleSolve():
    stuckInLoop = False
    lastSolved = (8,8)
    
    while not stuckInLoop:
        gridSquareCounter=1
        for rowNumber in range(9):
            row = rows[rowNumber]

            for colNumber in range(9):
                gridsquare = row[colNumber]
                
                    
                #if gridsquare is empty let's see if we can find a solution
                if gridsquare == " ":
                    solutions=[]
                    for number in range(1,10):
                        number = str(number)
                        if not rowContainsNumber(row, number) and not columnContainsNumber(colNumber, number) and not squareContainsNumber(rowNumber, colNumber, number):
                            solutions.append(number)
                    if len(solutions)==1:
                        row[colNumber] = solutions[0]
                        potentialSolutions[rowNumber][colNumber]=solutions[0]
                        lastSolved = (rowNumber, colNumber)
                    else:
                        potentialSolutions[rowNumber][colNumber]=solutions
                gridSquareCounter = gridSquareCounter + 1
                if gridSquareCounter>81:
                    if gridComplete():
                        return True
                    else:
                        return False

def isSolveImpossible():
    for row in potentialSolutions:
        for col in row:
            if type(col)==list and len(col)==0:
                return True
    return False


def getUnsolvedGridSquare(rowsToCheck, maxNoOfSolutions):
    for row in range(9):
        for col in range(9):
            
            gridsquare=rowsToCheck[row][col]
            if type(gridsquare)==list and len(gridsquare)<=maxNoOfSolutions:
                return gridsquare, row, col

G=nx.Graph()
nodes=[]
counter=0
def complexSolve(n, parentNode):
    global potentialSolutions
    global rows
    solutions, row, col = getUnsolvedGridSquare(potentialSolutions,n)

    

    for solution in solutions:
        global counter
        currentNode=str(counter) + ")" + str(row) + "," + str(col) + ":" + solution
        counter = counter+1
        G.add_node(currentNode)
        if parentNode != None:
            G.add_edge(parentNode, currentNode)


        printGrid()
        #print("trying solution:",solution,"at gridsquare",str(row),str(col))
        #save copies of the rows and potential solutions incase we go down a dead end and need to revert to a previous state
        potentialSolutionsCopy = copy.deepcopy(potentialSolutions)
        rowsCopy = copy.deepcopy(rows)

        rows[row][col]=solution
        potentialSolutions[row][col]=solution
        if simpleSolve():
            print("solution found")
            printGrid()
            return True
        else:
            #our simple solve attempt above will fill the grid with the best attempt at a solution, but it might be wrong or a deadend
            #if solve is impossible after a simple solve attempt, we need to revert our board state to what it was before the simple solve
            #and then continue with the next number in the list
            if isSolveImpossible():
                rows = copy.deepcopy(rowsCopy)
                potentialSolutions = copy.deepcopy(potentialSolutionsCopy)
                continue
            else:
                #simple solve produced a new grid which is not impossible to solve, but not yet solved, so we must have grid squares with multiple potential solutions still
                #lets recurse and iterate the remaining potential solutions
                if complexSolve(n,currentNode)==False:
                    #if complex solve returns false (see return False below) it means that the complex Solve call has gone down a dead end and cannot find a solution with any of its potential solutions
                    #therefore we must have an incorrect solution inputted at this level. So let's revert our grid to the previously saved state, and try the next possible solution
                    rows = copy.deepcopy(rowsCopy)
                    potentialSolutions = copy.deepcopy(potentialSolutionsCopy)
                    continue
                else:
                    #return true here if complex solve worked 
                    return True


    if not simpleSolve():
        #if we have iterated all the potential solutions for the current grid square, but we still cannot simple solve
        #then the previous gridsquare must have an incorrect potential solution, therefore return False so that the recursing function knows this was incorrect
        return False     
    else:
        return True

clear()
printGrid()

if not simpleSolve():
    printGrid()
    complexSolve(2,None)

#nx.draw(G,with_labels=True)
pos = nx.layout.spring_layout(G)
plot_instance = netgraph.InteractiveGraph(G, node_positions=pos,node_labels=G.nodes)
node_positions = plot_instance.node_positions

plt.savefig("path_graph1.png")
plt.show()
