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

killerSudokuGrid = [
    [3,  3,  15, 15, 15, 22, 4,  16, 15],
    [25, 25, 17, 17, 22, 22, 4,  16, 15],
    [25, 25, 9,  9,  22, 8,  20, 20, 15],
    [6,  14, 14, 9,  17, 8,  20, 17, 15],
    [6,  13, 13, 20, 17, 8,  17, 17, 12],
    [27, 13, 6,  20, 17, 20, 6,  6,  12],
    [27, 6,  6,  20, 10, 20, 20, 14, 14],
    [27, 8,  16, 10, 10, 15, 15, 14, 14],
    [27, 8,  16, 10, 13, 13, 13, 17, 17]
]

# AI
def solve(solutionGrid, killerGrid):
    foundEmptySquare = findEmpty(solutionGrid)
    if not foundEmptySquare:
        # Als er geen lege vakjes meer zijn is de puzzel opgelost
        return True
    else:
        row, col = foundEmptySquare

    for i in range(1,10):
        if checkValidity(solutionGrid, i, (row, col), killerGrid):
            solutionGrid[row][col] = i

            if solve(solutionGrid):
                return True

            solutionGrid[row][col] = 0

    return False

# Functie om met Constraint Satisfaction te valideren of zet valide is (Boolean)
def checkValidity(board, numberFilledIn, position, killerGrid):

    # Constraint op rij (horizontaal)
    # Voor elke horizontale waarde wordt gekeken of het getal niet hetzefde is als het ingevulde nummer, met uitzondering van de plek die net is ingevuld
    for i in range(len(board[0])):
        if board[position[0]][i] == numberFilledIn and position[1] != i:
            return False

    # Constraint op kolom (verticaal)
    # Voor elke verticale waarde wordt gekeken of het getal niet hetzefde is als het ingevulde nummer, met uitzondering van de plek die net is ingevuld
    for i in range(len(board)):
        if board[i][position[1]] == numberFilledIn and position[0] != i:
            return False

    # Constraint op vierkant (9x9)
    box_x = position[1] // 3
    box_y = position[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == numberFilledIn and (i, j) != position:
                return False

    # Killer-constraint
    print("Cage value:")
    print(killerGrid[position[0]][position[1]])
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

    print("Amount of rows in board:")
    print(len(board))
    # board [
    #   [0,..],
    #   [0,..],
    #   [0,..],
    #    ...
    #   ]

    # Itereren over waardes hierin kan via range(...) methode

    print("Amount of cells in single row:")
    print(len(board[0]))
    # board [
    #   [0,1,2,3,4,5,6,7,8],  <--   horizontale sudoku regel
    #   ]

    # for x in killerGrid: # elke rij
    #     for y in x: # elke waarde per rij
    #         print(y)
    killerCage = findKillerCageFriends(board, killerGrid, cageValue, position)

    # Als cage nog niet compleet is ingevuld, skip
    emptySpaceInCage = 0
    for i in range(killerCage):
        if board[position[i]] == 0:
            emptySpaceInCage = 1

    if emptySpaceInCage == 0:
        cageCount = 0
        # Optellen alle waardes en vergelijken met totale waarde die cage moet zijn bij oplossing
        for i in range(killerCage):
            cageCount = cageCount + board[position[i]]
        # Als alle cage waardes zijn ingevuld en de totale cage waarde wijkt af: False
        if cageValue != cageCount:
            return False

    return True

def findKillerCageFriends(board, killerGrid, cageValue, position):
    killerCage = []
    for r in range(len(board)):
        for v in range(len(board[r])):
            print("r = " + str(r))
            print("v = " + str(v))
            print("Comparing killer-cage value " + str(cageValue) + " to cell value " + str(killerGrid[r][v]))
            if killerGrid[r][v] == cageValue:
                # ToDo: Alleen match als de cel aangrenzend is aan de cel van de cageValue
                if (r >= position[0]-1) and (r <= position[0]+1) and (v >= position[1]-1) and (v <= position[1]+1) and ((r, v) != position):
                    matchedCoords = [r, v]
                    print("Cell found matching cage value: " + str(matchedCoords))
                    killerCage.append(matchedCoords)
                    # Recursie om verder/dieper te zoeken naar killer cage matches
                    findKillerCageFriends(board, killerGrid, cageValue, matchedCoords)

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
