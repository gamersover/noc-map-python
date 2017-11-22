def dijkstra(graph,src,dest):
	visited = []
	distances={}
	predecessors={}
	while src != dest:
	    # if it is the initial  run, initializes the cost
	    if not visited:
	        distances[src]=0
	    # visit the neighbors
	    for neighbor in graph[src] :
	        if neighbor not in visited:
	            new_distance = distances[src] + graph[src][neighbor]
	            if new_distance < distances.get(neighbor,float('inf')):
	                distances[neighbor] = new_distance
	                predecessors[neighbor] = src
	    # mark as visited
	    visited.append(src)
	    # now that all neighbors have been visited: recurse
	    # select the non visited node with lowest distance 'x'
	    # run Dijskstra with src='x'
	    unvisited={}
	    for k in graph:
	        if k not in visited:
	            unvisited[k] = distances.get(k,float('inf'))
	    x=min(unvisited, key=unvisited.get)
	    src = x
	path=[]
	pred=dest
	print(predecessors)
	while pred != None:
		path.append(pred)
		pred=predecessors.get(pred,None)
# 	print('shortest path: '+str(path)+" cost="+str(distances[dest]))
	return path

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    #unittest.main()
    # graph = {'s': {'a': 100, 'b': 1444},
    #         'a': {'s': 333, 'b': 444, 'c':118},
    #         'b': {'s': 422, 'a': 233, 'd': 222},
    #         'c': {'a': 22, 'd': 722, 't': 444},
    #         'd': {'b': 11, 'c': 111, 't': 555},
    #         't': {'c': 313, 'd': 115}}
    graph = {1:{1:0,    2:1,    4:1},
     		 2:{1:1,    2:0,    3:1,    5:1},
     		 3:{2:1,    3:0,    6:1},
     		 4:{1:1,	4:0,    5:1,    7:1},
     		 5:{2:1,    4:1,	5:0,	6:1,	8:1},
     		 6:{3:1, 	5:1,	6:0,	9:1},
     		 7:{4:1,	7:0,	8:1},
     		 8:{5:1,	7:1,	8:0,	9:1},
     	 	 9:{6:1,	8:1,	9:0}}
    a = dijkstra(graph,1,7)
    print(a)