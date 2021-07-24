import random


teacher = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

classroom = [[], [], []]

# 方式1，但存在着list为空的情况
# for t_index in range(len(teacher)):
# 	tmp = random.choice(teacher)
# 	c_index = random.randint(0, len(classroom) - 1)
# 	teacher.remove(tmp)
# 	classroom[c_index].append(tmp)

# 方式2，
random.shuffle(teacher)
i = random.randint(1, len(teacher) - 2)
j = random.randint(1, len(teacher) - i - 1)
k = len(teacher) - i - j

num = [i, j, k]

for num_index in range(len(num)):
	for t_index in range(num[num_index]):
		classroom[num_index].append(teacher.pop())

print(classroom)
