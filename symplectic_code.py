### I. GENERAL STUFF IN TYPE A ###

# I.1. Set of columns in A_n

def design_columns_less_than_n(n):
    Cols = list()
    Cols.append([])
    for i in range(1,n+1):
        for j in range(len(Cols)):
            Cols.append(Cols[j]+[i])
    return Cols

# I.2. Set of words in A_n of length k

def design_words_of_size_k(n, k, Words = [[]]):
    if k == 0:
        return Words
    temp_Words = [ word for word in Words ]
    Words = []
    for word in temp_Words:
        for i in range(1,n+1):
            Words.append(word + [i])
    return design_words_of_size_k(n, k-1, Words)





### II. ADMISSIBILITY IN TYPE C ###

## General remarks##
##	a) Here I realize the alphabet C_n as {1, 2, ..., n, n+1, ..., 2n}, that is \bar{k} = 2n - k + 1 for 1 <= k <= n.
##	b) The general problem is: Given a column A in C_n, check if it is admissible. This is done by checking the admissibility conditions for each 1 <= i <= n, i.e. if cardinality of N_i(A) = { x in A | x <= i or x >= i} <= i.
##	c) Usually I am interested in A being a column, but this is not specified in the code, as the admissibility condition can be phrased for any word
##	d) To phrase the admissibility condition I do a lot of (likely unnecessary) smaller functions


## II.1. Subword of A with letters x <= i

def i_subcol_of_col(A,i):
    isubcol = list()
    for j in range(len(A)):
        if A[j] <= i:
            isubcol.append(A[j])
    return isubcol

## II.2. Subword of A in C_n with letters x >= \bar{i}

def i_subcol_top_side(A,n,i):
    isubcol_topside = list()
    for j in range(len(A)):
        if 0 < 2*n-A[j]+1<= i:
            isubcol_topside.append(A[j])
    return isubcol_topside

## II.3. For word A in C_n, cardinality of N_i(A)

def how_admissible_for_i(A,n,i):
    l = 0
    for j in range(1,2*n+1):
        if ((j <= i) or (j>=2*n-i+1)) and (j in A):
            l +=1
    return l

## II.4. Checks if N_i(A) <= i

def i_admissibility(A,n,i):
    if len(i_subcol_of_col(A,i))+len(i_subcol_top_side(A,n,i))<=i:
        return 1
    else:
        return 0

## II.5. Counts how many i satisfy N_i(A) <= i

def admissibility_count(A,n):
    j = 0
    for i in range(1,n+1):
        j = j+i_admissibility(A,n,i)
    return j

## II.6. Checks admissibility of a column A in C_n

def is_admissible(A,n):
    if len(A) == 0:
        return True
    if admissibility_count(A,n) == n:
        return True
    else:
        return False

## II.7. Produces the set of admissible columns in C_n

def admissible_columns_n(n):
    admcols = list()
    for A in design_columns_less_than_n(2*n):
        if is_admissible(A,n) == True:
            admcols.append(A)
    return admcols






### III. ROOT OPERATORS ###
 
## General remarks: Here I define the Kashiwara operators e_i and f_i. In particular, there are functions to identify highest weight of a given word, as well as its connected component.

## III.1. defines the root operator f_i in C_n

def word_operator_f(word,n, i):
    i_indices = []
    for ind, letter in enumerate(word):
        if letter == i or letter == 2*n - i:
            i_indices.append(ind)
        elif letter == i + 1 or letter == 2*n - i + 1:
            if len(i_indices) > 0:
                i_indices.pop()
    if len(i_indices) == 0:
        return -1
    result_word = [x for x in word]
    if word[i_indices[0]] == i:
        result_word[i_indices[0]] = i+1
    else:
        result_word[i_indices[0]] = 2*n-i+1
    return result_word


## III.2. gives the root operator e_i on C_n

def word_operator_e(word,n, i):
    i_indices = []
    word_prim = list(reversed((word)))
    for ind, letter in enumerate(word_prim):
        if letter == i+1 or letter == 2*n - i+1:
            i_indices.append(ind)
        elif letter == i or letter == 2*n - i:
            if len(i_indices) > 0:
                i_indices.pop()
    if len(i_indices) == 0:
        return -1
    result_word_prim = [x for x in word_prim]
    if word_prim[i_indices[0]] == i+1:
        result_word_prim[i_indices[0]] = i
    else:
        result_word_prim[i_indices[0]] = 2*n-i
    return list(reversed((result_word_prim)))

## III.3. creates a list of { i | f_i.A is defined }

def when_f_applies(A,n):
    sequence = list()
    for i in range(1,n+1):
        if word_operator_f(A,n,i) != -1:
            sequence.append(i)
    return sequence

## III.4. creates a list of { i | e_i.A is defined}

def when_e_applies(A,n):
    sequence = list()
    for i in range(1,n+1):
        if word_operator_e(A,n,i) != -1:
            sequence.append(i)
    return sequence

## III.5. Defines the function phi_i = cardinality of { f_i.A, f_i^2.A, ... }

def phi_function_i(A,n,i):
    X = list()
    X.append(A)
    for j in range(len(A)):
        if word_operator_f(X[j],n,i) != -1:
            X.append(word_operator_f(X[j],n,i))
    return len(X)-1

## III.6. Defines the function epsilon_i = cardinality of { e_i.A, e_i^2.A, ... }

def epsilon_function_i(A,n,i):
    X = list()
    X.append(A)
    for j in range(len(A)):
        if word_operator_e(X[j],n,i) != -1:
            X.append(word_operator_e(X[j],n,i))
    return len(X)-1

## III.7. Produces set of a) lowest weight admissible columns; b) lowest weight words of length k in C_n

def lowest_weight_cols_C(n):
    lw = list()
    for A in admissible_columns_n(n):
        if len(when_f_applies(A,n)) == 0:
            lw.append(A)
    return lw

def lowest_weight_words_size_k_C(n,k):
    lw = list()
    for A in design_words_of_size_k(n,k, Words = [[]]):
        if len(when_f_applies(A,n)) == 0:
            lw.append(A)
    return lw

## III.8. Produces set of a) highest weight admissible columns; b) highest weight words of length k in C_n

def highest_weight_cols_C(n):
    hw = list()
    for A in admissible_columns_n(n):
        if len(when_e_applies(A,n)) == 0:
            hw.append(A)
    return hw

def highest_weight_words_size_k_C(n,k):
    hw = list()
    for A in design_words_of_size_k(n,k, Words = [[]]):
        if len(when_e_applies(A,n)) == 0:
            hw.append(A)
    return hw

## III.9. Computes list of words obtained by applying f operators to a given word A

def connected_component_of_f_side(A,n):
    connected = list()
    connected.append(A)
    for A in connected:
        for i in range(1,n+1):
            if (word_operator_f(A,n,i) != -1) and (word_operator_f(A,n,i)) not in connected:
                connected.append(word_operator_f(A,n,i))
    return connected

## III.10. Computes list of words obtained by applying e operators to a given word A

def connected_component_of_e_side(A,n):
    connected = list()
    connected.append(A)
    for A in connected:
        for i in range(1,n+1):
            if (word_operator_e(A,n,i) != -1) and (word_operator_e(A,n,i)) not in connected:
                connected.append(word_operator_e(A,n,i))
    return connected


## III.11. Computes the highest weight word for a given word w

def highest_weight_of_a_word(w,n):
    connected = connected_component_of_e_side(w,n)
    hw = connected[len(connected)-1]
    return hw

## III.12. Computes the connected component of a word w

def connected_component(A,n):
    A_prim = highest_weight_of_a_word(A,n)
    B = connected_component_of_f_side(A_prim,n)
    return B






#### IV. INSERTION ####

## General remarks:
##	a) Here I code the insertion of a letter into a column. The main mathematical reference for this is Lecouvey's article on Pl(C_n) from 2002.
##	b) I have two insertion algorithms, insert1 and insert2. I am not sure why

## IV.1. Gives a list/path in the crystal graph from word A to its highest weight A^0

def newthing(A,n):
    connected = list()
    connected.append(A)
    for A in connected:
        for i in range(1,n+1):
            if (word_operator_e(A,n,i) != -1) and (word_operator_e(A,n,i)) not in connected:
                connected.append(word_operator_e(A,n,i))
                break
    return connected

## IV.2. Gives the labels of the edges in the path newthing(A,n)

def path_to_HW(A,n):
    manja = list()
    T = newthing(A,n)
    for j in range(len(T)-1):
        for i in range(1,n+1):
            if T[j+1] == word_operator_e(T[j],n,i):
                manja.append(i)   
                break         
    return manja

## IV.3. Here for a list of indices A = [ i_1, i_2, ..., i_k ], and B a word in C_n, the applies f_{i_j} consecutively to B, for j = 1, 2, ..., k. One may think of A as being path_to_HW(B,n)

def new_word_operator_f(A,B,n):
    X = list()
    X.append(B)
    for i in range(len(A)):
        if word_operator_f(X[i],n,A[i]) != -1:
            X.append(word_operator_f(X[i],n,A[i]))
    return X[len(X)-1]


## IV.4. Defines the insertion of a letter x into a column A
## More detail: For an admissible column A, and a letter x in C_n, the highest weight of the word w = Ax has one of the following forms w^0 = 12...p1, or w^0 = 12...p(p+1), or w^0 = 12...p \bar{p}. This function checks precisely in which case we are.

def ins_type(A,n,x):
    B = [t for t in A]
    B.append(x)
    HW_B = highest_weight_of_a_word(B,n)
    path = path_to_HW(B,n)
    sympath = list(reversed((path)))
    B_prim = [t for t in range(1,len(B))]
    x_0 = HW_B[len(B)-1]
    D = []
    H = []
    if len(A) == 0:
        D.append(x)
        return D, H
    if (x > A[len(A)-1]) and (is_admissible(B,n)):
        return B, H
    if (x > A[len(A)-1]) and (not is_admissible(B,n)):
        for j in range(1,n+1):
            if (j in B) and (2*n-j+1 in B) and (how_admissible_for_i(B,n,j) == j+1):
                D.append(j)
                D.append(2*n-j+1)
                E = [t for t in B if t not in D]
                return E, H
    else: 
        G = [t for t in B_prim]
        G_prim = list(reversed((G)))
        G_prim.append(1)
        G_second = list(reversed((G_prim)))
        G_dritte = new_word_operator_f(sympath,G_second,n)
        H.append(G_dritte[0])
        G_dritte.pop(0)
        return G_dritte, H
    
## IV.5. Defines one part of the insertion

def insert_1(A,B,n):
    X = list()
    X.append(A)
    Y = list()
    Y.append([])
    for i in range(len(B)):
        D, E = ins_type(X[len(X)-1],n,B[i])
        X.append(D)
        if len(E) > 0:
            F, G = ins_type(Y[len(Y)-1],n,E[0])
            Y.append(F)
    return X[len(X)-1], Y[len(Y)-1]






#### V. CONFLUENCE ####

## V.1. swaps a couple of columns

def swap(A, B):
    new_A = B
    new_B = A
    return new_A, new_B

## V.2. checks if two columns form a standard tableau

def is_standard(A,B,n):
    C, D = insert_1(A,B,n)
    if len(A) == 0 or len(B) == 0:
        return True
    elif (C == B and A == D):
        return True
    else:
        return False

## V.3. computes right reduction length
## More detail: For two columns A, B, denote the insertion of B into A by (A <-- B). This function computes the length of the rewriting path ABC ===>_1 (A <-- B) C = A'B'C ===>_2 A' (B' <-- C) = A'B''C' ===>_3 (A' <-- B'') C' ......

def right_computation(A, B, C,n):
    i = 0 
    while (not is_standard(A, B,n)):
        i += 1
        B, A = insert_1(A,B,n)
        while (not is_standard(B,C,n)):
            i+=1
            C, B = insert_1(B,C,n)
            if len(B) == 0:
                B, C = swap(B,C)
    return i

## V.4. computes left reduction length
## More details: This function computes the length of the rewriting path ABC ===>_1 A (B <-- C) = AB'C' ===>_2 (A <-- B') C' = A'B''C ===>_3 A' (B'' <-- C') ......

def left_computation(A, B, C,n):
    i = 0 
    while (not is_standard(B, C,n)):
        i += 1
        C, B = insert_1(B,C,n)
        if len(B) == 0:
            B, C = swap(B,C)
        while (not is_standard(A,B,n)):
            i+=1
            B, A = insert_1(A,B,n)
    return i

## V.5. Computes the set of right (and left) reduction lengths for all triples of columns A, B, C.
## NOTE: This is very slow.

def set_of_right_lengths(Cols,n):
    setofredlengths = list()
    for A in Cols:
        for B in Cols:
            for C in Cols:
                setofredlengths.append((right_computation(A,B,C,n)))
    return setofredlengths

def set_of_left_lengths(Cols,n):
    setofredlengths = list()
    for A in Cols:
        for B in Cols:
            for C in Cols:
                setofredlengths.append((left_computation(A,B,C,n)))
    return setofredlengths




























