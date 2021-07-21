import random, copy

from itertools import combinations

solved_board = {
        6: 10000,
        7: 36,
        8: 720,
        9: 360,
        10: 80,
        11: 252,
        12: 108,
        13: 72,
        14: 54,
        15: 180,
        16: 72,
        17: 180,
        18: 119,
        19: 36,
        20: 306,
        21: 1080,
        22: 144,
        23: 1800,
        24: 3600
    }
def percent_perfect(n):
    x = CactpotGenerator()
    y = CactpotSolver()
    perfects = 0
    total = 0
    for i in range(n):
        board = x.generate_board()
        solve = y.perfect_solve_max(board)
        if solve == 10000:
            perfects += 1
        total += 1
        if i % (n/10) == 0:
            print(f"Attempt number {i}: {(perfects/total)* 100} %") 
    print(f"Attempt number {n}: {(perfects/total)* 100} %")

def maximum_ticket_value(n):
    x = CactpotGenerator()
    y = CactpotSolver()
    payout_board = {
        10000: 0,
        36: 0,
        720: 0,
        360: 0,
        80: 0,
        252: 0,
        108: 0,
        72: 0,
        54:0,
        180: 0,
        119: 0,
        36: 0,
        306: 0,
        1080: 0,
        1800: 0,
        3600: 0,
        144: 0
    }
    for i in range(n):
        board = x.generate_board()
        solved_max = y.perfect_solve_max(board)
        payout_board[solved_max] += 1
        if i % (n/10) == 0:
            print(f"Attempt number {i}")
    total = 0 
    for payout, amount in payout_board.items():
        total += (payout*amount)
        if amount != 0:
            print(f"{payout} MGP: {((amount/n) * 100):.3f} %")
    print(f"expected value: {(total/n):.3f}")

def complete_hidden_payout(n, passed_board=[]):
    # I am a small brained individual idk a better way to do this
    x = CactpotGenerator()
    total_payout = 0
    for i in range(n):
        if len(passed_board) == 0:
            board = x.generate_board()
        else:
            board = x.generate_board(passed_board)
        rand_num = random.randrange(0,8)
        sum_of_boards = 0
        if rand_num == 0:
            sum_of_boards =  board[0] + board[1] + board[2]
        elif rand_num == 1:
            sum_of_boards = board[3] + board[4] + board[5]
        elif rand_num == 2:
            sum_of_boards = board[6] + board[7] + board[8]
        elif rand_num == 3:
            sum_of_boards = board[0] + board[3] + board[6]
        elif rand_num == 4:
            sum_of_boards = board[1] + board[4] + board[7]
        elif rand_num == 5:
            sum_of_boards = board[2] + board[5] + board[8]
        elif rand_num == 6:
            sum_of_boards = board[0]+ board[4]+ board[8]
        elif rand_num == 7:
            sum_of_boards = board[2] + board[4] + board[6]
        total_payout += solved_board[sum_of_boards]
    #print(f"random value: {(total_payout/n):.3f}")
    return (total_payout/n)

def select(hidden_board, real_board):
    computed_evs = compute_evs(hidden_board)
    evs = max(list((computed_evs).values()))
    x = []
    for key, value in computed_evs.items():
        if value == evs:
            x.append(key)
    # why doesn't python have switches q.q
    x = random.choice(x)
    if x == 'h1':
        return solved_board[real_board[0] + real_board[1] + real_board[2]]
    elif x == 'h2':
        return solved_board[real_board[3] + real_board[4] + real_board[5]]
    elif x == 'h3':
        return solved_board[real_board[6] + real_board[7] + real_board[8]]
    elif x == 'v1':
        return solved_board[real_board[0] + real_board[3] + real_board[6]]
    elif x == 'v2':
        return solved_board[real_board[1] + real_board[4] + real_board[7]]
    elif x == 'v3':
        return solved_board[real_board[2] + real_board[5] + real_board[8]] 
    elif x == 'd1':
        return solved_board[real_board[0] + real_board[4] + real_board[8]]
    elif x == 'd2':
        return solved_board[real_board[2] + real_board[4] + real_board[6]] 

def lookahead_vs_nonlookahead(n):
    x = CactpotGenerator()
    y = CactpotSolver()
    look_correct = 0
    non_correct = 0
    random_count = 0
    for i in range(n):
        z = x.generate_hidden_board(1)
        hidden_board_look = copy.deepcopy(z[1])
        hidden_board_non = copy.deepcopy(z[1])
        real_board = z[0]
        maximum_ticket_value = y.perfect_solve_max(real_board)
        for j in range(3):
            picks_non = y.pick_no_lookahead(copy.deepcopy(hidden_board_non))
            picks_look = y.pick_lookahead(copy.deepcopy(hidden_board_look), 8)
            hidden_board_look = x.pick(hidden_board_look, real_board, random.choice(picks_look))
            hidden_board_non = x.pick(hidden_board_non, real_board, random.choice(picks_non))

        # this is wrong add a way to select from real
        selected_look = select(hidden_board_look, real_board)
        selected_non = select(hidden_board_non, real_board)
        if selected_look == maximum_ticket_value:
            look_correct += 1
        if selected_non == maximum_ticket_value:
            non_correct += 1
        random_payout = complete_hidden_payout(1, real_board)
        if random_payout == maximum_ticket_value:
            random_count += 1
    print(f"LookAhead: {(look_correct/n)*100}%")
    print(f"Non: {(non_correct/n)*100}%")
    print(f"Random: {(random_count/n)*100}%")

def compute_evs(hidden_board):
    # [x, x, x, x, x, x, x, x, 9]
    # this code is a monster
    unknowns = [1,2,3,4,5,6,7,8,9]
    knowns = []
    for y in hidden_board:
        if y != 'x':
            unknowns.remove(y)
            knowns.append(y)
    #horizontal
    ev_map = {}
    for x in range(0,3):
        total_score = 0
        total_unknowns = 0
        for j in range(3):
            if hidden_board[j+(x*3)] != 'x':
                total_score += hidden_board[j+(x*3)]
            elif hidden_board[j+(x*3)] == 'x':
                total_unknowns += 1
        list_combos = list(combinations(unknowns, total_unknowns))
        all_calcs = []
        for combo in list_combos:
            sum_of_combos = sum(combo) + total_score
            all_calcs.append(sum_of_combos)
        ev = sum(solved_board[calc] for calc in all_calcs)/len(all_calcs)
        ev_map[f'h{x+1}'] = ev
    #vertical
    for x in range(0,3):
        total_score = 0
        total_unknowns = 0
        for j in range(3):
            if hidden_board[(j*3)+(x)] != 'x':
                total_score += hidden_board[(j*3)+(x)]
            elif hidden_board[(j*3)+(x)] == 'x':
                total_unknowns += 1
        list_combos = list(combinations(unknowns, total_unknowns))
        all_calcs = []
        for combo in list_combos:
            sum_of_combos = sum(combo) + total_score
            all_calcs.append(sum_of_combos)
        ev = sum(solved_board[calc] for calc in all_calcs)/len(all_calcs)
        ev_map[f'v{x+1}'] = ev
    #diag

    total_score = 0
    total_unknowns = 0
    if hidden_board[0] != 'x':
        total_score += hidden_board[0]
    elif hidden_board[0] == 'x':
        total_unknowns += 1
    if hidden_board[4] != 'x':
        total_score += hidden_board[4]
    elif hidden_board[4] == 'x':
        total_unknowns += 1
    if hidden_board[8] != 'x':
        total_score += hidden_board[8]
    elif hidden_board[8] == 'x':
        total_unknowns += 1
    list_combos = list(combinations(unknowns, total_unknowns))
    all_calcs = []
    for combo in list_combos:
        sum_of_combos = sum(combo) + total_score
        all_calcs.append(sum_of_combos)
    ev = sum(solved_board[calc] for calc in all_calcs)/len(all_calcs)
    ev_map[f'd1'] = ev
    total_score = 0
    total_unknowns = 0
    if hidden_board[2] != 'x':
        total_score += hidden_board[2]
    elif hidden_board[2] == 'x':
        total_unknowns += 1
    if hidden_board[4] != 'x':
        total_score += hidden_board[4]
    elif hidden_board[4] == 'x':
        total_unknowns += 1
    if hidden_board[6] != 'x':
        total_score += hidden_board[6]
    elif hidden_board[6] == 'x':
        total_unknowns += 1
    list_combos = list(combinations(unknowns, total_unknowns))
    all_calcs = []
    for combo in list_combos:
        sum_of_combos = sum(combo) + total_score
        all_calcs.append(sum_of_combos)
    ev = sum(solved_board[calc] for calc in all_calcs)/len(all_calcs)
    ev_map[f'd2'] = ev
    return ev_map


class CactpotGenerator:
    def generate_board(self, preset_board=None):
        if preset_board is None:
            return self.__generate_random_board()
        if len(preset_board) == 9:
            return preset_board
        else:
            raise ValueError("Invalid board size")

    def generate_hidden_board(self, n):
        x = self.__generate_random_board()
        random_list = ['x'] * 9
        y = random.sample(range(0,9), n)
        for sample in y:
            random_list[sample] = x[sample]
        return (x, random_list)


    def __generate_random_board(self):
        x = list(range(1,10))
        random.shuffle(x)
        return x

    def pick(self, hidden_board, real_board, index):
        x = real_board[index]
        hidden_board[index] = x
        return hidden_board

class CactpotSolver:

    def generate_payouts(self, board):
        solved = []
        for j in range(0,3):
            sum_of_boards = board[j*3] + board[1+(j*3)] + board[2+(j*3)]
            solved.append(sum_of_boards)
        for j in range(0,3):
            sum_of_boards = board[j] + board[j+3] + board[j+6]
            solved.append(sum_of_boards)
        solved.append(board[0]+ board[4]+ board[8])
        solved.append(board[2]+ board[4]+ board[6])
        return solved
    def perfect_solve_max(self, board):
        return max(solved_board[x] for x in self.generate_payouts(board))

    def pick_no_lookahead(self, hidden_board):
        real_board = copy.deepcopy(hidden_board)
        unknowns = [1,2,3,4,5,6,7,8,9]
        for item in hidden_board:
            if item != 'x':
                unknowns.remove(item)
        avg_yield = []
        for i, item in enumerate(hidden_board):
            avg_list = []
            if item == "x":
                for j in unknowns:
                    hidden_board[i] = j
                    ev = compute_evs(hidden_board)
                    avg_list.append(max(list(ev.values())))
                hidden_board = copy.deepcopy(real_board)
            if len(avg_list) == 0:
                avg_yield.append(0)
            else:
                avg_yield.append(sum(avg_list)/len(avg_list))
        max_yield = max(avg_yield)
        return [i for i, x in enumerate(avg_yield) if x == max_yield]


    def pick_lookahead(self, hidden_board, n=4, in_call = False):
        # im bad at recursion so in_call is necessary here
        # n=4 cuz a traditional board only reveals 4, but you can always go deeper :3
        real_board = copy.deepcopy(hidden_board)
        count = 0
        total_ev_list = []
        unknowns = [1,2,3,4,5,6,7,8,9]
        for item in hidden_board:
            if item != 'x':
                unknowns.remove(item)
                count += 1
        if not in_call:
            lookahead = self.pick_no_lookahead(copy.deepcopy(hidden_board))
        else:
            lookahead = copy.deepcopy(unknowns)

        if n > len(real_board):
            raise IndexError("bruh can't be greater than the board size")
        if count == n and in_call:
            computed_evs = compute_evs(hidden_board)
            return list(computed_evs.values())
        elif count == n and not in_call:
            return self.pick_no_lookahead(hidden_board)
        else:
            for picked in lookahead:
                evs_list = []
                for num in unknowns:
                    hidden_board[picked] = num
                    evs_list = evs_list + self.pick_lookahead(copy.deepcopy(hidden_board), n, True)
                    if in_call:
                        return evs_list
                hidden_board = copy.deepcopy(real_board)
                if len(evs_list) != 0:
                    total_ev_list.append(sum(evs_list)/len(evs_list))
        max_indices = []
        for i, ev in enumerate(total_ev_list):
            if round(ev,3) == round(max(total_ev_list), 3):
                max_indices.append(lookahead[i])
        return max_indices

            
