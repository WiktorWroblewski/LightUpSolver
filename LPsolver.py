import time
import cplex
import docplex
from docplex.mp.model import Model


def to_cplex_set(list):
    for i in range(len(list)):
        list[i] = set(list[i])
    return list


def lp_solve(wall, connections, limitwall_val, limitwall_idx, columns, rows):
    start_time = time.perf_counter()
    model = Model(name='akari')

    wl = len(limitwall_val)
    wl_r = range(wl)
    limitwall_idx = to_cplex_set(limitwall_idx)

    c = len(columns)
    r = len(rows)
    c_r = range(c)
    r_r = range(r)
    columns = to_cplex_set(columns)
    rows = to_cplex_set(rows)

    n2 = len(connections)
    n2_r = range(n2)

    x = model.binary_var_list(n2, name='x')
    new_board = model.binary_var_list(n2, name='new_board')

    model.minimize(model.sum(x))

    for i in n2_r:
        sum_conn_x = model.sum(x[j] * connections[i][j] for j in n2_r)
        model.add_constraint(new_board[i] == model.min(1, sum_conn_x))

    for i in wl_r:
        model.add_constraint(model.sum(x[j] for j in limitwall_idx[i]) == limitwall_val[i])

    for i in c_r:
        model.add_constraint(model.sum(x[j] for j in columns[i]) <= 1)

    for i in r_r:
        model.add_constraint(model.sum(x[j] for j in rows[i]) <= 1)

    model.add_constraint(model.sum(new_board[i] for i in n2_r) == n2 - wall)

    solution = model.solve()

    end_time = time.perf_counter()
    time_lp = end_time - start_time

    if solution:
        return [int(solution[x[i]]) for i in n2_r], n2 - wall, time_lp
    else:
        return [0 for _ in n2_r], 0, time_lp
