# Internship Scraper

A modern web application for scraping internship opportunities from multiple job boards using Flask and Playwright.

## Prerequisites
1. Python 3.7 or higher installed
2. pip package manager

## Installation Steps

### 1. Install Python Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Install Playwright Browsers
After installing the Python packages, you need to install the browser binaries:
```powershell
playwright install
```

### 3. Run the Application
```powershell
python app.py
```

The application will start on `http://localhost:5000`

## Features
- 🔍 Search internships by keywords and location
- 🌐 Scrape from multiple sources (Indeed, LinkedIn)
- 📱 Responsive design with modern UI
- ⚡ Fast asynchronous scraping with Playwright
- 🎯 Filter results by source and number of pages

## Usage
1. Open your browser and go to `http://localhost:5000`
2. Enter your search keywords (e.g., "software engineering internship")
3. Optionally specify a location (e.g., "New York, NY")
4. Select which job boards to scrape from
5. Choose how many pages to scrape (1-5)
6. Click "Search Internships" and wait for results

## Notes
- The scraping process may take a few moments depending on the number of pages
- Some websites have anti-bot measures, so results may vary
- LinkedIn scraping is limited due to their strict bot detection
- Always respect websites' robots.txt and terms of service

## Troubleshooting
- If you get browser-related errors, make sure to run `playwright install`
- If the application doesn't start, check that all dependencies are installed
- For permission errors, try running the commands as administrator