import re
from tabulate import tabulate
from Token import Token
from Types import (Keyword, Identifier, Float, String, Bool,
				  Operator, Separator, Error, Integer, Char)
from types_table import (keywords, separators, operators, double_operators,
						 boolean_constants)
from exceptions2 import BracketsError, LexicalError


class LexAnaliser:
	def __init__(self, source_file):
		self.float_match = r'^[0-9]*[.,][0-9]+$'
		self.integer_match = r'^[-+]?\d*$'
		self.string_match = r'"\w*"'
		self.char_match = r"'.{1}'"
		self.variable_match = r'(^[a-zA-Z_$][a-zA-Z0-9_$]*$)'
		self.doub_op_match = r'(\+=|-=|\+\+|==|!=|\|\||&&|--|>=|<=)'
		self.source_file = source_file

	#пробелы, табуляции и переводы строк игнорируются анализатором языка си
	def remove_empty_tokens(self, tokens):
		whitespces = ['', ' ', '\t', '\n']
		tokens = list(filter(lambda x: x not in whitespces, tokens))
		return tokens


	def check_brackets(self, tokens):
		meetings = 0
		brackets_tokens = list()
		for token in tokens:
			if token.value == '(':
				meetings += 1
				brackets_tokens.append(token)
			elif token.value == ')':
				meetings -= 1
				brackets_tokens.append(token)
		if meetings > 0:
			raise BracketsError(tokens[len(brackets_tokens) - 1].start_pos, tokens[0].num_line,
			'Ожидался оператор {}'.format("')'"))
		elif meetings < 0:
			raise BracketsError(brackets_tokens[0].start_pos, tokens[0].num_line,
			'Ожидался оператор {}'.format("'('"))
		else:
			pass
		

	def find_tokens(self, line, num_line):
		res_tokens = list()
		copy_line = line

		tokens = re.findall(self.string_match, line)
		tokens += re.findall(self.char_match, line)
		tokens += re.findall(self.doub_op_match, line)
		for token in tokens:
			res_tokens.append([token, line.find(token), num_line])
			line = line.replace(token, '~' * len(token), 1)
			copy_line = copy_line.replace(token, '')
	
		for separator in separators:
			if line.find(separator) > -1:
				copy_line = copy_line.replace(separator, '~' + separator + '~')

		for operator in operators:
			pos = copy_line.find(operator)
			if (pos > -1 and (copy_line[pos] + copy_line[pos + 1]) not in double_operators
				and (copy_line[pos - 1] + copy_line[pos]) not in double_operators):
				copy_line = copy_line.replace(operator, '~' + operator + '~')

		tokens = re.split(r'[~]', copy_line)

		tokens = self.remove_empty_tokens(tokens)
		pos = -1
		for token in tokens:
			pos = line.find(token, pos + 1)
			if pos < 0:
				pos = 0
			res_tokens.append([token, pos, num_line])

		return sorted(res_tokens, key=lambda x: x[1])


	def classify_tokens(self, tokens):
		classified_tokens = list()
		for token in tokens:

			if token[0] in keywords:
				classified_tokens.append(Token(token[0], Keyword, 'keyword', token[1], token[2]))
			elif token[0] in operators or token[0] in double_operators:
				classified_tokens.append(Token(token[0], Operator, 'operator', token[1], token[2]))
			elif re.findall(self.float_match, token[0]):
				classified_tokens.append(Token(token[0], Float, 'float const', token[1], token[2]))
			elif re.findall(self.integer_match, token[0]):
				classified_tokens.append(Token(token[0], Integer, 'integer const', token[1], token[2]))
			elif re.findall(self.string_match, token[0]):
				classified_tokens.append(Token(token[0], String, 'string constant', token[1], token[2]))
			elif re.findall(self.char_match, token[0]):
				classified_tokens.append(Token(token[0], Char, 'char constant', token[1], token[2]))
			elif token[0] in boolean_constants:
				classified_tokens.append(Token(token[0], Bool, 'boolean constant', token[1], token[2]))
			elif token[0] in separators:
				classified_tokens.append(Token(token[0], Separator, 'separator', token[1], token[2]))
			elif re.findall(self.variable_match, token[0]):
				classified_tokens.append(Token(token[0], Identifier, 'identifier', token[1], token[2]))
			else:
				classified_tokens.append(Token(token[0], Error, 'error', token[1], token[2]))
				raise LexicalError(token[1], token[2], 'unknown lexem')

		self.check_brackets(classified_tokens)

		return classified_tokens


	def analise(self):
		tokens = list()
		num_line = 1
		with open(self.source_file, 'r') as source_file:
			for line in source_file:
				tokens += self.find_tokens(line, num_line)
				num_line += 1
		return self.classify_tokens(tokens)