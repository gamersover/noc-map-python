# -*- coding:utf-8 -*-
import random
import math
import numpy as np
from shortestpath import dijkstra
from matplotlib import pyplot as plt

#获取mesh参数
def getMesh(mesh_x):
	router_num = mesh_x * mesh_x
	parameter = mesh_x * (mesh_x - 1)
	return router_num, parameter

#获取图参数
def getGarphPara(mesh_x):
	"""
	graph:  noc拓扑结构
	task_graph:  任务图
	weight:  任务之间的通信量
	"""
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
		task_graph = [[1,2],[1,3],[2,4],[2,5],[3,6],[3,7],[4,8],[5,9],[6,9],[7,8],[7,10],
					  [8,11],[8,12],[8,13],[9,14],[10,14],[11,15],[14,16]]
		weight = [36,36,34,34,36,36,34,36,36,36,38,38,39,36,39,39,39,36]
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
			          [9,12],[10,13],[11,14],[11,15],[12,16],[13,17],[14,18],[15,18],[16,19],[17,20],
			          [17,24],[18,21],[19,21],[20,21],[21,22],[21,23],[23,25]]
		weight = [54,54,54,53,53,53,54,55,54,54,54,52,54,52,52,52,54,54,54,56,56,54,55,55,54,54,54,
		 	      54,54,56]
	return graph, task_graph, weight

#获取链路负载方差
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

class SA(object):
	"""
	模拟退火算法实现
	"""
	def __init__(self, router_num, temperatrue = 100, iter_num = 20):
		self.temperatrue = temperatrue
		self.iter_num = iter_num
		self.router_num = router_num
	
	def run(self):
		init = list(range(1,self.router_num + 1))
		random.shuffle(init)
		print("初始映射:",init)
		load_var = []
		load_var.append(get_load_var(init))
		while self.temperatrue > 0.01:
			for i in range(self.iter_num):
				p1 = random.randint(0,self.router_num - 1)
				p2 = random.randint(0,self.router_num - 1)
				while p1==p2:
					p1 = random.randint(0,self.router_num - 1)
					p2 = random.randint(0,self.router_num - 1)
				load_var1 = get_load_var(init)
				new_task = init[:]
				new_task[p1], new_task[p2] = new_task[p2], new_task[p1]
				load_var2 = get_load_var(new_task)
				delta_e = load_var2 - load_var1
				if delta_e < 0:
					init = new_task[:]
				elif math.exp(-delta_e/self.temperatrue) > random.uniform(0,1):
					init = new_task[:]
			load_var_temp = get_load_var(init)
			load_var.append(load_var_temp)
			self.temperatrue = self.temperatrue*0.99

			print(init)
			print(self.temperatrue)
			print(load_var_temp)

class GA(object):
	"""
	遗传算法实现
	"""
	def __init__(self, router_num, iter_num = 200, popsize = 150, elit = 0.3, mutprob = 0.01, crossprob = 0.7, step = 1):
		self.popsize = popsize
		self.elit = elit
		self.mutprob = mutprob
		self.crossprob = crossprob
		self.step = step
		self.router_num = router_num
		self.iter_num = iter_num

	def get_slots(self, vec):
  		slots = [i for i in range(1, self.router_num + 1)]
  		task_encoder = []
  		for i in range(len(vec)):
  			index = slots[vec[i]]
  			task_encoder.append(index)
  			del slots[vec[i]]
  		return task_encoder

	def mutate(self, vec, domain):
  		i = random.randint(0, self.router_num - 1)
  		res = []
  		if random.random() < 0.5 and vec[i] > domain[i][0]:
  			res = vec[0:i] + [vec[i] - self.step] + vec[i + 1:]
  		elif vec[i] < domain[i][1]:
  			res = vec[0:i] + [vec[i] + self.step] + vec[i + 1:]
  		else:
  			res = res
  		return res

	def crossover(self, r1, r2):
		i = random.randint(0, self.router_num - 1)
		return r1[0:i] + r2[i:]

	def run(self):
		domain = [(0, self.router_num - 1 - i) for i in range(self.router_num)]
		pop = []
		for i in range(self.popsize):
  			vec = [random.randint(domain[i][0], domain[i][1]) for i in range(self.router_num)]
  			pop.append(vec)
		topelite = int(self.elit * self.popsize)
		for i in range(self.iter_num):
			load_var = []
			for v in pop:
				v1 = self.get_slots(v)
				load_var.append([get_load_var(v1), v])
			load_var.sort()
			ranked = [v for (s,v) in load_var]
			pop = ranked[0: topelite]
			while len(pop) < self.popsize:
				if random.random() < self.mutprob:
					c = random.randint(0, topelite - 1)
					if len(ranked[c]) == self.router_num:
						temp = self.mutate(ranked[c], domain)
						# if temp == []:
							# print("******", ranked[c])
						if temp != [] and temp not in pop:
							pop.append(temp)
				elif random.random() < self.mutprob + self.crossprob:
					c1 = random.randint(0, topelite - 1)
					c2 = random.randint(0, topelite - 1)
					temp = self.crossover(ranked[c1],ranked[c2])
					if temp not in pop:
						pop.append(temp)
			print(load_var[0])
		print(self.get_slots(load_var[0][1]))



mesh_x = 4
router_num, parameter = getMesh(mesh_x)
graph, task_graph, weight = getGarphPara(mesh_x)
SA(router_num).run()
# GA(router_num).run()
# sum = sum(weight)
# print(sum)