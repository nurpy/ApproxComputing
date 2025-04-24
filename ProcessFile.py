
import math
from pysr import PySRRegressor
from gplearn.genetic import SymbolicRegressor
import numpy as np


def read_numbers_from_file(file_path):
    with open(file_path, 'r') as file:
        numbers = [float(line.strip()) for line in file]
    return numbers

def calculate_average(numbers):
    return sum(numbers) / len(numbers)

def calculate_standard_deviation(numbers, average):
    variance = sum((x - average) ** 2 for x in numbers) / len(numbers)
    return math.sqrt(variance)

def avg_and_std_deviation_of_file(file_path):
    file_path = file_path  # Change this to the path of your file
    numbers = read_numbers_from_file(file_path)

    if numbers:
        average = calculate_average(numbers)
        std_dev = calculate_standard_deviation(numbers, average)

        #finding indexes if its an array
        file_name = file_path
        var = file_name.split("#")
        indexArr=[ f"{[int(i)]}" for i in var if i.isdigit()] #variable indexes
        index_string = ''.join(indexArr)
            
        variable_name = file_name.split("_file")[0] + index_string
        #print(variable_name)
        #print(f'Average: {average}')
        #print(f'Standard Deviation: {std_dev}')
        return (variable_name,average,std_dev,numbers)
    else:
        raise("error no numbers")
        print("No numbers in the file.")
        return False
        print("No numbers in the file.")

def mean_percentage_error(arr1,arr2):
    total_error = 0
    for num1,num2 in zip(arr1,arr2):
        if num1 == 0:
            num1=1
        if num2 ==0:
            num2=1
        total_error+=abs((num1 - num2)/num2)
    #total_error = abs(count1[num1] - count2[num2]) for num1,num2 in zip(arr1,arr2)
    # Mean Absolute Error (MAE)
    mae = (total_error / len(arr1)) * 100
    return mae
def percentage_change(arr1, arr2):
    """
    Compare two integer arrays element-wise and return their percentage change.

    Formula: ((new - old) / |old|) * 100

    :param arr1: First list of integers (original values)
    :param arr2: Second list of integers (new values)
    :return: List of percentage changes
    """
    percentage_changes = []

    for old, new in zip(arr1, arr2):
        if old == 0:
            change = float('inf')  # Avoid division by zero
        else:
            change = ((new - old) / abs(old)) * 100
        percentage_changes.append(change)

    return percentage_changes


"""
vals = avg_and_std_deviation_of_file("out/^1^33Ave8_FUNCNAMEbuffer_file#1#.txt")[3]
vals2 = avg_and_std_deviation_of_file("out/^4^47Ave8_FUNCNAMEsum_file.txt")[3]
X = 2 * np.random.randn(100, 1)
Y= 2 * np.random.randn(100, 1)

count = 0
for x in vals:
    vals[count] = [x]
    count+=1
count=0
#for x in vals2:
#    vals2[count] = [x]
#    count+=1
#X.reshape(1,-1)
print(vals)
print(vals2)
sr = SymbolicRegressor(population_size=500, generations=50, stopping_criteria=0.001, random_state=42,const_range=(-50,50),init_method='grow',metric='mean absolute error',parsimony_coefficient=.1,p_hoist_mutation=0.05
                        ,init_depth=(1,1))
sr.fit(vals, vals2)
print(sr)
print("Discovered function:", sr._program)
print(sr.score(X,Y))
print(sr.get_params())
"""