from analiser import classify_tokens, find_tokens
from types_table import types, comparison_operators, end_of_line, assigment_operators
from exceptions2 import (IdentifierError, BracketsError, SyntxError,
						 ComparisonError, OperatorError)
from AstNode import AstNode
from Token import Token
import Types
import logging


class Parser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.position = 0

	def _skip(self):
		self.position += 1

	def _future_token(self, step):
		try:
			return self.tokens[self.position+step]
		except:
			return None

	def _curr_token(self):
		try:
			return self.tokens[self.position]
		except:
			return  self.tokens[self.position-1]

	def number(self):
		"""number -> <число>"""
		token = self._curr_token()
		self._skip()
		if token.type == Types.Integer or token.type == Types.Float:
			return AstNode(token)

	def identifier(self):
		"""identifier -> <идентификатор>"""
		token = self._curr_token()
		self._skip()
		if token.type == Types.Identifier:
			return AstNode(token)

	def boolean(self):
		"""boolean -> <константа логическиго типа>"""
		token = self._curr_token()
		self._skip()
		if token.type == Types.Bool:
			return AstNode(token)

	def type(self):
		"""type -> <тип>"""
		token = self._curr_token()
		self._skip()
		if token.value in types:
			return AstNode(token)
		else:
			raise SyntxError(token.start_pos, token.num_line,
					'ожидался тип')

	def comparison(self):
		"""comparison -> <сравнение>"""
		token = self._curr_token()
		self._skip()
		if token.value in comparison_operators:
			return AstNode(token)
		else:
			raise ComparisonError(token.start_pos, token.num_line,
					'ожидался оператор сравнения')

	def semicolon(self):
		"""semicolon -> ';'"""
		token = self._curr_token()
		self._skip()
		if token.value != end_of_line:
			raise SyntxError(token.start_pos, token.num_line,
					"ожидался оператор '{}'".format(end_of_line))

	def operator(self, operator):
		"""operator -> <оператор>"""
		token = self._curr_token()
		self._skip()
		if token.value != operator:
			raise OperatorError(token.start_pos, token.num_line,
					"ожидался оператор '{}'".format(operator))
		else:
			return token

	def assigment_operator(self):
		"""assigment operator -> <оператор с присвоением>"""
		token = self._curr_token()
		self._skip()
		if token.value in assigment_operators:
			return token
		else:
			raise OperatorError(token.start_pos, token.num_line,
					"ожидался оператор с присвоением")


	def parenthesis(self, symbol):
		"""parenthesis -> symbol"""
		token = self._curr_token()
		self._skip()
		if token.value != symbol:
			raise BracketsError(token.start_pos, token.num_line, 
    			"ожидался оператор {}".format(symbol))

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
		elif token.type == Types.Integer or token.type == Types.Float:
			return self.number()
		elif token.type == Types.Bool:
			return self.boolean()
		else:
			raise IdentifierError(token.start_pos, token.num_line,
				 "ожидалось число или идентификатор '{}'".format(token.value))

	def add(self):
		result = self.mult()
		token = self._curr_token()
		while token.value == '+' or token.value == '-':
			operation = token.value
			self._skip()
			temp = self.mult()
			if operation == '+':
				result = AstNode(token, result, temp)
			else:
				result = AstNode(token, result, temp)
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
				result = AstNode(token, result, temp)
			else:
				result = AstNode(token, result, temp)
			token = self._curr_token()
		return result

	def term(self):
		return self.add()

	def init(self):
		"""identifier '=' term ;"""
		identifier = self.identifier()
		assign_token = self.operator('=')
		value = self.term()
		self.semicolon()
		return AstNode(assign_token, identifier, value)

	def predicate(self):
		"""predicate -> term comparison term | term"""
		left = self.term()
		if self._curr_token().value in comparison_operators:
			comparison = self.comparison()
			right = self.term()
			return AstNode(comparison.token, left, right)
		else:
			return left

	def if_condition(self):
		"""if condition -> if '(' predicate ')'"""
		if_token = self.operator('if')
		self.parenthesis('(')
		predicate = self.predicate()
		self.parenthesis(')')
		return AstNode(if_token, predicate)

	def while_cycle(self):
		"""while cycle -> while '(' predicate ')'"""
		while_token = self.operator('while')
		self.parenthesis('(')
		predicate = self.predicate()
		self.parenthesis(')')
		return AstNode(while_token, predicate)

	def expression(self, semicolon=True):
		"""indetifier (= | += | -= | *= | /= term) | ('++' | --) """
		identifier = self.identifier()
		curr_token = self._curr_token()
		if curr_token.value == '++' or curr_token.value == '--':
			self._skip()
			return AstNode(curr_token, identifier)
		else:
			oper = self.assigment_operator()
		term = self.term()
		if semicolon == True:
			self.semicolon()

		return AstNode(oper, identifier, term)


	def for_cycle(self):
		"""for cycle -> for '(' init | type init ';' predicate ';' expression ')' """
		for_token = self.operator('for')
		self.parenthesis('(')
		curr_token = self._curr_token()
		if curr_token.value in types:
			first_block = self.assign(with_initializing=True)
		else:
			first_block = self.init()
		second_block = self.predicate()
		self.semicolon()
		third_block = self.expression(semicolon=False)
		self.parenthesis(')')
		return AstNode(for_token, first_block, second_block, third_block)


	def assign(self, with_initializing=False):
		"""assign -> type init | type identifier"""
		type_token = self.type()
		future_token = self._future_token(2)
		if future_token == ';' or future_token is None:
			if with_initializing == True:
				raise OperatorError(future_token.start_pos, future_token.num_line, 
						'ожидалась инициализация')

			identifier = self.identifier()
			return AstNode(type_token.token, identifier)
		else:
			init_token = self.init()
			return AstNode(type_token.token, init_token)
			
			


	def program(self):
		"""program -> assign | if_condition"""
		program_token = Token('program', Types.Program, 'program', 0, 0)
		program = AstNode(program_token)
		while(True):
			future_token = self._future_token(1)
			if future_token is None:
				break
			tree = self.for_cycle()
		#if tree == None:
		#	self.position = 0
		#	tree = self.if_condition()
		#if tree == None:
		#	return
			program.add_child(tree)
		return program



s = '((5 + 7) * (9 - 1));'
s = """for(int i = 0; i < 4; i++)
	   for(j = 3 + 3; j != 9; j = j + 4)"""
i = 'if (a > 4 + 7 * (3 + 3))'
i = 'for(j=3+3;j!=9;j=j+4)'
try:
	tokens = classify_tokens(find_tokens(s, 1))
	parser = Parser(tokens)
	print(s)
	tree = parser.program()
except SyntxError as error:
	print(parser._curr_token())
	print(error)
	exit(1)
print('-'*20)
tree.print(tree)
