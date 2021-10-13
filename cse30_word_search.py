"""
This program searches for words in an input grid. It takes two parameters
Minimum Length of the words to be searched
A dictionary file that the words will be searched in
Additionally, it expects the grid to be entered as a user input

The searched words must be contiguous, but must be searched along the
horizontal, vertical, and diagonal directions. Since for each dimension,
we can go front or back, there are a total of 8 directions to be
searched.

Strings of length >= the specified lengths are constructed, and then
searched in the dictionary using binary search. Valid words are returned
in a sorted order.
"""
import sys


def search_in_dictionary(word_to_check, low, high):
    """
    Does a binary search on the dictionary for a word
    param word_to_check: Word to search in the dictionary
    param low: lower end of the search list
    param high: Upper end of the search list
    return: True or False
    """
    if high < low:
        return False

    mid = (low + high) // 2

    if word_to_check == sorted_dict[mid]:
        # words_found.append(word_to_check)
        return True

    if word_to_check < sorted_dict[mid]:
        return search_in_dictionary(word_to_check, low, mid - 1)

    return search_in_dictionary(word_to_check, mid + 1, high)


def create_slices(arr, slice_length):
    """
    Given an array arr and a slice length, construct a list of contiguous elements from
    the array of size >= slice length, in both the forward and reversed orders. For
    example, given an array [1, 2, 3, 4], and a slice length of 2, the function should
    generate the lists ([1, 2], [1, 2, 3], [1, 2, 3, 4], [2, 3], [2, 3, 4], [3, 4],
    [4, 3], [4, 3, 2], [4, 3, 2, 1], [3, 2], [3, 2, 1], [2, 1]).
    The order of the lists is not important.
    param arr: Input array to be sliced
    param slice_length: Minimum length of the slice to be used for array
    return: List of sliced elements of the array
    """
    return_list = []
    arr_reversed = list(reversed(arr))

    for i in range(len(arr) - slice_length + 1):
        for j in range(i + slice_length, len(arr) + 1):
            return_list.append(''.join(arr[i:j]))
            return_list.append(''.join(arr_reversed[i:j]))
    return return_list


def traverse_horizontal(grid, size, min_len):
    """
    For each row in the input grid, return contiguous words of length >= min_len
    param grid: Input grid
    param size: Number of rows/columns in the grid
    param min_len: Minimum length of the words to be returned
    return: List of all words of length >= min_len
    """
    return_list = []
    for i in range(size):
        revg = list(reversed(grid[i]))
        for j in range(size):
            for k in range(j + min_len, size + 1):
                return_list.append(''.join(grid[i][j:k]))
                return_list.append(''.join(revg[j:k]))

    return return_list


def traverse_vertical(grid, size, min_len):
    """
    For each column in the input grid, return contiguous words of length >= min_len
    param grid: Input grid
    param size: Number of rows/columns in the grid
    param min_len: Minimum length of the words to be returned
    return: List of all words of length >= min_len
    """
    return_list = []
    cols = list(zip(*grid))
    for i in range(size):
        revc = list(reversed(cols[i]))
        for j in range(size):
            for k in range(j + min_len, size + 1):
                return_list.append(''.join(cols[i][j:k]))
                return_list.append(''.join(revc[j:k]))

    return return_list


def traverse_diag_left_from_top(grid, size, min_len):
    """
    For each diagonal going left in the input grid, return contiguous words
    of length >= min_len. The diagonal is scanned only from the top row,
    since we consider the order of the words in both directions
    param grid: Input grid
    param size: Number of rows/columns in the grid
    param min_len: Minimum length of the words to be returned
    return: List of all words of length >= min_len
    """
    elem = []
    return_list = []
    for i in range(min_len - 1, size):
        k = i
        for j in range(0, i + 1):
            # Create a list of elements in the left diagonal
            # row starting from an element in row 0
            elem.append(grid[j][k])
            k -= 1
        for item in create_slices(elem, min_len):
            return_list.append(item)
        elem = []
    return return_list


def traverse_diag_right_from_top(grid, size, min_len):
    """
    For each diagonal going right in the input grid, return contiguous words
    of length >= min_len. The diagonal is scanned only from the top row,
    since we consider the order of the words in both directions
    param grid: Input grid
    param size: Number of rows/columns in the grid
    param min_len: Minimum length of the words to be returned
    return: List of all words of length >= min_len
    """
    elem = []
    return_list = []
    for i in range(size - min_len + 1):
        k = i
        for j in range(0, size - i):
            # Create a list of elements in the right diagonal
            # row starting from an element in row 0
            elem.append(grid[j][k])
            k += 1
        for item in create_slices(elem, min_len):
            return_list.append(item)
        elem = []
    return return_list


def traverse_diag_left_from_bottom(grid, size, min_len):
    """
    For each diagonal going left in the input grid, return contiguous words
    of length >= min_len. The diagonal is scanned only from the bottom row,
    and only for the diagonals not covered by the top row diagonal scan functions.
    param grid: Input grid
    param size: Number of rows/columns in the grid
    param min_len: Minimum length of the words to be returned
    return: List of all words of length >= min_len
    """
    elem = []
    return_list = []
    for i in range(min_len - 1, size - 1):
        k = i
        for j in range(size - 1, size - i - 2, -1):
            # Create a list of elements in the left diagonal
            # row starting from an element in row n - 1
            elem.append(grid[j][k])
            k -= 1
        for item in create_slices(elem, min_len):
            return_list.append(item)
        elem = []
    return return_list


def traverse_diag_right_from_bottom(grid, size, min_len):
    """
    For each diagonal going right in the input grid, return contiguous words
    of length >= min_len. The diagonal is scanned only from the bottom row,
    and only for the diagonals not covered by the top row diagonal scan functions.
    param grid: Input grid
    param size: Number of rows/columns in the grid
    param min_len: Minimum length of the words to be returned
    return: List of all words of length >= min_len
    """
    elem = []
    return_list = []
    for i in range(1, size - min_len + 1):
        k = i
        for j in range(size - 1, i - 1, -1):
            # Create a list of elements in the right diagonal
            # row starting from an element in row n - 1
            elem.append(grid[j][k])
            k += 1
        for item in create_slices(elem, min_len):
            return_list.append(item)
        elem = []
    return return_list


if __name__ == '__main__':
    min_length = int(sys.argv[1])
    dict_file = sys.argv[2]

    input_data = sys.stdin.readlines()
    grid_size = len(input_data)

    A = []
    for line in input_data:
        A.append(list(line.strip()))

    words_to_search = list()
    words_to_search.append(traverse_vertical(A, grid_size, min_length))
    words_to_search.append(traverse_horizontal(A, grid_size, min_length))
    words_to_search.append(traverse_diag_left_from_top(A, grid_size, min_length))
    words_to_search.append(traverse_diag_right_from_top(A, grid_size, min_length))
    words_to_search.append(traverse_diag_left_from_bottom(A, grid_size, min_length))
    words_to_search.append(traverse_diag_right_from_bottom(A, grid_size, min_length))

    unsorted_dict = []
    with open(dict_file, 'r') as fh:
        words = fh.readlines()

    for word in words:
        unsorted_dict.append(word.upper().strip())

    sorted_dict = sorted(unsorted_dict)

    words_found = []

    for word_list in words_to_search:
        for word in word_list:
            if search_in_dictionary(word, 0, len(sorted_dict)):
                words_found.append(word)

    unique_words = []
    for word in sorted(words_found):
        if word not in unique_words:
            unique_words.append(word)

    for word in unique_words:
        print(word)
