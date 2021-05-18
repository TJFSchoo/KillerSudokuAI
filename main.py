import time

# Time snapshot
startTime = time.time()

# Sudoku grid to be filled in
solutionGrid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# Killer cage grid
# Source: https://www.theguardian.com/lifeandstyle/2020/jan/12/observer-killer-sudoku
killerSudokuGrid = [
    [9, 15, 15, 18, 14, 8, 8, 27, 10],
    [9, 23, 15, 18, 14, 14, 27, 27, 10],
    [23, 23, 15, 18, 18, 15, 27, 23, 10],
    [14, 23, 17, 17, 17, 15, 15, 23, 23],
    [14, 21, 20, 20, 17, 15, 9, 14, 14],
    [21, 21, 20, 19, 19, 20, 9, 14, 25],
    [21, 13, 10, 10, 19, 20, 19, 14, 25],
    [13, 13, 13, 10, 20, 20, 19, 19, 25],
    [22, 22, 22, 17, 17, 17, 3, 3, 25]
]

# Function to solve solution based on provided killer grid
def solve(grid, killerGrid):
    foundEmptySquare = findEmpty(grid)
    if not foundEmptySquare:
        # No blank spaces means the Sudoku is solved
        print("Finished. Total runtime: " + str(round(time.time() - startTime)) + " seconds")
        return True
    else:
        row, col = foundEmptySquare
    for i in range(1, 10):
        if checkValidity(grid, i, (row, col), killerGrid):
            grid[row][col] = i
            if solve(grid, killerGrid):
                return True
            grid[row][col] = 0
    return False

# Function providing constraint satisfaction
def checkValidity(board, numberFilledIn, position, killerGrid):
    print("Runtime: " + str(round(time.time() - startTime)) + " seconds, board: " + str(solutionGrid))

    # Baby-step 1: Horizontal constraint [1-9 may only appear once per row]
    for i in range(len(board[0])):
        if board[position[0]][i] == numberFilledIn and position[1] != i:
            return False

    # Baby-step 2: Vertical constraint [1-9 may only appear once per column]
    for i in range(len(board)):
        if board[i][position[1]] == numberFilledIn and position[0] != i:
            return False

    # Baby-step 3: Square constraint [1-9 may only appear once per 3x3 square]
    squareX = position[1] // 3
    squareY = position[0] // 3

    for i in range(squareY * 3, squareY * 3 + 3):
        for j in range(squareX * 3, squareX * 3 + 3):
            if board[i][j] == numberFilledIn and (i, j) != position:
                return False

    # Not-so-baby-step: Killer constraint [Must obey killerGrid cage-values]
    cageValue = killerGrid[position[0]][position[1]]
    killerCage = findKillerCageFriends(board, killerGrid, cageValue, position, [(-1, -1)], "none")

    # If squares related to killer-cage are not completely filled in yet before the last cage-square, skip
    count = 0
    emptyCageSpaceInTheMiddle = 0
    finalEmptyCageSpace = 0
    killerCage.sort()
    for i in killerCage:
        count = count + 1
        verticalCoords = i[0]
        horizontalCoords = i[1]

        # Check whether number filled in is already present in the killer cage (not allowed)
        if board[verticalCoords][horizontalCoords] == numberFilledIn:
            return False

        # If all other cage values are filled in, and last value is not yet filled in, proceed with check
        if board[verticalCoords][horizontalCoords] == 0 and count != len(killerCage):
            emptyCageSpaceInTheMiddle = 1
        if board[verticalCoords][horizontalCoords] == 0 and count == len(killerCage) and emptyCageSpaceInTheMiddle == 0:
            finalEmptyCageSpace = 1

    if finalEmptyCageSpace == 1:
        cageTotalValue = 0
        for i in killerCage:
            verticalCoords = i[0]
            horizontalCoords = i[1]
            cageTotalValue = cageTotalValue + board[verticalCoords][horizontalCoords]
        cageTotalValue = cageTotalValue + numberFilledIn
        if cageValue != cageTotalValue:
            return False
        else:
            return True
    else:
        return True

# Function to determine matching killed cage squares
def findKillerCageFriends(board, killerGrid, cageValue, targetPosition, positionsToIgnore, origin):
    killerCage = []

    upSearch = 1
    rightSearch = 1
    downSearch = 1
    leftSearch = 1

    leftCount = 0
    rightCount = 0
    upCount = 0
    downCount = 0

    # Left Search
    while leftSearch == 1 and origin != "right":
        if killerGrid[targetPosition[0]][(targetPosition[1] - leftCount)] == cageValue:
            matchedPosition = [targetPosition[0], targetPosition[1] - leftCount]
            duplicateFound = 0
            for a in positionsToIgnore:
                if a == matchedPosition:
                    duplicateFound = 1
            if duplicateFound == 0:
                killerCage.append(matchedPosition)
                positionsToIgnore.append(matchedPosition)
            leftCount = leftCount + 1
            if matchedPosition[1] > 0:
                newTargetPosition = [matchedPosition[0], (matchedPosition[1] - 1)]
                goDeeperIntoSameDirection = findKillerCageFriends(board,
                                                                  killerGrid,
                                                                  cageValue,
                                                                  newTargetPosition,
                                                                  positionsToIgnore,
                                                                  "left")
                for a in goDeeperIntoSameDirection:
                    killerCage.append(a)
            else:
                leftSearch = 0
        else:
            leftSearch = 0

    # Right Search
    while rightSearch == 1 and origin != "left":
        if killerGrid[targetPosition[0]][(targetPosition[1] + rightCount)] == cageValue:
            matchedPosition = [targetPosition[0], targetPosition[1] + rightCount]
            duplicateFound = 0
            for a in positionsToIgnore:
                if a == matchedPosition:
                    duplicateFound = 1
            if duplicateFound == 0:
                killerCage.append(matchedPosition)
                positionsToIgnore.append(matchedPosition)
            rightCount = rightCount + 1
            if matchedPosition[1] < 8:
                newTargetPosition = [matchedPosition[0], (matchedPosition[1] + 1)]
                goDeeperIntoSameDirection = findKillerCageFriends(board,
                                                                  killerGrid,
                                                                  cageValue,
                                                                  newTargetPosition,
                                                                  positionsToIgnore,
                                                                  "right")
                for a in goDeeperIntoSameDirection:
                    killerCage.append(a)
            else:
                rightSearch = 0
        else:
            rightSearch = 0

    # Up Search
    while upSearch == 1 and origin != "down":
        if killerGrid[(targetPosition[0] - upCount)][targetPosition[1]] == cageValue:
            matchedPosition = [targetPosition[0] - upCount, targetPosition[1]]
            duplicateFound = 0
            for a in positionsToIgnore:
                if a == matchedPosition:
                    duplicateFound = 1
            if duplicateFound == 0:
                killerCage.append(matchedPosition)
                positionsToIgnore.append(matchedPosition)
            upCount = upCount + 1
            if matchedPosition[0] > 0:
                newTargetPosition = [matchedPosition[0] - 1, (matchedPosition[1])]
                goDeeperIntoSameDirection = findKillerCageFriends(board,
                                                                  killerGrid,
                                                                  cageValue,
                                                                  newTargetPosition,
                                                                  positionsToIgnore,
                                                                  "up")
                for a in goDeeperIntoSameDirection:
                    killerCage.append(a)
            else:
                upSearch = 0
        else:
            upSearch = 0

    # Down Search
    while downSearch == 1 and origin != "up":
        if killerGrid[(targetPosition[0] + downCount)][targetPosition[1]] == cageValue:
            matchedPosition = [targetPosition[0] + downCount, targetPosition[1]]
            duplicateFound = 0
            for a in positionsToIgnore:
                if a == matchedPosition:
                    duplicateFound = 1
            if duplicateFound == 0:
                killerCage.append(matchedPosition)
                positionsToIgnore.append(matchedPosition)
            downCount = downCount + 1
            if matchedPosition[0] < 8:
                newTargetPosition = [matchedPosition[0] + 1, (matchedPosition[1])]
                goDeeperIntoSameDirection = findKillerCageFriends(board,
                                                                  killerGrid,
                                                                  cageValue,
                                                                  newTargetPosition,
                                                                  positionsToIgnore,
                                                                  "down")
                for a in goDeeperIntoSameDirection:
                    killerCage.append(a)
            else:
                downSearch = 0
        else:
            downSearch = 0
    return killerCage

# Function to print filled-in Sudoku grid
def printSolutionGrid(grid):
    for i in range(len(grid)):
        if i % 3 == 0 and i != 0:
            print("------ ------- ------")

        for j in range(len(grid[0])):
            if j % 3 == 0 and j != 0:
                print("| ", end="")
            if j == 8:
                print(grid[i][j])
            else:
                print(str(grid[i][j]) + " ", end="")

# Function to find empty squares on Sudoku grid
def findEmpty(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                return i, j
    return None

# Calling the functions
print("Start:")
printSolutionGrid(solutionGrid)
solve(solutionGrid, killerSudokuGrid)
print("")
print("Solution:")
printSolutionGrid(solutionGrid)
