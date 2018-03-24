"""
Week 4
"""

DESKTOP = True

import math
import random
import urllib2

if DESKTOP:
    import matplotlib.pyplot as plt
    import matplotlib
    #import alg_project4_solution as student
else:
    import simpleplot
    import userXX_XXXXXXX as student

# URLs for data files
PAM50_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_PAM50.txt"
HUMAN_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_HumanEyelessProtein.txt"
FRUITFLY_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_FruitflyEyelessProtein.txt"
CONSENSUS_PAX_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_ConsensusPAXDomain.txt"
WORD_LIST_URL = "http://storage.googleapis.com/codeskulptor-assets/assets_scrabble_words3.txt"


###############################################
# provided code

def read_scoring_matrix(filename):
    """
    Read a scoring matrix from the file named filename.
    Argument:
    filename -- name of file containing a scoring matrix
    Returns:
    A dictionary of dictionaries mapping X and Y characters to scores
    """
    scoring_dict = {}
    scoring_file = urllib2.urlopen(filename)
    ykeys = scoring_file.readline()
    ykeychars = ykeys.split()
    for line in scoring_file.readlines():
        vals = line.split()
        xkey = vals.pop(0)
        scoring_dict[xkey] = {}
        for ykey, val in zip(ykeychars, vals):
            scoring_dict[xkey][ykey] = int(val)
    return scoring_dict


def read_protein(filename):
    """
    Read a protein sequence from the file named filename.
    Arguments:
    filename -- name of file containing a protein sequence
    Returns:
    A string representing the protein
    """
    protein_file = urllib2.urlopen(filename)
    protein_seq = protein_file.read()
    protein_seq = protein_seq.rstrip()
    return protein_seq


def read_words(filename):
    """
    Load word list from the file named filename.
    Returns a list of strings.
    """
    # load assets
    word_file = urllib2.urlopen(filename)

    # read in files as string
    words = word_file.read()

    # template lines and solution lines list of line string
    word_list = words.split('\n')
    #print("Loaded a dictionary with", len(word_list), "words")
    return word_list


def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """
    Takes as input a set of characters alphabet and three scores diag_score, off_diag_score, and dash_score.
    The function returns a dictionary of dictionaries whose entries are indexed by pairs of characters in alphabet plus '-'.
    The score for any entry indexed by one or more dashes is dash_score.
    The score for the remaining diagonal entries is diag_score.
    Finally, the score for the remaining off-diagonal entries is off_diag_score.
    """
    scoring_matrix = {}
    scoring_matrix['-'] = {'-': dash_score}
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

    dp_table = [[0 for dummy_idx in range(len_y + 1)] for dummy_idx in range(len_x + 1)]

    for row_index in range(1, len_x + 1):
        dp_table[row_index][0] = dp_table[row_index - 1][0] + scoring_matrix[seq_x[row_index - 1]]['-']
        if (dp_table[row_index][0] < 0) and (global_flag == False):
            dp_table[row_index][0] = 0

    for col_index in range(1, len_y + 1):
        dp_table[0][col_index] = dp_table[0][col_index - 1] + scoring_matrix['-'][seq_y[col_index - 1]]
        if (dp_table[0][col_index] < 0) and (global_flag == False):
            dp_table[0][col_index] = 0

    for row_index in range(1, len_x + 1):
        for col_index in range(1, len_y + 1):
            diag = dp_table[row_index - 1][col_index - 1] + scoring_matrix[seq_x[row_index - 1]][seq_y[col_index - 1]]
            upper = dp_table[row_index][col_index - 1] + scoring_matrix['-'][seq_y[col_index - 1]]
            left = dp_table[row_index - 1][col_index] + scoring_matrix[seq_x[row_index - 1]]['-']

            dp_table[row_index][col_index] = max(upper, max(diag, left))
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

    while row_index != 0 and col_index != 0:
        if alignment_matrix[row_index][col_index] == alignment_matrix[row_index - 1][col_index - 1] + \
                scoring_matrix[seq_x[row_index - 1]][seq_y[col_index - 1]]:
            new_seq_x = seq_x[row_index - 1] + new_seq_x
            new_seq_y = seq_y[col_index - 1] + new_seq_y
            row_index -= 1
            col_index -= 1
        else:
            if alignment_matrix[row_index][col_index] == alignment_matrix[row_index - 1][col_index] + \
                    scoring_matrix[seq_x[row_index - 1]]['-']:
                new_seq_x = seq_x[row_index - 1] + new_seq_x
                new_seq_y = '-' + new_seq_y
                row_index -= 1
            else:
                new_seq_x = '-' + new_seq_x
                new_seq_y = seq_y[col_index - 1] + new_seq_y
                col_index -= 1

    while row_index != 0:
        new_seq_x = seq_x[row_index - 1] + new_seq_x
        new_seq_y = '-' + new_seq_y
        row_index -= 1
    while col_index != 0:
        new_seq_x = '-' + new_seq_x
        new_seq_y = seq_y[col_index - 1] + new_seq_y
        col_index -= 1

    return (score, new_seq_x, new_seq_y)


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
    for dummy_idx_i in range(row_index + 1):
        for dummy_idx_j in range(col_index + 1):
            if alignment_matrix[dummy_idx_i][dummy_idx_j] > score:
                score = alignment_matrix[dummy_idx_i][dummy_idx_j]
                start_i = dummy_idx_i
                start_j = dummy_idx_j

    new_seq_x = ""
    new_seq_y = ""
    row_index = start_i
    col_index = start_j

    while row_index != 0 and col_index != 0:
        if alignment_matrix[row_index][col_index] == alignment_matrix[row_index - 1][col_index - 1] + \
                scoring_matrix[seq_x[row_index - 1]][seq_y[col_index - 1]]:
            new_seq_x = seq_x[row_index - 1] + new_seq_x
            new_seq_y = seq_y[col_index - 1] + new_seq_y
            row_index -= 1
            col_index -= 1
        else:
            if alignment_matrix[row_index][col_index] == alignment_matrix[row_index - 1][col_index] + \
                    scoring_matrix[seq_x[row_index - 1]]['-']:
                new_seq_x = seq_x[row_index - 1] + new_seq_x
                new_seq_y = '-' + new_seq_y
                row_index -= 1
            else:
                new_seq_x = '-' + new_seq_x
                new_seq_y = seq_y[col_index - 1] + new_seq_y
                col_index -= 1
        if alignment_matrix[row_index][col_index] == 0:
            break

    while row_index != 0:
        if alignment_matrix[row_index][0] == 0:
            break
        new_seq_x = seq_x[row_index - 1] + new_seq_x
        new_seq_y = '-' + new_seq_y
        row_index -= 1
    while col_index != 0:
        if alignment_matrix[0][col_index] == 0:
            break
        new_seq_x = '-' + new_seq_x
        new_seq_y = seq_y[col_index - 1] + new_seq_y
        col_index -= 1

    return (score, new_seq_x, new_seq_y)


def check_spelling(checked_word, dist, word_list):
    res = set([])
    alphabet = set(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])
    score_matrix = build_scoring_matrix(alphabet,2,1,0)
    for word in word_list:
        g_alignment_m = compute_alignment_matrix(checked_word, word, score_matrix,True)
        score_tup = compute_global_alignment(checked_word, word, score_matrix, g_alignment_m)
        new_dist = len(checked_word) + len(word) - score_tup[0]
        if new_dist<= dist:
            res.add(word)

    return res

def cal_per(str1,str2):
    total = len(str1)
    match = 0.0
    for index,char in enumerate(str1):
        if char == str2[index]:
            match += 1
    return (match/total)*100

def generate_null_distribution(seq_x, seq_y, scoring_matrix, num_trials):
    scoring_distribution = {}
    rand_y = list(seq_y)
    for dummy_idx in range(num_trials):
        random.shuffle(rand_y)
        local_alignment_g = compute_alignment_matrix(seq_x, "".join(rand_y), scoring_matrix, False)
        tup = compute_local_alignment(seq_x, "".join(rand_y), scoring_matrix, local_alignment_g)
        score = tup[0]
        score_list.append(score)
        if score not in scoring_distribution:
            scoring_distribution[score] = 1
        else:
            scoring_distribution[score] += 1

        if dummy_idx%100 == 0:
            print(dummy_idx)

    return scoring_distribution




###################################################################
##############################TESTING##############################
###################################################################

human_protein = read_protein(HUMAN_EYELESS_URL)
fruitely_protein = read_protein(FRUITFLY_EYELESS_URL)
scoring_matrix = read_scoring_matrix(PAM50_URL)

#print(scoring_matrix)
alignment_matrix = compute_alignment_matrix(human_protein, fruitely_protein, scoring_matrix, False)
#print(alignment_matrix)
local_alignment = compute_local_alignment(human_protein, fruitely_protein, scoring_matrix, alignment_matrix)

print(local_alignment[0])
#print(local_alignment[1])
#print(local_alignment[2])

local_human = ""
for dummy_idx in range(135):
    local_human += (random.choice(list("ACBEDGFIHKMLNQPSRTWVYXZ")))

print(local_human)
#local_human = "HSGVNQLGGVFVNGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATPEVVSKIAQYKRECPSIFAWEIRDRLLSEGVCTNDNIPSVSSINRVLRNLASEKQQ"
local_fruitely = local_alignment[2]

c_pax_domain = read_protein(CONSENSUS_PAX_URL)
#print(c_pax_domain)

alignment_matrix = compute_alignment_matrix(local_human, c_pax_domain, scoring_matrix, True)
global_c_pax = compute_global_alignment(local_human, c_pax_domain, scoring_matrix, alignment_matrix)
#
# print(global_c_pax[0])
# print(global_c_pax[1])
# print(global_c_pax[2])

res1 = cal_per(global_c_pax[1] , global_c_pax[2])
print("Human match : ",res1)

alignment_matrix = compute_alignment_matrix(local_fruitely, c_pax_domain, scoring_matrix, True)
global_c_pax_f = compute_global_alignment(local_fruitely, c_pax_domain, scoring_matrix, alignment_matrix)

# print(global_c_pax_f[0])
# print(global_c_pax_f[1])
# print(global_c_pax_f[2])

res1 = cal_per(global_c_pax_f[1],global_c_pax_f[2])
print(res1)




score_list = []

scoring_dist = generate_null_distribution(human_protein, fruitely_protein, scoring_matrix, 10)

x_score = scoring_dist.keys()
y_val = []
score_sum = 0
for item in x_score:
    y_val.append(scoring_dist[item] / 1000.0)

for item in score_list:
    score_sum += item

mean = score_sum / 1000.0
print("Mean : ",mean)

sd_sum = 0
for sc in score_list:
    sd_sum += (sc - mean) ** 2

sd = (sd_sum / 1000.0) ** (0.5)
print("SD : ",sd)

z_score = (875 - mean) / (sd)
print("Z score : ",z_score)


matplotlib.rc('figure', figsize=(16, 8))

plt.bar(x_score, y_val)
plt.title("Null distribution for Hypothesis testing using 1000 trials")
plt.xlabel("Scores")
plt.ylabel("Fraction of trials")
#plt.show()
plt.savefig('Question_4_bar_2.png')



word_list = read_words(WORD_LIST_URL)

ans8 = check_spelling("firefly",2,word_list)

print(ans8)
