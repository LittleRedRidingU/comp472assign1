import matplotlib.pyplot as plt
import math
import Astar

row, col = 3, 4
# graph = [
#     "🦠", "💊", "🎡", "",
#     "💊", "", "🦠", "",
#     "🎡", "🦠", "💊", "💊"
# ]

graph = [
    "🦠", "💊", "🎡", "",
    "💊", "", "", "",
    "🎡", "", "💊", "💊"
]

# full demo
# row = int(input("please enter your desired row number: "))
# col = int(input("please enter your desired column number: "))
# print('__________________________________________________')
# print('note: 1 for quarantine, 2 for vaccine, 3 for playground, 0 for empty')
# print('Example: 1 2 3 0 2 0 1 0 3 1 2 2')
# graph = list(map(int, input("please enter the place arrangement list(" + str(row * col) + "): ").split()))
# print('__________________________________________________')
# for i, num in enumerate(graph):
#     graph[i] = ["🦠", "💊", "🎡", ""][num-1]
role = str(input("please enter the role player(c, v, p): "))
start_place = int(
    input("please enter the start place(an index of list staring from 1 to " + str(row * col) + "): ")) - 1


def col_index(place):
    return place % col


def row_level(place):
    return int((place - col_index(place)) / col)


# a list of surrounding points, [left-top, right-top, left-bottom, right-bottom]
def points_near_place(place):
    r_level = row_level(place)
    return [place + r_level, place + r_level + 1, place + r_level + col + 1,
            place + r_level + col + 2]


# decision making of the staring point:

start_point_list = points_near_place(start_place)
# c: 'right-top', v: 'left-bottom', p: 'should be any surrounding points? or surrounding edges only? confused!'
if role == 'c':
    print(start_point_list[1])
if role == 'v':
    print(start_point_list[2])
if role == 'p':
    print(start_point_list)


def get_starting_point():
    start_point_list = points_near_place(start_place)
    # c: 'right-top', v: 'left-bottom', p: 'should be any surrounding points? or surrounding edges only? confused!'
    if role == 'c':
        return start_point_list[1]
    if role == 'v':
        return start_point_list[2]
    # if role == 'p':
    #     return (start_point_list)


# define a method to check places near a (index of the) place
def places_near_place(p):
    # a list of surrounding places, [Up, left, right, bottom]
    np_list = [p - col, p - 1, p + 1, p + col]
    # check if place out of requirements, replace with ""
    for index, number in enumerate(np_list):
        if number > (row * col - 1) or number < 0:
            np_list[index] = ""
    # check if a place is left most or right most, replace with ""
    # left most checking
    if p % col == 0:
        np_list[1] = ""
    # right most checking
    elif p % col == col - 1:
        np_list[2] = ""
    return np_list


def cost(place):
    return {"c": {"🦠": 0, "💊": 2, "🎡": 3, "": 1},
            "v": {"🦠": 3, "💊": 0, "🎡": 1, "": 2, },
            "p": {"🦠": 'inf', "💊": 2, "🎡": 0, "": 1},
            }[role][place]


def edge_cost(place1, place2):
    if place1 != '' and place2 != '':
        return (float(cost(graph[place1])) + float(cost(graph[place2]))) / 2
    if place1 == '' or place2 == '':
        if place1 != '':
            return cost(graph[place1])
        elif place2 != '':
            return cost(graph[place2])
        else:
            return ''


# cost of each edge (for entered role)
# start recording costs of row edges
# In default just get top edges, if target place is at bottom,
# save it to another list, and put them back once place list is empty
# later on this part was decided to serve graphs only.
cost_r = []
cost_r_bottom = []
for i, p in enumerate(graph):
    neighbors = places_near_place(i)
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

# start recording costs of col edges
cost_c = []
for i, p in enumerate(graph):
    neighbors = places_near_place(i)
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

print(cost_r)
print(cost_c)


# decided to make some general method for a single BFS
# what we need: costs of edges around a point, positions of points around a point
# for role v: highest cost of each diagonal line around a point, positions of those point
def point_r_level(point):
    return int((point - point % (col + 1)) / (col + 1))


def point_c_level(point):
    return int(point % (col + 1))


def cal_h_role_c(pos, des):
    return abs(point_r_level(des) - point_r_level(pos)) + abs(point_c_level(des) - point_c_level(pos))


# For testing
print(point_r_level(7))
print(point_c_level(7))
print(cal_h_role_c(4, 8))


# return positions of places around a point
def places_near_point(point):
    prl = point_r_level(point)
    return [point - prl - col - 1, point - prl - col, point - prl - 1, point - prl]


# return positions of points around a point
# [left-top, top, right-top, left, right, left-bottom, bottom, right-bottom]
# just cross: [1,3,4,6]
# just diagonal: [0,2,5,7]
def points_near_point(point):
    li = [point - col - 2, point - col - 1, point - col, point - 1, point + 1,
          point + col, point + col + 1, point + col + 2]
    for k, item in enumerate(li):
        if item < 0:
            li[k] = ''
    return li


# return costs of edges around a point
# note the cost of edges is in this order [up, right, down, left]
def near_point_edges(point):
    if point < 0:
        return ["", "", "", ""]
    pnp = places_near_point(point)
    prl = point_r_level(point)
    if pnp[0] < 0 or point % (col + 1) == 0:
        pnp[0] = ""
    if pnp[1] <= 0 or point % (col + 1) == col:
        pnp[1] = ""
    if prl == row or point % (col + 1) == 0:
        pnp[2] = ""
    if prl == row or point % (col + 1) == col:
        pnp[3] = ""
    edges = [edge_cost(pnp[0], pnp[1]),
             edge_cost(pnp[1], pnp[3]),
             edge_cost(pnp[3], pnp[2]),
             edge_cost(pnp[2], pnp[0])]
    return edges


# [ top, left, right, bottom]
def points_near_point_c(point):
    li = [point - col - 1, point + 1,
          point + col +1, point - 1]
    for k, item in enumerate(li):
        if item < 0:
            li[k] = ''
    list_edge = near_point_edges(point)
    for i in range((len(list_edge))):
        if list_edge[i] == '':
            li[i] = ''
    return li

print(points_near_point_c(1))
print(near_point_edges(1))
print("CCCCCCCCCCCCCCCCCCC")

def diagonal_costs(li, j, k):
    if li[j] == "" or li[k] == "":
        return ""
    else:
        return math.sqrt(li[j] ** 2 + li[k] ** 2)


# return cost of diagonal line [left-top, right-top, left-bottom, right-bottom
def diagonal_line(point):
    pn_point = points_near_point(point)
    diagonal_list = []
    # gather the edge data of surrounding points
    left_point_npe = near_point_edges(pn_point[3])
    top_point_npe = near_point_edges(pn_point[1])
    right_point_npe = near_point_edges(pn_point[4])
    bottom_point_npe = near_point_edges(pn_point[6])
    # find diagonal costs
    left_n_top_cost = diagonal_costs(left_point_npe, 0, 1)
    top_n_left_cost = diagonal_costs(top_point_npe, 2, 3)
    diagonal_list.append(max(left_n_top_cost, top_n_left_cost))
    right_n_top_cost = diagonal_costs(right_point_npe, 0, 3)
    top_n_right_cost = diagonal_costs(top_point_npe, 2, 1)
    diagonal_list.append(max(right_n_top_cost, top_n_right_cost))
    left_n_bottom_cost = diagonal_costs(left_point_npe, 2, 1)
    bottom_n_left_cost = diagonal_costs(bottom_point_npe, 0, 3)
    diagonal_list.append(max(left_n_bottom_cost, bottom_n_left_cost))
    right_n_bottom_cost = diagonal_costs(right_point_npe, 2, 3)
    bottom_n_right_cost = diagonal_costs(bottom_point_npe, 0, 1)
    diagonal_list.append(max(right_n_bottom_cost, bottom_n_right_cost))
    return diagonal_list


# get node index
def get_node_index(point):
    return point_c_level(point), point_r_level(point)


# estimate cost from starting point to goal point
def heuristic_role_c(start_point, end_point):
    x0, y0 = get_node_index(start_point)
    print("x %d" % x0)
    print(y0)
    x1, y1 = get_node_index(end_point)
    print(x1)
    print(y1)
    d_x = round(float(abs(x1 - x0) * 0.2), 1)
    d_y = round(float(abs(y1 - y0) * 0.1), 1)
    return d_x + d_y


# [up, right, down, left]
g_cost_n = []
open_list_c=[]
close_list_c=[]
def move_node_c(curr_point, goal_point ):

    x0, y0 = get_node_index(curr_point)
    x1, y1 = get_node_index(goal_point)
    # [up, right, down, left]
    child = points_near_point_c(curr_point)


    open_list_c.extend(child)
    for i in range(len(open_list_c)):
        if open_list_c[i]==curr_point:
            open_list_c[i]=''
    close_list_c.append(curr_point)

    gn_list = near_point_edges(curr_point)
    g_total = 0
    if len(g_cost_n)==0:
        g_total=0
    elif len(g_cost_n)==1:
        g_total = g_cost_n[0]
    else:
        for i in range(len(g_cost_n)):
            g_total = g_total+g_cost_n[i]


    if gn_list[0] != '':
        up = gn_list[0] + heuristic_role_c(child[0], goal_point)
    else:
        up = 100000
    if gn_list[1] != '':
        right = gn_list[1] + heuristic_role_c(child[1], goal_point)
    else:
        right = 100000
    if gn_list[2] != '':
        down = gn_list[2] + heuristic_role_c(child[2], goal_point)
    else:
        down = 100000
    if gn_list[3] != '':
        left = gn_list[3] + heuristic_role_c(child[3], goal_point)
    else:
        left = 100000
    print("4 ponts up,rith,down,left")
    print(up)
    print(right)
    print(down)
    print(left)

    print("4 ponts end")
    min_cost = min(up, right, down, left)
    if min_cost == up:
        y0 = y0 - 1
        g_cost_n.append(gn_list[0]+g_total)
    elif min_cost == right:
        x0 = x0 + 1
        g_cost_n.append(gn_list[1]+g_total)
    elif min_cost == down:
        y0 = y0 + 1
        g_cost_n.append(gn_list[2]+g_total)
    elif min_cost == left:
        x0 = x0 - 1
        g_cost_n.append(gn_list[3]+g_total)

    next_point = (y0 * (col + 1) + x0)
    return next_point



def A_star_c(start_point, end_point):

    place_index = places_near_point(start_point)
    a=get_node_index(start_point)
    print(a)
    print("The current point is %d" % start_point)


    flag = True
    while flag:
        print("sssssssss")
        print(get_node_index(start_point))
        print("nNNNNNN")

        next_point=move_node_c(start_point, end_point)

        print("The next point is %d" % next_point)

        print( places_near_point(next_point))

        for i in range(len(place_index)):
            if place_index[i]>=0 and place_index[i]< col*row:

                if graph[place_index[i]] == "🦠":
                    print("You already the goal state")
                    flag = False
                    break
                else:
                    print("we will keep searching")

                    start_point = move_node_c(next_point, end_point)
                    print("The another&& next point is %d" % start_point)
                    break
    print("find place finally")
    return








# return a list of cost when point p inside of grid place
def cost_role_p_inside(place):
    edge_cost_near_p = []
    # up, left, right, bottom
    place_near_p = places_near_place(place)
    for j in range(len(place_near_p)):
        # get cost of 4 edges around place, order is up, left, right and bottom
        edge_cost_near_p.append((edge_cost(place_near_p[j], place)) + cost(place))
    return edge_cost_near_p


# # point could be A,B,C,D etc...but put in order of left_top, right_top, left_down, right_down
# def get_grid_index(point_a, point_b, point_c, point_d):
#     left_top_point = ord(point_a)
#     right_top_point = ord(point_b)
#     left_down_point = ord(point_c)
#     right_down_point = ord(point_d)
#     if ( abs(left_top_point - right_top_point)!=1 or abs(left_down_point-right_down_point)!=1 )


keyIn = input("please enter the point to get surrounding edge costs: ")
check = ord(keyIn) - 65

print("the point index around point " + keyIn + " are " + str(points_near_point(check)))
print("the cost of crossing edges around point " + keyIn + " are " + str(near_point_edges(check)))
#print("the cost of diagonal line around point " + keyIn + " are " + str(diagonal_line(check)))
start_p = get_starting_point()
end_point = ord(input("please insert end point:")) - 65

print(end_point)
print("********************")
print(start_p)
print("********************")

A_star_c(start_p, end_point)



print("bbb********************")


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
