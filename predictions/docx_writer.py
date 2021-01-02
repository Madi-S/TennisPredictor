


class DOCXWriter:

    def __init__(self, filename: str):
        '''
        Initialize DOCX Writer by creating DOCX with given filename

        :param filename: `str` for the DOCX file name
        :return: returns nothing
        '''
        with open(filename + '.docx', 'w') as _:
            pass

    def write(self, data: dict):
        '''
        Write given `dict` data to a .docx document

        :param player_name: Player name
        :return: returns path to PDF document with stats and `player_name` statistics ot `False` if no statistics for `player_name` were found
        '''
        pass