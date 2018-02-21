from analiser import classify_tokens, find_tokens
from types_table import types, comparison_operators
from AstNode import AstNode
from Token import Token
import Types

class Parser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.position = 0

	def _skip(self):
		self.position += 1

	def _next_token(self):
		self._skip()
		return self.tokens[self.position]

	def _curr_token(self):
		try:
			return self.tokens[self.position]
		except:
			return self.tokens[len(self.tokens) - 1]

	def number(self):
		"""number -> <число>"""
		token = self._curr_token()
		self._skip()
		if token.type == Types.Integer:
			return AstNode(token)
		elif token.type == Types.Float:
			return AstNode(token)

	def identifier(self):
		"""identifier -> <идентификатор>"""
		token = self._curr_token()
		self._skip()
		if token.type == Types.Identifier:
			return AstNode(token)

	def type(self):
		"""type -> <тип>"""
		token = self._curr_token()
		self._skip()
		if token.value in types:
			return AstNode(token) 

	def comparison(self):
		"""comparison -> <сравнение>"""
		token = self._curr_token()
		self._skip()
		if token.value in comparison_operators:
			return AstNode(token)
		else:
			print('ERROR {}:{}: ожидался оператор сравнения'.format(token.start_pos,
					token.num_line))
			exit()

	def parenthesis(self, symbol):
		"""parenthesis -> symbol"""
		token = self._curr_token()
		self._skip()
		if token.value != symbol:
			print('ERROR {}:{}: ожидался оператор {}'.format(token.start_pos,
					token.num_line, symbol))
			exit()

	def group(self):
		"""group -> '(' term ')' | identifier | number"""
		token = self._curr_token()

		if token.value == '(':
			self._skip()
			result = self.term()
			token = self._curr_token()
			if token.value == ')':
				self._skip()
				return result
		elif token.type == Types.Identifier:
			return self.identifier()
		elif token.value in types:
			return self.type()
		else:
			return self.number()

	def add(self):
		result = self.mult()
		token = self._curr_token()
		while token.value == '+' or token.value == '-':
			operation = token.value
			self._skip()
			temp = self.mult()
			if operation == '+':
				result = AstNode(token, child_l=result, child_r=temp)
			else:
				result = AstNode(token, child_l=result, child_r=temp)
			token = self._curr_token()
		return result

	def mult(self):
		result = self.group()
		token = self._curr_token()
		while token.value == '*' or token.value == '/':
			operation = token.value
			self._skip()
			temp = self.group()
			if operation == '*':
				result = AstNode(token, child_l=result, child_r=temp)
			else:
				result = AstNode(token, child_l=result, child_r=temp)
			token = self._curr_token()
		return result

	def term(self):
		return self.add()

	def init(self):
		"""identifier '=' term ;"""
		ident_token = self._curr_token()
		if ident_token.type == Types.Identifier:
			identifier = self.identifier()
			assign_token = self._curr_token()
			if assign_token.value != '=':
				print('ERROR {}:{}: ожидался оператор {}'.format(assign_token.start_pos,
						assign_token.num_line, "'='"))
			self._skip()
			value = self.term()
			self._skip()
			token = self._curr_token()
			if token.value != ';':
				print('ERROR {}:{}: ожидался оператор {}'.format(assign_token.start_pos,
						assign_token.num_line, "';'"))
			return AstNode(assign_token, identifier, value)

	def predicate(self):
		"""predicate -> term comparison term | term"""
		left = self.term()
		comparison = self.comparison()
		right = self.term()
		return AstNode(comparison.token, left, right)

	def if_condition(self):
		"""if_condition -> if '(' predicate ')'"""
		if_token = self._curr_token()
		if if_token.value == 'if':
			self._skip()
			self.parenthesis('(')
			predicate = self.predicate()
			self.parenthesis(')')
			return AstNode(if_token, predicate, None)


	def assign(self):
		"""assign -> type init"""
		type_token = self.type()
		if type_token != None:
			init_token = self.init()
			return AstNode(type_token.token, child_l=init_token, child_r=None)


	def program(self):
		"""program -> assign | if_condition"""
		program_token = Token('program', Types.Program, 'program', 0, 0)
		program = AstNode(program_token)
		tree = self.assign()
		if tree == None:
			self.position = 0
			tree = self.if_condition()
		if tree == None:
			return
		program.add_child(tree)
		return program



s = 'int a = (5 + 7) * 9 - 1;'
i = 'if (a > 4 + 7 * (3 + 3))'
tokens = classify_tokens(find_tokens(s, 1))
parser = Parser(tokens)
tree = parser.program()
print(s)
print(tree.token.value)
tree.print_tree(tree)
tokens = classify_tokens(find_tokens(i, 1))
parser = Parser(tokens)
tree = parser.program()
print(i)
print(tree.token.value)
tree.print_tree(tree)
