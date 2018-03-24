"""
Assignment Week-4
"""

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """
    Takes as input a set of characters alphabet and three scores diag_score, off_diag_score, and dash_score.
    The function returns a dictionary of dictionaries whose entries are indexed by pairs of characters in alphabet plus '-'.
    The score for any entry indexed by one or more dashes is dash_score.
    The score for the remaining diagonal entries is diag_score.
    Finally, the score for the remaining off-diagonal entries is off_diag_score.
    """
    scoring_matrix = {}
    scoring_matrix['-'] = {'-' : dash_score}
    for char in alphabet:
        scoring_matrix[char] = {}
        scoring_matrix[char]['-'] = dash_score
        scoring_matrix['-'][char] = dash_score
        for other_char in alphabet:
            if char != other_char:
                scoring_matrix[char][other_char] = off_diag_score
            else:
                scoring_matrix[char][other_char] = diag_score
    
    return scoring_matrix
    

def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """ 
    Takes as input two sequences seq_x and seq_y whose elements share a common alphabet with the scoring matrix scoring_matrix. 
    The function computes and returns the alignment matrix for seq_x and seq_y as described in the Homework. 
    If global_flag is True, each entry of the alignment matrix is computed using the method described in Question 8 of the Homework. 
    If global_flag is False, each entry is computed using the method described in Question 12 of the Homework.
    """
    len_x = len(seq_x)
    len_y = len(seq_y)

    dp_table = [[0 for dummy_idx in range(len_y+1)] for dummy_idx in range(len_x+1)]

    for row_index in range(1,len_x+1):
        dp_table[row_index][0] = dp_table[row_index-1][0] + scoring_matrix[seq_x[row_index-1]]['-']
        if (dp_table[row_index][0] < 0) and (global_flag == False):
                dp_table[row_index][0] = 0
                
    for col_index in range(1,len_y+1): 
        dp_table[0][col_index] = dp_table[0][col_index-1] + scoring_matrix['-'][seq_y[col_index-1]]
        if (dp_table[0][col_index] < 0) and (global_flag == False):
                dp_table[0][col_index] = 0
                
    for row_index in range(1,len_x+1):
        for col_index in range(1,len_y+1):
            diag = dp_table[row_index-1][col_index-1] + scoring_matrix[seq_x[row_index-1]][seq_y[col_index-1]]
            upper = dp_table[row_index][col_index-1] + scoring_matrix['-'][seq_y[col_index-1]]
            left = dp_table[row_index-1][col_index] + scoring_matrix[seq_x[row_index-1]]['-']

            dp_table[row_index][col_index] = max(upper,max(diag,left))
            print(dp_table[row_index][col_index])
            if (dp_table[row_index][col_index] < 0) and (global_flag == False):
                dp_table[row_index][col_index] = 0

    return dp_table


def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Takes as input two sequences seq_x and seq_y whose elements share a common alphabet with the scoring matrix scoring_matrix. 
    This function computes a global alignment of seq_x and seq_y using the global alignment matrix alignment_matrix.
    The function returns a tuple of the form (score, align_x, align_y) where score is the score of the global alignment align_x and align_y. 
    Note that align_x and align_y should have the same length and may include the padding character '-'.
    """
    row_index = len(seq_x)
    col_index = len(seq_y)
    score = alignment_matrix[row_index][col_index]
    new_seq_x = ""
    new_seq_y = ""

    while row_index != 0 and  col_index != 0 :
        if alignment_matrix[row_index][col_index] == alignment_matrix[row_index-1][col_index-1] + scoring_matrix[seq_x[row_index-1]][seq_y[col_index-1]] :
            new_seq_x = seq_x[row_index-1] + new_seq_x
            new_seq_y = seq_y[col_index-1] + new_seq_y
            row_index -= 1
            col_index -= 1
        else:
            if alignment_matrix[row_index][col_index] == alignment_matrix[row_index-1][col_index] + scoring_matrix[seq_x[row_index-1]]['-'] :
                new_seq_x = seq_x[row_index-1] + new_seq_x
                new_seq_y = '-' + new_seq_y
                row_index -= 1
            else:
                new_seq_x = '-' + new_seq_x
                new_seq_y = seq_y[col_index-1] + new_seq_y
                col_index -= 1

    while row_index != 0:
        new_seq_x = seq_x[row_index-1] + new_seq_x
        new_seq_y = '-' + new_seq_y
        row_index -= 1
    while col_index != 0:
        new_seq_x = '-' + new_seq_x
        new_seq_y = seq_y[col_index-1] + new_seq_y
        col_index -= 1

    return (score,new_seq_x,new_seq_y)


def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Takes as input two sequences seq_x and seq_y whose elements share a common alphabet with the scoring matrix scoring_matrix. 
    This function computes a local alignment of seq_x and seq_y using the local alignment matrix alignment_matrix.
    The function returns a tuple of the form (score, align_x, align_y) where score is the score of the optimal local alignment align_x and align_y. 
    Note that align_x and align_y should have the same length and may include the padding character '-'.
    """
    row_index = len(seq_x)
    col_index = len(seq_y)
    score = -1
    start_i = start_j = -1
    for dummy_idx_i in range(row_index+1):
        for dummy_idx_j in range(col_index+1):
            if alignment_matrix[dummy_idx_i][dummy_idx_j] > score:
                score = alignment_matrix[dummy_idx_i][dummy_idx_j]
                start_i = dummy_idx_i
                start_j = dummy_idx_j
    
    new_seq_x = ""
    new_seq_y = ""
    row_index = start_i
    col_index = start_j

    while row_index != 0 and  col_index != 0 :
        if alignment_matrix[row_index][col_index] == alignment_matrix[row_index-1][col_index-1] + scoring_matrix[seq_x[row_index-1]][seq_y[col_index-1]] :
            new_seq_x = seq_x[row_index-1] + new_seq_x
            new_seq_y = seq_y[col_index-1] + new_seq_y
            row_index -= 1
            col_index -= 1
        else:
            if alignment_matrix[row_index][col_index] == alignment_matrix[row_index-1][col_index] + scoring_matrix[seq_x[row_index-1]]['-'] :
                new_seq_x = seq_x[row_index-1] + new_seq_x
                new_seq_y = '-' + new_seq_y
                row_index -= 1
            else:
                new_seq_x = '-' + new_seq_x
                new_seq_y = seq_y[col_index-1] + new_seq_y
                col_index -= 1
        if alignment_matrix[row_index][col_index] == 0:
            break

    while row_index != 0:
        if alignment_matrix[row_index][0] == 0:
            break
        new_seq_x = seq_x[row_index-1] + new_seq_x
        new_seq_y = '-' + new_seq_y
        row_index -= 1
    while col_index != 0:
        if alignment_matrix[0][col_index] == 0:
            break
        new_seq_x = '-' + new_seq_x
        new_seq_y = seq_y[col_index-1] + new_seq_y
        col_index -= 1

    return (score,new_seq_x,new_seq_y)
