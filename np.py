import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

# data = {
#     "name": ["Amit", "Rahul", "Neha", "Pooja"],
#     "age": [25, 30, 28, 22],
#     "city": ["Delhi", "Mumbai", "Pune", "Chennai"]
# }
# df = pd.DataFrame(data, index=[101, 102, 103, 104])
# print(df)
'''# Select row with index label 102
print(df.loc[102])
# Select multiple rows
print(df.loc[[101, 103]])
# Select specific rows & columns
print(df.loc[101:103, ["name", "age"]])'''

'''# First row
print(df.iloc[0])
# First 2 rows
print(df.iloc[0:2])
# Rows and columns by position
print(df.iloc[0:3, 0:2])'''

# print(df.loc[df["age"] > 25])

df = pd.read_csv("students.csv")
'''print(df.head())     # first 5 rows
print(df.tail())     # last 5 rows
print(df.shape)      # rows, columns
print(df.columns)    # column names
print(df.info())     # data types'''

# print(df[["Name", "Marks"]])

# print(df[(df["Marks"] > 70) & (df["Age"] < 22)])

# print(df.sort_values("Marks"))
# print(df.sort_values("Marks", ascending=False))

# print(df.isnull().sum())
#print(df["Marks"].fillna(0, inplace=True))
# print(df.dropna(inplace=True))
# print(df)

#print(df.groupby("Age")["Marks"].mean())

'''df["Result"] = df["Marks"].apply(lambda x: "Pass" if x >= 40 else "Fail")
print(df)

plt.bar(df["Name"], df["Marks"])
plt.show()'''

#print(df.groupby("Age")["Marks"].agg(["mean", "max", "min"]))

# df["Grade"] = df["Marks"].apply(
#     lambda x: "A" if x >= 80 else "B")
# print(df)

# print(df.drop("Age", axis=1, inplace=True))
# print(df)

# print(df.duplicated())
#df.drop_duplicates(inplace=True)
# print(df)

print(df["Age"].value_counts())













