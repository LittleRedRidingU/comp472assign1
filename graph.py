# -------------------------------------------------------
# Assignment 1
# Written by Lingli Lin_40065176, Yaqi Kang_40061670, Zisen Ling_40020293
# For COMP 472 Section AK-X, AI-X AL-X – Summer 2021
# --------------------------------------------------------
import sys

import matplotlib.pyplot as plt
import math
import copy

row, col = 3, 4
# graph = [
#     "🦠", "", "🎡", "",
#     "", "", "🦠", "💊",
#     "🎡", "🦠", "", ""
# ]

graph = [
    "🦠", "", "🎡", "",
    "", "", "", "💊",
    "🎡", "", "", ""
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
#     graph[i] = ["🦠", "💊", "🎡", ""][num - 1]
role = str(input("Please enter the role player(c, v, p): "))
if role == "c" or role == "v":
    start_place = int(
        input("Please enter the start place(an index of list staring from 1 to " + str(row * col) + "): ")) - 1
elif role == "p":
    start_format = str(input("Do you want to go to place, edge or point? "))
    if start_format == "place":
        role_p_detailed = "p-place"
        start_place = int(
            input("Please enter the start place(an index of list staring from 1 to " + str(row * col) + "): ")) - 1
    elif start_format == "edge":
        role_p_detailed = "p-edge"
        start_point1 = int(ord(input("Please enter the first point of edge in format of alphabet ")) - 65)
        start_point2 = int(ord(input("Please enter the second point of edge in format of alphabet ")) - 65)
    elif start_format == "point":
        role_p_detailed = "p-point"
        start_point = int(ord(input("Please enter the point in format of alphabet ")) - 65)
    else:
        role_p_detailed = "undefined"


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
def get_starting_point():
    # c: 'right-top', v: 'left-bottom', p: 'should be any surrounding points? or surrounding edges only? confused!'
    if role == 'c':
        start_point_list = points_near_place(start_place)
        return start_point_list[1]
    elif role == 'v':
        start_point_list = points_near_place(start_place)
        return start_point_list[2]
    elif role == 'p':
        if role_p_detailed == 'p-place':
            return start_place
        elif role_p_detailed == 'p-edge':
            return [start_point1, start_point2]
        elif role_p_detailed == 'p-point':
            return start_point
        else:
            print("start format error: \"undefined\", system terminated")
            sys.exit()


# define a method to check places near a (index of the) place
def places_near_place(place):
    # a list of surrounding places, [Up, left, right, bottom]
    np_list = [place - col, place - 1, place + 1, place + col]
    # check if place out of requirements, replace with ""
    for index, number in enumerate(np_list):
        if number > (row * col - 1) or number < 0:
            np_list[index] = ""
    # check if a place is left most or right most, replace with ""
    # left most checking
    if place % col == 0:
        np_list[1] = ""
    # right most checking
    elif place % col == col - 1:
        np_list[2] = ""
    return np_list


def cost(place):
    return {"c": {"🦠": 0, "💊": 2, "🎡": 3, "": 1},
            "v": {"🦠": 3, "💊": 0, "🎡": 1, "": 2, },
            "p": {"🦠": math.inf, "💊": 2, "🎡": 0, "": 1},
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


# decided to make some general method for a single BFS
# what we need: costs of edges around a point, positions of points around a point
# for role v: highest cost of each diagonal line around a point, positions of those point
def point_r_level(point):
    return int((point - point % (col + 1)) / (col + 1))


def point_c_level(point):
    return int(point % (col + 1))


def cal_h_role_c(pos, des):
    return abs(point_r_level(des) - point_r_level(pos)) + abs(point_c_level(des) - point_c_level(pos))


# return positions of places around a point
def places_near_point(point):
    prl = point_r_level(point)
    return [point - prl - col - 1, point - prl - col, point - prl - 1, point - prl]


# return positions of points around a point
# [left-top, top, right-top, left, right, left-bottom, bottom, right-bottom]
# just cross: [1,3,4,6]
# just diagonal: [0,2,5,7]
def points_near_point(point):
    pnp = [point - col - 2, point - col - 1, point - col, point - 1, point + 1,
           point + col, point + col + 1, point + col + 2]
    prl = point_r_level(point)
    if pnp[0] < 0 or pnp[0] % (col + 1) == col:
        pnp[0] = ""
    if pnp[1] < 0:
        pnp[1] = ""
    if pnp[2] < 0 or pnp[2] % (col + 1) == 0:
        pnp[2] = ""
    if pnp[3] < 0 or pnp[3] % (col + 1) == col:
        pnp[3] = ""
    if pnp[4] < 0 or pnp[4] % (col + 1) == 0:
        pnp[4] = ""
    if prl == row or pnp[5] % (col + 1) == col:
        pnp[5] = ""
    if prl == row:
        pnp[6] = ""
    if prl == row or pnp[7] % (col + 1) == 0:
        pnp[7] = ""
    return pnp


# return costs of edges around a point
# note the cost of edges is in this order [up, right, down, left]
def near_point_edges(point):
    if point == "" or point < 0:
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


def diagonal_costs(li, j, k):
    if li[j] == "" or li[k] == "":
        return 10000
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


# find all desired end point of places for c
def find_end_points_by_place(place_icon):
    result = []
    for index, e in enumerate(graph):
        if e == place_icon:
            result.append(points_near_place(index))
    result = [item for sublist in result for item in sublist]
    result = list(set(result))
    return result


# estimate cost from starting point to goal point
# manhattan distance
def heuristic_role_c(s_point):
    x0, y0 = get_node_index(s_point)
    points = find_end_points_by_place("🦠")
    H = []
    for index, e in enumerate(points):
        x1, y1 = get_node_index(e)
        print(
            "\u0020||Start point (" + str(x0) + ", " + str(y0) + "), " + "end point (" + str(x1) + ", " + str(y1) + ")")
        d_x = round(float(abs(x1 - x0) * 0.2), 1)
        d_y = round(float(abs(y1 - y0) * 0.1), 1)
        H.append(d_x + d_y)
    return min(H)


# Diagonal Distance
def heuristic_role_v(s_point):
    x0, y0 = get_node_index(s_point)
    points = find_end_points_by_place("💊")
    H = []
    for index, e in enumerate(points):
        x1, y1 = get_node_index(e)
        print(
            "\u0020||Start point (" + str(x0) + ", " + str(y0) + "), " + "end point (" + str(x1) + ", " + str(y1) + ")")
        d_x = abs(x1 - x0)
        d_y = abs(y1 - y0)
        d_min = min(d_x, d_y)
        diagonal_distance = math.sqrt(0.2 ** 2 + 0.1 ** 2)
        D = 0.2 if d_x < d_y else 0.1
        H.append(round(float((d_x * 0.2 + d_y * 0.1) + diagonal_distance * d_min - 2 * D * d_min), 2))
    return min(H)


# modified manhattan distance
# we use it because the distance other than the start place is the same as manhattan distance
def heuristic_role_p(s):
    delta = 10000
    if role_p_detailed == "p-point":
        delta = 0
    elif role_p_detailed == "p-place":
        # the distance from the center to the corner:
        # This value is just right for the furthest and the nearest distance moved within the grid
        delta = math.sqrt((0.2 / 2) ** 2 + (0.1 / 2) ** 2)
    elif role_p_detailed == "p-edge":
        # the distance is the average of an edge cost and suppose role p always starting from midpoint of an edge
        delta = (0.1 + 0.2) / 2 / 2
    H = []
    x0, y0 = get_node_index(s)
    points = find_end_points_by_place("🎡")
    for e in points:
        x1, y1 = get_node_index(e)
        print(
            "\u0020||Start point (" + str(x0) + ", " + str(y0) + "), " + "end point (" + str(x1) + ", " + str(
                    y1) + ")")
        d_x = round(float(abs(x1 - x0) * 0.2), 1)
        d_y = round(float(abs(y1 - y0) * 0.1), 1)
        if d_x + d_y == 0:
            H.append(d_x + d_y)
        else:
            H.append(d_x + d_y + delta)
    return min(H)


# return selected place_near_point
def places_near_point_advanced(point):
    points_np = points_near_point(point)
    places_np = places_near_point(point)
    # hide place if corresponding point is missing
    t = {1: [0, 1], 3: [0, 2], 4: [1, 3], 6: [2, 3]}
    for ind in t:
        if points_np[ind] == "":
            for j in t[ind]:
                places_np[j] = ""
    return places_np


def A_star_c(s_point):
    # opened_list[opened=[closed_list=[], g_cost_update=[], record_cost]]
    # step 1 (initialization)
    pn_point = places_near_point_advanced(s_point)
    for x in range(len(pn_point)):
        if pn_point[x] != "" and 0 <= pn_point[x] < col * row:
            if graph[pn_point[x]] == "🦠":
                return "found"
    opened_list = [[[s_point], [0], heuristic_role_c(s_point)]]
    loop_timer = 0
    lowest_index = 0
    while loop_timer < 1000:
        # step 2 (finding the opened has lowest record_cost)
        for index, item in enumerate(opened_list):
            if item[2] <= opened_list[lowest_index][2]:
                lowest_index = index
        print("Switching opened for which has the lowest record_cost " + str(opened_list[lowest_index][2]))
        # step 3 (evaluate points, push into the opened_list)
        closed_list = opened_list[lowest_index][0]
        curr_point = opened_list[lowest_index][0][-1]
        # [left-top, top, right-top, left, right, left-bottom, bottom, right-bottom]
        points_np = points_near_point(curr_point)
        # top, right, down, left
        children = [points_np[1], points_np[4], points_np[6], points_np[3]]
        # top, right, down, left
        gn_list = near_point_edges(curr_point)
        for index, ch in enumerate(children):
            # left-top, right-top, left-bottom, right-bottom
            if ch not in closed_list:
                if ch != '':
                    place_np = places_near_point_advanced(ch)
                    # before pushing any value, check if this point has reached destination
                    for x in range(len(place_np)):
                        if place_np[x] != "" and 0 <= place_np[x] < col * row:
                            if graph[place_np[x]] == "🦠":
                                print("Position has found with lowest cost, here is the route:", end=" ")
                                for ind in opened_list[lowest_index][0]:
                                    print(chr(ind + 65), end="-")
                                print(chr(65 + ch))
                                return "found"
                    # push required value into opened_list
                    this_opened = copy.deepcopy(opened_list[lowest_index])
                    if gn_list[index] != '':
                        this_opened[1].append(float(gn_list[index]))
                        result_cost = sum(this_opened[1]) + float(gn_list[index]) + heuristic_role_c(ch)
                    else:
                        this_opened[1].append(10000)
                        result_cost = 10000
                    this_opened[0].append(ch)
                    this_opened[2] = result_cost
                    print(this_opened)
                    opened_list.append(this_opened.copy())
        # delete the opened that triggered this run
        del opened_list[lowest_index]
        loop_timer += 1
    print("no such place found, program terminated")


def A_star_v(s_point):
    # opened_list[opened=[closed_list=[], g_cost_update=[], record_cost]]
    # step 1 (initialization)
    pn_point = places_near_point_advanced(s_point)
    for x in range(len(pn_point)):
        if pn_point[x] != "" and 0 <= pn_point[x] < col * row:
            # Todo difference1
            if graph[pn_point[x]] == "💊":
                return "found"
    # Todo difference2
    opened_list = [[[s_point], [0], heuristic_role_v(s_point)]]
    loop_timer = 0
    lowest_index = 0
    while loop_timer < 1000:
        # step 2 (finding the opened has lowest record_cost)
        for index, item in enumerate(opened_list):
            if item[2] <= opened_list[lowest_index][2]:
                lowest_index = index
        print("Switching opened for which has the lowest record_cost " + str(opened_list[lowest_index][2]))
        # step 3 (evaluate points, push into the opened_list)
        closed_list = opened_list[lowest_index][0]
        curr_point = opened_list[lowest_index][0][-1]
        # [left-top, top, right-top, left, right, left-bottom, bottom, right-bottom]
        points_np = points_near_point(curr_point)
        # top, right, down, left
        # Todo difference3
        children = points_np
        # Todo difference4
        # [up, right, down, left]
        gn_list_cross = near_point_edges(curr_point)
        # [left-top, right-top, left-bottom, right-bottom]
        gn_list_diagonal = diagonal_line(curr_point)
        # [left - top, top, right - top, left, right, left - bottom, bottom, right - bottom]
        gn_list = [gn_list_diagonal[0], gn_list_cross[0], gn_list_diagonal[1], gn_list_cross[3], gn_list_cross[1],
                   gn_list_diagonal[2], gn_list_cross[2], gn_list_diagonal[3]]
        for index, ch in enumerate(children):
            # left-top, right-top, left-bottom, right-bottom
            if ch not in closed_list:
                if ch != '':
                    place_np = places_near_point_advanced(ch)
                    # before pushing any value, check if this point has reached destination
                    for x in range(len(place_np)):
                        if place_np[x] != "" and 0 <= place_np[x] < col * row:
                            # TODO difference5
                            if graph[place_np[x]] == "💊":
                                print("Position has found with lowest cost, here is the route:", end=" ")
                                for ind in opened_list[lowest_index][0]:
                                    print(chr(ind + 65), end="-")
                                print(chr(65 + ch))
                                return "found"
                    # push required value into opened_list
                    this_opened = copy.deepcopy(opened_list[lowest_index])
                    if gn_list[index] != '':
                        this_opened[1].append(float(gn_list[index]))
                        # TODO difference6
                        result_cost = sum(this_opened[1]) + float(gn_list[index]) + heuristic_role_v(ch)
                    else:
                        this_opened[1].append(10000)
                        result_cost = 10000
                    this_opened[0].append(ch)
                    this_opened[2] = result_cost
                    print(this_opened)
                    opened_list.append(this_opened.copy())
        # delete the opened that triggered this run
        del opened_list[lowest_index]
        loop_timer += 1
    print("no such place found, program terminated")


def starter_p(s):
    place_n_point = ""
    points_n_place = []
    if role_p_detailed == "p-point":
        points_n_place = [s]
        place_n_point = places_near_point_advanced(s)
    elif role_p_detailed == "p-place":
        points_n_place = points_near_place(s)
        place_n_point = [places_near_point_advanced(points_n_place[0]), places_near_point_advanced(points_n_place[1]),
                         places_near_point_advanced(points_n_place[2]), places_near_point_advanced(points_n_place[3])]
        place_n_point = [num for elem in place_n_point for num in elem]
    elif role_p_detailed == "p-edge":
        points_n_place = s
        place_n_point = [places_near_point_advanced(s[0]), places_near_point_advanced(s[1])]
        place_n_point = [num for elem in place_n_point for num in elem]
    for x in range(len(place_n_point)):
        if place_n_point[x] != "" and 0 <= place_n_point[x] < col * row:
            if graph[place_n_point[x]] == "🎡":
                return "found"
    lowest_index = 0
    best_p_list = []
    for s in points_n_place:
        best_p_list.append(A_star_p(s))
    for index, item in enumerate(best_p_list):
        if item[2] <= best_p_list[lowest_index][2]:
            lowest_index = index
    print("Position has found with lowest cost, here is the route:", end=" ")
    for ind in best_p_list[lowest_index][0]:
        print(chr(ind + 65), end="-")
    print("")


def A_star_p(s):
    # opened_list[opened=[closed_list=[], g_cost_update=[], record_cost]]
    # step 1 (initialization)
    opened_list = [[[s], [0], heuristic_role_p(s)]]
    loop_timer = 0
    lowest_index = 0
    while loop_timer < 1000:
        # step 2 (finding the opened has lowest record_cost)
        for index, item in enumerate(opened_list):
            if item[2] <= opened_list[lowest_index][2]:
                lowest_index = index
        print("Switching opened for which has the lowest record_cost " + str(opened_list[lowest_index][2]))
        # step 3 (evaluate points, push into the opened_list)
        closed_list = opened_list[lowest_index][0]
        curr_point = opened_list[lowest_index][0][-1]
        # [left-top, top, right-top, left, right, left-bottom, bottom, right-bottom]
        points_np = points_near_point(curr_point)
        # top, right, down, left
        children = [points_np[1], points_np[4], points_np[6], points_np[3]]
        # top, right, down, left
        gn_list = near_point_edges(curr_point)
        for index, ch in enumerate(children):
            # left-top, right-top, left-bottom, right-bottom
            if ch not in closed_list:
                if ch != '':
                    place_np = places_near_point_advanced(ch)
                    # before pushing any value, check if this point has reached destination
                    for x in range(len(place_np)):
                        if place_np[x] != "" and 0 <= place_np[x] < col * row:
                            # TODO 2
                            if graph[place_np[x]] == "🎡":
                                this_opened = copy.deepcopy(opened_list[lowest_index])
                                if gn_list[index] != '':
                                    this_opened[1].append(float(gn_list[index]))
                                    result_cost = sum(this_opened[1]) + float(gn_list[index]) + heuristic_role_c(ch)
                                else:
                                    this_opened[1].append(10000)
                                    result_cost = 10000
                                this_opened[0].append(ch)
                                this_opened[2] = result_cost
                                return this_opened
                    # push required value into opened_list
                    this_opened = copy.deepcopy(opened_list[lowest_index])
                    if gn_list[index] != '':
                        this_opened[1].append(float(gn_list[index]))
                        result_cost = sum(this_opened[1]) + float(gn_list[index]) + heuristic_role_c(ch)
                    else:
                        this_opened[1].append(10000)
                        result_cost = 10000
                    this_opened[0].append(ch)
                    this_opened[2] = result_cost
                    print(this_opened)
                    opened_list.append(this_opened.copy())
        # delete the opened that triggered this run
        del opened_list[lowest_index]
        loop_timer += 1
    print("no such place found")
    return [[[-1], [0], 100000]]


#     # return a list of cost when point p inside of grid place
# def cost_role_p_inside(place):
#     edge_cost_near_p = []
#     # up, left, right, bottom
#     place_near_p = places_near_place(place)
#     for j in range(len(place_near_p)):
#         # get cost of 4 edges around place, order is up, left, right and bottom
#         edge_cost_near_p.append((edge_cost(place_near_p[j], place)) + cost(place))
#     return edge_cost_near_p


# def calling_for_P(index_of_place, point1, point2):
#     if index_of_place == "" and point1 != "" and point2 != "":
#         "edge"
#     if index_of_place == "" and point1 != "" and point2 == "":
#         "point1"
#     if index_of_place == "" and point1 == "" and point2 != "":
#         "point2"
#     if index_of_place != "" and point1 == "" and point2 == "":
#         "place"


# keyIn = input("Please enter the point to get surrounding edge costs: ")
# check = ord(keyIn) - 65
#
# print("The point index around point " + keyIn + " are " + str(points_near_point(check)))
# print("The cost of crossing edges around point " + keyIn + " are " + str(near_point_edges(check)))
# print("The cost of diagonal line around point " + keyIn + " are " + str(diagonal_line(check)))


start_p = get_starting_point()
# end_p = ord(input("Please insert end point:")) - 65
if role == 'p':
    if role_p_detailed == 'p-place':
        print("Your starting place is " + str(start_p+1))
    elif role_p_detailed == 'p-edge':
        print("Your starting edge is " + chr(start_p[0] + 65) + "-" + chr(start_p[1] + 65))
    elif role_p_detailed == 'p-point':
        print("Your starting point is " + chr(start_p + 65) + "(index:" + str(start_p) + ") ")
elif role == 'c' or 'v':
    print("Your starting point is " + chr(start_p + 65) + "(index:" + str(start_p) + ") ")
print("********************")
if role == 'c':
    A_star_c(start_p)
elif role == 'v':
    A_star_v(start_p)
elif role == 'p':
    starter_p(start_p)
print("----end of program----")

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
