
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