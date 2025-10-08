1. Run `pip install -r requirements.txt`

cd /Users/oco/Documents/ai-agent

# Activate the virtual environment
source venv/bin/activate

# Then run Playwright commands
playwright install chromium

We use a Chromium web driver to render the scrapped pages.

We will be testing out Selenium and playwright

`source venv/bin/activate && pip install selenium`



3. To start do --- `source venv/bin/activate && uvicorn app.main:app --reload`
4. Use small queries for tests
5. Avoid repeated queries, against sites-- implement delays and proxies across sites 

Next steps
- Implement redis cache and simple react UI
- Add proxy rotation and request throttling in cloud run
- Run scrapers as isolated services in cloud run


When restarting and if having port conflicts run: lsof -ti:8080 | xargs kill -9`
then `lsof -i:8000` to check if port 8080 is free.
