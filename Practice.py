import numpy as np
import pandas as pd

# # 1.Reverse a String
# def string(s):
#     a= s[::-1]
#     print(a)
    
# b=input("enter a string: ")
# string(b)


# # 2.Given a positive integer num, write a function that returns true if num is a perfect square else false.
# def perfectsq(a):
  
#     if a<0:
#         return "enter valid no"
    
#     b=int(a**0.5)
#     if b*b==a:
#         return True
#     else:
#         return False

# n=int(input("enter the no : "))
# print(perfectsq(n))


# # 3.Given an integer array arr[], find the subarray (containing at least one element) which has the maximum possible sum, and return that sum.
# def max_subarray_sum(arr):
    
#     current_sum = arr[0]
#     max_sum = arr[0]

#     start = 0          # start index of current subarray
#     end = 0            # end index of max subarray
#     temp_start = 0     # temporary start index

#     for i in range(1, len(arr)):
#         if arr[i] > current_sum + arr[i]:
#             current_sum = arr[i]
#             temp_start = i   
#         else:
#             current_sum += arr[i]

#         if current_sum > max_sum:
#             max_sum = current_sum
#             start = temp_start
#             end = i

#     return max_sum, arr[start:end+1]

# arr = np.array(list(map(int, input("Enter numbers: ").split())))
# print(arr)
# max_sum, subarray = max_subarray_sum(arr)
# print("Subarray:", subarray)
# print("Maximum Sum:", max_sum)


# # 4.Check if Two Strings Are Anagrams
# s = input("enter 1st string: ").lower()
# t = input("enter 2nd string: ").lower()
# if len(s) == len(t):
#     cnt = {}
#     for ch in s:
#         cnt[ch] = cnt.get(ch, 0) + 1
#     for ch in t:
#         if cnt.get(ch, 0) == 0:
#             print(False)
#             break
#         cnt[ch] -= 1
#     else:
#         print(True)
# else:
#     print(False)

# # OR

# s = input("Enter 1st string: ").lower()
# t = input("Enter 2nd string: ").lower()
# if len(s) != len(t):
#     print(False)
# else:
#     for ch in set(s):
#         if s.count(ch) != t.count(ch):
#             print(False)
#             break
#     else:
#         print(True)

# OR

# from collections import Counter
# s = input("Enter 1st string: ").lower()
# t = input("Enter 2nd string: ").lower()
# print(Counter(s) == Counter(t))


# # Given an integer array arr, write a function that returns true if the number of occurrences of each value in the array is unique, otherwise return false.
# def unique_occurrences(arr):
#     count = {}
#     # Step 1: count occurrences
#     for num in arr:
#         count[num] = count.get(num, 0) + 1
#     # Step 2: check if frequencies are unique
#     frequencies = list(count.values())
#     return len(frequencies) == len(set(frequencies))
# arr = list(map(int, input("Enter array elements separated by space: ").split()))
# result = unique_occurrences(arr)
# print("Array:", arr)
# print("Are occurrences unique?", result)

# OR

# def unique_occurrences(arr):
#     count = {}
#     for num in arr:
#         if num in count:
#             count[num] += 1
#         else:
#             count[num] = 1
#     freq = list(count.values())
#     return True
# arr = list(map(int, input("Enter array elements separated by space: ").split()))
# result = unique_occurrences(arr)
# print("Array:", arr)
# print("Are occurrences unique?", result)



