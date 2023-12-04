'''
--- Day 3: Gear Ratios ---
You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?

Part 1 ANSWER: 525119

--- Part Two ---
The engineer finds the missing part and installs it in the engine! As the engine springs to life, you jump in the closest gondola, finally ready to ascend to the water source.

You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately, the gondola has a phone labeled "help", so you pick it up and the engineer answers.

Before you can explain the situation, she suggests that you look out the window. There stands the engineer, holding a phone in one hand and waving with the other. You're going so slowly that you haven't even left the station. You exit the gondola.

The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?

PART 2 ANSWER: 76504829

'''
from collections import defaultdict
from math import prod

SCHEMATICS_FILE = 'schematic.txt'
DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]
SYMBOLS = {'!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '+', '=', '?', '/'}
GEAR = '*'

def parse_schematic() -> list[list[int]]:
    '''
    Parse schematic file into 2D array.
    '''
    arr = []
    schematic_file = open(SCHEMATICS_FILE, 'r')
    for line in schematic_file:
        arr.append([char for char in line.strip()])
    return arr

def adjacent_to_symbol(x, y, arr) -> tuple[bool, list[tuple[int, int]]]:
    '''
    Determines if a given coordinate is adjacent to a symbol    
    '''
    is_part = False
    gears = []
    for [dx, dy] in DIRECTIONS:
        adj_x = x + dx
        adj_y = y + dy
        
        if adj_x < 0 or adj_y < 0 or adj_x >= len(arr) or adj_y >= len(arr[0]):
            continue

        if arr[adj_x][adj_y] in SYMBOLS:
            is_part = True
            if arr[adj_x][adj_y] == GEAR:
                gears.append((adj_x, adj_y))
    return is_part, gears

def part_1() -> int:
    arr = parse_schematic()
    num_rows = len(arr)
    num_cols = len(arr[0])

    total = 0

    for i in range(num_rows):
        current_num = ''
        is_part_num = False
        for j in range(num_cols):
            character = arr[i][j]

            # Any digit
            if character.isdigit():
                current_num += character
                if adjacent_to_symbol(i, j, arr):
                    is_part_num = True

            # End of number (symbol or period, flush if part number was determined)
            elif current_num != '':
                if is_part_num:
                    total += int(current_num)
                # Reset current_num
                current_num = ''
                is_part_num = False
        
        # If end of line is reached, need to check again
        if current_num != '':
            if is_part_num:
                total += int(current_num)
    
    return total

def part_2() -> int:
    '''
    An alternative approach would be to start from the symbols -> numbers,
    however, that would require a lot more rewriting of part 1.
    '''
    arr = parse_schematic()
    num_rows = len(arr)
    num_cols = len(arr[0])

    # We map gear coordinate to numbers 
    # with a strong assumption that part numbers are unique
    gears_to_parts = defaultdict(set)

    total = 0

    for i in range(num_rows):
        current_num = ''
        current_gears = []
        is_part_num = False
        for j in range(num_cols):
            character = arr[i][j]

            # Any digit
            if character.isdigit():
                current_num += character
                is_adj_to_symbol, gears = adjacent_to_symbol(i, j, arr)
                if is_adj_to_symbol:
                    is_part_num = True
                    current_gears.extend(gears)

            # End of number (symbol or period, flush if part number was determined)
            elif current_num != '':
                if is_part_num:
                    for gear in current_gears:
                        gears_to_parts[gear].add(int(current_num))

                # Reset current_num
                current_num = ''
                current_gears = []
                is_part_num = False
        
        # If end of line is reached, need to check again
        if current_num != '':
            if is_part_num:
                for gear in current_gears:
                        gears_to_parts[gear].add(int(current_num))
    
    for parts in gears_to_parts.values():
        if len(parts) == 2:
            total += prod(parts)

    return total


print(part_1())
print(part_2())