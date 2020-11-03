from prettytable import PrettyTable
import csv
from random import randint
import random
from scipy.stats import chi2

def fill_table():
    with open('table.csv', 'w', newline='') as out_csv_file:
        csv_out = csv.writer(out_csv_file)
        for k in [1, 11, 111]:
            row = []
            for j in range(5000):
                row.append(random.randint(k - 1, 9 * k))
            csv_out.writerow(row)

class MyRandom:
    def __init__(self):
        self.current = 1
        self.m = 2.**31
        self.k = 1664525
        self.b = 1013904223

    def get_number(self, low=0, high=100):
        self.current = (self.k * self.current + self.b) % self.m
        result = int(low + self.current % (high - low))
        return result

def table_random(size):
    one_digit = []
    two_digit = []
    three_digit = []
    data = []
    with open('table.csv', newline='') as csvfile:
        tmp = csv.reader(csvfile, delimiter=',')
        for row in tmp:
            data.append(row)

    data_len = len(data[0])
    for i in range(size):
        one_digit.append(int(data[0][randint(0, data_len)]))
        two_digit.append(int(data[1][randint(0, data_len)]))
        three_digit.append(int(data[2][randint(0, data_len)]))

    return one_digit, two_digit, three_digit

def calc_proc(sequence):
    k = 10
    sum_all = 0
    all_digits = []

    for number in sequence:
        all_digits.extend(map(int, list(str(number))))
    theor = len(all_digits) / 10
    for i in range(k):
        count = 0
        for digit in all_digits:
            if digit == i:
                count += 1
        sum_all += ((count - theor)**2) / theor
    return sum_all, 1 - chi2.cdf(sum_all, k - 3)

def main():
    fill_table()
    numbers = [i for i in range(1, 16)]

    my_random_class = MyRandom()
    one_digit_alg = [my_random_class.get_number(0, 9) for i in range(len(numbers))]
    two_digit_alg = [my_random_class.get_number(10, 99) for i in range(len(numbers))]
    three_digit_alg = [my_random_class.get_number(100, 999) for i in range(len(numbers))]
    table_alg = PrettyTable()
    table_alg.add_column('порядковый номер', numbers)
    table_alg.add_column('x-последовательность', one_digit_alg)
    table_alg.add_column('xx-последовательность', two_digit_alg)
    table_alg.add_column('xxx-последовательность', three_digit_alg)
    x2a1, x2a2, x2a3 = calc_proc(one_digit_alg), calc_proc(two_digit_alg), calc_proc(three_digit_alg)
    table_alg.add_row(['коэффициент X2', x2a1[0], x2a2[0], x2a3[0]])
    table_alg.add_row(['1 - альфа', x2a1[1], x2a2[1], x2a3[1]])
    print("Алгоритмический метод")
    print(table_alg)

    print()
    print()

    one_digit_tbl, two_digit_tbl, three_digit_tbl = table_random(len(numbers))
    table_tbl = PrettyTable()
    table_tbl.add_column('порядковый номер', numbers)
    table_tbl.add_column('x-последовательность', one_digit_tbl)
    table_tbl.add_column('xx-последовательность', two_digit_tbl)
    table_tbl.add_column('xxx-последовательность', three_digit_tbl)
    x2a1, x2a2, x2a3 = calc_proc(one_digit_tbl), calc_proc(two_digit_tbl), calc_proc(three_digit_tbl)
    table_tbl.add_row(['коэффициент X2', x2a1[0], x2a2[0], x2a3[0]])
    table_tbl.add_row(['1 - alpha', x2a1[1], x2a2[1], x2a3[1]])
    print("Табличный метод")
    print(table_tbl)

    print()
    cal1 = calc_proc([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    print("Для <X>: ", (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1))
    print(" \t коэффициент X2 = ", cal1[0], " 1 - альфа = ", cal1[1])
    print()
    cal1 = calc_proc([1, 2, 3, 4, 5, 6, 7, 8, 9])
    print("Для <X>: ", (1, 2, 3, 4, 5, 6, 7, 8, 9))
    print(" \t коэффициент X2 = ", cal1[0], " 1 - альфа = ", cal1[1])
    print()

if __name__ == '__main__':
    main()
