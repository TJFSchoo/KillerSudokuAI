import time

solutionGrid = [
    [0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0,  0,  0,  0,  0,  0,  0,  0,  0]
]

# killerSudokuGrid = [
#     [3,  3,  15, 15, 15, 22, 4,  16, 15],
#     [25, 25, 17, 17, 22, 22, 4,  16, 15],
#     [25, 25, 9,  9,  22, 8,  20, 20, 15],
#     [6,  14, 14, 9,  17, 8,  20, 17, 15],
#     [6,  13, 13, 20, 17, 8,  17, 17, 12],
#     [27, 13, 6,  20, 17, 20, 6,  6,  12],
#     [27, 6,  6,  20, 10, 20, 20, 14, 14],
#     [27, 8,  16, 10, 10, 15, 15, 14, 14],
#     [27, 8,  16, 10, 13, 13, 13, 17, 17]
# ]

# https://www.theguardian.com/lifeandstyle/2020/jan/12/observer-killer-sudoku
killerSudokuGrid = [
    [ 9, 15, 15, 18, 14,  8,  8, 27, 10],
    [ 9, 23, 15, 18, 14, 14, 27, 27, 10],
    [23, 23, 15, 18, 18, 15, 27, 23, 10],
    [14, 23, 17, 17, 17, 15, 15, 23, 23],
    [14, 21, 20, 20, 17, 15,  9, 14, 14],
    [21, 21, 20, 19, 19, 20,  9, 14, 25],
    [21, 13, 10, 10, 19, 20, 19, 14, 25],
    [13, 13, 13, 10, 20, 20, 19, 19, 25],
    [22, 22, 22, 17, 17, 17,  3,  3, 25]
]

# AI
def solve(solutionGrid, killerGrid):
    foundEmptySquare = findEmpty(solutionGrid)
    if not foundEmptySquare:
        # Als er geen lege vakjes meer zijn is de puzzel opgelost
        return True
    else:
        row, col = foundEmptySquare

    for i in range(1, 10):
        if checkValidity(solutionGrid, i, (row, col), killerGrid):
            solutionGrid[row][col] = i

            if solve(solutionGrid, killerGrid):
                return True

            solutionGrid[row][col] = 0

    return False

# Functie om met Constraint Satisfaction te valideren of zet valide is (Boolean)
def checkValidity(board, numberFilledIn, position, killerGrid):
    print("Currently filled in board: " + str(solutionGrid))
    #("Trying to fill in number: " + str(numberFilledIn))
    #time.sleep(1)

    # Constraint op rij (horizontaal)
    # Voor elke horizontale waarde wordt gekeken of het getal niet hetzefde is als het ingevulde nummer, met uitzondering van de plek die net is ingevuld
    for i in range(len(board[0])):
        if board[position[0]][i] == numberFilledIn and position[1] != i:
            #print("Horizontal constraint: FALSE")
            return False

    # Constraint op kolom (verticaal)
    # Voor elke verticale waarde wordt gekeken of het getal niet hetzefde is als het ingevulde nummer, met uitzondering van de plek die net is ingevuld
    for i in range(len(board)):
        if board[i][position[1]] == numberFilledIn and position[0] != i:
            #print("Vertical constraint: FALSE")
            return False

    # Constraint op vierkant (9x9)
    box_x = position[1] // 3
    box_y = position[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == numberFilledIn and (i, j) != position:
                #print("Square constraint: FALSE")
                return False

    # Killer-constraint
    #print("Cage value:")
    #print(killerGrid[position[0]][position[1]])
    cageValue = killerGrid[position[0]][position[1]]
    killerCage = []

    # List aanvullen met alle aanliggende coordinaten die bij de killer cage horen
    # Eerst horizontaal checken, bij elke horizontale match ook verticaal checken
    # Voor iedere horizontale waarde: ( -> 1-9)

    # print("Board used for Killer-constraint:")
    # print(board)
    # print("First row of board:")
    # print(board[0])
    # print("First value of first row of board:")
    # print(board[0][0])

    # print("Amount of rows in board:")
    # print(len(board))
    # board [
    #   [0,..],
    #   [0,..],
    #   [0,..],
    #    ...
    #   ]

    # Itereren over waardes hierin kan via range(...) methode

    # print("Amount of cells in single row:")
    # print(len(board[0]))
    # board [
    #   [0,1,2,3,4,5,6,7,8],  <--   horizontale sudoku regel
    #   ]

    # for x in killerGrid: # elke rij
    #     for y in x: # elke waarde per rij
    #         print(y)

    killerCage = findKillerCageFriends(board, killerGrid, cageValue, position, [(-1, -1)], "none")
    # killerCage = findKillerCageFriends(board, killerGrid, cageValue, position, [(-1, -1)])
    #print("Matching killer cage for value " + str(cageValue) + ", position " + str(position) + ":")
    #print(str(killerCage))

    # Als cage nog niet compleet is ingevuld, skip
    emptySpaceInCage = 0
    count = 0
    emptyCageSpaceInTheMiddle = 0
    finalEmptyCageSpace = 0
    killerCage.sort()
    for i in killerCage:
        count = count + 1
        verticalCoords = i[0]
        horizontalCoords = i[1]

        if board[verticalCoords][horizontalCoords] == 0 and count != len(killerCage):
            emptyCageSpaceInTheMiddle = 1

        # If all other cage values are filled in, and last value is not yet filled in, return true and proceed with check
        if board[verticalCoords][horizontalCoords] == 0 and count == len(killerCage) and emptyCageSpaceInTheMiddle == 0:
            finalEmptyCageSpace = 1

    if finalEmptyCageSpace == 1:
        #print("Final blank space found in cage, killer-constraint activated:")
        cageTotalValue = 0
        # Optellen alle waardes en vergelijken met totale waarde die cage moet zijn bij oplossing
        for i in killerCage:
            verticalCoords = i[0]
            horizontalCoords = i[1]
            cageTotalValue = cageTotalValue + board[verticalCoords][horizontalCoords]
        cageTotalValue = cageTotalValue + numberFilledIn
        #print("Assigned cage value: " + str(cageValue))
        #print("Total filled-in cage value: " + str(cageTotalValue))
        # Als alle cage waardes zijn ingevuld en de totale cage waarde wijkt af: False
        if cageValue != cageTotalValue:
            #print("Killer constraint: FALSE")
            return False
        else:
            #print("Cage value correct!")
            return True

    else:
        #print("Skipping killer-constraint for now due to blank spaces.")

     return True

# def findKillerCageFriends(board, killerGrid, cageValue, targetPosition, positionsToIgnore):
#     killerCage = []
#     for r in range(len(board)):
#         for v in range(len(board[r])):
#             if killerGrid[r][v] == cageValue:
#                 if (r >= targetPosition[0] - 3) and (r <= targetPosition[0] + 3) and (v >= targetPosition[1] - 3) and (v <= targetPosition[1] + 3):
#
#                     # Zoek naar duplicate coordinaten in killer cage buffer
#                     duplicateFound = 0
#                     for a in positionsToIgnore:
#                         if a == (r, v):
#                             duplicateFound = 1
#
#                     # Indien uniek, opslaan
#                     if duplicateFound == 0:
#                         killerCage.append([r, v])
#
#                     positionsToIgnore.append([r, v])
#     return killerCage

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
    while(leftSearch == 1 and origin != "right"):
        #time.sleep(1)
        #print("LEFT search called, from origin: " + origin + ", cage value to find: " + str(cageValue) + ", origin position: " + str(targetPosition))
        #print("-- Target position: " + str(targetPosition[0]) + ", " + str((targetPosition[1] - leftCount)) + ", found cage value: " + str(killerGrid[targetPosition[0]][(targetPosition[1] - leftCount)]))
        if killerGrid[targetPosition[0]][(targetPosition[1] - leftCount)] == cageValue:
            matchedPosition = [targetPosition[0], targetPosition[1] - leftCount]
            duplicateFound = 0
            for a in positionsToIgnore:
                if a == matchedPosition:
                    duplicateFound = 1
            if duplicateFound == 0:
                #print("-- New match found! " + str(matchedPosition))
                killerCage.append(matchedPosition)
                positionsToIgnore.append(matchedPosition)
            leftCount = leftCount + 1
            if(matchedPosition[1] > 0):
                newTargetPosition = [matchedPosition[0], (matchedPosition[1] - 1)]
                #print("-> Going recursive from LEFT search with new target position: " + str(newTargetPosition) + ", previous positions: " + str(positionsToIgnore))
                goDeeperIntoSameDirection = findKillerCageFriends(board,
                                                                    killerGrid,
                                                                    cageValue,
                                                                    newTargetPosition,
                                                                    positionsToIgnore,
                                                                    "left")

                #print("<- Return one level: " + str(newTargetPosition) + ", matches to append from LEFT search: " + str(goDeeperIntoSameDirection))
                for a in goDeeperIntoSameDirection:
                    killerCage.append(a)
            else:
                #print("-- Skipping LEFT search because there is no space on the left side of matched position " + str(matchedPosition))
                leftSearch = 0
        else:
            # Stop searching in left direction
            #print("-- Skipping LEFT search because there is no cage value match")
            leftSearch = 0

    # right Search
    while (rightSearch == 1 and origin != "left"):
        #time.sleep(1)
        #print("RIGHT search called, from origin: " + origin + ", cage value to find: " + str(cageValue) + ", origin position: " + str(targetPosition))
        #print("-- Target position: " + str(targetPosition[0]) + ", " + str((targetPosition[1] + rightCount)) + ", found cage value: " + str(killerGrid[targetPosition[0]][(targetPosition[1] + rightCount)]))
        if killerGrid[targetPosition[0]][(targetPosition[1] + rightCount)] == cageValue:
            matchedPosition = [targetPosition[0], targetPosition[1] + rightCount]
            duplicateFound = 0
            for a in positionsToIgnore:
                if a == matchedPosition:
                    duplicateFound = 1
            if duplicateFound == 0:
                #print("-- New match found! " + str(matchedPosition))
                killerCage.append(matchedPosition)
                positionsToIgnore.append(matchedPosition)
            rightCount = rightCount + 1
            if (matchedPosition[1] < 8):
                newTargetPosition = [matchedPosition[0], (matchedPosition[1] + 1)]
                #print("-> Going recursive from RIGHT search with new target position: " + str(newTargetPosition) + ", previous positions: " + str(positionsToIgnore))
                goDeeperIntoSameDirection = findKillerCageFriends(board,
                                                                    killerGrid,
                                                                    cageValue,
                                                                    newTargetPosition,
                                                                    positionsToIgnore,
                                                                    "right")
                #print("<- Return one level: " + str(newTargetPosition) + ", matches to append from RIGHT search: " + str(goDeeperIntoSameDirection))
                for a in goDeeperIntoSameDirection:
                    killerCage.append(a)
            else:
                #print("-- Skipping RIGHT search because there is no space on the right side of matched position " + str(matchedPosition))
                rightSearch = 0
        else:
            # Stop searching in right direction
            #print("-- Skipping RIGHT search because there is no cage value match")
            rightSearch = 0

    # up Search
    while (upSearch == 1 and origin != "down"):
        #time.sleep(1)
        #print("UP search called, from origin: " + origin + ", cage value to find: " + str(cageValue) + ", origin position: " + str(targetPosition))
        #print("-- Target position: " + str((targetPosition[0] - upCount)) + ", " + str(targetPosition[1]) + ", found cage value: " + str(killerGrid[(targetPosition[0] - upCount)][targetPosition[1]]))
        if killerGrid[(targetPosition[0] - upCount)][targetPosition[1]] == cageValue:
            matchedPosition = [targetPosition[0] - upCount, targetPosition[1]]
            duplicateFound = 0
            for a in positionsToIgnore:
                if a == matchedPosition:
                    duplicateFound = 1
            if duplicateFound == 0:
                #print("-- New match found! " + str(matchedPosition))
                killerCage.append(matchedPosition)
                positionsToIgnore.append(matchedPosition)
            upCount = upCount + 1
            if (matchedPosition[0] > 0):
                newTargetPosition = [matchedPosition[0] - 1, (matchedPosition[1])]
                #print("-> Going recursive from DOWN search with new target position: " + str(newTargetPosition) + ", previous positions: " + str(positionsToIgnore))
                goDeeperIntoSameDirection = findKillerCageFriends(board,
                                                                      killerGrid,
                                                                      cageValue,
                                                                      newTargetPosition,
                                                                      positionsToIgnore,
                                                                      "up")
                #print("<- Return one level: " + str(newTargetPosition) + ", matches to append from UP search: " + str(goDeeperIntoSameDirection))
                for a in goDeeperIntoSameDirection:
                    killerCage.append(a)
            else:
                #print("-- Skipping UP search because there is no space on the up side of matched position " + str(matchedPosition))
                upSearch = 0
        else:
            # Stop searching in up direction
            #print("-- Skipping UP search because there is no cage value match")
            upSearch = 0

    # down Search
    while (downSearch == 1 and origin != "up"):
        #time.sleep(1)
        #print("DOWN search called, from origin: " + origin + ", cage value to find: " + str(cageValue) + ", origin position: " + str(targetPosition))
        #print("-- Target position: " + str((targetPosition[0] + downCount)) + ", " + str(targetPosition[1]) + ", found cage value: " + str(killerGrid[(targetPosition[0] + downCount)][targetPosition[1]]))
        if killerGrid[(targetPosition[0] + downCount)][targetPosition[1]] == cageValue:
            matchedPosition = [targetPosition[0] + downCount, targetPosition[1]]
            duplicateFound = 0
            for a in positionsToIgnore:
                if a == matchedPosition:
                    duplicateFound = 1
            if duplicateFound == 0:
                #print("-- New match found! " + str(matchedPosition))
                killerCage.append(matchedPosition)
                positionsToIgnore.append(matchedPosition)
            downCount = downCount + 1
            if (matchedPosition[0] < 8):
                newTargetPosition = [matchedPosition[0] + 1, (matchedPosition[1])]
                #print("-> Going recursive from UP search with new target position: " + str(newTargetPosition) + ", previous positions: " + str(positionsToIgnore))
                goDeeperIntoSameDirection = findKillerCageFriends(board,
                                                                    killerGrid,
                                                                    cageValue,
                                                                    newTargetPosition,
                                                                    positionsToIgnore,
                                                                    "down")
                #print("<- Return one level: " + str(newTargetPosition) + ", matches to append from DOWN search: " + str(goDeeperIntoSameDirection))
                for a in goDeeperIntoSameDirection:
                    killerCage.append(a)
            else:
                #print("-- Skipping DOWN search because there is no space on the down side of matched position " + str(matchedPosition))
                downSearch = 0
        else:
            # Stop searching in down direction
            #print("-- Skipping DOWN search because there is no cage value match")
            downSearch = 0

    return killerCage

def printSolutionGrid(solutionGrid):
    for i in range(len(solutionGrid)):
        # Na elke derde rij een horizontale streep
        if i % 3 == 0 and i != 0:
            print("------ ------- ------")

        # Na elk derde getal een verticale streep
        for j in range(len(solutionGrid[0])):
            # !=0 vanwege geen streep aan de buitenkant, end="" zorgt ervoor dat er geen backslash (naar volgende regel springen) komt
            if j % 3 == 0 and j != 0:
                print("| ", end="")
            # einde v/d regel
            if j == 8:
                print(solutionGrid[i][j])
            else:
                print(str(solutionGrid[i][j]) + " ", end="")

# Functie voor het afgaan van vakjes van een board, op zoek naar nog niet ingevulde vakjes
def findEmpty(solutionGrid):
    for i in range(len(solutionGrid)):
        for j in range(len(solutionGrid[0])):
            if solutionGrid[i][j] == 0:
                return (i, j)  # rij, kolom
    return None

print("Start:")
printSolutionGrid(solutionGrid)
solve(solutionGrid, killerSudokuGrid)
print("")
print("Oplossing:")
printSolutionGrid(solutionGrid)
