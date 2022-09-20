# -*- coding:UTF-8 -*-
import jpype
from jpype import *
import os.path

jarpath = os.path.abspath('.') #这个函数__用来获取当前 python 脚本所在的绝对路径

jpype.startJVM(r'C:\Program Files\Java\jdk-17.0.4\bin\server\jvm.dll', "-ea", r"-Djava.class.path=C:\Users\lianqinglongfei\Desktop\DyItemSpider\android\com\test.jar")

JDClass = JClass("test")

jd = JDClass()
# jprint = java.lang.System.out.println #申请 Java 输出类的输出函数
# jprint(jd.sayHello("waw")) #调用该类中的 sayHello 函数，并用 Java 输出函数打印 Java 返回值
# jprint(jd.calc(2, 4)) #调用该类中的求和函数，并用 Java 输出函数打印 Java 返回值

#关闭 Java 虚拟机，可写可不写，不写会在程序结束时自动关闭
jpype.shutdownJVM()
