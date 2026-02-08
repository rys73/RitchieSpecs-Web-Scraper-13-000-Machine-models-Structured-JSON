# RitchieSpecs Web Scraper – 13,000+ Structured Machine Models

## Project Overview
This project demonstrates a **large-scale web scraping pipeline** capable of extracting **13,000+ machine models** from [RitchieSpecs](https://www.ritchiespecs.com).

Each model is stored in **structured JSON** with multiple fields (manufacturer, machine type, model name, etc.), making it ready for **analysis, reporting, or integration into other systems**.
---

## Technologies Used
- **Python 3**
- **Playwright (Async)** – dynamic scraping of thousands of pages
- **JSON** – structured output
- **Logging** – progress tracking and error handling
- **Async programming** – efficient, large-scale scraping
---

## Scraping Workflow
1. Navigate all manufacturers
2. Filter out non-relevant machine types (like "All xxx equipment")
3. Access each machine type page to extract all models
4. Store each model as a structured JSON object (5+ fields)
5. Handle slow-loading pages and errors gracefully
📁 Output: `ritchiespecs.json` (~13,000 models)
---

## Project Value
- Shows capability to **handle large, structured datasets**
- **End-to-end scraping pipeline**
- Ready for **data analysis, machine learning, or reporting**
- Demonstrates efficiency and reliability in **high-volume web scraping projects**
---

## How to Run
```bash
pip install playwright
playwright install
python ritchiespecs_scraper.py
