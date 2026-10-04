def prog(inp, sortorders):
    if inp == 1: show_all_ord(sortorders)
    if inp == 2: sortub(sortorders)
    if inp == 3: sortcat(sortorders)
    if inp == 4: statfilt()
    if inp == 5: catfilt()
    if inp == 6: costumer()
    if inp == 7: krupn()
    if inp == 8: stat()
    if inp == 9: savereport()

def show_all_ord(sortorders):
    for el in sortorders:
        print(el)

def sortub(spisok):
    ubsort = sorted(spisok, key=lambda y: (-y['price'], y['number']))
    for el in ubsort:
        print(el)

def sortcat(spisok):
    catsort = sorted(spisok, key=lambda y: (y['category'], y['customer']))
    for el in catsort:
        print(el)
    

def statfilt():
    pass

def catfilt():
    pass

def costumer():
    pass

def krupn():
    pass

def stat():
    pass

def savereport():
    pass




notsortord = [el.strip().split(';') for el in open('/Users/michail/study/inf/Michail_P_B26-902/lab_02/input.txt')]
numbers = []
sortorders = []
for el in notsortord:
    if len(el) == 6 and el[0] not in numbers:
        try:
            numbers.append(int(el[0]))
            sortorders.append({
                'number': int(el[0]),
                'customer': el[1].strip(),
                'category': el[2].strip(),
                'quantity': int(el[3]),
                'price': float(el[4]),
                'status': el[5].strip()
            })
        except ValueError:
            pass
i = 0
while i < len(sortorders):
    order = sortorders[i]
    if any(order[key] == '' or order[key] == ' ' for key in ('number', 'customer', 'category', 'quantity', 'price', 'status') or int(order['price']) < 0):
        del sortorders[i]
        continue

    try:
        order['number'] = int(order['number'])
        order['quantity'] = int(order['quantity'])
        order['price'] = float(order['price'])
        i += 1
    except ValueError:
        del sortorders[i]

while True:
    print("""
1. Показать все заказы
2. Показать заказы по убыванию стоимости
3. Показать заказы по категориям
4. Найти заказы по статусу
5. Найти заказы по категории
6. Найти заказы покупателя
7. Показать крупные заказы
8. Показать статистику
9. Сохранить отчёт
0. Завершить программу
""")
    vvod = int(input())
    if vvod == 0:
        break
    else:
        prog(vvod, sortorders)


    

# with open("report.txt", "w", encoding="utf-8") as f:
#     for el in sortorders:
#         f.write(str(el) + "\n")
