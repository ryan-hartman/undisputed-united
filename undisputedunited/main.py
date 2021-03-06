import pandas as pd

from undisputedunited.parser.current_season_parser import CurrentSeasonParser
from undisputedunited.parser.historic_parser import HistoricParser
from undisputedunited.template.readme_updater import update_readme


def main():
    current_champion = None
    changes = pd.DataFrame()
    for match in build_datasets().itertuples():
        if match.result != 'D' and (
                current_champion is None or match.home == current_champion or match.away == current_champion):
            winner = match.home if match.result == 'H' else match.away
            if winner != current_champion:
                current_champion = winner
                changes = changes.append([match])
    print(f'The current Undisputed United are {current_champion}')
    update_readme(changes.iloc[-1])


def build_datasets():
    historic_df = HistoricParser().parse('data/top_four_leagues_1888_2020.csv')
    current_df = CurrentSeasonParser().parse('https://fixturedownload.com/download/epl-2020-GMTStandardTime.csv')
    return pd.concat([historic_df, current_df])


if __name__ == "__main__":
    main()
