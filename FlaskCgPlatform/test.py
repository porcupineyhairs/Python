from functools import wraps


def decorator(func):
	@wraps(func)
	def inner_func():
		inner_obj = 'inner_obj'
		print("ininner_func:{}".format(inner_obj))
		return func(inner_obj)
	return inner_func


@decorator
def func_with_param(*args):
	print("infunc_with_parm:{}".format(args[0]))


func_with_param()  # 调用
