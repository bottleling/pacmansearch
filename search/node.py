class Node:
	def __init__(self, state, parent=None, action=None, step_cost=1):
		self.state = state
		self.parent= parent #parent node
		self.action=action #action on parent to get to this state
		if (parent !=None):
			self.path_cost = self.parent.path_cost + step_cost
		else:
			self.path_cost = step_cost

	def __repr__:
		s = "Node %s" % self.state
		return s

	def getChildren(self, problem): #from searchAgents
		successors = problem.getSuccessors()
		children = []
		for (s in successors):
			node = Node(s[0],self,s[1],s[2])
			children.append(node)
		return children

	def getPath(self):
		current_node = self
		path = [current_node]
		while current_node:
			path.append(current_node)
			current_node = current_node.parent
		return path
