class AstNode:
	def __init__(self, token, child_l = None, child_r = None):
		self.token = token
		self.parent = None
		self.childs = list()
		self.child_l = child_l
		self.child_r = child_r
		if child_l != None:
			self.add_child(child_l)
		if child_r != None:
			self.add_child(child_r)
		self.i = 0

	def add_child(self, child):
		#if child.parent != None:
		#	child.parent.childs.remove(child)
		#f child in self.childs:
		#	self.childs.remove(child)
		self.childs.append(child)
		child.parent = self

	def remove_child(self, child):
		self.childs.remove(child)
		if child.parent == self:
			child.parent = None

	def get_child(self, index):
		return self.childs[index]

	def print_tree(self, start_child, ident=3):
		for child in start_child.childs:
			print((' ' * (ident - 1) + '|'))
			print((' ' * ident) + '—— ' + child.token.value)
			self.print_tree(child, ident=(ident + 3))