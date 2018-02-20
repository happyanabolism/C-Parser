from analiser import classify_tokens, find_tokens
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
		print('{}: token: {}'.format('num', self._curr_token().value))
		token = self._curr_token()
		self._skip()
		if token.type == Types.Integer:
			return AstNode(token)
		elif token.type == Types.Float:
			return AstNode(token)

	def identifier(self):
		"""identifier -> <идентификатор>"""
		print('{}: token: {}'.format('ident', self._curr_token().value))
		token = self._curr_token()
		self._skip()
		if token.type == Types.Identifier:
			return AstNode(token) 

	def group(self):
		"""group -> '(' term ')' | identifier | number"""
		print('{}: token: {}'.format('group', self._curr_token().value))
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
		else:
			return self.number()

	def add(self):
		print('{}: token: {} {}'.format('add', self._curr_token().value, 1))
		result = self.mult()
		print('{}: token: {} result: {}'.format('add', self._curr_token().value, result))
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
		print('{}: token: {} {}'.format('mult', self._curr_token().value, 1))
		result = self.group()
		token = self._curr_token()
		print('{}: token: {}'.format('mult', self._curr_token().value))
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

	def assign(self):
		"""identifier '=' term"""
		ident_token = self._curr_token()
		if ident_token.type == Types.Identifier:
			identifier = self.identifier()
		assign_token = self._curr_token()
		if assign_token.value != '=':
			print('ERROR {}:{}: ожидался оператор {}'.format(assign_token.start_pos,
					assign_token.num_line, "'='"))
			exit()
		self._skip()
		value = self.term()
		return AstNode(assign_token, identifier, value)

	def program(self):
		"""program -> ( assign )*"""
		program_token = Token('program', Types.Program, 'program', 0, 0)
		program = AstNode(program_token)
		program.add_child(self.assign())
		return program




tokens = classify_tokens(find_tokens('a = 5', 1))
parser = Parser(tokens)
tree = parser.program()
print('a = 5')
print(tree.token.value)
tree.print_tree(tree)