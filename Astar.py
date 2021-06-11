# import graph
#
#
# opened_list = [[[graph.start_p], [0], graph.heuristic_role_c(graph.start_p)]]
#
#
#
#
#
#
#
#
#
#
# def move_node_c(curr_point):
#     # if goal point is reached, return current point
#     x0, y0 = get_node_index(curr_point)
#     # indices of four points near curr_point
#     children = points_near_point_c(curr_point)
#
#     for ch in children:
#         if ch not in close_list_c:
#             open_list_c.append(ch)
#         elif ch in close_list_c:
#             open_list_c.append('')
#
#     for li_i in range(len(open_list_c)):
#         if open_list_c[li_i] == curr_point:
#             open_list_c[li_i] = ''
#     close_list_c.append(curr_point)
#
#     gn_list = near_point_edges(curr_point)
#     for index in range(4):
#         if open_list_c[index] == '':
#             gn_list[index] = ''
#     g_total = 0
#     if len(g_cost_n) == 0:
#         g_total = 0
#     elif len(g_cost_n) == 1:
#         g_total = g_cost_n[0]
#     else:
#         for co in range(len(g_cost_n)):
#             g_total = g_total + g_cost_n[co]
#
#     # A* Cost of edges: [up, right, down, left]
#     print("Comparing A* edge cost around current point")
#     e_cost = []
#     for index in range(4):
#         if gn_list[index] != '':
#             e_cost.append(float(gn_list[index]) + heuristic_role_c(int(children[index])))
#         else:
#             print("\u0020||Start point out of bound")
#             e_cost.append(100000)
#     print("A* cost of edges:" + str(e_cost))
#     min_cost = min(e_cost)
#
#     if min_cost == e_cost[0]:
#         y0 = y0 - 1
#         g_cost_n.append(gn_list[0] + g_total)
#     elif min_cost == e_cost[1]:
#         x0 = x0 + 1
#         g_cost_n.append(gn_list[1] + g_total)
#     elif min_cost == e_cost[2]:
#         y0 = y0 + 1
#         g_cost_n.append(gn_list[2] + g_total)
#     elif min_cost == e_cost[3]:
#         x0 = x0 - 1
#         g_cost_n.append(gn_list[3] + g_total)
#
#     open_list_c.clear()
#     next_point = (y0 * (col + 1) + x0)
#     return next_point
#
#
# def A_star_c(s_point):
#     path = []
#     print("The current point is " + chr(s_point + 65) + "(" + str(s_point) + ")")
#     flag = True
#     while flag:
#         next_point = move_node_c(s_point)
#         path.append(next_point)
#         print("The next point is " + chr(next_point + 65) + "(" + str(next_point) + ")")
#         place_index = places_near_point(next_point)
#
#         for x in range(len(place_index)):
#             if 0 <= place_index[x] < col * row:
#                 if graph[place_index[x]] == "🦠":
#                     print("The goal state reached")
#                     flag = False
#                     break
#                 else:
#                     print("keep searching>>>>>>>>>>>>>")
#                     s_point = next_point
#                     break
#     print("<----Place found---->")
#     print("The path is: ")
#     for i in path:
#         letter_point = chr(i + 65)
#         if i == path[-1]:
#             print(letter_point, end=" ")
#         else:
#             print(letter_point, "->", end=" ")
#     return
#
#
# def A_star_v(s_point):
#     print("The current point is " + chr(s_point + 65) + "(" + str(s_point) + ")")
#     flag = True
#     while flag:
#         next_point = move_node_v(s_point)
#         print("The next point is " + chr(next_point + 65) + "(" + str(next_point) + ")")
#         place_index = places_near_point(next_point)
#
#         for x in range(len(place_index)):
#             if 0 <= place_index[x] < col * row:
#                 if graph[place_index[x]] == "💊":
#                     print("The goal state reached")
#                     flag = False
#                     break
#
#                 else:
#                     print("keep searching>>>>>>>>>>>>>")
#                     s_point = next_point
#                     break
#     print("<----Place found---->")
#     return
#
# g_cost_n_v = []
# open_list_v = []
# close_list_v = []
#
#
# def move_node_v(curr_point):
#     x0, y0 = get_node_index(curr_point)
#     # indices of four points near curr_point
#     # children = points_near_point_c(curr_point)
#     children = points_near_point(curr_point)
#
#     for ch in children:
#         if ch not in close_list_v:
#             open_list_v.append(ch)
#         elif ch in close_list_v:
#             open_list_v.append('')
#
#     for li_i in range(len(open_list_v)):
#         if open_list_v[li_i] == curr_point:
#             open_list_v[li_i] = ''
#     close_list_v.append(curr_point)
#
#     gn_list = near_point_edges(curr_point)
#
#     # add processing of diagonal lines
#     gn_list.extend(diagonal_line(curr_point))
#
#     for index in range(8):
#         if open_list_v[index] == '':
#             gn_list[index] = ''
#     g_total = 0
#     if len(g_cost_n_v) == 0:
#         g_total = 0
#     elif len(g_cost_n_v) == 1:
#         g_total = g_cost_n_v[0]
#     else:
#         for co in range(len(g_cost_n_v)):
#             g_total = g_total + g_cost_n_v[co]
#
#     # A* Cost of edges: [up, right, down, left]
#     print("Comparing A* edge cost around current point")
#     e_cost = []
#     for index in range(8):
#         if gn_list[index] != '':
#             e_cost.append(float(gn_list[index]) + heuristic_role_v(int(children[index])))
#         else:
#             print("\u0020||Start point out of bound")
#             e_cost.append(100000)
#     print("A* cost of edges:" + str(e_cost))
#     min_cost = min(e_cost)
#
#     if min_cost == e_cost[0]:
#         y0 = y0 - 1
#         g_cost_n_v.append(gn_list[0] + g_total)
#     elif min_cost == e_cost[1]:
#         x0 = x0 + 1
#         g_cost_n_v.append(gn_list[1] + g_total)
#     elif min_cost == e_cost[2]:
#         y0 = y0 + 1
#         g_cost_n_v.append(gn_list[2] + g_total)
#     elif min_cost == e_cost[3]:
#         x0 = x0 - 1
#         g_cost_n_v.append(gn_list[3] + g_total)
#     elif min_cost == e_cost[4]:
#         x0 = x0 - 1
#         y0 = y0 - 1
#         g_cost_n_v.append(gn_list[4] + g_total)
#     elif min_cost == e_cost[5]:
#         x0 = x0 + 1
#         y0 = y0 - 1
#         g_cost_n_v.append(gn_list[5] + g_total)
#     elif min_cost == e_cost[6]:
#         x0 = x0 - 1
#         y0 = y0 + 1
#         g_cost_n_v.append(gn_list[6] + g_total)
#     elif min_cost == e_cost[7]:
#         x0 = x0 + 1
#         y0 = y0 + 1
#         g_cost_n_v.append(gn_list[7] + g_total)
#
#     open_list_c.clear()
#     next_point = (y0 * (col + 1) + x0)
#     return next_point