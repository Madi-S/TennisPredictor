# Import some kind of package to write docx

from os import chdir

class Writer:
    def __init__(self, filename: str):
        if not isinstance(filename, str):
            raise TypeError('Filename should consists of `.` or `?` and must be a string')
        self._filename = filename
        chdir('..')
        # TODO: Write `filename`.docx

    def write(self, data: dict):
        pass

if __name__ == '__main__':
    w = Writer('tennis_predictions')