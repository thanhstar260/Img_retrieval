def combine_3results(A: list, B: list, C: list, K, w_A=1, w_B=2, w_C=2):
    results = {}
    D = A+B+C
    # D = set(D)
    # print(D)
    for i in range(len(D)):
        results[D[i]] = 0

    length = len(A)
    for i in range(length):
        # print(results[A[i]] + w_A)
        results[A[i]] += (length-i)*w_A
        results[B[i]] += (length-i)*w_B    
        results[C[i]] += (length-i)*w_C

    sorted_keys = sorted(results.items(), key=lambda x: x[1],reverse=True)[:K]
    # sorted_keys = sorted(results.keys(), key=lambda x: results[x], reverse=True)[:K]
    return sorted_keys

def combine_2results(A:list,B:list,K,w_A=1,w_B=2):
    results = {}
    D = A+B
    # D = set(D)
    # print(D)
    for i in range(len(D)):
        results[D[i]] = 0

    length = len(A)
    for i in range(length):
        # print(results[A[i]] + w_A)
        results[A[i]] += (length-i)*w_A
        results[B[i]] += (length-i)*w_B    

    sorted_keys = sorted(results.items(), key=lambda x: x[1],reverse=True)[:K]
    # sorted_keys = sorted(results.keys(), key=lambda x: results[x], reverse=True)[:K]
    return sorted_keys


if __name__ == "__main__":

    A = [1, 2, 3, 4, 5]
    B = [2, 4, 6, 8, 10]
    C = [3, 6, 9, 12, 15]

    K = 5
    w_A = 1
    w_B = 2
    w_C = 2

    results3 = combine_3results(A, B, C, w_A=w_A, w_B=w_B, w_C=w_C,K = K)
    results2 = combine_2results(A, B, w_A=w_A, w_B=w_B,K = K)

    print(results3)
    print(results2)

