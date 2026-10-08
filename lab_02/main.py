#основные функции программы
def show_all_1(sorted_students):
    return sorted_students

def rating_2(sorted_students):
    return sorted(sorted_students, key=lambda y: (-y['itog'], y['student_name']))

def find_group_3(sorted_students, group_name):
    group_name = group_name.strip().lower()
    return [
        el for el in sorted_students
        if el['group'].strip().lower() == group_name
    ]

def find_student_name_4(sorted_students, name):
    name = name.strip().lower()
    return [
        el for el in sorted_students
        if name in el['student_name'].lower()
    ]

def student_selection_5(sorted_students):
    return [
        el for el in sorted_students
        if el['itog'] >= 180
        and el['scores'][0] >= 50
        and el['scores'][1] >= 50
        and el['scores'][2] >= 50
    ]

def group_stats_6(sorted_students):
    groups = sorted({p['group'] for p in sorted_students})
    stat_groups = {}
    for el1 in groups:
        groupballs = []
        studballs = {}
        for el2 in sorted_students:
            if el2['group'] == el1:
                groupballs.append(el2['itog'])
                studballs[str(el2['itog'])] = el2['student_name']

                
        stat_groups[f'group {el1}'] = { 'srball': sum(groupballs)//len(groupballs), 'maxball': max(groupballs), 'studmaxball': studballs[str(max(groupballs))]}
    return stat_groups


def task_stats_6(sorted_students):
    taskst1, taskst2, taskst3 = [], [], []
    for el in sorted_students:
        taskst1.append(el['scores'][0])
        taskst2.append(el['scores'][1])
        taskst3.append(el['scores'][2])
    task_scores = (taskst1, taskst2, taskst3)
    return [
        {
            'average': sum(scores) // len(scores),
            'minimum': min(scores),
            'maximum': max(scores),
        }
        for scores in task_scores
    ]
    
def save_report_7(corzap, er, ungr, reit, otbor, grpst, stust):
    with open("report.txt", "w", encoding="utf-8") as f:
        f.write(f'Корректных записей: {len(corzap)}\n')
        f.write(f'Некорректных записей: {len(er)}\n')
        f.write(f'Уникальные группы: {", ".join(sorted(ungr))}\n')
        f.write('Общий рейтинг: \n')
        for r in reit:
            f.write(r + '\n')
        f.write('Прошедшие отбор: \n')
        for ot in otbor:
            f.write(ot + '\n')
        f.write('Статистика по группам: \n')
        
        for group, data in grpst.items():
            f.write(group.replace('group', ''))
            f.write('  Средний итог:', data['srball'])
            f.write('  Максимальный итог:', data['maxball'])
            f.write('  Лидер:', data['studmaxball'])
            f.write()
        f.write('Статистика по группам')
        
        f.write('\nОшибки входных данных:\n')
        for e in er:
            f.write(e + '\n')


#вспомогательные функции
def spisokprint(students):
    for el in students:
                    print(f"{el['number']} | {el['student_name']} | {el['group']} | "
                          f"баллы: {el['scores'][0]}, {el['scores'][1]}, {el['scores'][2]} | "
                          f"итог: {el['itog']} | средний: {el['srbal']:.2f} | {el['category']}")
                    
def get_category(total):
    if total >= 240:
        return 'Отличный результат'
    elif total >= 180:
        return 'Хороший результат'
    elif total >= 120:
        return 'Удовлетворительный результат'
    else:
        return 'Требуется подготовка'


#главная функция
def main():
    while True:
            print("""
            1. Показать всех участников
            2. Показать общий рейтинг
            3. Найти участников по группе
            4. Найти участников по части имени
            5. Показать участников, прошедших отбор
            6. Показать статистику
            7. Сохранить отчёт
            0. Завершить программу
            """)
            a = input().strip()
            if a == '0':
                break
            if a not in ('1', '2', '3', '4', '5', '6', '7'):
                print('Неизвестный пункт меню, попробуйте ещё раз.')
                continue
    
            if a == '1':
                students = show_all_1(sortpeople)
                spisokprint(students)
            elif a == '2':
                students = rating_2(sortpeople)
                spisokprint(students)
            elif a == '3':
                print('Введите название учебной группы:')
                students = find_group_3(sortpeople, input())
                if not students:
                    print('Участников этой группы нет.')
                spisokprint(students)
            elif a == '4':
                print('Введите имя:')
                students = find_student_name_4(sortpeople, input())
                if not students:
                    print('Учасников с таким именем нет')
                spisokprint(students)
            elif a == '5':
                students = student_selection_5(sortpeople)
                spisokprint(students)
            elif a == '6':
                group_stats = group_stats_6(sortpeople)
                for group, data in group_stats.items():
                    print(group.replace('group', ''))
                    print('  Средний итог:', data['srball'])
                    print('  Максимальный итог:', data['maxball'])
                    print('  Лидер:', data['studmaxball'])
                    print()
    
                task_stats = task_stats_6(sortpeople)
                for task_number, data in enumerate(task_stats, start=1):
                    print(f"""
    Задание {task_number}:
        Средний балл: {data['average']}
        Минимальный балл: {data['minimum']}
        Максимальный балл: {data['maximum']}
    """)
            elif a == '7':
                groups = {p['group'] for p in sortpeople}
                save_report_7(sortpeople, errors, groups, rating_2(sortpeople), student_selection_5(sortpeople), group_stats_6(sortpeople), task_stats_6(sortpeople))
                print('Отчёт сохранён в report.txt')
    

#начало программы 
notsort = [el.strip().split(';') for el in open('input.txt', encoding='utf-8')]
sortpeople = []
numbers = []
errors = []

for line_no, el in enumerate(notsort, start=1):
    if el == ['']:
        continue

    el = [x.strip() for x in el]

    if len(el) != 6:
        errors.append(f'Строка {line_no}: неверное количество полей.')
        continue

    try:
        number = int(el[0])
    except ValueError:
        errors.append(f'Строка {line_no}: номер участника должен быть целым числом.')
        continue
    if number <= 0:
        errors.append(f'Строка {line_no}: номер участника должен быть положительным.')
        continue

    if number in numbers:
        errors.append(f'Строка {line_no}: повторяющийся номер участника {number}.')
        continue

    if el[1] == '':
        errors.append(f'Строка {line_no}: имя участника не должно быть пустым.')
        continue

    if el[2] == '':
        errors.append(f'Строка {line_no}: название группы не должно быть пустым.')
        continue

    scores = []
    score_ok = True
    for task_no in range(3):
        try:
            score = int(el[3 + task_no])
        except ValueError:
            errors.append(f'Строка {line_no}: балл за задачу {task_no + 1} должен быть целым числом.')
            score_ok = False
            break
        if score < 0 or score > 100:
            errors.append(f'Строка {line_no}: балл должен находиться в диапазоне от 0 до 100.')
            score_ok = False
            break
        scores.append(score)
    if not score_ok:
        continue

    total = sum(scores)
    numbers.append(number)
    sortpeople.append({
        'number': number,
        'student_name': el[1],
        'group': el[2],
        'scores': scores,
        'itog': total,
        'srbal': round(total / 3, 2),
        'category': get_category(total)
    })

main()