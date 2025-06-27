from flask import Flask, render_template, request, jsonify
import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from datetime import datetime
import logging
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class InternshipScraper:
    def __init__(self):
        self.timeout = 30000  # 30 seconds
        self.max_retries = 3
        self.retry_delay = 2000  # 2 seconds

    async def scrape_indeed(self, keyword="internship", location="Coimbatore, Tamil Nadu", max_pages=2):
        """Scrape internships from Indeed with improved robustness"""
        internships = []
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]

        async with async_playwright() as p:
            browser = None
            try:
                browser = await p.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
                )
                page = await browser.new_page()

                for page_num in range(max_pages):
                    try:
                        start = page_num * 10
                        url = f"https://www.indeed.com/jobs?q={keyword}&l={location}&start={start}"

                        logger.info(f"Scraping Indeed page {page_num + 1}: {url}")

                        # Randomly select a user agent
                        await page.set_extra_http_headers({
                            'User-Agent': random.choice(user_agents)
                        })

                        # Try to load the page with retries
                        await self._load_page_with_retry(page, url)

                        # Wait for job cards to be present
                        await page.wait_for_selector('[data-jk]', timeout=self.timeout)

                        # Extract job listings
                        job_cards = await page.query_selector_all('[data-jk]')

                        if not job_cards:
                            logger.warning(f"No job cards found on page {page_num + 1}")
                            continue

                        for card in job_cards:
                            try:
                                internship = await self._extract_indeed_job_data(card)
                                if internship:
                                    internships.append(internship)
                            except Exception as e:
                                logger.error(f"Error extracting job data: {str(e)}")
                                continue

                        logger.info(f"Scraped {len(job_cards)} job cards from page {page_num + 1}")

                    except Exception as e:
                        logger.error(f"Error scraping page {page_num + 1}: {str(e)}")
                        continue

            except Exception as e:
                logger.error(f"Error scraping Indeed: {str(e)}")
            finally:
                if browser:
                    await browser.close()

        return internships

    async def scrape_linkedin(self, keyword="internship", location="Coimbatore, Tamil Nadu", max_pages=2):
        """Scrape internships from LinkedIn with improved robustness"""
        internships = []
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]

        async with async_playwright() as p:
            browser = None
            try:
                browser = await p.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
                )
                page = await browser.new_page()

                for page_num in range(max_pages):
                    try:
                        start = page_num * 25
                        url = f"https://www.linkedin.com/jobs/search?keywords={keyword}&location={location}&start={start}"

                        logger.info(f"Scraping LinkedIn page {page_num + 1}: {url}")

                        # Randomly select a user agent
                        await page.set_extra_http_headers({
                            'User-Agent': random.choice(user_agents)
                        })

                        # Try to load the page with retries
                        await self._load_page_with_retry(page, url)

                        # Wait for job cards to be present
                        await page.wait_for_selector('.job-search-card', timeout=self.timeout)

                        # Extract job listings
                        job_cards = await page.query_selector_all('.job-search-card')

                        if not job_cards:
                            logger.warning(f"No job cards found on page {page_num + 1}")
                            continue

                        for card in job_cards:
                            try:
                                internship = await self._extract_linkedin_job_data(card)
                                if internship:
                                    internships.append(internship)
                            except Exception as e:
                                logger.error(f"Error extracting LinkedIn job data: {str(e)}")
                                continue

                        logger.info(f"Scraped {len(job_cards)} job cards from page {page_num + 1}")

                    except Exception as e:
                        logger.error(f"Error scraping LinkedIn page {page_num + 1}: {str(e)}")
                        continue

            except Exception as e:
                logger.error(f"Error scraping LinkedIn: {str(e)}")
            finally:
                if browser:
                    await browser.close()

        return internships

    async def scrape_naukri(self, keyword="internship", location="Coimbatore, Tamil Nadu", max_pages=2):
        """Scrape internships from Naukri.com with improved robustness"""
        internships = []
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]

        async with async_playwright() as p:
            browser = None
            try:
                browser = await p.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
                )
                page = await browser.new_page()

                for page_num in range(1, max_pages + 1):
                    try:
                        # URL encode the parameters
                        encoded_keyword = keyword.replace(' ', '%20')
                        encoded_location = location.replace(' ', '%20').replace(',', '%2C')
                        url = f"https://www.naukri.com/{encoded_keyword}-jobs-in-{encoded_location}-{page_num}"

                        logger.info(f"Scraping Naukri page {page_num}: {url}")

                        # Randomly select a user agent
                        await page.set_extra_http_headers({
                            'User-Agent': random.choice(user_agents)
                        })

                        # Try to load the page with retries
                        await self._load_page_with_retry(page, url)

                        # Wait for job cards to be present
                        await page.wait_for_selector('.jobTuple', timeout=self.timeout)

                        # Extract job listings
                        job_cards = await page.query_selector_all('.jobTuple')

                        if not job_cards:
                            logger.warning(f"No job cards found on page {page_num}")
                            continue

                        for card in job_cards[:10]:  # Limit to first 10 per page
                            try:
                                internship = await self._extract_naukri_job_data(card)
                                if internship:
                                    internships.append(internship)
                            except Exception as e:
                                logger.error(f"Error extracting Naukri job data: {str(e)}")
                                continue

                        logger.info(f"Scraped {len(job_cards)} job cards from page {page_num}")

                    except Exception as e:
                        logger.error(f"Error scraping Naukri page {page_num}: {str(e)}")
                        continue

            except Exception as e:
                logger.error(f"Error scraping Naukri: {str(e)}")
            finally:
                if browser:
                    await browser.close()

        return internships

    async def _load_page_with_retry(self, page, url):
        """Helper method to load a page with retries"""
        for attempt in range(self.max_retries):
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=self.timeout)
                await page.wait_for_timeout(self.retry_delay)
                return
            except PlaywrightTimeoutError as e:
                if attempt == self.max_retries - 1:
                    raise
                logger.warning(f"Timeout loading page (attempt {attempt + 1}): {e}")
                await page.wait_for_timeout(self.retry_delay * (attempt + 1))
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise
                logger.warning(f"Error loading page (attempt {attempt + 1}): {e}")
                await page.wait_for_timeout(self.retry_delay * (attempt + 1))

    async def _get_inner_text(self, element, selector):
        """Helper method to get inner text of an element with retries"""
        for attempt in range(self.max_retries):
            try:
                elem = await element.query_selector(selector)
                if elem:
                    return await elem.inner_text()
                return "N/A"
            except Exception as e:
                if attempt == self.max_retries - 1:
                    logger.error(f"Failed to get inner text after {self.max_retries} attempts: {e}")
                    return "N/A"
                await asyncio.sleep(0.5)

    async def _get_attribute(self, element, selector, attribute):
        """Helper method to get attribute of an element with retries"""
        for attempt in range(self.max_retries):
            try:
                elem = await element.query_selector(selector)
                if elem:
                    return await elem.get_attribute(attribute)
                return ""
            except Exception as e:
                if attempt == self.max_retries - 1:
                    logger.error(f"Failed to get attribute after {self.max_retries} attempts: {e}")
                    return ""
                await asyncio.sleep(0.5)

    async def _extract_indeed_job_data(self, card):
        """Extract job data from Indeed job card"""
        try:
            title = await self._get_inner_text(card, 'h2 a span')
            company = await self._get_inner_text(card, '[data-testid="company-name"]')
            location_text = await self._get_inner_text(card, '[data-testid="job-location"]')
            summary = await self._get_inner_text(card, '.slider_container .slider_item')
            link = await self._get_attribute(card, 'h2 a', 'href')

            if not title or title == "N/A":
                return None

            if link and not link.startswith('http'):
                link = f"https://www.indeed.com{link}"

            return {
                'title': self._clean_text(title),
                'company': self._clean_text(company),
                'location': self._clean_text(location_text),
                'summary': self._truncate_text(summary, 200),
                'link': link,
                'source': 'Indeed',
                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            logger.error(f"Error extracting Indeed job data: {str(e)}")
            return None

    async def _extract_linkedin_job_data(self, card):
        """Extract job data from LinkedIn job card"""
        try:
            title = await self._get_inner_text(card, '.base-search-card__title')
            company = await self._get_inner_text(card, '.base-search-card__subtitle')
            location_text = await self._get_inner_text(card, '.job-search-card__location')
            link = await self._get_attribute(card, '.base-card__full-link', 'href')

            if not title or title == "N/A":
                return None

            return {
                'title': self._clean_text(title),
                'company': self._clean_text(company),
                'location': self._clean_text(location_text),
                'summary': "Click to view details on LinkedIn",
                'link': link,
                'source': 'LinkedIn',
                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            logger.error(f"Error extracting LinkedIn job data: {str(e)}")
            return None

    async def _extract_naukri_job_data(self, card):
        """Extract job data from Naukri job card"""
        try:
            title = await self._get_inner_text(card, '.title')
            company = await self._get_inner_text(card, '.comp-name')
            location_text = await self._get_inner_text(card, '.locWdth')
            summary = await self._get_inner_text(card, '.job-desc')
            link = await self._get_attribute(card, '.title', 'href')

            if not title or title == "N/A":
                return None

            if link and not link.startswith('http'):
                link = f"https://www.naukri.com{link}"

            return {
                'title': self._clean_text(title),
                'company': self._clean_text(company),
                'location': self._clean_text(location_text),
                'summary': self._truncate_text(summary, 200),
                'link': link,
                'source': 'Naukri',
                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            logger.error(f"Error extracting Naukri job data: {str(e)}")
            return None

    def _clean_text(self, text):
        """Helper method to clean text"""
        if not text:
            return "N/A"
        return text.strip()

    def _truncate_text(self, text, length):
        """Helper method to truncate text"""
        clean_text = self._clean_text(text)
        return f"{clean_text[:length]}..." if len(clean_text) > length else clean_text

# Initialize scraper
scraper = InternshipScraper()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
async def scrape_internships():
    try:
        data = request.get_json()
        keyword = data.get('keyword', 'internship')
        location = data.get('location', 'Coimbatore, Tamil Nadu')
        sources = data.get('sources', ['indeed'])
        max_pages = min(int(data.get('max_pages', 2)), 5)  # Limit to 5 pages max

        all_internships = []

        if 'indeed' in sources:
            try:
                indeed_results = await scraper.scrape_indeed(keyword, location, max_pages)
                all_internships.extend(indeed_results)
                logger.info(f"Indeed scraped: {len(indeed_results)} jobs")
            except Exception as e:
                logger.error(f"Indeed scraping failed: {e}")

        if 'linkedin' in sources:
            try:
                linkedin_results = await scraper.scrape_linkedin(keyword, location, max_pages)
                all_internships.extend(linkedin_results)
                logger.info(f"LinkedIn scraped: {len(linkedin_results)} jobs")
            except Exception as e:
                logger.error(f"LinkedIn scraping failed: {e}")

        if 'naukri' in sources:
            try:
                naukri_results = await scraper.scrape_naukri(keyword, location, max_pages)
                all_internships.extend(naukri_results)
                logger.info(f"Naukri scraped: {len(naukri_results)} jobs")
            except Exception as e:
                logger.error(f"Naukri scraping failed: {e}")

        return jsonify({
            'success': True,
            'internships': all_internships,
            'count': len(all_internships)
        })

    except Exception as e:
        logger.error(f"Error in scrape_internships: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
