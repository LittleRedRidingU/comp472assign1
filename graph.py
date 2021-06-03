import matplotlib.pyplot as plt

# quick demo
# row, col = 3, 4
# graph = [
#     "🦠", "💊", "🎡", "",
#     "💊", "", "🦠", "",
#     "🎡", "🦠", "💊", "💊"
# ]

# full demo
row = int(input("please enter your desired row number: "))
col = int(input("please enter your desired column number: "))
print('__________________________________________________')
print('note: 1 for quarantine, 2 for vaccine, 3 for playground, 0 for empty')
print('Example: 1 2 3 0 2 0 1 0 3 1 2 2')
graph = list(map(int, input("please enter the place arrangement list(" + str(row * col) + "): ").split()))
print('__________________________________________________')
for i, num in enumerate(graph):
    graph[i] = ["🦠", "💊", "🎡", ""][num-1]
role = str(input("please enter the role player(c, v, p): "))
start_place = int(
    input("please enter the start place(an index of list staring from 1 to " + str(row * col) + "): ")) - 1


def col_index(place):
    return place % col


def row_level(place):
    return int((place - col_index(place)) / col)


# a list of surrounding points, [left-top, right-top, left-bottom, right-bottom]
def near_place_list(place):
    r_level = row_level(place)
    return [place + r_level, place + r_level + 1, place + r_level + col + 1,
            place + r_level + col + 2]


# decision making of the staring point:
start_point_list = near_place_list(start_place)
# c: 'right-top', v: 'left-bottom', p: 'should be any surrounding points? or surrounding edges only? confused!'
if role == 'c':
    print(start_point_list[1])
if role == 'v':
    print(start_point_list[2])
if role == 'p':
    print(start_point_list)


# define a method for near place checking
def near_place(p):
    # a list of surrounding places, [Up, left, right, bottom]
    near_place_list = [p - col, p - 1, p + 1, p + col]
    # check if place out of requirements, replace with ""
    for index, number in enumerate(near_place_list):
        if number > (row * col - 1) or number < 0:
            near_place_list[index] = ""
    # check if a place is left most or right most, replace with ""
    # left most checking
    if p % col == 0:
        near_place_list[1] = ""
    # right most checking
    elif p % col == col - 1:
        near_place_list[2] = ""
    return near_place_list


def cost(place):
    return {"c": {"🦠": 0, "💊": 2, "🎡": 3, "": 1},
            "v": {"🦠": 3, "💊": 0, "🎡": 1, "": 2, },
            "p": {"🦠": 'inf', "💊": 2, "🎡": 0, "": 1},
            }[role][place]


def edge_cost(place1, place2):
    if place1 != '' and place2 != '':
        return (float(cost(graph[place1])) + float(cost(graph[place2])))/2
    if place1 == '' or place2 == '':
        if place1 != '':
            return cost(graph[place1])
        elif place2 != '':
            return cost(graph[place2])
        else:
            return ''


# cost of edges around point
def near_point_edges(point):
    # find places around point
    point_r_level = int((point - point % (col + 1)) / (col + 1))
    print(point_r_level)
    near_point_places = [point - point_r_level - col - 1, point - point_r_level - col, point - point_r_level - 1,
                         point - point_r_level]
    if near_point_places[0] < 0 or point % (col + 1) == 0:
        near_point_places[0] = ""
    if near_point_places[1] <= 0 or point % (col + 1) == col:
        near_point_places[1] = ""
    if point_r_level == row or point % (col + 1) == 0:
        near_point_places[2] = ""
    if point_r_level == row or point % (col + 1) == col:
        near_point_places[3] = ""
    print(near_point_places)
    edges = [edge_cost(near_point_places[0], near_point_places[1]),
             edge_cost(near_point_places[1], near_point_places[3]),
             edge_cost(near_point_places[3], near_point_places[2]),
             edge_cost(near_point_places[2], near_point_places[0])]
    return edges


print(near_point_edges(int(input("please enter the index of a point to get surrounding edge costs"))))

# cost of each edge (for entered role)
# start recording costs of row edges
# In default just get top edges, if target place is at bottom,
# save it to another list, and put them back once place list is empty
cost_r = []
cost_r_bottom = []
for i, p in enumerate(graph):
    neighbors = near_place(i)
    if neighbors[0] == "":
        cost_top = cost(p)
    else:
        if cost(p) == 'inf' or cost(graph[neighbors[0]]) == 'inf':
            cost_top = 'inf'
        else:
            cost_top = (cost(p) + cost(graph[neighbors[0]])) / 2
    cost_r.append(cost_top)
    if row_level(i) + 1 == row:
        cost_r_bottom.append(cost(p))
cost_r.extend(cost_r_bottom)

cost_c = []
for i, p in enumerate(graph):
    neighbors = near_place(i)
    if neighbors[1] == "":
        cost_left = cost(p)
    else:
        if cost(p) == 'inf' or cost(graph[neighbors[1]]) == 'inf':
            cost_left = 'inf'
        else:
            cost_left = (cost(p) + cost(graph[neighbors[1]])) / 2
    cost_c.append(cost_left)
    if col_index(i) + 1 == col:
        cost_c.append(cost(p))

# graph part:
# 1. grid drawing
fig, ax = plt.subplots(figsize=(col * 2, row))
plt.axis("off")
for r in range(0, row + 1):
    ax.plot([0, col * 2], [r, r], "k-", lw=1)
for c in range(0, (col + 1) * 2, 2):
    ax.plot([c, c], [0, row], "k-", lw=1)
# 2. add pics
for i, txt in enumerate(graph):
    ax.annotate(
        txt if txt else str(i + 1),
        ((i % col) * 2 + 1, (row - i // col) - 0.5),
        ha="center", va="center",
        fontsize=30,
        fontname="Segoe UI Emoji")
# 3. add name to the point (staring from A)
for rc in range((col + 1) * (row + 1)):
    ax.annotate(
        chr(rc + 65) if rc < 26 else chr((rc % 26) + 65) + str(rc // 26),
        ((rc % (col + 1)) * 2 + 0.1, ((row + 1) - rc // (col + 1)) - 1) if (rc % (col + 1)) == 0 else (
            (rc % (col + 1)) * 2 - 0.1, ((row + 1) - rc // (col + 1)) - 1),
        ha="left" if (rc % (col + 1)) == 0 else "right",
        va="bottom",
        fontsize=15,
        fontname="Segoe UI Emoji")
# 4. display edge cost of row
for r in range(col * (row + 1)):
    ax.annotate(
        cost_r[r],
        ((r % col) * 2 + 0.95, ((row + 1) - r // col) - 1.13),
        ha="left",
        va="bottom",
        fontsize=12,
        fontname="Segoe UI Emoji",
        color='red',
        bbox=dict(facecolor='w', edgecolor='none', pad=0))
# 5. display edge cost of col
for c in range((col + 1) * row):
    ax.annotate(
        cost_c[c],
        ((c % (col + 1)) * 2 - 0.05, (row - c // (col + 1)) - 0.65),
        ha="left",
        va="bottom",
        fontsize=12,
        fontname="Segoe UI Emoji",
        color='red',
        bbox=dict(facecolor='w', edgecolor='none', pad=0))
plt.show()
