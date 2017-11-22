#coding=UTF-8
import math
import random
import numpy as np
from shortestpath import dijkstra
from matplotlib import pyplot as plt

def getMesh(mesh_x):
	router_num = mesh_x * mesh_x
	parameter = mesh_x * (mesh_x - 1)
	return router_num, parameter

def getGarphPara(mesh_x):
	if mesh_x == 3:
		graph = {1:{1:0,    2:1,    4:1},
 		 2:{1:1,    2:0,    3:1,    5:1},
 		 3:{2:1,    3:0,    6:1},
 		 4:{1:1,	4:0,    5:1,    7:1},
 		 5:{2:1,    4:1,	5:0,	6:1,	8:1},
 		 6:{3:1, 	5:1,	6:0,	9:1},
 		 7:{4:1,	7:0,	8:1},
 		 8:{5:1,	7:1,	8:0,	9:1},
 	 	 9:{6:1,	8:1,	9:0}}
		# task_graph = [[1,2],[1,3],[2,4],[2,7],[3,4],[3,5],[3,6],[4,8],[5,8],[6,8],[5,9],[7,9]]
		# weight = [28,29,29,29,32,29,30,29,29,30,28,29]
		task_graph = [[1,2],[1,3],[1,4],[2,5],[3,5],[3,6],[4,7],[5,8],[6,8],[6,9],[7,8],[8,9]]
		# weight = [30,29,29,30,30,30,30,30,29,29,30,29]
		weight = [28,29,29,29,32,29,30,29,29,29,29,29]
	elif mesh_x == 4:
		graph = {1:{1:0,    2:1,    5:1},
 		 2:{1:1,    2:0,    3:1,    6:1},
 		 3:{2:1,    3:0,    4:1,	7:1},
 		 4:{3:1,	4:0,    8:1},
 		 5:{1:1,    5:0,	6:1,	9:1},
 		 6:{2:1, 	5:1,	6:0,	7:1,	10:1},
 		 7:{3:1,	6:1,	7:0,	8:1,	11:1},
 		 8:{4:1,	7:1,	8:0,	12:1},
 	 	 9:{5:1,	9:0,	10:1,	13:1},
 	 	10:{6:1,	9:1,	10:0,	11:1,	14:1},
 	 	11:{7:1,	10:1,	11:0,	12:1,	15:1},
 	 	12:{8:1,	11:1,	12:0,	16:1},
 	 	13:{9:1,	13:0,	14:1},
 	 	14:{10:1,	13:1,	14:0,	15:1},
 	 	15:{11:1,	14:1,	15:0,	16:1},
 	 	16:{12:1,	15:1,	16:0}}
		task_graph = [[1,2],[1,3],[2,4],[2,5],[3,6],[3,7],[4,8],[5,8],[5,9],[5,10],[6,10],[6,11],[7,11],
			  [8,12],[9,12],[10,13],[11,14],[11,15],[12,16],[13,16],[14,16],[15,16]]
		weight = [50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50]
	elif mesh_x == 5:
		graph = {1:{1:0,    2:1,    6:1},
 		 2:{1:1,    2:0,    3:1,    7:1},
 		 3:{2:1,    3:0,    4:1,	8:1},
 		 4:{3:1,	4:0,    5:1,	9:1},
 		 5:{1:1,    5:0,	10:1},
 		 6:{1:1, 	6:0,	7:1,	11:1},
 		 7:{2:1,	6:1,	7:0,	8:1,	12:1},
 		 8:{3:1,	7:1,	8:0,	9:1,	13:1},
 	 	 9:{4:1,	8:1,	9:0,	10:1,	14:1},
 	 	10:{5:1,	9:1,	10:0,	15:1},
 	 	11:{6:1,	11:0,	12:1,	16:1},
 	 	12:{7:1,	11:1,	12:0,	13:1,	17:1},
 	 	13:{8:1,	12:1,	13:0,	14:1,	18:1},
 	 	14:{9:1,	13:1,	14:0,	15:1,	19:1},
 	 	15:{10:1,	14:1,	15:0,	20:1},
 	 	16:{11:1,	16:0,	17:1,	21:1},
 	 	17:{12:1,	16:1,	17:0,	18:1,	22:1},
 	 	18:{13:1,	17:1,	18:0,	19:1,	23:1},
 	 	19:{14:1,	18:1,	19:0,	20:1,	24:1},
 	 	20:{15:1,	19:1,	20:0,	25:1},
 	 	21:{16:1,	21:0,	22:1},
 	 	22:{17:1,	21:1,	22:0,	23:1},
 	 	23:{18:1,	22:1,	23:0,	24:1},
 	 	24:{19:1,	23:1,	24:0,	25:1},
 	 	25:{20:1,	24:1,	25:0}}
		task_graph = [[1,2],[1,3],[2,4],[2,7],[3,5],[3,6],[4,8],[5,8],[6,8],[7,9],[7,10],[7,11],[8,12],
			  [9,12],[10,13],[11,14],[11,15],[12,16],[13,19],[13,17],[14,18],[15,18],[16,19],
			  [17,20],[17,24],[18,21],[18,25],[19,21],[20,21],[21,22],[21,23],[23,25]]
		weight = [50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,
		  50,50,50,50,50]
	return graph, task_graph, weight

def get_load_var(task_encoder):
	comm = [[task_encoder[i[0]-1], task_encoder[i[1]-1]] for i in task_graph]
	link_all = []
	for i in range(len(comm)):
		link = []
		path = dijkstra(graph, comm[i][0], comm[i][1])
		for index in range(len(path)-1):
			min_num = min(path[index], path[index+1])
			if abs(path[index+1] - path[index]) == 1:
				link_num = min_num - math.floor(min_num/mesh_x)
			else:
				link_num = min_num + parameter
			link.append(link_num)
		link_all.append(link)
	load = {}
	link_comm = []
	for j in range(1,parameter*2 + 1):
		sum = 0
		for i in link_all:
			if j in i:
				index = link_all.index(i)
				link_comm.append([j, index])
				sum = sum + weight[index]
		load[j] = sum
	value_list = [value for value in load.values()]
	load_var = np.array(value_list).var()
	return load_var




#距离与速度的加法
def add_dv(d,v):
	d_copy = d[:]
	for i in v:
		temp = d_copy[i[0]]
		d_copy[i[0]] = d_copy[i[1]]
		d_copy[i[1]] = temp
	return d_copy
#小数与速度的乘法
def mul(eta,v):
	v_copy = v[:]
	v_ = []
	for i in v_copy:
		if random.random() < eta:
			v_.append(i)
	return v_
#距离与距离的减法
def sub(d1, d2):
	v = []
	for i in range(len(d1)):
		index = d2.index(d1[i])
		if i != index:
			v_ = [[i,index]]
			d2 = add_dv(d2,v_)
			v.append(v_[0])
	return v
#速度与速度的加法
def add_vv(alpha, v1, beta, v2, gamma, v3):
	v = mul(alpha, v1) + mul(beta, v2) + mul(gamma, v3)
	return v


def init_popvfitness(popsize, router_num):
	pop = []
	for i in range(popsize):
		pop_list = list(range(1,router_num + 1))
		random.shuffle(pop_list)
		pop.append(pop_list)
	v = []
	for i in range(popsize):
		v_list = []
		for j in range(random.randint(1,router_num)):
			x = random.randint(0,router_num-2)
			v_list.append([x, random.randint(x+1,router_num-1)])
		v.append(v_list)
	fitness = np.zeros(popsize)
	for i in range(popsize):
		fitness[i] = get_load_var(pop[i])
	return pop, v, fitness

def get_init_best(fitness, pop):
	gbestpop, gbestfitness = pop[fitness.argmin()], fitness.min()
	pbestpop, pbestfitness = pop.copy(), fitness.copy()
	return gbestpop, gbestfitness, pbestpop, pbestfitness

alpha = 0.5
# beta = 0.3
# gamma = 0.3
popsize = 150

mesh_x = 3
router_num, parameter = getMesh(mesh_x)
graph, task_graph, weight = getGarphPara(mesh_x)

pop, v, fitness = init_popvfitness(popsize, router_num)
print("初始种群：", pop)
print('初始速度：', v)
print('初始适应度：', fitness)

gbestpop, gbestfitness, pbestpop, pbestfitness = get_init_best(fitness, pop)
print('初始最好种群与适应度：', gbestpop, gbestfitness)
print('初始最好个体与适应度：', pbestpop, pbestfitness)

maxgen = 200
for i in range(maxgen):
	for j in range(popsize):
		beta = random.random()
		gamma = 1 - alpha - beta
		v[j] = add_vv(alpha, v[j], beta, sub(pbestpop[j], pop[j]), gamma, sub(gbestpop, pop[j]))
	for j in range(popsize):
		pop[j] = add_dv(pop[j], v[j])
	for j in range(popsize):
		fitness[j] = get_load_var(pop[j])
	# print('更新后的适应度：', fitness)
	for j in range(popsize):
		if fitness[j] < pbestfitness[j]:
			pbestfitness[j] = fitness[j]
			pbestpop[j] = pop[j].copy()
	# print('更新后的个体适应度：',pbestfitness)
	# print('更新后的最好 个体：', pbestpop)
	for j in range(popsize):
		if pbestfitness.min() < gbestfitness:
			gbestfitness = pbestfitness.min()
			gbestpop = pop[pbestfitness.argmin()].copy()
	print('更新后的最好群体适应度：', gbestfitness)
	print('更新后的最好群体：', gbestpop)
