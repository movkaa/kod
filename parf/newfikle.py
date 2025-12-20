# class kot: #класс шаблон для обедка
#     def __init__(self,name,xBocT): 
#         self.name=name # атруюбты эты обекты которые сожержат эа перемнные которорыне перенадджлжеэать 
#         self.xBocT=xBocT # селф это ссссылока на текущий обект
#     def weow(self):
#         return f"{self.name} говорит мяу" 
# kot1 = kot("сем","нет") # оюкт который сожедритт атриьут 
# print(kot1.weow())

class animal: 
    def __init__(self, name):
     self.name = name

class dog(animal):
    def __init__(self, name, age):
        super().__init__(name)
        self.age = age

    def bark(self):
        print(f"{self.name}: Гаф!")

dog1 = dog('Бобоик', 99)
dog1.bark()
dog2 = dog ("ЙОц", 3)
dog2.bark()