from analiser import classify_tokens, find_tokens
from AstNode import AstNode
import Token
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
		print('{}: token: {}'.format('num', self._curr_token().value))
		token = self._curr_token()
		self._skip()
		if token.type == Types.Integer:
			return AstNode(token)
		elif token.type == Types.Float:
			return AstNode(token)

	def group(self):
		print('{}: token: {}'.format('group', self._curr_token().value))
		token = self._curr_token()

		if token.value == '(':
			self._skip()
			result = self.term()
			token = self._curr_token()
			if token.value == ')':
				self._skip()
				return result
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
				result += temp
			else:
				result -= temp
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
				result *= temp
			else:
				result /= temp
			token = self._curr_token()
		return result

	def term(self):
		return add()



tokens = classify_tokens(find_tokens('3+4*(2+7-3)+5*10', 1))
for token in tokens:
	print(token)
parser = Parser(tokens)
print(parser.term())