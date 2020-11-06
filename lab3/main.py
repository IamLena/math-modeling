import random
from prettytable import PrettyTable
from numpy import linalg

def get_Kolmogorov_coeffs(matrix):
    n = len(matrix)

    return [
        [matrix[j][i] if j != i else (-sum(matrix[i]) + matrix[i][i]) for j in range(n)]
        if i != (n - 1) else [1 for i in range(n)]
        for i in range(n)
        ]


def get_limit_probabilities(matrix):
    coeffs = get_Kolmogorov_coeffs(matrix)
    return linalg.solve(coeffs, [0 if i != (len(matrix) - 1) else 1 for i in range(len(matrix))]).tolist()


def calculate(matrix):
    limit_p = [round(x, 4) for x in get_limit_probabilities(matrix)]
    return limit_p


def generate_matrix(size):
    # return [
    #     [round(random.random(), 4) for j in range(size)]
    #     for i in range(size)
    # ]
    return [
        [(j / 10) for j in range(size)]
        for i in range(size)
    ]


def print_matrix(matrix):
    table = PrettyTable()
    names = [""]
    names.extend([("e"+str(i + 1)) for i in range(len(matrix))])
    table.field_names = names
    for i in range(len(matrix)):
        tmp = [item for item in matrix[i]]
        tmp.insert(0, ("e"+str(i + 1)))
        table.add_row(tmp)
    print(table)


def print_results(results_p):
    table = PrettyTable()
    table.add_column("Состояния", [("e"+str(i + 1)) for i in range(len(results_p))])
    table.add_column("Предельные вероятности", results_p)
    print(table)


def main():
    random.seed()
    input_size = int(input("Введите количество состояний системы: "))
    if (0 < input_size < 10):
        matrix = generate_matrix(input_size)

        print_matrix(matrix)
        results_p = calculate(matrix)
        print_results(results_p)
    else:
        print("система должна иметь не больше 10 состояний")


if __name__ == '__main__':
    main()
