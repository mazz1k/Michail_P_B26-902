class Node:
    """Узел связной структуры: значение и ссылка на следующий узел."""

    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node


class Stack:
    """Стек на узлах: последний добавленный элемент извлекается первым."""

    def __init__(self):
        self.head = None

    def push(self, value):
        """Положить значение на вершину стека."""
        self.head = Node(value, self.head)

    def pop(self):
        """Снять значение с вершины. Для пустого стека - IndexError."""
        if self.head is None:
            raise IndexError("pop из пустого стека")
        value = self.head.value
        self.head = self.head.next
        return value

    def remove_value(self, value):
        """Удалить первое вхождение значения. True, если нашли, иначе False."""
        previous = None
        current = self.head
        while current is not None:
            if current.value == value:
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next
                return True
            previous = current
            current = current.next
        return False

    def __repr__(self):
        """Строка для вывода стека: от вершины вниз."""
        values = []
        current = self.head
        while current is not None:
            values.append(repr(current.value))
            current = current.next
        return "Stack(" + " -> ".join(values) + ")"


class Queue:
    """Очередь на узлах: добавление в хвост, извлечение из головы."""

    def __init__(self):
        self.head = None
        self.tail = None

    def enqueue(self, value):
        """Добавить значение в конец очереди."""
        new_node = Node(value)
        if self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def dequeue(self):
        """Извлечь значение из начала. Для пустой очереди - IndexError."""
        if self.head is None:
            raise IndexError("dequeue из пустой очереди")
        value = self.head.value
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        return value

    def is_empty(self):
        """Вернуть True, если очередь пуста."""
        return self.head is None

    def __repr__(self):
        """Строка для вывода очереди: от головы к хвосту."""
        values = []
        current = self.head
        while current is not None:
            values.append(repr(current.value))
            current = current.next
        return "Queue(" + " -> ".join(values) + ")"


class LinkedList:
    """Односвязный список: история выдач."""

    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, value):
        """Добавить значение в конец списка."""
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def reverse(self):
        """Развернуть список, меняя ссылки next."""
        previous = None
        current = self.head
        self.tail = self.head
        while current is not None:
            next_node = current.next
            current.next = previous
            previous = current
            current = next_node
        self.head = previous

    def to_list(self):
        """Вернуть значения всех узлов по порядку (рекурсивный обход)."""
        return collect_values(self.head)

    def find(self, isbn):
        """Найти запись по ISBN (рекурсивный поиск, O(n))."""
        return find_by_isbn(self.head, isbn)

    def __repr__(self):
        """Строка для вывода списка: от головы к хвосту."""
        values = []
        current = self.head
        while current is not None:
            values.append(repr(current.value))
            current = current.next
        return "LinkedList(" + " -> ".join(values) + ")"


def collect_values(node):
    """Вернуть значения всех узлов, начиная с данного (рекурсивно)."""
    if node is None:
        return []
    return [node.value] + collect_values(node.next)


def find_by_isbn(node, isbn):
    """Найти запись с нужным ISBN, начиная с узла (рекурсивно)."""
    if node is None:
        return None
    if node.value["isbn"] == isbn:
        return node.value
    return find_by_isbn(node.next, isbn)