from PyQt5.QtWidgets import QMessageBox


def preprocessAndConvert(value):
    if isinstance(value, str):  # Remove commas
        value = value.replace(',', '')
    try:
        # Convert to float, then to int if it's a whole number
        numberValue = float(value)
        return numberValue if numberValue % 1 else int(numberValue)
    except ValueError:
        return value

# BUBBLE SORT ALGORITHM


def bubbleSort(data):
    n = len(data)
    processedData = [preprocessAndConvert(value) for value in data]

    for i in range(n):
        for j in range(0, n-i-1):
            if processedData[j] > processedData[j+1]:
                processedData[j], processedData[j +
                                                1] = processedData[j+1], processedData[j]

    for i in range(n):
        data[i] = processedData[i]
    return data

# INSERTION SORT ALGORITHM


def insertionSort(data):
    n = len(data)
    processedData = [preprocessAndConvert(value) for value in data]

    for i in range(1, n):
        key = processedData[i]
        j = i - 1
        # Move elements of processedData[0..i-1] that are greater than key to one position ahead of their current position
        while j >= 0 and processedData[j] > key:
            processedData[j + 1] = processedData[j]
            j -= 1
        processedData[j + 1] = key
    for i in range(n):
        data[i] = processedData[i]
    return data

# SELECTION SORT ALGORITHM


def selectionSort(data):
    n = len(data)
    processedData = [preprocessAndConvert(value) for value in data]

    for i in range(n):
        minIndex = i  # Find the minimum element in remaining unsorted array
        for j in range(i + 1, n):
            if processedData[j] < processedData[minIndex]:
                minIndex = j
        # Swap the found minimum element with the first element
        processedData[i], processedData[minIndex] = processedData[minIndex], processedData[i]

    for i in range(n):
        data[i] = processedData[i]

    return data

# MERGE SORT ALGORITHM


def mergeSort(data):
    if len(data) > 1:
        mid = len(data) // 2
        leftHalf = data[:mid]  # Dividing the elements into 2 halves
        rightHalf = data[mid:]
        mergeSort(leftHalf)
        mergeSort(rightHalf)

        i = j = k = 0
        # Copy data to temp arrays L[] and R[]
        while i < len(leftHalf) and j < len(rightHalf):
            if preprocessAndConvert(leftHalf[i]) < preprocessAndConvert(rightHalf[j]):
                data[k] = leftHalf[i]
                i += 1
            else:
                data[k] = rightHalf[j]
                j += 1
            k += 1

        while i < len(leftHalf):  # Checking if any element was left
            data[k] = leftHalf[i]
            i += 1
            k += 1

        while j < len(rightHalf):
            data[k] = rightHalf[j]
            j += 1
            k += 1
    return data

# QUICK SORT ALGORITHM


def quickSort(data):
    if len(data) <= 1:
        return data
    else:
        pivot = preprocessAndConvert(data[len(data) // 2])
        left = [x for x in data if preprocessAndConvert(x) < pivot]
        middle = [x for x in data if preprocessAndConvert(x) == pivot]
        right = [x for x in data if preprocessAndConvert(x) > pivot]
        # Choose the middle element as pivot,Elements less than pivot,Elements equal to pivot,Elements greater than pivot an then Concatenate results
        return quickSort(left) + middle + quickSort(right)

# COUNTING SORT ALGORITHM


def countingSort(data):
    processedData = [preprocessAndConvert(value) for value in data]

    numericData = [x for x in processedData if isinstance(
        x, (int, float))]  # Separate numeric and non-numeric data
    nonNumericData = [
        x for x in processedData if not isinstance(x, (int, float))]
    if numericData:
        # Create a mapping for float to integer indices
        minValue = min(numericData)
        maxValue = max(numericData)
        rangeofElements = int(maxValue - minValue) + 1

        count = [0] * rangeofElements
        output = [0] * len(numericData)

        for number in numericData:  # Store the count of each number
            index = int(number - minValue)
            count[index] += 1
        # Modify the count array to get the positions of each number
        for i in range(1, len(count)):
            count[i] += count[i - 1]
        for number in reversed(numericData):
            index = int(number - minValue)
            output[count[index] - 1] = number
            count[index] -= 1
        sortedNumericData = output  # Output array
    else:
        sortedNumericData = []

    # Sort non-numeric data (strings) alphabetically
    sortedNumericData = sorted(nonNumericData)
    # Combine the sorted numeric and non-numeric data
    return sortedNumericData + sortedNumericData


def countingSortforRadix(data, exp):
    n = len(data)
    output = [0] * n
    count = [0] * 10
    for i in range(n):
        value = preprocessAndConvert(data[i])
        if isinstance(value, (int, float)):  # Only process numeric values
            index = int(value // exp) % 10
            count[index] += 1
    for i in range(1, 10):
        count[i] += count[i - 1]

    for i in range(n - 1, -1, -1):
        value = preprocessAndConvert(data[i])
        if isinstance(value, (int, float)):
            index = int(value // exp) % 10
            output[count[index] - 1] = data[i]
            count[index] -= 1
        else:
            output[i] = data[i]  # non-numeric as itis
    for i in range(n):
        data[i] = output[i]


def alphabeticalSort(data):
    return sorted([value for value in data if isinstance(value, str)])

# RADIX SORT ALGORITHM


def radixSort(data):
    numericData = []
    nonNumericData = []

    for value in data:
        try:
            processed_value = preprocessAndConvert(value)
            if isinstance(processed_value, (int, float)):
                numericData.append(processed_value)
            else:
                nonNumericData.append(value)
        except Exception as e:
            nonNumericData.append(value)
    try:  # Sort numeric data using Radix Sort
        if numericData:
            maxValue = max(numericData)
            exp = 1
            while maxValue / exp > 0:
                countingSortforRadix(numericData, exp)
                exp *= 10
    except Exception as e:
        QMessageBox.critical(None, "Sorting Error",
                             f"Error while sorting numeric data: {e}")
        return data
    sortedNumericData = alphabeticalSort(nonNumericData)
    return [str(num) for num in numericData] + sortedNumericData

# BUCKET SORT ALGORITHM


def bucketSort(data, num_buckets=10):
    numericData = [preprocessAndConvert(value) for value in data if isinstance(
        preprocessAndConvert(value), (int, float))]
    nonNumericData = [value for value in data if not isinstance(
        preprocessAndConvert(value), (int, float))]

    if not numericData:
        return sorted(nonNumericData)
    # Maximum and minimum values in the numeric data
    maxValue = max(numericData)
    minValue = min(numericData)
    buckets = [[] for _ in range(num_buckets)]  # buckets

    bucket_range = (maxValue - minValue) / num_buckets
    for value in numericData:
        index = int((value - minValue) // bucket_range)
        if index == num_buckets:  # Edge case for the maximum value
            index -= 1
        buckets[index].append(value)
    sorted_buckets = []
    for bucket in buckets:
        sorted_buckets.extend(sorted(bucket))

    sorted_data = sorted_buckets + nonNumericData
    return sorted_data

# GNOME SORT ALGORITHM


def gnomeSort(data):
    try:
        n = len(data)
        index = 0
        processedData = [preprocessAndConvert(value) for value in data]
        while index < n:
            if index == 0:
                index += 1
            if processedData[index] >= processedData[index - 1]:
                index += 1
            else:
                processedData[index], processedData[index -
                                                    1] = processedData[index - 1], processedData[index]
                index -= 1
        for i in range(n):
            data[i] = processedData[i]

        return data

    except Exception as e:
        QMessageBox.critical(None, "Sorting Error",
                             f"Error in gnome_sort: {e}")
        return data

# BEAD SORT ALGORITHM


def beadSort(data):
    try:
        processedData = [preprocessAndConvert(value) for value in data]

        if not all(isinstance(x, (int, float)) and x >= 0 for x in processedData):
            raise ValueError(
                "All values must be non-negative integers or floats.")

        maxDecimalPlaces = max(len(str(x).split('.')[1]) if '.' in str(
            x) else 0 for x in processedData)
        scale = 10 ** maxDecimalPlaces  # handle decimal places

        scaledData = [int(value * scale) for value in processedData]
        # find the maximum value to determine the size of the beads array
        maxValue = int(max(scaledData)) if scaledData else 0
        beads = [[0] * (maxValue + 1) for _ in range(len(processedData))]

        # Find the maximum value to determine the size of the beads array
        for i, value in enumerate(scaledData):
            for j in range(value):
                beads[i][j] = 1  # Place a bead
        for j in range(maxValue + 1):
            count = 0
            for i in range(len(processedData)):
                count += beads[i][j]  # Count beads in each column
                beads[i][j] = 0
            for i in range(count):
                beads[len(processedData) - 1 - i][j] = 1
        sorted_data = [0] * len(processedData)
        for i in range(len(processedData)):
            sorted_data[i] = sum(beads[i]) / scale
        return sorted_data
    except Exception as e:
        print(f"Error in bead_sort: {e}")
        return data  # Return original data in case of error

# COCKTAIL SHAKER ALGORITHM


def cocktailShakerSort(data):
    try:
        n = len(data)
        swapped = True
        start = 0
        end = n - 1
        while swapped:
            swapped = False
            for i in range(start, end):
                if preprocessAndConvert(data[i]) > preprocessAndConvert(data[i + 1]):
                    data[i], data[i + 1] = data[i + 1], data[i]
                    swapped = True
            if not swapped:
                break
            end -= 1  # Move the end point back
            swapped = False
            for i in range(end, start, -1):
                if preprocessAndConvert(data[i]) < preprocessAndConvert(data[i - 1]):
                    data[i], data[i - 1] = data[i - 1], data[i]
                    swapped = True
            start += 1  # Move one step forward
        return data
    except Exception as e:
        print(f"Error in cocktail_shaker_sort: {e}")
        return data
