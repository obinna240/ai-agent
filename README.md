1. Run `pip install -r requirements.txt`
2. playright install chromium
3. uvicorn app.main:app --reload
4. Use small queries for tests
5. Avoid repeated queries, against sites-- implement delays and proxies across sites 

Next steps
- Implement redis cache and simple react UI
- Add proxy rotation and request throttling in cloud run
- Run scrapers as isolated services in cloud run
