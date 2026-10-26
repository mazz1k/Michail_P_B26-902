


def same_object(a, b):
    return id(a) == id(b)
    
#"""True, если a и b — один и тот же объект."""
# использовать id
def same_value(a, b):
    return a == b
#"""True, если значения a и b равны."""
# использовать ==
def deep_compare(a, b):
    return a == b
#"""True, если структуры a и b равны на всех уровнях вложенности."""
# использовать ==
#Проверьте себя на таких случаях:
a = [1, 2, 3]
b = a
c = [1, 2, 3]
print(same_object(a, b)) # True
print(same_object(a, c))# False
print(same_value(a, c)) # True
print(deep_compare([[1, 2]], [[1, 2]]))# True
print(deep_compare([[1, 2]], [[1, 3]])) 
# False