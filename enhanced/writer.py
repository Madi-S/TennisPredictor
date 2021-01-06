from docx import Document
from random import choice


w, l = None, None
easy_game = {
    '{} excelled {} in many stats. Moreover, {} in a good shape, comparing to {}. To sum up, {} should win here confidently': [w, l, w, l, w],
    'Considering players\' statistics, {} is much better than {}. What is more, many betting experts suggest to bet on {}. Hence, my prediction - winner {}': [w, l, w, w],
    'Today\'s match should be a cakewalk for {}. Taking into consideration that he scored much more than {}, {} has to take victory over {}': [w, l, w, l],
    '{} is an apparent favourite here. Tennis experts say that {} has little chances here. {} and {} are on different levels, so {} should win today': [w, l, l, w, w],
}
hard_game = {
    'This will be a tight fight between {} and {}. Some tennis portals presume that {} will triumph over {}. Nonetheless, others consider {} as favourite. Final prediction: small bet on {}': [w, l, w, l, l, w],
    '{} and {} are relatively equal tennis players. Of course, {} surpass {} in some indicators. However, {} also shows some good tennis. Accordingly, a risky match here but {} has a small advatage over {}': [l, w, w, l, l, w, l],
    '{} vs {} - a clash of two big tennis figures. Players have scored approximately equal amount of points but {} scored a little bit more. Thus and so, small bet on {} is a good choice': [l, w, w, w],
    'An even match for today: {} vs {}. {} and {} are in good shape and anyone can win today as tennis experts assume. Nevertheless, {} has a higher score than {} and this is a sign for a small bet on {}': [w, l, w, l, w, l],
}


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

        self._d.add_heading(
            f'{p1} ({betting_tips["Odds"][p1]}) vs {p2} ({betting_tips["Odds"][p2]})', 0)
        self._d.add_heading(
            f'{betting_tips["Tournament"].replace(".",". ")}', 0)
        self._d.add_heading(f'{data["Time"]}\n', 0)

        for p in players:
            for o in bio:
                self._d.add_paragraph(f'{o}: {stats[p][o]}')
            self._d.add_paragraph(
                f'Bets tendency on winner - {p}: {betting_tips["BetsTendency"][p]}\n')

        self._d.add_paragraph(
            f'Bets tendency on total over: {betting_tips["BetsTendency"]["TotalOver"]}')
        self._d.add_paragraph(
            f'Bets tendency on total under: {betting_tips["BetsTendency"]["TotalUnder"]}')

        self._d.add_paragraph(f'Head to heads: {data["H2H"]}')

        p = self._d.add_paragraph('\n')
        p.add_run('Top Betting tips:').bold = True

        for b in betting_tips['Predictions']:
            for o in order:
                self._d.add_paragraph(f'{o}: {b[o]}')
            self._d.add_paragraph('\n')

        p = self._d.add_paragraph('\n')
        p.add_run(
            f'Conclusion: {p1} scored {data["Points"][p1]} and {p2} scored {data["Points"][p2]}\n{data["Conclusion"]}').bold = True

        self._d.save(self._filename)
