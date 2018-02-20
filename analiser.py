import re
from tabulate import tabulate
from Token import Token
from Types import (Keyword, Identifier, Float, String,
				  Operator, Separator, Error, Integer, Char)

float_match = r'^[0-9]*[.,][0-9]+$'
integer_match = r'^[-+]?\d*$'
string_match = r'".*"'
char_match = r"'.{1}'"
variable_match = r'(^[a-zA-Z_$][a-zA-Z0-9_$]*$)'

keywords = ('else', 'auto',	'enum',	'operator', 'bool', 'true',
            'break', 'case', 'extern', 'typedef', 'false', 'register', 'char',
            'float', 'for', 'return', 'const', 'short',	'unsigned',	'signed',
            'continue', 'if', 'sizeof', 'virtual', 'default', 'static', 'void',
            'delete', 'int', 'volatile', 'do', 'long', 'struct', 'double', 'switch',
            'while', 'define', 'include', )

operators = ('=', '+', '-', '*', '/', '%', '<', '>', '|', '&', '^', '[', ']', ']')
double_operators = ('==', '>=', '<=', '++', '--', '<<', '>>', '||', '&&', '+=', '-=',)
separators = (' ', ';', '{', '}', ')', '(', ',', '\t', '#', '\n', )

#пробелы, табуляции и переводы строк игнорируются анализатором языка си
def remove_empty_tokens(tokens):
	whitespces = ['', ' ', '\t', '\n']
	tokens = list(filter(lambda x: x not in whitespces, tokens))
	return tokens


def find_tokens(line, num_line):
	res_tokens = list()
	copy_line = line

	tokens = re.findall(string_match, line)
	tokens += re.findall(char_match, line)
	for token in tokens:
		res_tokens.append([token, line.find(token), num_line])
		copy_line = copy_line.replace(token, '')

	for separator in separators:
		if line.find(separator) > -1:
			copy_line = copy_line.replace(separator, '~' + separator + '~')
	for double_operator in double_operators:
		if line.find(double_operator) > -1:
			copy_line = copy_line.replace(double_operator, '~' + double_operator + '~')
	for operator in operators:
		pos = copy_line.find(operator)
		if pos > -1 and (copy_line[pos] + copy_line[pos + 1]) not in double_operators:
			copy_line = copy_line.replace(operator, '~' + operator + '~')

	tokens = re.split(r'[~]', copy_line)
	tokens = remove_empty_tokens(tokens)
	pos = -1
	for token in tokens:
		pos = line.find(token, pos + 1)
		res_tokens.append([token, pos, num_line])

	return res_tokens


def classify_tokens(tokens):
	classified_tokens = list()
	for token in tokens:

		if token[0] in keywords:
			classified_tokens.append(Token(token[0], Keyword, 'keyword', token[1], token[2]))
		elif token[0] in operators or token[0] in double_operators:
			classified_tokens.append(Token(token[0], Operator, 'operator', token[1], token[2]))
		elif re.findall(float_match, token[0]):
			classified_tokens.append(Token(token[0], Float, 'float const', token[1], token[2]))
		elif re.findall(integer_match, token[0]):
			classified_tokens.append(Token(token[0], Integer, 'integer const', token[1], token[2]))
		elif re.findall(string_match, token[0]):
			classified_tokens.append(Token(token[0], String, 'string constant', token[1], token[2]))
		elif re.findall(char_match, token[0]):
			classified_tokens.append(Token(token[0], Char, 'char constant', token[1], token[2]))
		elif token[0] in separators:
			classified_tokens.append(Token(token[0], Separator, 'separator', token[1], token[2]))
		elif re.findall(variable_match, token[0]):
			classified_tokens.append(Token(token[0], Identifier, 'identifier', token[1], token[2]))
		else:
			classified_tokens.append(Token(token[0], Error, 'error', token[1], token[2]))

	return sorted(classified_tokens, key=lambda x: x.start_pos)



if __name__ == '__main__':
	classified_tokens = list()
	with open('test_files/test.c', 'r') as file:
		num_line = 1
		for line in file:
			classified_tokens += classify_tokens(find_tokens(line, num_line))
			num_line += 1
#	classified_tokens = classify_tokens(find_tokens("""5""", 1))
	for token in classified_tokens:
		print(token)