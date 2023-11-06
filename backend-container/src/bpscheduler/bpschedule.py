import sys
import os
if not hasattr(os, 'add_dll_directory'):
    def add_dll_directory(path):
        pass
current_working_directory = os.getcwd()
src_directory = os.path.join(current_working_directory, 'src')
sys.path.append(src_directory)
from models import (GameInfo, DraftInfo, FranchiseInfo, GameStatsTeamInfo, GameStatTeamSummaryInfo,
                     MetaDataInfo, PlayByPlayGameStatsTeamInfo, PlayByPlayInfo, PulsePlay, PlayerStats,
                      PlayerDCIinfo, SeasonStatOppo, SeasonStatPlayer, SeasonStatTeam, StandingsInfo, TeamInfo, TransactionInfo)
import requests

