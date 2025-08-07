import unittest
from nba_teams import NBATeams  # Assuming the previous code is saved in nba_teams.py

class TestNBATeams(unittest.TestCase):
    def setUp(self):
        """Create a fresh NBATeams instance for each test."""
        self.nba = NBATeams()

    def test_get_abbreviation(self):
        """Test getting abbreviations from team names."""
        self.assertEqual(self.nba.get_abbreviation('Boston Celtics'), 'BOS')
        self.assertEqual(self.nba.get_abbreviation('Los Angeles Lakers'), 'LAL')
        self.assertIsNone(self.nba.get_abbreviation('Invalid Team'))
        self.assertIsNone(self.nba.get_abbreviation(''))

    def test_get_team_name(self):
        """Test getting team names from abbreviations."""
        self.assertEqual(self.nba.get_team_name('GSW'), 'Golden State Warriors')
        self.assertEqual(self.nba.get_team_name('MIA'), 'Miami Heat')
        self.assertIsNone(self.nba.get_team_name('ABC'))
        self.assertIsNone(self.nba.get_team_name(''))

    def test_is_valid_team(self):
        """Test team name validation."""
        self.assertTrue(self.nba.is_valid_team('Miami Heat'))
        self.assertTrue(self.nba.is_valid_team('Brooklyn Nets'))
        self.assertFalse(self.nba.is_valid_team('Brook Nets'))
        self.assertFalse(self.nba.is_valid_team('Invalid Team'))
        self.assertFalse(self.nba.is_valid_team(''))
        # Test case sensitivity
        self.assertFalse(self.nba.is_valid_team('MIAMI HEAT'))

    def test_is_valid_abbreviation(self):
        """Test abbreviation validation."""
        self.assertTrue(self.nba.is_valid_abbreviation('LAL'))
        self.assertTrue(self.nba.is_valid_abbreviation('BOS'))
        self.assertFalse(self.nba.is_valid_abbreviation('ABC'))
        self.assertFalse(self.nba.is_valid_abbreviation(''))
        # Test case sensitivity
        self.assertFalse(self.nba.is_valid_abbreviation('lal'))

    def test_get_all_teams(self):
        """Test retrieving all team names."""
        all_teams = self.nba.get_all_teams()
        self.assertIsInstance(all_teams, list)
        self.assertEqual(len(all_teams), 30)
        self.assertIn('Boston Celtics', all_teams)
        self.assertIn('Los Angeles Lakers', all_teams)

    def test_get_all_abbreviations(self):
        """Test retrieving all abbreviations."""
        all_abbrevs = self.nba.get_all_abbreviations()
        self.assertIsInstance(all_abbrevs, list)
        self.assertEqual(len(all_abbrevs), 30)
        self.assertIn('BOS', all_abbrevs)
        self.assertIn('LAL', all_abbrevs)

    def test_bidirectional_lookup(self):
        """Test that lookups work in both directions."""
        team_name = 'Miami Heat'
        abbrev = self.nba.get_abbreviation(team_name)
        self.assertEqual(self.nba.get_team_name(abbrev if abbrev else ""), team_name)

if __name__ == '__main__':
    unittest.main()