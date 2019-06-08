import csv

class CsvFile():

    __headers = list()

    __file_headers = list()

    __csv = list()

    def __init__(self, file, headers=None):

        self.__csv = self.get_csv(file)

        self.__file_headers = self.__csv.pop(0)

        self.__headers = self.get_headers(headers)
    
    def get_csv(self, file):
        return [row for row in csv.reader(file.read().decode('utf-8').splitlines())]

    def get_headers(self, headers):
        return self.validate_headers(headers) if headers else self.__file_headers

    def validate_headers(self, headers):
        headers = [header.strip() for header in headers]
        for header in headers:
            if header not in self.__file_headers:
                raise ValueError("Wrong Headers Specified")
        return headers

    def top(self):
        return self.__headers

    def body(self):
        return self.__csv

    def position(self, header):
        return self.__file_headers.index(header)

    def __str__(self):
        return ", ".join(self.__file_headers)

