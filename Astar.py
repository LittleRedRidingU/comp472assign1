
# cost of edges around place
# def near_place_edges(place):
#     neighbors_list = near_place(place)
#     cost_list = []
#     if neighbors_list[0] == "":
#         cost_list.append(cost(graph[place]))
#     else:
#         cost_list.append((cost(graph[place]) + cost(graph[neighbors_list[0]])) / 2)
#     if neighbors_list[1] == "":
#         cost_list.append(cost(graph[place]))
#     else:
#         cost_list.append((cost(graph[place]) + cost(graph[neighbors_list[1]])) / 2)
#     if neighbors_list[2] == "":
#         cost_list.append(cost(graph[place]))
#     else:
#         cost_list.append((cost(graph[place]) + cost(graph[neighbors_list[2]])) / 2)
#     if neighbors_list[3] == "":
#         cost_list.append(cost(graph[place]))
#     else:
#         cost_list.append((cost(graph[place]) + cost(graph[neighbors_list[3]])) / 2)
#     return cost_list


class Node:
    def __init__(self, name, point, value, parent):
        self.name = name
        self.point = point
        self.parent = parent
        self.hn = 0



    def __self__(self):
        return("Node name is: %s\n g cost for this nod is: %f\n estimate heuristic cost for this nod is: %f"
               % (self.name, self.gn, self.hn))


# use Manhattan method to estimate the cost for role c fro the current position to goal position
def heuristic_role_c(cur_node, goal_node):
    # x0,y0=get_node_index(cur_node)
    x0, y0 = cur_node.point
    x1, y1 = goal_node.point
    d_x = round(float(abs(x1 - x0) * 0.2), 1)
    d_y = round(float(abs(y1 - y0) * 0.1), 1)
    return d_x + d_y





