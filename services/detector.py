import itertools as it

class Detector():
    
    __file = ...

    __level = ...

    __total_duplicates = 0

    __messages = list()

    __column_data = list()

    __column_duplicates = list()
    
    def __init__(self, csvfile, level):

        self.__file = csvfile

        self.__level = level

        self.__messages = list()

        self.__total_duplicates = 0

        self.__column_data = list()

        self.__column_duplicates = list()

    def totals(self):
        return self.__total_duplicates

    def duplicates(self):
        return self.__messages
    
    def detect(self):
        for header in self.__file.top():
            self.get_column_data(header)
        self.get_column_duplicates()
        self.push_duplicates()

    def get_column_data(self, header):
        self.__column_data.append(
            [row[index].lower() for index, row in zip(it.repeat(self.__file.position(header)), self.__file.body())]
        )

    def get_column_duplicates(self):
        for column_data in self.__column_data:
            container = []
            self.__column_duplicates.append(
                [row_number 
                for row_number, data in zip(it.count(2), column_data) 
                if self.match(data, row_number, column_data, container)]
            ) 
    
    def push_duplicates(self):
        if self.__level == "loose" and len(self.__file.top()) > 1:
            return self.push_duplicates_for_loose()
        for index, head in zip(it.count(), self.__file.top()):
            column_duplicates = self.__column_duplicates[index]
            if column_duplicates:
                self.__total_duplicates += len(column_duplicates)
                for row_number in column_duplicates:
                    value = self.__file.body()[row_number - 2][self.__file.position(head)]
                    self.compose_message(row_number, head, value)
                

    def push_duplicates_for_loose(self):
        intersect_duplicates = set(self.__column_duplicates[0]).intersection(*self.__column_duplicates)
        if intersect_duplicates:
            self.__total_duplicates = len(intersect_duplicates)
            for row_number in intersect_duplicates:
                self.compose_message(row_number, str(self.__file))

    def compose_message(self, row_number, head, value = ""):
        self.__messages.append(
            f"Possible Duplicate {value}, Found on Line {row_number}: Header(s)" + "<br />" + f"{head}"
        )

    def match(self, data, row_number, column_data, counter):
        matched = column_data.count(data) > 1
        if matched:
            counter.append(data)
        if counter.count(data) < 2:
            return False
        return matched
        
    