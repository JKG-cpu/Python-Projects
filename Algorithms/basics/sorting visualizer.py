def bubble_sort(arr):
    n = len(arr)

    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

test_list = [1, 60, 25, 50, 100, 90, 20, 35, 45, 0]
print(f"Sorting List: {test_list}")
bubble_sort(test_list)
print(f"Sorted List: {test_list}")

# Selection
def selection_sort(arr):
    n = len(arr)

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        arr[i], arr[min_idx] = arr[min_idx], arr[i] 

test_list2 = [1, 75, 50, 25, 100]
print(f"Sorting List: {test_list2}")
selection_sort(test_list2)
print(f"Sorted List: {test_list2}")

# Insertion
def insertion_sort(arr):
    for i in range(1, len(arr)):
        current_value = arr[i]
        position = i

        while position > 0 and arr[position - 1] > current_value:
            arr[position] = arr[position - 1]
            position -= 1
        
        arr[position] = current_value

test_list3 = [0, 25, 75, 100, 5, 20, 10]
print(f"Sorting List: {test_list3}")
insertion_sort(test_list3)
print(f"Sorted List: {test_list3}")
