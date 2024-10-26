from bs4 import BeautifulSoup
import csv

# Load HTML content from a local file
with open('teams.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Initialize BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Specify CSV output file name
csv_file = 'nba_franchises.csv'

# Define column headers
headers = [
    'Team Name', 'League', 'Start Year', 'End Year', 'Total Years',
    'Games Played', 'Wins', 'Losses', 'Win-Loss %', 'Playoff Appearances',
    'Division Titles', 'Conference Titles', 'Championships'
]

# Open CSV file for writing
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)

    # Parse each team row
    for row in soup.find_all('tr', class_=['full_table', 'partial_table']):
        # Get the end year (year_max) and skip if it's before 1979-1980
        end_year = row.find('td', {'data-stat': 'year_max'}).text
        if end_year < '1979-80':
            continue  # Skip rows with end year before 1979-80

        # Extract data for the row
        team_name = row.find('th', {'data-stat': 'franch_name'}).text if row['class'][0] == 'full_table' else row.find('th', {'data-stat': 'team_name'}).text
        league = row.find('td', {'data-stat': 'lg_id'}).text
        start_year = row.find('td', {'data-stat': 'year_min'}).text
        years = row.find('td', {'data-stat': 'years'}).text
        games_played = row.find('td', {'data-stat': 'g'}).text
        wins = row.find('td', {'data-stat': 'wins'}).text
        losses = row.find('td', {'data-stat': 'losses'}).text
        win_loss_pct = row.find('td', {'data-stat': 'win_loss_pct'}).text
        playoff_appearances = row.find('td', {'data-stat': 'years_playoffs'}).text
        division_titles = row.find('td', {'data-stat': 'years_division_champion'}).text
        conference_titles = row.find('td', {'data-stat': 'years_conference_champion'}).text
        championships = row.find('td', {'data-stat': 'years_league_champion'}).text

        # Write row to CSV
        writer.writerow([
            team_name, league, start_year, end_year, years, games_played,
            wins, losses, win_loss_pct, playoff_appearances, division_titles,
            conference_titles, championships
        ])

print(f"Data has been successfully written to {csv_file}")
