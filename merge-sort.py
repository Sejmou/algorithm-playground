# note: for Python < 3.9 you apparently have to use List instead of list for type annotations and import it as well?
# otherwise type for list items cannot be specified with subscript?
# could alternatively also use quotes around e.g. list[int], apparently: https://stackoverflow.com/a/62775680
# from typing import List

def mergesort(arr: list[int]):
  arr = arr.copy()
  _sort_with_mergesort(arr, [None] * len(arr), 0, len(arr) - 1)
  return arr

def _sort_with_mergesort(arr: list[int], temp: list[int], left_start: int, right_end: int, depth=''):
  '''
  recursive helper function called by mergesort; returns when sort is finished
  '''
  if left_start >= right_end:
    return

  # divide and conquer: split array into halves; we will eventually get back sorted halves through the power of recursion :)
  middle = (left_start + right_end) // 2 # note: '//' is integer division operator in Python 3; with '/' result would be float, we don't want that here; details: https://en.wikibooks.org/wiki/Python_Programming/Operators#Division_and_Type_Conversion
  right_start = middle + 1
  left_end = middle

  #print(f'{left_start=}, {middle=}, {right_end=}')
  print(f'{depth}splitting into halves:')
  print(f'{depth}left half: {arr[left_start:(middle + 1)]}')
  print(f'{depth}right half: {arr[(middle + 1):(right_end + 1)]}\n')
  
  _sort_with_mergesort(arr, temp, left_start, left_end, depth=depth+' ')
  _sort_with_mergesort(arr, temp, right_start, right_end, depth=depth+'  ')

  # the sorted halves can be merged into the temporary array again in such a way that the elements remain sorted
  # after returning from recursion (left_start and right_end are start and end of original array) we will have our sorted array in the temporary array variable
  _merge_halves(arr, temp, left_start, right_end, depth=depth)

def _merge_halves(arr: list[int], temp: list[int], left_start: int, right_end: int, depth=''):
  middle = (left_start + right_end) // 2
  right_start = middle + 1
  left_end = middle

  print(f'{depth}start merging halves {arr[left_start:left_end + 1]} and {arr[right_start:right_end + 1]}')
  print(f'{depth}{f"{arr=}, {temp=}" if arr != temp else f"arr=temp={arr}"}')

  # iterate over sorted left and right halves,
  # writing sorted values from both halves into temp array
  i = left_start
  left_i = left_start
  right_i = right_start
  
  while left_i <= left_end and right_i <= right_end:
    if arr[left_i] <= arr[right_i]:
      # we need to copy over value from left half next as it is smaller
      #print(f'{depth}next val: {arr[left_i]}')
      temp[i] = arr[left_i]
      # of course, then we should also move the left index up (don't wanna add same number multiple times!)
      left_i += 1

    else:
      #print(f'{depth}next val: {arr[right_i]}')
      temp[i] = arr[right_i]
      right_i += 1

    i += 1

  # copy over remaining elements from half that contains remaining elements
  # at this stage, either all elements of left half or all elements of right half have already been copied
  # all remaining elements from other half must be larger!

  # we can compute the remaining slice like this
  remaining_slice = arr[right_i:right_end + 1] if left_i > left_end else arr[left_i:left_end + 1]
  #print(f'{depth}{remaining_slice=}')
  # and then just fill up the temporary array with it
  temp[i:(right_end + 1)] = remaining_slice

  arr[left_start:right_end + 1] = temp[left_start:right_end + 1]
  print(f'{depth}merged halves, result: {temp[left_start:right_end + 1]}')
  print(f'{depth}{f"{arr=}, {temp=}" if arr != temp else f"arr=temp={arr}"}\n')

  

if __name__ == "__main__":
  test = [5, 10, 30, 20, 4, 9, 8, 7, 3]
  print(f'input: {test}\n')
  print(f'output: {mergesort(test)}')