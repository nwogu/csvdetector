from .csvfile import CsvFile
from .detector import Detector

class Handler():

    __context = {}

    def __init__(self):

        self.__context.update({
        "total": 0,
        "messages": []
    })

    def handle(self, request):
        headers = request.POST['headers']
        headers = headers.split("," ) if headers and headers != "" else list()
        csvfile = CsvFile(request.FILES['csv_file'], headers)
        detector = Detector(csvfile, request.POST['level'])
        detector.detect()
        self.__context.update({
            'total': detector.totals(),
            'messages': detector.duplicates()
        })
        
    def let_context(self):
        return self.__context