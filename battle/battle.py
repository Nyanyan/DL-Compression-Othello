import subprocess
from random import shuffle
from tqdm import trange
from random import shuffle, choice
import matplotlib.pyplot as plt
import japanize_matplotlib
from othello_py import *

level = 5

N_SET_GAMES = 500

print('level', level, 'n_games', N_SET_GAMES)
#'''
player_info = [
    ['edax-4.4', 'eval.dat'],
    #['default_eval', 'eval.egev'],
    ['既存手法', 'sgd.egev'],
    ['モデル16', 'model16.egev'],
    ['モデル32', 'model32.egev'],
    ['モデル64', 'model64.egev'],
    ['モデル128', 'model128.egev'],
    ['モデル256', 'model256.egev'],
    ['8bit圧縮', '8bit.egev'],
    ['4bit圧縮', '4bit.egev'],
]
CODINGAME = False
EDAX = True
#'''
'''
player_info = [
    ['codingame', ''], 
    ['edax-4.4', 'eval.dat'],
    ['既存手法', 'sgd.egev'],
    ['モデル16', 'model16.egev'],
    ['モデル32', 'model32.egev'],
    ['モデル64', 'model64.egev'],
    ['モデル128', 'model128.egev'],
    ['モデル256', 'model256.egev'],
    ['8bit圧縮', '8bit.egev'],
    ['4bit圧縮', '4bit.egev'],
]
CODINGAME = True
EDAX = True
'''

players = []

if CODINGAME:
    players.append(
        [
            'codingame', 
            '', 
            [
                subprocess.Popen(('codingame.out ' + str(level)).split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL),
                subprocess.Popen(('codingame.out ' + str(level)).split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            ],
            # W D L
            [[0, 0, 0] for _ in range(len(player_info))]
        ]
    )

if EDAX:
    players.append(
        [
            'edax-4.4', 
            'eval.dat', 
            [
                subprocess.Popen(('edax-4.4 -q -l ' + str(level)).split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL),
                subprocess.Popen(('edax-4.4 -q -l ' + str(level)).split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            ],
            # W D L
            [[0, 0, 0] for _ in range(len(player_info))]
        ]
    )

start_idx = 0
if CODINGAME:
    start_idx += 1
if EDAX:
    start_idx += 1
for name, eval_file in player_info[start_idx:]:
    players.append(
        [
            name, 
            eval_file, 
            [
                subprocess.Popen(('Egaroucid_for_Console_6_3_0_Windows_x64_SIMD/Egaroucid_for_Console_6_3_0_x64_SIMD.exe -quiet -nobook -level ' + str(level) + ' -eval eval/' + eval_file).split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL),
                subprocess.Popen(('Egaroucid_for_Console_6_3_0_Windows_x64_SIMD/Egaroucid_for_Console_6_3_0_x64_SIMD.exe -quiet -nobook -level ' + str(level) + ' -eval eval/' + eval_file).split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            ],
            # W D L
            [[0, 0, 0] for _ in range(len(player_info))]
        ]
    )

with open('xot/openingslarge.txt', 'r') as f:
    openings = [elem for elem in f.read().splitlines()]

shuffle(openings)

def play_battle(p0_idx, p1_idx, opening_idx):
    if CODINGAME and (p0_idx == 0 or p1_idx == 1) and level > 5:
        for i in range(2):
            players[0][2][i].kill()
            players[0][2][i] = subprocess.Popen(('codingame.out ' + str(level)).split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    player_idxes = [p0_idx, p1_idx]
    opening = openings[opening_idx]
    for player in range(2): # which plays black. p0 plays `player`, p1 plays `1 - player`
        record = ''
        o = othello()
        # play opening
        for i in range(0, len(opening), 2):
            if not o.check_legal():
                o.player = 1 - o.player
                o.check_legal()
            x = ord(opening[i].lower()) - ord('a')
            y = int(opening[i + 1]) - 1
            record += opening[i] + opening[i + 1]
            o.move(y, x)
        # play with ai
        while True:
            if not o.check_legal():
                o.player = 1 - o.player
                if not o.check_legal():
                    break
            grid_str = 'setboard '
            for yy in range(hw):
                for xx in range(hw):
                    if o.grid[yy][xx] == black:
                        grid_str += 'b'
                    elif o.grid[yy][xx] == white:
                        grid_str += 'w'
                    else:
                        grid_str += '.'
            if o.player == black:
                grid_str += ' b\n'
            else:
                grid_str += ' w\n'
            player_idx = player_idxes[o.player ^ player]
            #print(players[player_idx][0], grid_str[:-1])
            players[player_idx][2][player].stdin.write(grid_str.encode('utf-8'))
            players[player_idx][2][player].stdin.write('go\n'.encode('utf-8'))
            players[player_idx][2][player].stdin.flush()
            line = ''
            while line == '' or line == '>':
                line = players[player_idx][2][player].stdout.readline().decode().replace('\r', '').replace('\n', '')
            coord = line[-2:].lower()
            #print(players[player_idx][0], coord)
            try:
                y = int(coord[1]) - 1
                x = ord(coord[0]) - ord('a')
            except:
                print('error')
                print(grid_str[:-1])
                print(o.player, player)
                print(coord)
                for i in range(2):
                    players[i][2][player].kill()
                    #players[i][2][player].stdin.write('quit\n'.encode('utf-8'))
                    #players[i][2][player].stdin.flush()
                exit()
            record += chr(ord('a') + x) + str(y + 1)
            if not o.move(y, x):
                o.print_info()
                print(grid_str[:-1])
                print(o.player, player)
                print(coord)
                print(y, x)
        if o.n_stones[player] > o.n_stones[1 - player]:
            players[p0_idx][3][p1_idx][0] += 1
            players[p1_idx][3][p0_idx][2] += 1
        elif o.n_stones[player] < o.n_stones[1 - player]:
            players[p1_idx][3][p0_idx][0] += 1
            players[p0_idx][3][p1_idx][2] += 1
        else:
            players[p0_idx][3][p1_idx][1] += 1
            players[p1_idx][3][p0_idx][1] += 1
    

def print_result():
    for i in range(len(players)):
        w = 0
        d = 0
        l = 0
        for ww, dd, ll in players[i][3]:
            w += ww
            d += dd
            l += ll
        r = (w + d * 0.5) / max(1, w + d + l)
        print(i, players[i][0], players[i][1], w + d + l, w, d, l, r, sep='\t')

def print_all_result():
    for i in range(len(players)):
        name, eval_file, _, result = players[i]
        print(name, end='\t')
        for j in range(len(players)):
            if i == j:
                print('-', end='\t')
            else:
                w, d, l = result[j]
                r = (w + d * 0.5) / max(1, w + d + l)
                print("{:.4f}".format(r), end='\t')
        w = 0
        d = 0
        l = 0
        for ww, dd, ll in players[i][3]:
            w += ww
            d += dd
            l += ll
        r = (w + d * 0.5) / max(1, w + d + l)
        print("{:.4f}".format(r))


plot_data = [[] for _ in range(len(players))]

def output_plt():
    for i in range(len(players)):
        w = 0
        d = 0
        l = 0
        for ww, dd, ll in players[i][3]:
            w += ww
            d += dd
            l += ll
        r = (w + d * 0.5) / max(1, w + d + l)
        plot_data[i].append(r)
        name = players[i][0]
        plt.plot(plot_data[i], label=name)
    plt.xlabel('n_battles')
    plt.ylabel('win rate (%)')
    plt.legend(loc='upper center', bbox_to_anchor=(.5, -.15), ncol=3)
    plt.savefig('graph.png', bbox_inches='tight')
    plt.clf()

print('n_players', len(players))

for i in range(N_SET_GAMES):
    for p0 in range(len(players)):
        #for p0 in [0]: # codingame vs others
        for p1 in range(p0 + 1, len(players)):
            play_battle(p0, p1, i)
    print(i)
    print_result()
    print_all_result()
    output_plt()

print('done', N_SET_GAMES, 'level', level)
print_all_result()
    

for i in range(len(players)):
    for j in range(2):
        players[i][2][j].kill()
        #players[i][2][j].stdin.write('quit\n'.encode('utf-8'))
        #players[i][2][j].stdin.flush()
