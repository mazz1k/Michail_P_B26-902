"""Учёт библиотечных выдач на собственных связных структурах данных."""

from copy import deepcopy
from pathlib import Path

from data_structures import Stack, Queue, LinkedList


# Загрузка и проверка данных
def parse_issue(line, numbers, records_by_isbn):
    """Разобрать одну запись или сообщить причину ошибки через ValueError."""
    fields = [field.strip() for field in line.split(';')]
    if len(fields) != 5:
        raise ValueError('неверное количество полей.')

    try:
        number = int(fields[0])
    except ValueError:
        raise ValueError('номер выдачи должен быть целым числом.') from None
    if number <= 0:
        raise ValueError('номер выдачи должен быть положительным.')
    if number in numbers:
        raise ValueError(f'повторяющийся номер выдачи {number}.')

    for name, value in zip(('читатель', 'isbn', 'раздел', 'название'), fields[1:]):
        if not value:
            raise ValueError(f"пустое обязательное поле: '{name}'.")
    if fields[2] in records_by_isbn:
        raise ValueError(f'повторяющийся ISBN {fields[2]}.')

    return {
        'number': number,
        'reader': fields[1],
        'isbn': fields[2],
        'section': fields[3],
        'title': fields[4],
    }


def sort_issue_queue(issue_queue):
    """Сортировать очередь по номерам выбором, без промежуточного списка."""
    current = issue_queue.head
    while current is not None:
        minimum = current
        candidate = current.next
        while candidate is not None:
            if candidate.value['number'] < minimum.value['number']:
                minimum = candidate
            candidate = candidate.next
        current.value, minimum.value = minimum.value, current.value
        current = current.next


def parse_issues(lines):
    """Вернуть очередь по номерам, индекс ISBN, ошибки и число верных записей."""
    records_by_isbn = {}
    numbers = set()
    errors = []
    for line_no, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            record = parse_issue(line, numbers, records_by_isbn)
        except ValueError as error:
            errors.append(f'Строка {line_no}: {error}')
            continue
        numbers.add(record['number'])
        records_by_isbn[record['isbn']] = record

    issue_queue = Queue()
    for record in records_by_isbn.values():
        issue_queue.enqueue(record)
    sort_issue_queue(issue_queue)
    return issue_queue, records_by_isbn, errors, len(records_by_isbn)


def load_issues(path=None):
    """Прочитать UTF-8 файл выдач; по умолчанию он находится рядом с программой."""
    if path is None:
        path = Path(__file__).with_name('issues.txt')
    with Path(path).open(encoding='utf-8-sig') as input_file:
        return parse_issues(input_file)


# Основные операции
def issue_book(issue_queue, history, return_stack):
    """Выдать первую книгу, обновив историю и стек; для пустой очереди вернуть None."""
    if issue_queue.is_empty():
        return None
    record = issue_queue.dequeue()
    history.append(deepcopy(record))
    return_stack.push(record['isbn'])
    return deepcopy(record)


def return_book(return_stack, isbn):
    """Удалить ISBN возвращённой книги из стека; вернуть признак успеха."""
    return return_stack.remove_value(isbn.strip())


def cancel_last_issue(return_stack):
    """Снять последний невозвращённый ISBN; историю сохранить согласно ТЗ."""
    if return_stack.head is None:
        return None
    return return_stack.pop()


def get_history(history):
    """Получить независимую копию истории через рекурсивный обход узлов."""
    return deepcopy(history.to_list())


def reverse_history(history):
    """Развернуть ссылки истории и вернуть копию полученного порядка."""
    history.reverse()
    return get_history(history)


def find_book(records_by_isbn, isbn):
    """Найти книгу в хэш-таблице за O(1) в среднем и вернуть копию записи."""
    return deepcopy(records_by_isbn.get(isbn.strip()))


def find_in_history(history, isbn):
    """Рекурсивно найти книгу в истории за O(n) и вернуть копию записи."""
    return deepcopy(history.find(isbn.strip()))


def get_unique_sections(records_by_isbn):
    """Получить множество разделов всех корректных записей файла."""
    return {record['section'] for record in records_by_isbn.values()}


def section_statistics(records_by_isbn, history, return_stack):
    """Посчитать фактические выдачи и невозвращённые книги по разделам."""
    statistics = {}
    for section in get_unique_sections(records_by_isbn):
        statistics[section] = {
            'issue_count': 0,
            'unreturned_count': 0,
            'last_issue': None,
            'max_number': None,
        }

    current = history.head
    while current is not None:
        record = current.value
        data = statistics[record['section']]
        data['issue_count'] += 1
        maximum = max(data['max_number'] or 0, record['number'])
        data['max_number'] = maximum
        data['last_issue'] = maximum
        current = current.next

    current = return_stack.head
    while current is not None:
        record = records_by_isbn[current.value]
        statistics[record['section']]['unreturned_count'] += 1
        current = current.next
    return statistics


# Вывод и сохранение отчёта
def format_issue(record):
    """Сформировать строку с данными одной выдачи."""
    return (f"{record['number']} | {record['reader']} | {record['isbn']} | "
            f"{record['section']} | {record['title']}")


def print_issues(records, empty_message):
    """Вывести записи или сообщение об их отсутствии."""
    if not records:
        print(empty_message)
    for record in records:
        print(format_issue(record))


def format_statistics(statistics):
    """Сформировать текст статистики, включая случай пустого набора."""
    if not statistics:
        return 'Нет корректных записей для вычисления статистики.'
    lines = []
    sections = list(statistics)
    sections.sort()
    for section in sections:
        data = statistics[section]
        latest = data['last_issue'] if data['last_issue'] is not None else '-'
        maximum = data['max_number'] if data['max_number'] is not None else '-'
        lines.extend([
            section,
            f"  Количество выдач: {data['issue_count']}",
            f"  Ещё не возвращено: {data['unreturned_count']}",
            f'  Номер самой поздней выдачи: {latest}',
            f'  Максимальный номер выдачи: {maximum}',
        ])
    return '\n'.join(lines)


def save_report(records_by_isbn, history, return_stack, errors, path=None):
    """Сохранить статистику, историю и ошибки в UTF-8 отчёт без изменения данных."""
    if path is None:
        path = Path(__file__).with_name('issues_report.txt')
    sections = list(get_unique_sections(records_by_isbn))
    sections.sort()
    statistics = section_statistics(records_by_isbn, history, return_stack)
    issued = get_history(history)
    lines = [
        f'Корректных записей: {len(records_by_isbn)}',
        f'Некорректных записей: {len(errors)}',
        'Уникальные разделы: ' + (', '.join(sections) if sections else 'нет'),
        '\nСтатистика по разделам:',
        format_statistics(statistics),
        '\nСписок выданных книг (текущий порядок истории):',
    ]
    lines.extend(format_issue(record) for record in issued)
    if not issued:
        lines.append('Книги ещё не выдавались.')
    lines.append('\nОшибки входных данных:')
    lines.extend(errors if errors else ['Ошибок нет.'])
    Path(path).write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return Path(path)


def run_menu(issue_queue, records_by_isbn, history, return_stack, errors,
             report_path=None):
    """Обработать команды пользователя, передавая данные в отдельные функции."""
    while True:
        print('''
1. Показать очередь выдач
2. Выдать книгу
3. Вернуть книгу по ISBN
4. Отменить последнюю выдачу
5. Показать историю выдач
6. Развернуть историю
7. Показать статистику
8. Найти книгу по ISBN
9. Сохранить отчёт
0. Завершить программу
''')
        choice = input('Выберите пункт меню: ').strip()
        if choice == '0':
            break
        if choice == '1':
            print_issues(issue_queue.to_list(), 'Очередь выдач пуста.')
        elif choice == '2':
            record = issue_book(issue_queue, history, return_stack)
            if record is None:
                print('Очередь выдач пуста. Выдать книгу невозможно.')
            else:
                print('Выдана книга:', format_issue(record))
        elif choice == '3':
            isbn = input('Введите ISBN возвращаемой книги: ').strip()
            if return_book(return_stack, isbn):
                print('Возврат книги зарегистрирован.')
            else:
                print('ISBN отсутствует в стеке возвратов: книга не выдавалась, '
                      'уже возвращена или её выдача отменена.')
        elif choice == '4':
            isbn = cancel_last_issue(return_stack)
            if isbn is None:
                print('Стек возвратов пуст. Отменять нечего.')
            else:
                print(f'Последняя активная выдача отменена: {isbn}.')
        elif choice == '5':
            print_issues(get_history(history), 'История выдач пуста.')
        elif choice == '6':
            print_issues(reverse_history(history), 'История выдач пуста.')
        elif choice == '7':
            sections = list(get_unique_sections(records_by_isbn))
            sections.sort()
            print('Уникальные разделы:', ', '.join(sections) if sections else 'нет')
            print(format_statistics(
                section_statistics(records_by_isbn, history, return_stack)))
        elif choice == '8':
            isbn = input('Введите ISBN для поиска: ').strip()
            record = find_book(records_by_isbn, isbn)
            if record is None:
                print('Книга с таким ISBN не найдена в каталоге.')
            else:
                print('Поиск в хэш-таблице:', format_issue(record))
            issued = find_in_history(history, isbn)
            if issued is None:
                print('В истории выдач книга не найдена.')
            else:
                print('Рекурсивный поиск в истории:', format_issue(issued))
        elif choice == '9':
            try:
                path = save_report(records_by_isbn, history, return_stack,
                                   errors, report_path)
            except OSError as error:
                print(f'Не удалось сохранить отчёт: {error}')
            else:
                print(f'Отчёт сохранён: {path}')
        else:
            print('Неизвестный пункт меню, попробуйте ещё раз.')


def run_asserts():
    """Проверить структуры, обработку записей, операции и независимость копий."""
    from tempfile import TemporaryDirectory

    queue = Queue()
    queue.enqueue('первая')
    queue.enqueue('вторая')
    assert queue.to_list() == ['первая', 'вторая']
    assert queue.dequeue() == 'первая'
    assert queue.dequeue() == 'вторая'
    assert queue.is_empty() and queue.tail is None
    try:
        queue.dequeue()
    except IndexError as error:
        assert 'пустой' in str(error)
    else:
        assert False, 'Пустая очередь должна выбрасывать IndexError'
    queue.enqueue('после опустошения')
    assert queue.dequeue() == 'после опустошения'

    stack = Stack()
    stack.push('первая')
    stack.push('средняя')
    stack.push('последняя')
    assert stack.remove_value('средняя') is True
    assert stack.remove_value('отсутствует') is False
    assert stack.pop() == 'последняя'
    assert stack.pop() == 'первая'
    try:
        stack.pop()
    except IndexError as error:
        assert 'пустого' in str(error)
    else:
        assert False, 'Пустой стек должен выбрасывать IndexError'

    lines = [
        '3;Третий читатель;ISBN-3;история;Третья книга',
        ' 1 ; Первый читатель ; ISBN-1 ; техника ; Первая книга ',
        '2;Второй читатель;ISBN-2;техника;Вторая книга',
        '',
        '4;мало полей',
        'номер;Читатель;ISBN-4;история;Книга',
        '0;Читатель;ISBN-4;история;Книга',
        '-4;Читатель;ISBN-4;история;Книга',
        '1;Читатель;ISBN-4;история;Книга',
        '4; ;ISBN-4;история;Книга',
        '4;Читатель; ;история;Книга',
        '4;Читатель;ISBN-4; ;Книга',
        '4;Читатель;ISBN-4;история; ',
        '4;Читатель;ISBN-1;история;Книга',
    ]
    original_lines = lines[:]
    issue_queue, catalog, errors, count = parse_issues(lines)
    assert lines == original_lines
    assert count == 3 and len(errors) == 10
    assert errors[0].startswith('Строка 5:')
    assert 'повторяющийся номер' in errors[4]
    assert 'повторяющийся ISBN' in errors[-1]
    assert [record['number'] for record in issue_queue.to_list()] == [1, 2, 3]
    assert catalog['ISBN-1']['reader'] == 'Первый читатель'
    assert get_unique_sections(catalog) == {'история', 'техника'}

    history = LinkedList()
    returns = Stack()
    assert get_history(history) == []
    assert reverse_history(history) == []
    assert find_in_history(history, 'ISBN-1') is None
    assert cancel_last_issue(returns) is None
    assert return_book(returns, 'ISBN-1') is False
    assert section_statistics(catalog, history, returns)['техника']['issue_count'] == 0

    first = issue_book(issue_queue, history, returns)
    assert first['number'] == 1
    first['title'] = 'Изменённая копия'
    assert catalog['ISBN-1']['title'] == 'Первая книга'
    assert get_history(history)[0]['title'] == 'Первая книга'
    assert issue_book(issue_queue, history, returns)['number'] == 2
    assert issue_book(issue_queue, history, returns)['number'] == 3
    assert issue_book(issue_queue, history, returns) is None
    assert [record['number'] for record in get_history(history)] == [1, 2, 3]
    assert return_book(returns, ' ISBN-2 ') is True
    assert return_book(returns, 'ISBN-2') is False
    statistics = section_statistics(catalog, history, returns)
    assert statistics['техника'] == {
        'issue_count': 2, 'unreturned_count': 1, 'last_issue': 2, 'max_number': 2,
    }
    assert statistics['история']['unreturned_count'] == 1
    assert cancel_last_issue(returns) == 'ISBN-3'
    assert cancel_last_issue(returns) == 'ISBN-1'
    assert cancel_last_issue(returns) is None
    assert len(get_history(history)) == 3

    assert [record['number'] for record in reverse_history(history)] == [3, 2, 1]
    assert history.tail.value['number'] == 1 and history.tail.next is None
    history.append({'number': 4, 'isbn': 'ISBN-4'})
    assert [record['number'] for record in get_history(history)] == [3, 2, 1, 4]
    assert find_in_history(history, 'ISBN-2')['number'] == 2
    assert find_in_history(history, 'нет') is None
    result = find_book(catalog, ' ISBN-1 ')
    result['reader'] = 'Изменённая копия'
    assert catalog['ISBN-1']['reader'] == 'Первый читатель'
    assert find_book(catalog, 'нет') is None
    snapshot = get_history(history)
    snapshot[0]['title'] = 'Изменённая копия'
    assert get_history(history)[0]['title'] == 'Третья книга'

    # Повторный вызов создаёт отдельные структуры и не накапливает данные.
    other_queue, other_catalog, other_errors, other_count = parse_issues(lines)
    assert other_count == count and other_errors == errors
    assert other_queue is not issue_queue and other_catalog is not catalog
    assert other_catalog['ISBN-1'] is not catalog['ISBN-1']
    empty_queue, empty_catalog, empty_errors, empty_count = parse_issues([])
    assert empty_queue.is_empty() and empty_catalog == {}
    assert empty_errors == [] and empty_count == 0
    assert section_statistics({}, LinkedList(), Stack()) == {}

    with TemporaryDirectory() as folder:
        input_path = Path(folder) / 'issues.txt'
        input_path.write_text('\n'.join(lines), encoding='utf-8')
        loaded_queue, loaded_catalog, loaded_errors, loaded_count = load_issues(input_path)
        assert loaded_count == 3 and loaded_errors == errors
        loaded_history, loaded_returns = LinkedList(), Stack()
        issue_book(loaded_queue, loaded_history, loaded_returns)
        before = deepcopy((loaded_catalog, loaded_errors, get_history(loaded_history)))
        before_queue = loaded_queue.to_list()
        before_stack = repr(loaded_returns)
        report_path = save_report(loaded_catalog, loaded_history, loaded_returns,
                                  loaded_errors, Path(folder) / 'report.txt')
        report = report_path.read_text(encoding='utf-8')
        assert 'Корректных записей: 3' in report and 'Некорректных записей: 10' in report
        assert 'ISBN-1' in report and errors[0] in report
        assert (loaded_catalog, loaded_errors, get_history(loaded_history)) == before
        assert loaded_queue.to_list() == before_queue
        assert repr(loaded_returns) == before_stack


def main(input_path=None, report_path=None):
    """Загрузить файл и запустить меню; все основные данные хранить локально."""
    try:
        issue_queue, catalog, errors, count = load_issues(input_path)
    except FileNotFoundError:
        print('Ошибка: файл issues.txt не найден рядом с программой.')
        return 1
    except UnicodeError:
        print('Ошибка: входной файл должен быть сохранён в кодировке UTF-8.')
        return 1
    except OSError as error:
        print(f'Не удалось прочитать входной файл: {error}')
        return 1

    print(f'Загружено корректных записей: {count}. Некорректных: {len(errors)}.')
    for error in errors:
        print(error)
    run_menu(issue_queue, catalog, LinkedList(), Stack(), errors, report_path)
    return 0


if __name__ == '__main__':
    run_asserts()
    print('Все автоматические проверки пройдены.')
    try:
        raise SystemExit(main())
    except (EOFError, KeyboardInterrupt):
        print('\nВвод завершён. Программа остановлена.')
