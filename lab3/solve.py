from numpy import linalg

TIME_DELTA = 1e-3
EPS = 1e-3


def get_Kolmogorov_coeffs(matrix):
    n = len(matrix)
    return [
        [matrix[j][i] if j != i else -sum(matrix[i]) for j in range(n)]
        if i != (n - 1) else [1 for i in range(n)]
        for i in range(n)
        ]


def get_limit_probabilities(matrix):
    coeffs = get_Kolmogorov_coeffs(matrix)
    return linalg.solve(coeffs, [0 if i != (len(matrix) - 1) else 1 for i in range(len(matrix))]).tolist()


def get_probability_increments(matrix, start_probabilities):
    n = len(matrix)
    return [
        TIME_DELTA * sum([-sum(matrix[i]) * start_probabilities[j] if i == j
                          else matrix[j][i] * start_probabilities[j] for j in range(n)])
        for i in range(n)
    ]


def get_limit_times(matrix, limit_probabilities):
    n = len(matrix)
    start_probabilities = [1.0 / n for i in range(n)]
    current_time = 0.0
    current_probabilities = start_probabilities.copy()
    limit_times = [0.0 for i in range(n)]
    while not all(limit_times):
        dp = get_probability_increments(matrix, start_probabilities)
        for i in range(n):
            if not limit_times[i] and abs(current_probabilities[i] - limit_probabilities[i]) <= EPS:
                limit_times[i] = current_time
            current_probabilities[i] += dp[i]
            current_time += TIME_DELTA
    return limit_times


def calculate_time(matrix):
    limit_p = [round(x, 4) for x in get_limit_probabilities(matrix)]
    limit_t = [round(x, 4) for x in get_limit_times(matrix, limit_p)]
    return limit_p, limit_t
