class AstNode:
	def __init__(self, token, *args):
		self.token = token
		self.parent = None
		self.childs = list()
		for child in args:
			self.add_child(child)
		self.i = 0

	def add_child(self, child):
		self.childs.append(child)
		child.parent = self

	def add_childs(self, childs):
		for child in childs:
			self.childs.append(child)
			child.parent = self


	def remove_child(self, child):
		self.childs.remove(child)
		if child.parent == self:
			child.parent = None

	def get_child(self, index):
		return self.childs[index]

	def print(self, start_child):
		print(' |'+start_child.token.value)
		self.print_tree(start_child)

	def print_tree(self, start_child, ident=2):
		for child in start_child.childs:
			print(' |'+ ('-' * ident) + '|' + child.token.value)
			self.print_tree(child, ident=(ident+2))