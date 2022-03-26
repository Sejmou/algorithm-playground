# Sparse matrices are matrices that contain only little non-zero values compared to the size of the matrix (columns * rows)
# For those types of matrices, more memory efficient code implementations exist

# The two code examples below demonstrate the inner workings of Compressed Sparse Row (CSR) matrices
# Commonly, they are also called CRS matrices, after the storage method (Compressed Row Storage)
# Using CSR matrices is much more memory efficient for matrices with a low average percentage of non-zero values per row
# The examples use SciPy's scipy.sparse.csr_matrix implementation (https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html)

# Compressed Sparse Row (CSR) matrices
#
# text explanation + illustration of how csr_matrix works and what purpose its data, indices, and indptr serve: https://stackoverflow.com/a/52299730/13727176

def get_nonzero_value_positions(csr_matrix):
    m = csr_matrix
    print(f'The CSR Matrix has {m.shape[0]} rows and {m.shape[1]} columns')
    print('data:', a.data, f'(i.e. {data.size} non-zero values)')
    print('indices', a.indices,
          f'(stores columns of each non-zero value; same size as data)')
    print('indptr:', a.indptr,
          f'(used for retrieving rows of non-zero values; size: {m.indptr.size}, as matrix has {m.shape[0]} rows)')
    print()

    val_pos = []

    for i, num in enumerate(m.data):
        print(
            f'  searching for matrix position of value {num} (at index {i} in data):')
        col = m.indices[i]
        print(f'    indices[{i}] = {col} -> {num} belongs to column {col}')
        j = 0

        print(
            f'    To find the row the current value {num} belongs to, check indptr')
        while m.indptr[j] <= i:
            print(
                f'      indptr[{j}] = {m.indptr[j]} <= {i} = index of current value {num} in data')
            print(f'        check next value in indptr')
            j = j+1
        row = j - 1
        print(
            f'      indptr[{j}] = {m.indptr[j]} >= index of current value {num} in data ({i}) -> {num} belongs to row {j}-1 = {row}')

        print(f'    row and column of value {num}: ({row}, {col})')
        print()
        val_pos.append((num, (row, col)))

    print('values and positions:')
    print(val_pos)


get_nonzero_value_positions(a)
print()


def reconstruct_row_values(csr_matrix, row_number):
    m = csr_matrix

    if row_number < 0 or row_number > m.indices[-1]:
        raise ValueError(f'row {row_number} does not exist')

    row_vals_start = m.indptr[row_number]
    next_row_vals_start = m.indptr[row_number + 1]
    vals = m.data[row_vals_start:next_row_vals_start]
    cols = m.indices[row_vals_start:next_row_vals_start]
    return vals, cols
