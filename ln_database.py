
class LNDataBase:
    def __init__(self, filename):
        self.filename = filename
        self.numbers = None
        self.file = None
        self.load()

    def load(self):
        self.file = open(self.filename, "r")
        self.numbers = []

        for line in self.file:
            number = line.strip().split(";")
            self.numbers = number

        self.file.close()

    def get_number(self, number):
        if number in self.numbers:
            return self.numbers
        else:
            return -1

    def add_number(self, number):
        if number not in self.numbers:
            self.numbers.append(number)
            self.save()
            return 1
        else:
            print("Number exists already")
            return -1

    def save(self):
        with open(self.filename, "w") as f:
            for number in self.numbers:
                f.write(number + ';' + '\n')
