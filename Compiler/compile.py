from distutils.core import setup
from Cython.Build import cythonize
setup(
    ext_modules=cythonize("MsSql.py")  # 注意这里推荐使用相对路径，编译出的so文件在引用其他模块时可能会出现路径问题
)
