def solution(A):
    # write your code in Python 3.6
    count = 0
    for i in range(len(A)):
        maximum = max(A[0:i+1])
        if i != len(A)-1:
            if maximum < A[i+1]:
                count += 1

    return count


a = [2,1,6,4,3,7]
print(solution(a))
