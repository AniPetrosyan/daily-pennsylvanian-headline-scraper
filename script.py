"""
Scrapes the latest editorial headline from The Daily Pennsylvanian website and saves it to a JSON file.
This file tracks the editorial headlines over time, allowing for historical headline data accumulation.
"""

import os
import sys

import daily_event_monitor

from bs4 import BeautifulSoup
import requests
import loguru


def scrape_latest_editorial():
    url = "https://www.thedp.com/section/editorials"
    response = requests.get(url)
    loguru.logger.info(f"Request URL: {response.url}")
    loguru.logger.info(f"Request status code: {response.status_code}")

    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        editorial_headline_tag = soup.find("h3", class_="standard-link")
        if editorial_headline_tag and editorial_headline_tag.find("a"):
            editorial_headline = editorial_headline_tag.find("a").get_text(strip=True)
            loguru.logger.info(f"Latest editorial headline: {editorial_headline}")
            return editorial_headline
        else:
            loguru.logger.error("Failed to find the editorial headline.")
            return ""
    else:
        loguru.logger.error(f"Failed to retrieve the page, status code: {response.status_code}")
        return ""

if __name__ == "__main__":

    # Setup logger to track runtime
    loguru.logger.add("scrape.log", rotation="1 day")

    # Create data dir if needed
    loguru.logger.info("Creating data directory if it does not exist")
    try:
        os.makedirs("data", exist_ok=True)
    except Exception as e:
        loguru.logger.error(f"Failed to create data directory: {e}")
        sys.exit(1)

    # Load daily event monitor
    loguru.logger.info("Loading daily event monitor")
    dem = daily_event_monitor.DailyEventMonitor(
        "data/daily_pennsylvanian_editorial_headlines.json"
    )

    # Run scrape
    loguru.logger.info("Starting scrape")
    try:
        data_point = scrape_latest_editorial()
    except Exception as e:
        loguru.logger.error(f"Failed to scrape data point: {e}")
        data_point = None

    # Save data
    if data_point is not None:
        dem.add_today(data_point)
        dem.save()
        loguru.logger.info("Saved daily event monitor")

    def print_tree(directory, ignore_dirs=[".git", "__pycache__"]):
        loguru.logger.info(f"Printing tree of files/dirs at {directory}")
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            level = root.replace(directory, "").count(os.sep)
            indent = " " * 4 * (level)
            loguru.logger.info(f"{indent}+--{os.path.basename(root)}/")
            sub_indent = " " * 4 * (level + 1)
            for file in files:
                loguru.logger.info(f"{sub_indent}+--{file}")

    print_tree(os.getcwd())

    loguru.logger.info("Printing contents of data file {}".format(dem.file_path))
    with open(dem.file_path, "r") as f:
        loguru.logger.info(f.read())

    # Finish
    loguru.logger.info("Scrape complete")
    loguru.logger.info("Exiting")
