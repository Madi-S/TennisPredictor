# Import some kind of package to write docx

from os import chdir

class Writer:
    def __init__(self, filename: str):
        if not isinstance(filename, str):
            raise TypeError('Filename should consists of `.` or `?` and must be a string')
        self._filename = filename
        chdir('..')
        # TODO: Create `filename`.docx

    def write(self, data: dict):
        # What to write:
        # 1) Real names list (players names)
        # 2) Some stats form tennislive to show
        # 3) Winner1 odds and Winner2 odds
        # 4) Predictions from vprognoze and info to them
        # 5) Conclusion
        pass

if __name__ == '__main__':
    w = Writer('tennis_predictions')