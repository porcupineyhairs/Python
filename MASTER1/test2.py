students = [[3, 'Jack', 12], [2, 'Rose', 13], [1, 'Tom', 10], [5, 'Sam', 12], [4, 'Joy', 8]]
students = sorted(students, key=(lambda x: x[0]))
print(students)
