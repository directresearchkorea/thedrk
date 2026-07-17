# Recruitment Lead‑Generation Crawler

## Overview
This project automatically gathers information about Korean and Japanese restaurants in Seoul that have a high delivery share or operate 24 hours. The collected data is saved as **restaurants.csv** and can be visualized with a premium HTML dashboard (separate project).

## Folder Structure
```
recruitment_crawler/
│   PRD.md                 # Project specification (this file)
│   requirements.txt        # Python dependencies
│   run_crawler.bat         # Windows batch script for setup & execution
│   README.md               # THIS document – usage guide
│
├───crawler/
│       main.py            # Core asynchronous crawler (Playwright)
│       keywords.json       # Category → sub‑category → keyword mapping
│
├───data/                  # Generated at runtime
│       raw_data.json       # Raw JSON output (debugging)
│       restaurants.csv     # Final deduplicated CSV (UTF‑8‑SIG)
│
└───logs/                  # Execution logs
        crawl.log          # Timestamped log file
```

## Prerequisites
- **OS**: Windows 10/11 (PowerShell or CMD)
- **Python**: 3.11+ (ensure `python` is on your PATH)
- **Internet**: Access to Naver and delivery‑app sites (no proxy blocks)
- **Disk permissions**: Write permission in this folder

## Quick Start (Windows)
1. Open a Command Prompt (or PowerShell) in this folder.
2. Run the batch script:
   ```bat
   run_crawler.bat
   ```
   This will:
   - Create a virtual environment (`venv`) if it does not exist
   - Activate the environment
   - Upgrade `pip` and install all dependencies from `requirements.txt`
   - Install Playwright Chromium binaries
   - Execute the crawler (`crawler/main.py`)
3. After completion you will find:
   - `data/raw_data.json` – raw JSON dump of every restaurant record
   - `data/restaurants.csv` – cleaned, deduplicated CSV ready for Excel/Sheets
   - `logs/crawl.log` – detailed log of the run

## Customising Keywords
Edit **crawler/keywords.json** to add or modify categories, sub‑categories, and the search keywords that drive the crawler. The JSON schema is:
```json
{
  "categories": [
    {
      "name": "CategoryName",
      "subcategories": [
        {
          "name": "SubCategoryName",
          "keywords": ["keyword1", "keyword2"]
        }
      ]
    }
  ]
}
```
The crawler will iterate over every keyword, appending the meta‑information (category, sub‑category, keyword) to each restaurant record.

## Logging
All actions are logged to **logs/crawl.log** with timestamps and log level. Errors are recorded as `ERROR:` lines, while progress information uses `INFO:`.

## Extending the Project
- **Add delivery‑app rating & review extraction** – modify `crawler/main.py` to include additional page parsing after the Naver step.
- **24 hour tag detection** – incorporate a secondary Playwright request to the delivery‑app detail page and look for the `24시간` text.
- **Dashboard UI** – create a separate static web app that loads `data/restaurants.csv` via `fetch()` and offers filter & CSV download functionality.

---
*Generated automatically from PRD specifications.*
