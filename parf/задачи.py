# a=str(input("напиши любую сторку "))
# print(a+"!")
# print(f"{a}!")

# a=str(input("напиши любую сторку "))
# print(a[::-1])

# a=str(input("секретное слово "))
# print(len(a), a[2])

# a=str(input("напиши что то "))
# print(a.upper())  

# a=str(input("пиши "))
# print(a*3)

# a=int(input("напиши сумму"))
# b=int(input("напиши процент чаевых"))
# c=a/100
# e=c*b
# w=a+e
# print(w)

# a=int(input("введите минуты"))
# b=a*60
# print(b)

# a=int(input("введите число"))
# b=a*a
# c=a*a*a
# print(b,c)

# a=str(input("введите имя"))
# b=str(input("введите фамилию"))
# print(a[0]+b[0])

# a=input("введите слово ")
# x=["у","е","а","э","я","и","ю"]
# b=0
# for i in a:
#     if i in x:
#         b+=1
# print(b)

# a={"Россия":"Москва","Америка":"Вашингтон"}
# p=str(input("введите страну: "))
# print(a.get(p, "нет данных"))

# prod=[]
# for i in range(5):
#     a=str(input("введите товар "))
#     prod.append(a)

# for i,prod in enumerate(prod):
#     print(i,prod)

# chis=[]
# for i in range(5):
#     a=int(input("введите число "))
#     chis.append(a)
# print(chis)
# print(chis[::-1])

# arr = []
# for i in range(3):
#     a=int(input("Введите оценку: "))
#     arr.append(a)
# d=sum(arr)
# c=d/3
# print(round(c,1))

# b=["яблоко", "лимон", "хлеб"]
# a=str(input("Ведите слово "))
# if a in b:
#     print("есть")
# else:
#     print("нет")

# a=int(input("сумму"))
# if a % 100 == 0:
#     print("делится")
# else:
#     print("не делится")

# for i in range(1, 11):
#     print(i, i**2)

# a=int(input("Ваедите число"))     
# for i in range(a,0,-1):
#     print(i)

# a=int(input("Ваедите число "))
# b=1
# for c in range(1,a+1):
#     b*=c
# print(b) 

# a=str(input("Ваедите предложения "))
# c=a.split()
# b=len(c)
# print(b)

# import random 
# x=[]
# for i in range(1,6):
#     a=random.randint(1, 10)
#     x.append(a)
# print(x)
# print(sum(x),min(x),max(x))


# import random
# x=["марк","пётр"]
# c=["идёт","ест","прогоняют"]
# v=["из магазина","с лавки"]
# print(random.choice(x),(random.choice(c)),(random.choice(v)))

# a=int(input("введите градусы цельсия"))
# c=a*9/5+32
# print(c)

# import random
# a=int(input("Сколько раз подбросить монетку?"))
# resh=0
# orel=0
# for c in range(a):
#     b=random.randint(0,1)
#     if b == 1:
#       resh +=1
#     else:
#         orel +=1
# print(resh,orel)  



