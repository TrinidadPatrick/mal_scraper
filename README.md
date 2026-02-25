# MyAnimeList Scraper

A web scraper built with Python and Playwright to extract anime datas from MyAnimeList. It fetches data for various categories including top-rated, airing, upcoming, TV series, and movies.

## Prerequisites

- [Python 3.8+](https://www.python.org/downloads/)
- `pip` (standard with Python)

## Installation & Setup

Follow these steps to set up the project on your local machine:

1. **Create a Virtual Environment**
   Open your terminal in the project directory and run:

   ```bash
   python -m venv venv
   ```

2. **Activate the Virtual Environment**
   - **Windows:**
     ```powershell
     .\venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

3. **Run the Setup Script**
   Execute the provided batch file to install dependencies and set up Playwright:
   ```bash
   .\setup_scraper.bat
   ```

## Usage

Once the setup is complete and your virtual environment is active, you can start the scraper by running:

```bash
python main.py
```

The scraper will launch a Chromium browser (non-headless by default) and begin fetching data for different anime categories.

## Project Structure

- `main.py`: Entry point for the application.
- `scrapers/`: Contains the logic for parsing and extracting data.
- `output_json/`: All scraped data is saved here in JSON format.
- `browser_setup.py`: Configuration for the Playwright browser instance.
- `requirements.txt`: Python package dependencies.

## Output

The scraper generates JSON files in the `output_json/top_animes/` directory:

- `top_animes.json`
- `top_airing_animes.json`
- `top_upcoming_animes.json`
- `top_tv_animes.json`
- `top_movie_animes.json`

## License

[MIT](LICENSE)
