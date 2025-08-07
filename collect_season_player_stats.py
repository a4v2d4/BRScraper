from enum import Enum, auto
import pandas as pd
from BRScraper import nba
import logging
from typing import Optional
from datetime import datetime
import sys
import traceback


class SeasonType(Enum):
    """Enum for different types of NBA seasons"""
    REGULAR = auto()
    PLAYOFF = auto()

    def __str__(self) -> str:
        return self.name.lower()

    @property
    def display_name(self) -> str:
        return "regular season" if self == SeasonType.REGULAR else "playoff"


def setup_logging(log_level: int = logging.DEBUG, logs_dir: str = "logs") -> str:
    """
    Set up logging configuration with both file and console handlers.

    Args:
        log_level (int): Logging level to use (default: logging.DEBUG)
        logs_dir (str): Directory to store log files (default: "logs")

    Returns:
        str: Path to the created log file
    """
    import os

    # Create logs directory if it doesn't exist
    try:
        os.makedirs(logs_dir, exist_ok=True)
        logging.debug(f"Ensured logs directory exists: {logs_dir}")
    except Exception as e:
        print(f"Error creating logs directory {logs_dir}: {str(e)}")
        logs_dir = "."  # Fallback to current directory

    # Create log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f'nba_stats_scraper_{timestamp}.log'
    log_filepath = os.path.join(logs_dir, log_filename)

    # Create formatters for different levels of detail
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )

    try:
        # File handler with detailed formatting
        file_handler = logging.FileHandler(log_filepath)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)

        # Console handler with simpler formatting
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)

        # Root logger configuration
        logging.root.setLevel(log_level)
        logging.root.handlers = []  # Clear any existing handlers
        logging.root.addHandler(file_handler)
        logging.root.addHandler(console_handler)

        logging.debug(f"Logging initialized. Log file: {log_filepath}")
        return log_filepath

    except Exception as e:
        print(f"Error setting up logging: {str(e)}")
        raise


def get_single_season_stats(year: int, season_type: SeasonType) -> Optional[pd.DataFrame]:
    """
    Fetch stats for a single season.

    Args:
        year (int): The NBA season year
        season_type (SeasonType): Type of season stats to fetch

    Returns:
        Optional[pd.DataFrame]: DataFrame containing the stats, or None if failed
    """
    try:
        logging.info(f"Fetching {season_type.display_name} stats for {year}")
        logging.debug(f"Making API call with parameters: year={
                      year}, playoffs={season_type == SeasonType.PLAYOFF}")

        df = nba.get_stats(
            season=year,
            info='totals',
            playoffs=(season_type == SeasonType.PLAYOFF),
            rename=False
        )

        if df is None or df.empty:
            logging.warning(f"No data returned for {year} {
                            season_type.display_name}")
            return None

        logging.debug(f"Data shape before adding columns: {df.shape}")

        # Remove 'Awards' column -- can get collect info later (and/or in different manor)
        name_of_col_to_remove = 'Awards'
        if name_of_col_to_remove in df.columns:
            df.drop(name_of_col_to_remove, axis=1, inplace=True)
        elif season_type == SeasonType.REGULAR:
            logging.error(f"Error: no 'Awards' column for {year} {
                season_type.display_name} stats.")
        
        name_of_col_to_remove = 'Season'
        if name_of_col_to_remove in df.columns:
            df.drop(name_of_col_to_remove, axis=1, inplace=True)

        # Ignore cummulative rows for multiple teams
        if 'Team' in df.columns:
            df = df[~df['Team'].str.endswith('TM', na=False)]  # Filter out rows where 'Team' ends with 'TM'

        # Add year column for reference
        df['season_year'] = year
        df['season_type'] = str(season_type)

        logging.info(f"Successfully fetched {len(df)} records for {
                     year} {season_type.display_name}")
        logging.debug(f"Final data shape: {df.shape}, columns: {
                      df.columns.tolist()}")
        return df

    except Exception as e:
        logging.error(f"Error fetching {
                      season_type.display_name} stats for {year}")
        logging.error(f"Exception details: {str(e)}")
        logging.debug(f"Traceback: {traceback.format_exc()}")
        return None


def get_stats_for_years(
    first_year: int,
    last_year: int,
    season_type: SeasonType
) -> pd.DataFrame:
    """
    Fetch stats for multiple seasons.

    Args:
        first_year (int): Starting year
        last_year (int): Ending year
        season_type (SeasonType): Type of season stats to fetch

    Returns:
        pd.DataFrame: Combined stats for all seasons
    """
    season_dfs = []

    logging.info(f"Starting collection of {season_type.display_name} stats from {
                 first_year} to {last_year}")

    for year in range(first_year, last_year + 1):
        df = get_single_season_stats(year, season_type)
        if df is not None and not df.empty:
            logging.debug(f"Adding DataFrame for {
                          year} to collection. Shape: {df.shape}")
            season_dfs.append(df)
        else:
            logging.warning(f"Skipping {year} due to empty or None DataFrame")

    # Combine all DataFrames
    if not season_dfs:
        logging.warning(f"No data was collected for {
                        season_type.display_name} stats")
        return pd.DataFrame()

    logging.debug(f"Concatenating {len(season_dfs)} DataFrames")
    all_stats = pd.concat(season_dfs, ignore_index=True)
    logging.info(f"Successfully collected {len(all_stats)} total records")
    logging.debug(f"Final combined DataFrame shape: {all_stats.shape}")
    return all_stats


def save_stats_to_csv(
    df: pd.DataFrame,
    filename: str,
    output_dir: str = "nba_stats_output"
) -> None:
    """
    Save DataFrame to CSV file.

    Args:
        df (pd.DataFrame): DataFrame to save
        filename (str): Name of the file
        output_dir (str): Directory to save the file
    """
    import os

    try:
        logging.debug(f"Attempting to save DataFrame with shape {
                      df.shape} to {filename}")

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        logging.debug(f"Output directory ensured: {output_dir}")

        # Save to CSV
        output_path = os.path.join(output_dir, filename)
        df.to_csv(output_path, index=False)
        logging.info(f"Successfully saved data to {output_path}")

    except Exception as e:
        logging.error(f"Error saving data to {filename}")
        logging.error(f"Exception details: {str(e)}")
        logging.debug(f"Traceback: {traceback.format_exc()}")


def main(first_year: int, last_year: int, season_type: SeasonType):
    """
    Main function to run the NBA stats scraper.

    Args:
        first_year (int): Starting year for data collection
        last_year (int): Ending year for data collection
        season_type (SeasonType): Type of season stats to collect
    """
    logging.info(f"Starting NBA stats collection: years {
                 first_year}-{last_year}, type: {season_type.display_name}")

    # Get stats
    stats_df = get_stats_for_years(
        first_year=first_year,
        last_year=last_year,
        season_type=season_type
    )

    # Save results
    if not stats_df.empty:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{str(season_type)}_stats_{timestamp}.csv"
        save_stats_to_csv(stats_df, filename)
    else:
        logging.warning("No data to save - resulting DataFrame is empty")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='NBA Stats Scraper')
    parser.add_argument('--first-year', type=int, default=1980,
                        help='First year to collect stats from')
    parser.add_argument('--last-year', type=int, default=2024,
                        help='Last year to collect stats from')
    parser.add_argument(
        '--season-type',
        type=str,
        choices=[season_type.name for season_type in SeasonType],
        default=SeasonType.REGULAR.name,
        help='Type of season stats to collect'
    )
    parser.add_argument(
        '--log-level',
        type=str,
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO',
        help='Set the logging level'
    )

    args = parser.parse_args()

    # Setup logging before anything else
    setup_logging(log_level=getattr(logging, args.log_level))

    try:
        main(
            args.first_year,
            args.last_year,
            SeasonType[args.season_type]
        )
    except Exception as e:
        logging.critical(f"Unhandled exception in main execution")
        logging.critical(f"Exception details: {str(e)}")
        logging.debug(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)
