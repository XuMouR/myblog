from django.test import TestCase


# Create your tests here.

# *args **kwargs 的区别及其使用

#

# def func04(*args,a,b):
#     print("func04>>",a,b,args)
# func04(1,2,a=5,b=7)


# *args用于接受动态参数 a,b这种，*args 接受参数后，打印args的结果是一个元组 ()
# **kwargs用于接受动态关键字参数，打印kwargs  结果为一个字典
# def func(**kwargs):
#     print(kwargs)
# func(a=1, b=3, c=78)
dic={"a":1,"b":2,"c":3}
ret=dic.get("a")
print(ret)