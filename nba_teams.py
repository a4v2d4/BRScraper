# nba_teams.py 

# class for looking team abbrev. from name and vice-versa
class NBATeams:
    def __init__(self):
        self.teams = {
            "Atlanta Hawks": "ATL",                         # 1950 (year when first season ended)
            "Boston Celtics": "BOS",                        # 1947 (year when first season ended)
            "Brooklyn Nets": "NJN",                         # 1968 (year when first season ended)
            "Charlotte Hornets": "CHA",                     # 1989 (year when first season ended)
            "Chicago Bulls": "CHI",                         # 1967 (year when first season ended)
            "Cleveland Cavaliers": "CLE",                   # 1971 (year when first season ended)
            "Dallas Mavericks": "DAL",                      # 1981 (year when first season ended)
            "Denver Nuggets": "DEN",                        # 1968 (year when first season ended)
            "Detroit Pistons": "DET",                       # 1949 (year when first season ended)
            "Golden State Warriors": "GSW",                 # 1947 (year when first season ended)
            "Houston Rockets": "HOU",                       # 1968 (year when first season ended)
            "Indiana Pacers": "IND",                        # 1968 (year when first season ended)
            "Los Angeles Clippers": "LAC",                  # 1971 (year when first season ended)
            "Los Angeles Lakers": "LAL",                    # 1949 (year when first season ended)
            "Memphis Grizzlies": "MEM",                     # 1996 (year when first season ended)
            "Miami Heat": "MIA",                            # 1989 (year when first season ended)
            "Milwaukee Bucks": "MIL",                       # 1969 (year when first season ended)
            "Minnesota Timberwolves": "MIN",                # 1990 (year when first season ended)
            "New Orleans Pelicans": "NOH",                  # 2003 (year when first season ended)
            "New York Knicks": "NYK",                       # 1947 (year when first season ended)
            "Oklahoma City Thunder": "OKC",                 # 1968 (year when first season ended)
            "Orlando Magic": "ORL",                         # 1990 (year when first season ended)
            "Philadelphia 76ers": "PHI",                    # 1950 (year when first season ended)
            "Phoenix Suns": "PHO",                          # 1969 (year when first season ended)
            "Portland Trail Blazers": "POR",                # 1971 (year when first season ended)
            "Sacramento Kings": "SAC",                      # 1949 (year when first season ended)
            "San Antonio Spurs": "SAS",                     # 1968 (year when first season ended)
            "Toronto Raptors": "TOR",                       # 1996 (year when first season ended)
            "Utah Jazz": "UTA",                             # 1975 (year when first season ended)
            "Washington Wizards": "WAS",                    # 1962 (year when first season ended)
        }

        # more than 30 because diff. abbreviations due to chaning team names -- see https://www.basketball-reference.com/teams/
        self.team_abbrevs = {
            # main abbreviations
            'ATL': "Atlanta Hawks",                      # 1950 (year when first season ended)
            'BOS': "Boston Celtics",                         # 1947 (year when first season ended)
            'NJN': "Brooklyn Nets",                      # 1968 (year when first season ended)
            'CHO': "Charlotte Hornets",                      # 1989 (year when first season ended)
            'CHI': "Chicago Bulls",                      # 1967 (year when first season ended)
            'CLE': "Cleveland Cavaliers",                        # 1971 (year when first season ended)
            'DAL': "Dallas Mavericks",                       # 1981 (year when first season ended)
            'DEN': "Denver Nuggets",                         # 1968 (year when first season ended)
            'DET': "Detroit Pistons",                        # 1949 (year when first season ended)
            'GSW': "Golden State Warriors",                      # 1947 (year when first season ended)
            'HOU': "Houston Rockets",                        # 1968 (year when first season ended)
            'IND': "Indiana Pacers",                         # 1968 (year when first season ended)
            'LAC': "Los Angeles Clippers",                       # 1971 (year when first season ended)
            'LAL': "Los Angeles Lakers",                         # 1949 (year when first season ended)
            'MEM': "Memphis Grizzlies",                      # 1996 (year when first season ended)
            'MIA': "Miami Heat",                         # 1989 (year when first season ended)
            'MIL': "Milwaukee Bucks",                        # 1969 (year when first season ended)
            'MIN': "Minnesota Timberwolves",                         # 1990 (year when first season ended)
            'NOH': "New Orleans Pelicans",                       # 2003 (year when first season ended)
            'NYK': "New York Knicks",                        # 1947 (year when first season ended)
            'OKC': "Oklahoma City Thunder",                      # 1968 (year when first season ended)
            'ORL': "Orlando Magic",                      # 1990 (year when first season ended)
            'PHI': "Philadelphia 76ers",                         # 1950 (year when first season ended)
            'PHO': "Phoenix Suns",                       # 1969 (year when first season ended)
            'POR': "Portland Trail Blazers",                         # 1971 (year when first season ended)
            'SAC': "Sacramento Kings",                       # 1949 (year when first season ended)
            'SAS': "San Antonio Spurs",                      # 1968 (year when first season ended)
            'TOR': "Toronto Raptors",                        # 1996 (year when first season ended)
            'UTA': "Utah Jazz",                      # 1975 (year when first season ended)
            'WAS': "Washington Wizards",                         # 1962 (year when first season ended)

            # other abbreviations for same teams due to team name change
            "BRK": "Brooklyn Nets", # 2012-13	2024-25
            "NOP": "New Orleans Pelicans", # 2013-14	2024-25
            "SEA": "Seattle SuperSonics", # 1967-68	2007-08
            "CHA": "Charlotte Bobcats", # 2004-05	2013-14
            "NOK": "New Orleans/Oklahoma City Hornets", # 2005-06	2006-07
        }
    
    def get_abbreviation(self, team_name: str) -> str | None:
        """
        Get team abbreviation from full name.
        Returns None if team not found.
        """
        return self.teams.get(team_name)
    
    def get_team_name(self, abbreviation: str) -> str | None:
        """
        Get full team name from abbreviation.
        Returns None if abbreviation not found.
        """
        return self.team_abbrevs.get(abbreviation)
    
    def is_valid_team(self, team_name: str) -> bool:
        """Check if a team name is valid."""
        return team_name in self.teams
    
    def is_valid_abbreviation(self, abbreviation: str) -> bool:
        """Check if an abbreviation is valid."""
        return abbreviation in self.team_abbrevs
    
    def get_all_teams(self) -> list:
        """Get a list of all team names."""
        return list(self.teams.keys())
    
    def get_all_abbreviations(self) -> list:
        """Get a list of all team abbreviations."""
        return list(self.teams.values())