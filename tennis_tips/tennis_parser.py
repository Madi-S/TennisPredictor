from get_matches import VprognozeHTML
from tennislive_stats import TennisLiveStats
from ultimate_stats import UltimateStats


class Parser(VprognozeHTML, TennisLiveStats, UltimateStats):
    pass
