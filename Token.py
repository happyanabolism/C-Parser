import Types

class Token:
    def __init__(self, value, type, type_name, start_pos, num_line):
        self.value = value
        self.type = type
        self.start_pos = start_pos
        self.num_line = num_line
        self.type_name = type_name

    def __str__(self):
        return 'name: {:<9}type: {:<20}start position: {:<15}' \
               'line number: {}'.format(self.value, self.type_name, self.start_pos, self.num_line)