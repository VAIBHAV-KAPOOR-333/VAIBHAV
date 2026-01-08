import numpy as np
import pandas as pd

'''numbers = [1, 2, 3, 4]
print(numbers)

arr = np.array([1, 2, 3, 4])
print(arr)

arr = np.array([1, 2, 3, 4])
print(arr + 10)
print(arr * 2)'''

'''arr = np.array([1, 2, 3, 4])
print(arr.shape)   # size
print(arr.dtype)   # data type'''

# np.zeros(5)
# np.ones(5)
# np.arange(1, 10)
# np.arange(1, 10, 2)

'''matrix = np.array([
    [1, 2, 3],
    [4, 5, 6]
])

print(matrix)
print(matrix[1][1])  

arr = np.array([10, 20, 30])
print(arr.sum())
print(arr.mean())
print(arr.max())
print(arr.min())'''

# arr = np.array([5, 10, 15, 20])
# print(arr * 3)
# print(arr.mean())

'''data = {
    "Name": ['Alex', 'Bob', 'Charlie'],
    "Age": [20, 22, 21],
    "Marks": [80, 75, 90],
    "N": ['A', 'B', 'C']
}
df = pd.DataFrame(data)
print(df)
print(df["Name"])
print(df["Marks"])
print(df["Age"])
print(type(df['N']))

print(df.loc[0])   # first row
print(df.iloc[1])  # second row

df["Passed"] = df["Marks"] >= 40
print(df)

print(df["Marks"].mean())
print(df["Marks"].max())

print(df[df["Marks"] >= 80])'''

# df = pd.read_csv("students.csv")
# print(df)
# df.to_csv("output.csv", index=False)











