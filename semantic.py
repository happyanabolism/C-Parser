#!/usr/bin/python

from parser2 import Parser
from analiser import LexAnaliser
from exceptions2 import SemanticError
import Types

class SemanticAnaliser:
	def __init__(self, ast_tree):
		self.ast_tree = ast_tree
		self.identifiers = {}

	def find_assigned_ids(self, ast_tree):
		for child in ast_tree.childs:
			if child.token.type == Types.Assign:
				self.identifiers[child.get_child(0).token.value] = child.get_child(0).get_child(0).token.value
			self.find_assigned_ids(child)

	def analise(self):
		self.find_assigned_ids(self.ast_tree)


analiser = LexAnaliser('test_files/test.c')
tokens = analiser.analise()
#for token in tokens:
#	print(token)
parser = Parser(tokens)
tree = parser.program()
semantic_analiser = SemanticAnaliser(tree)
semantic_analiser.analise()
for k, v in semantic_analiser.identifiers.items():
	print(k, ' ', v)