class SyntxError(Exception):
	def __init__(self, start_pos, num_line, description):
		self.description = '{} {}:{}: {}'.format(self.__class__.__name__,
				start_pos, num_line, description)

	def __str__(self):
		return self.description

class BracketsError(SyntxError):
	pass

class IdentifierError(SyntxError):
	pass

class ComparisonError(SyntxError):
	pass