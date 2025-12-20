#r - read (Чтение файла)\
#w - Запись (полностью перезаисывает содержание)
#a - Добавить в конец файла

with open("text.txt", "w", encoding="utf-8") as f:
    f.write("Йоу")

with open ("text.txt","r",encoding="utf-8") as f:
    a = f.read()
print(a)