#!/usr/bin/env python3

import sys

def load_from_txt(path):
    file = open(path, 'r')
    solids = []
    entities = []
    first_part = True

    door = False
    len_line = 0

    for line in file:
        matrix_line = list(line)
        matrix_line.pop()

        if matrix_line == []:
            # Verify if the board is not empty
            if len_line == 0:
                clode_file(file, "empty board")

            first_part = False

            # Verify door in corner of last line
            if solids[-1][0] == '3' or solids[-1][-1] == '3':
                clode_file(file, "don't put a door in the corner")

            # Verify walls in last line
            for el in solids[-1]:
                if el != '1':
                    if el == '3':
                        # Verify unicity of door
                        if door:
                            clode_file(file, "only one door please")
                        door = True
                    else:
                        clode_file(file, "you need to have wall around")
            continue

        if len_line == 0:
            len_line = len(matrix_line)

            # Verify door in corner of first line
            if matrix_line[0] == '3' or matrix_line[-1] == '3':
                clode_file(file, "don't put a door in the corner")

            # Verify walls in first line
            for el in matrix_line:
                if el != '1':
                    if el == '3':
                        # Verify unicity of door
                        if door:
                            clode_file(file, "only one door please")
                        door = True
                    else:
                        clode_file(file, "you need to have wall around")
        else:
            # Verify walls in first and second column
            if first_part and (matrix_line[0] != '1' or matrix_line[-1] != '1'):
                # Verify unicity of door
                if (matrix_line[0], matrix_line[-1]) in (('3', '1'), ('1', '3')):
                    if door:
                        clode_file(file, "only one door please")
                    door = True
                else:
                    clode_file(file, "you need to have wall around")
            # Verify the length of door
            if len_line != len(matrix_line):
                clode_file(file, "you can't have different line length")

        if first_part:
            solids.append(matrix_line)
        else:
            entities.append(matrix_line)

    # Verify the presence of door
    if not door:
        clode_file(file, "one door please")
    if len(solids) != len(entities):
        clode_file(file, "you can't have different column length")

    # Verify the door corrdinate and no door inside
    door_location = (0, 0)
    for i in range(len(solids)):
        for j in range(len_line):
            if int(solids[i][j]) < 0 or int(solids[i][j]) > 9:
                clode_file(file, "invalid solids")
            if solids[i][j] == '3':
                if door_location != (0, 0):
                    clode_file(file, "you can't have door in the middle")
                door_location = (i, j)
            solids[i][j] = int(solids[i][j])
            entities[i][j] = int(entities[i][j])

    return solids, entities, door_location


def clode_file(file, message):
    print(message)
    file.close()
    sys.exit()


if __name__ == "__main__":
    solids, entities, door_location = load_from_txt("test.txt")
    print(solids, entities, door_location)
