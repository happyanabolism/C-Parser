from analiser import classify_tokens, find_tokens
from types_table import types, comparison_operators, end_of_line, assigment_operators
from exceptions2 import (IdentifierError, BracketsError, SyntxError, LexicalError,
						 ComparisonError, OperatorError, BraceError)
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
			return  self.tokens[len(self.tokens)-1]

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
		if token.type != Types.Identifier:
			raise SyntxError(token.start_pos, token.num_line,
					'ожидался идентификатор')
		return AstNode(token)

	def boolean(self):
		"""boolean -> <константа логическиго типа>"""
		token = self._curr_token()
		self._skip()
		if token.type == Types.Bool:
			return AstNode(token)

	def char(self):
		"""char -> <константа символьного типа>"""
		token = self._curr_token()
		self._skip()
		if token.type == Types.Char:
			return AstNode(token)

	def string(self):
		"""string -> <константа строкового типа>"""
		token = self._curr_token()
		self._skip()
		if token.type == Types.String:
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
			print(token)
			raise OperatorError(token.start_pos, token.num_line,
					"ожидался оператор с присвоением")


	def parenthesis(self, symbol):
		"""parenthesis -> '(' | ')'"""
		token = self._curr_token()
		self._skip()
		if token.value != symbol:
			raise BracketsError(token.start_pos, token.num_line, 
    			"ожидался оператор '{}'".format(symbol))

	def brace(self, symbol):
		"""brace -> '{' | '}'"""
		token = self._curr_token()
		self._skip()
		if token.value != symbol:
			raise BraceError(token.start_pos, token.num_line,
				"ожидался оператор '{}'".format(symbol))


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
		"""identifier '=' term | string | char;"""
		identifier = self.identifier()
		assign_token = self.operator('=')
		
		curr_token = self._curr_token()
		print(curr_token)

		if curr_token.type == Types.Char:
			value = self.char()
		elif curr_token.type == Types.String:
			value = self.string()	
		else:
			value = self.term()
		print(self._curr_token())
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
		main_block = self.block()
		if_condition = AstNode(if_token, predicate)
		if_condition.add_childs(main_block)
		return if_condition

	def while_cycle(self):
		"""while cycle -> while '(' predicate ')'"""
		while_token = self.operator('while')
		self.parenthesis('(')
		predicate = self.predicate()
		self.parenthesis(')')
		main_block = self.block()
		while_cycle = AstNode(while_token, predicate)
		while_cycle.add_childs(main_block)
		return while_cycle

	def expression(self, semicolon=True):
		"""indetifier (= | += | -= | *= | /= term) | ('++' | --) """
		identifier = self.identifier()
		curr_token = self._curr_token()
		if curr_token.value == '++' or curr_token.value == '--':
			self._skip()
			if semicolon == True:
				self.semicolon()
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
		main_block = self.block()
		for_cycle = AstNode(for_token, first_block, second_block, third_block)
		for_cycle.add_childs(main_block)
		return for_cycle


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
			
	
	def block(self):
		"""block -> '{' (assing | expression | for cycle | if condition
						 | while cycle | function)* '}'"""
		childs = list()
		self.brace('{')
		while True:
			curr_token = self._future_token(0)
			if curr_token.value == '}':
				break
			elif curr_token.value == 'if':
				tree = self.if_condition()
			elif curr_token.value == 'while':
				tree = self.while_cycle()
			elif curr_token.value == 'for':
				tree = self.for_cycle()
			elif curr_token.value in types:
				tree = self.assign()
			else:
				tree = self.expression()
			childs.append(tree)
		self.brace('}')
		return childs		


	def program(self):
		"""program -> assign | if_condition"""
		program_token = Token('program', Types.Program, 'program', 0, 0)
		program = AstNode(program_token)
		while True:
			future_token = self._future_token(0)
			if future_token is None:
				break
			elif future_token.value == 'if':
				tree = self.if_condition()
			elif future_token.value == 'while':
				tree = self.while_cycle()
			elif future_token.value == 'for':
				tree = self.for_cycle()
			elif future_token.value in types:
				tree = self.assign()
			else:
				tree = self.expression()
			program.add_child(tree)
		return program


s = ''
with open('test_files/test.c') as file:
	for line in file:
		s+=line
print(s[:52])
try:
	tokens = classify_tokens(find_tokens(s, 1))
	parser = Parser(tokens)
	print(s)
	tree = parser.program()
except SyntxError as error:
	print(error)
	exit(1)
except LexicalError as error:
	print(error)
	exit(1)
print('-'*20)
tree.print(tree)
