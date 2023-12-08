"my very first sudoku solver"
from collections import Counter

import numpy as np

from grids import grid_2 as grid


def extract_from_set(element):
    if isinstance(element, set):
        if len(element) == 1:
            return list(element)[0]
    return element


extract_from_set = np.vectorize(extract_from_set, otypes=[np.dtype])
apply_to_set_elements = np.vectorize(lambda x: isinstance(x, set))


def generate_map_function(element):
    return np.vectorize(lambda x: True if (isinstance(x, set) and element in x) else False)

def get_rows(square: np.array):
    rows = square.any(axis=1)
    counts = np.count_nonzero(rows)
    if counts==1:
        return [True, np.where(rows)[0][0]]
    else:
        return [False, 0]
    
def get_columns(square: np.array):
    columns = square.any(axis=0)
    counts = np.count_nonzero(columns)
    if counts==1:
        
        return [True, np.where(columns)[0][0]]
    else:
        return [False, 0]
    
    

def generate_all_map_functions():
    generate_dict = {}
    for i in range(1, 10):
        generate_dict[i] = generate_map_function(i)
    return generate_dict

func_dict = generate_all_map_functions()

def get_incusions(square):
    res_dict = {}
    for i in range(1, 10):
        map_func = func_dict[i]
        res_dict[i] = map_func(square)
    for index, num_square in res_dict.items():
        res_dict[index] = get_rows(num_square)
        res_dict[index].extend(get_columns(num_square))
    

def get_columns_and_rows(input_array):
    row_values = []
    for row in input_array:
        row_values.append(set(np.unique(row)))
    column_values = []
    for column in input_array.T:
        column_values.append(set(np.unique(column)))
    return column_values, row_values


def get_suggestions(input_array):
    column_values, row_values = get_columns_and_rows(input_array)

    suggestions = np.full((9, 9), set(range(1, 10)))

    suggestions = suggestions - column_values
    suggestions = (suggestions.T - row_values).T
    suggestions[input_array > 0] = input_array[input_array > 0]
    return suggestions


def set_zeros(input_array):
    set_indexes = apply_to_set_elements(input_array)
    input_array[set_indexes] = 0
    return input_array


def counter_numbers_in_square(square: np.array):
    flat = square.flatten()
    sets = flat[apply_to_set_elements(flat)]
    counters = [Counter(numbers_set) for numbers_set in sets]
    counters_sum = sum(counters, start=Counter())
    return counters_sum


def set_one_occuring_elements_in_square(square: np.array):
    counter = counter_numbers_in_square(square)
    numbers = [number for number, count in counter.items() if count == 1]

    for number in numbers:
        map_func = func_dict[number]
        i, j = np.where(map_func(square))
        i = i[0]
        j = j[0]
        square[i, j] = number


def solve_sudoku(grid):
    pairs = list(zip(list(range(0, 9, 3)), list(range(2, 9, 3))))
    #tmp = get_suggestions(grid)
    while True:
        tmp = get_suggestions(grid)
        for pair in pairs:
            for second_pair in pairs:
                next_square = grid[
                    pair[0]: pair[1] + 1, second_pair[0]: second_pair[1] + 1
                ]
                tmp_square = tmp[
                    pair[0]: pair[1] + 1, second_pair[0]: second_pair[1] + 1
                ]
                restrictions = set(next_square.flatten())
                tmp_square[apply_to_set_elements(tmp_square)] = (
                    tmp_square[apply_to_set_elements(tmp_square)] - restrictions
                )
                set_one_occuring_elements_in_square(tmp_square)
                get_incusions(tmp_square)
        tmp = extract_from_set(tmp)
        tmp = set_zeros(tmp)

        if (grid == tmp).all():
            break
        grid = tmp
    return grid