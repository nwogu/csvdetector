from .csvfile import CsvFile
from .detector import Detector

class Handler():

    __context = {}

    __errors = []

    def __init__(self):

        self.__context.update({
        "total": 0,
        "messages": [],
        "errors": self.__errors
    })

    def handle(self, request):
        headers = request.POST['headers']
        headers = headers.split("," ) if headers and headers != "" else list()
        try:
            csvfile = CsvFile(request.FILES['csv_file'], headers)
            detector = Detector(csvfile, request.POST['level'])
            detector.detect()
            self.__context.update({
            'total': detector.totals(),
            'messages': detector.duplicates(),
            'errors': []
            })
        except ValueError as error:
            self.__errors.append(str(error))

    def let_context(self):
        return self.__context