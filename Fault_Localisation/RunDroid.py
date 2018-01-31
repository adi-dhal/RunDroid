#########################################################

########################################################
edges = [['0','1'],['1','2'],['1','4'],['2','3'],['2','4'],['3','4'],['4','5'],['5','6'],['6','7']]
test_cases = []		#list of all test_case objects
cfgs = []		#list of all cfg objects
result_vector = []	#list of results of test cases
node_convg_mat = []	#coverage matrice of nodes
edge_convg_mat = []	#coverage matrice of edges
node_susp_deg = []	#Suspicion degree vector for nodes
edge_susp_deg = []	#Suspicion degree vector for edges
mod_node_susp_deg = []	#modified Suspicion degree vector for nodes
final_node_susp_deg = []#final Suspicion degree vector for nodes
##########################################################
#	CFG accounting for the cfg for each test case
'''
node_convg_vector list of nodes with index as block number and value as 1 if exist in cfg
edge_convg_vector list of list with index as edge number and incident nodes as list
'''
##########################################################
class cfg():
	def __init__(self,node_convg_vector,edge_convg_vector):
		self.node_convg_vector = node_convg_vector
		self.edge_convg_vector = edge_convg_vector
	def is_incident_with(self,node):
		edge_list= []
		for i,item in enumerate(self.edge_convg_vector):
			if str(node) == item[0]:
				edge_list.append(i)
		return edge_list
				
		
			
#################################################################
#	Test Case accounting for each test case from sample space
'''
input_vector list of input variable for test case
status result of the test case
'''
#################################################################
class test_case():
	def __init__(self,input_vector,status):
		self.input_vector = input_vector
		self.status = status
#################################################################


def generate_node_convg():
	for item in cfgs:
		node_convg_mat.append(item.node_convg_vector)	
	
def generate_edge_convg(): 
	for item in cfgs:
		temp = []
		for i in edges:
			if i in item.edge_convg_vector:
				temp.append('1')
			else:
				temp.append('0')
		edge_convg_mat.append(temp)
		
def generate_result_vector():
	for item in test_cases:
		if item.status == True:
			result_vector.append('1')
		else :
			result_vector.append('0')

######################################################################
'''
Using Dstar (star=2) as score for suspicion for each node or edge
		D^2 = A ^ 2 / (B + C)
		
		A : Number of failed test cases that cover that node/edge in cfg
		B : Number of failed test cases that don't cover that node/edge in cfg
		C : Number of passed test cases that cover that node/edge in cfg
'''
######################################################################
def generate_node_susp_deg():
	for block in range (len(node_convg_mat[0])):
		A = 0
		B = 0
		C = 0
		for test in range(len(node_convg_mat)):
			if result_vector[test] == '0':
				if node_convg_mat[test][block] == '1':
					A += 1
				else:
					B += 1
			else:
				if node_convg_mat[test][block] == '1':
					C += 1
		if (B+C != 0):
			node_susp_deg.append((A**2)/((B+C)*1.0))
		else:
			node_susp_deg.append(100)

def generate_edge_susp_deg():
	for i in range (len(edge_convg_mat[0])):
		A = 0
		B = 0
		C = 0
		for j in range(len(edge_convg_mat)):
			if result_vector[j] == '0':
				if edge_convg_mat[j][i] == '1':
					A += 1
				else:
					B += 1
			else:
				if edge_convg_mat[j][i] == '1':
					C += 1
		
		edge_susp_deg.append((A**2)/((B+C)*1.0))
		
def generate_mod_node_susp_deg(graph):
	for i in range(len(node_susp_deg)):
		edge_set = graph.is_incident_with(i)
		val = 0
		for item in edge_set:
			if edge_susp_deg[item] > val:
				val = edge_susp_deg[item]
		mod_node_susp_deg.append(val)	
	
	
def main():
	print "Graph Mining Technique for Fault Localization"
	
	with open('test_cases.txt','r') as f:
		for line in f:
			line = line.split('\n')[0]
			test_cases.append(test_case(line.split(','),False))
	#Invoke RunDroid to run for each test case and produce result
		#System call
	with open ("cfg.txt",'r') as f:
		for line in f:
			node_convg_vector = []
			edge_convg_vector = []
			line = line.split('\n')[0]
			a , b = line.split('_')
			node_convg_vector = a.split(',')
			b = b.split(',')
			for item in b:
				edge_convg_vector.append(item.split('-')) 
			cfgs.append(cfg(node_convg_vector,edge_convg_vector))
	with open ("result.txt",'r') as f:
		for k,line in enumerate (f):
			line = line.split("\n")[0]
			if line == "true":
				test_cases[k].status = True
				
			
	generate_node_convg()
	generate_edge_convg()
	generate_result_vector()
	generate_node_susp_deg()
	generate_edge_susp_deg()
	graph = cfg([1,1,1,1,1,1,1,1],edges)
	generate_mod_node_susp_deg(graph)
	#print mod_node_susp_deg
	
	code = dict()
	code = {0:"void onClick(View v){\n\tnum=getNumber();",1:"if(v.getId()==R.id.btn1){",2:"\n\t\tif(num==0){",3:"\n\t\t\tnum=1;",4:"\n\t\t}\n\t}\n\tThread t = createThread(v.getId());",5:"\n\tt.start();",6:"\n}\n}TaskThread.run(){\n\tif(v.getId()==R.id.btn1){",7:"\n\t\tloadData(num);"}
	for i in range(8):
		print code[i] +"-----------"+ str(mod_node_susp_deg[i])
	print "\n\t}\n}"

if __name__ == "__main__":
    main()

