# class Coordinate(object):
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#     def __repr__(self):
#         return "Coord: " + str(self.__dict__)
# def add(a, b):
#     return Coordinate(a.x + b.x, a.y + b.y)
# def sub(a, b):
#     return Coordinate(a.x - b.x, a.y - b.y)
#
# def wrapper(func):
#     def checker(a, b): # 1
#         if a.x < 0 or a.y < 0:
#             a = Coordinate(a.x if a.x > 0 else 0, a.y if a.y > 0 else 0)
#         if b.x < 0 or b.y < 0:
#             b = Coordinate(b.x if b.x > 0 else 0, b.y if b.y > 0 else 0)
#         ret = func(a, b)
#         if ret.x < 0 or ret.y < 0:
#             ret = Coordinate(ret.x if ret.x > 0 else 0, ret.y if ret.y > 0 else 0)
#         return ret
#     return checker
#
#
# one = Coordinate(100, 200)
# two = Coordinate(300, 200)
# add = wrapper(add)
# sub = wrapper(sub)
# sub(one, two)
#
#
#
# def improve(func):
#     def inner(*args, **kwargs):
#         print('Improved version, {}, {}'.format(args,kwargs))
#         return func(*args, **kwargs)
#     return inner()
#
# '''
# Another example
# '''
#
# def entry_exit(f):
#     def new_f():
#         print("Entering", f.__name__)
#         f()
#         print("Exited", f.__name__)
#     return new_f
#
# @entry_exit
# def func1():
#     print("inside func1()")
#
# @entry_exit
# def func2():
#     print("inside func2()")
#
# func1()
# func2()
# print(func1.__name__)
#
#
#
def check_include_exclude(self, func):
    def inner(func):
        run_list = []
        if include_list is None:
            include_list = list(self.wlcs.keys())
        if exclude_list is not None:
            include_list = [wlc_name for wlc_name in include_list if wlc_name not in exclude_list]
        return func

    return inner

def print_run_list(include_list=None, exclude_list=None):
    '''
    Dummy function to check parameters
    :param include_list:
    :param exclude_list:
    :return:
    '''
    print(include_list)

