import time
import threading


def Fibonacci_Recursion_tool(n):
	if n <= 0:
		return 0
	elif n == 1:
		return 1
	else:
		return Fibonacci_Recursion_tool(n - 1) + Fibonacci_Recursion_tool(n - 2)


def Fibonacci_Recursion(n, k):
	o = threading.currentThread()
	print(o.getName())
	result_list = []
	for i in range(1, int(n) + 1):
		result_list.append(Fibonacci_Recursion_tool(i))
	print(result_list)
	# return result_list


def Print(n):
	print(n)


if __name__ == '__main__':
	t = threading.Thread(target=Fibonacci_Recursion, args=('35', '0'))
	print(time.ctime())
	# k = Fibonacci_Recursion(36)
	t.start()
	Print(10)
	print(time.ctime())
