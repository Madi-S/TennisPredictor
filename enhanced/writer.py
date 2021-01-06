from docx import Document


bio = ['Name', 'Age', 'Country', 'Ranking', 'RankingPeak',
       'Points', 'PrizeMoney', 'TotalMatches', 'Winrate%']
order = ['Outcome', 'Odds',  'Explanation']


class DOCXWriter:

    def __init__(self, filename: str):
        '''
        Initialize DOCX Writer by creating DOCX with given filename

        :param filename: `str` for the DOCX file name
        :return: returns nothing
        '''
        self._filename = filename + '.docx'
        self._d = Document()

    def write(self, betting_tips: dict, stats: dict, data: dict):
        '''
        Save given data to .docx file

        :param betting_tips: `dict` of betting tips, odds, bets tendency, players' names
        :param stats: `dict` containing detailed statistics of each player
        :param data: `dict` containing time, h2h, conclusion and points scored for each player
        :return: returns nothing
        '''
        players = betting_tips['Players']
        p1, p2 = players

        self._d.add_heading(f'{p1} ({betting_tips["Odds"][p1]}) vs {p2} ({betting_tips["Odds"][p2]})', 0)
        self._d.add_heading(f'{betting_tips["Tournament"].replace(".",". ")}', 0)
        self._d.add_heading(f'{data["Time"]}\n', 0)

        for p in players:
            for o in bio:
                self._d.add_paragraph(f'{o}: {stats[p][o]}')
            self._d.add_paragraph(f'Bets tendency on winner - {p}: {betting_tips["BetsTendency"][p]}\n')
        
        self._d.add_paragraph(f'Bets tendency on total over: {betting_tips["BetsTendency"]["TotalOver"]}')
        self._d.add_paragraph(f'Bets tendency on total under: {betting_tips["BetsTendency"]["TotalUnder"]}')

        self._d.add_paragraph(f'Head to heads: {data["H2H"]}')

        p = self._d.add_paragraph('\n')
        p.add_run('Top Betting tips:').bold = True

        for b in betting_tips['Predictions']:
            for o in order:
                self._d.add_paragraph(f'{o}: {b[o]}')
            self._d.add_paragraph('\n')

        p = self._d.add_paragraph('\n')
        p.add_run(f'Conclusion: {p1} scored {data["Points"][p1]} and {p2} scored {data["Points"][p2]}\n{data["Conclusion"]}').bold = True

        self._d.save(self._filename)