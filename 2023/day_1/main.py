'''
--- Day 1: Trebuchet?! ---
Something is wrong with global snow production, and you've been selected to take a look. The Elves have even given you a map; on it, they've used stars to mark the top fifty locations that are likely to be having problems.

You've been doing this long enough to know that to restore snow operations, you need to check all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

You try to ask why they can't just use a weather machine ("not powerful enough") and where they're even sending you ("the sky") and why your map looks mostly blank ("you sure ask a lot of questions") and hang on did you just say the sky ("of course, where do you think snow comes from") when you realize that the Elves are already loading you into a trebuchet ("please hold still, we need to strap you in").

As they're making the final adjustments, they discover that their calibration document (your puzzle input) has been amended by a very young Elf who was apparently just excited to show off her art skills. Consequently, the Elves are having trouble reading the values on the document.

The newly-improved calibration document consists of lines of text; each line originally contained a specific calibration value that the Elves now need to recover. On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.

For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of the calibration values?

ANSWER: 54561

--- Part Two ---
Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.

What is the sum of all of the calibration values?

ANSWER: 54076
'''

CALIBRATION_FILE = 'calibration_doc.txt'
NUMBER_MAP = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

def main():
    calibration = open(CALIBRATION_FILE, 'r')
    total = 0
    for line in calibration:
        val = parse_calibration_value_p2(line)
        print(val)
        total += val
    
    print(f'The sum of all calibration values is {total}')


def parse_calibration_value(line: str) -> int:
    """
    Converts a calibration string to a calibration value (combine first and last digit).
    """
    first_digit = None
    second_digit = None

    for char in line:
        if char.isdigit():
            if not first_digit:
                first_digit = int(char)
            else:
                second_digit = int(char)

    if second_digit:
        return first_digit * 10 + second_digit

    return first_digit * 10 + first_digit

def parse_calibration_value_p2(line: str) -> int:
    """
    Converts a calibration string to a calibration value (combine first and last digit).
    **INCLUDING DIGITS REPRESENTED AS STRINGS**
    """
    # Store index, value
    first = [-1, None]
    second = [-1, None]

    # First search for regular integer digits
    for i, char in enumerate(line):
        if char.isdigit():
            if first[0] == -1:
                first = [i, int(char)]
            else:
                second = [i, int(char)]
    
    # Assign the second to be the same as first if only first is defined
    if first[0] > 0 and second[0] < 0:
        second = first
        
    # Find the first and last occurances of each substring
    for digit_str, val in NUMBER_MAP.items():
        index = line.find(digit_str)
        if index >= 0 and (first[0] == -1 or first[0] > index):
            first = [index, val]

        index = line.rfind(digit_str)
        if index >= 0 and (second[0] == -1 or second[0] < index):
            second = [index, val]

    if second[0] > 0:
        return first[1] * 10 + second[1]
    
    return first[1] * 10 + first[1]

if __name__ == '__main__':
    main()