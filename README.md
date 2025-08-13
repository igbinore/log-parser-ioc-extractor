\# 🕵️‍♂️ Log Parser \& IOC Extractor



I built this to speed up the boring part of investigations: pulling IOCs out of messy logs.  

Upload a file (or paste text), extract indicators (IPs, domains, URLs, hashes, emails), filter by type, de-duplicate with counts, and export what you need.



---



\## 🚀 What it does

\- \*\*Upload or paste\*\* logs – handles plain text quickly.

\- \*\*Auto IOC detection\*\* – IPv4, domains, URLs, MD5/SHA1/SHA256, emails.

\- \*\*De-dup with counts\*\* – groups the same IOC and shows how often it appeared.

\- \*\*Filter by IOC type\*\* – focus on IPs, domains, hashes, etc.

\- \*\*Export\*\* – CSV, JSON, or a ZIP bundle (CSV + JSON).

\- \*\*Copy to clipboard\*\* – per row or copy all.



---



\## 📸 Screenshots



\*\*Full IOC Extraction View\*\*  

!\[Full IOC Extraction](screenshots/full\_ioc\_view.png)



\*\*Filtered by IOC Type (IPs only)\*\*  

!\[Filtered View - IPs](screenshots/filtered\_ips\_view.png)



)



---



\## ⚙️ Setup



```bash

git clone https://github.com/<your-username>/log-parser-ioc-extractor.git

cd log-parser-ioc-extractor



\# Virtual environment

python -m venv venv

venv\\Scripts\\activate   # Windows

\# source venv/bin/activate   # Mac/Linux



\# Install deps

pip install -r requirements.txt

▶️ Run

Backend (FastAPI)



bash

Copy

Edit

cd backend

python -m uvicorn app:app --reload --port 8001

Frontend

Open frontend/index.html in your browser.



🧱 Structure

pgsql

Copy

Edit

log-parser-ioc-extractor/

│   README.md

│   requirements.txt

│   .gitignore

│

├── backend/

│   └── app.py

│

├── frontend/

│   └── index.html

│

├── samples/

│   └── auth.log.txt

│

└── screenshots/

&nbsp;   ├── full\_ioc\_view.png

&nbsp;   ├── filtered\_ips\_view.png

&nbsp;   └── export\_csv\_view.png

🛠️ Stack

Backend: FastAPI (Python)



Frontend: Bootstrap 5, Vanilla JS



Parsing: Regex + Pandas



Exports: CSV / JSON / ZIP



💡 Why I built this

Manually scraping IOCs from logs wastes time during an incident. I wanted a small, clear tool I can run locally, share with teammates, and extend later (OTX/AbuseIPDB enrichment hooks are easy to drop in).



📜 License

MIT — feel free to use and modify.

