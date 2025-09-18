### CourtSight Crawler — MA Criminal Case Scraper (Comprehensive)

This project is a Scrapy-based web crawler to collect Indonesian Supreme Court (Mahkamah Agung) criminal case decisions from the official Decision Directory website. Crawled data can be stored in a local database via utilities in the `db` directory and optionally orchestrated with Airflow using `docker-compose`.

### Key Features
- **Scrapy spiders** for criminal case listing and detail pages (`pidana/spiders`).
- **Database persistence** via `db/util.py` (SQLite/other engines depending on your configuration).
- **Ready-to-use database schema** in `db/schema.sql` for initial setup.
- **Optional Airflow integration** for scheduling crawls.
- **Docker Compose support** to spin up supporting services quickly.

### Prerequisites
- Python 3.10 (using a virtual environment is recommended)
- Recent `pip`
- Git (optional)
- Docker & Docker Compose (optional, for Airflow/orchestration)

### Project Structure (brief)
```text
courtsight-crawler/
  airflow/
    dags/
    plugins/
  db/
    schema.sql
    util.py
  pidana/
    pidana/
      items.py
      pipelines.py
      settings.py
      spiders/
        list_pidana.py
        details.py
        pidana.py
    scrapy.cfg
  docker-compose.yaml
  README.md
  requirements.txt
```

### Installation and Environment Setup

1) Clone or download this repository.

2) Create and activate a virtual environment:

Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux/macOS (bash/zsh):
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3) Install dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Note: If you prefer using the pre-existing `venv/` inside this project, you can activate it directly. However, creating a fresh environment is recommended to avoid conflicts.

### Database Configuration

- Initial schema is provided in `db/schema.sql`.
- Connection utilities and helpers reside in `db/util.py`.

Initialize schema (example for SQLite):
```bash
sqlite3 courtsight.db < db/schema.sql
```

If you rely on `db/util.py` helpers to ensure tables exist, run the relevant module or initialization functions (inspect the file to see what is exposed). For other databases (PostgreSQL/MySQL), adjust the connection string and apply the schema accordingly.

### Running Scrapy Spiders

Activate your virtual environment, then from the project root run one of the following:

- List/index criminal decisions:
```bash
scrapy -s LOG_LEVEL=INFO -c list -a start_page=1 -a end_page=5 -a category="pidana-umum" -a save_to_db=true -a throttle=true -a delay=1.0 -a concurrent=8 -a retries=3 crawl pidana
```

- Decision details (use links gathered from the listing or specific args if supported):
```bash
scrapy -s LOG_LEVEL=INFO -c details -a url_file=links.csv -a save_to_db=true crawl pidana
```

- Dedicated `list_pidana` spider:
```bash
scrapy crawl list_pidana -s LOG_LEVEL=INFO
```

- Dedicated `details` spider:
```bash
scrapy crawl details -s LOG_LEVEL=INFO
```

Important notes:
- The `-c` (command) parameter only applies if the spider implements command-specific logic. Otherwise, use the spider name directly (e.g., `scrapy crawl pidana`) and pass `-a` as implemented.
- Inspect `pidana/pidana/spiders/*.py` to see supported arguments (e.g., `start_page`, `end_page`, `save_to_db`, etc.).

### Output and Data Persistence

- The pipeline in `pidana/pidana/pipelines.py` handles item persistence. When `save_to_db=true`, items are stored through `db/util.py`.
- You can also export results to files (JSON/CSV) via Scrapy options, e.g.:
```bash
scrapy crawl list_pidana -O output.json
```

### Running with Docker Compose (optional)

If you want to run supporting services (e.g., Airflow) via Docker Compose:
```bash
docker compose up -d
```

The command above will start services defined in `docker-compose.yaml`. Ensure Docker is running and your user has proper privileges.

### Orchestration with Airflow (optional)

- DAGs are under `airflow/dags` and plugins under `airflow/plugins`.
- After `docker compose up -d`, access the Airflow UI in your browser (see port mapping in `docker-compose.yaml`, typically `http://localhost:8080`).
- Configure required connections/variables (e.g., database URI, spider parameters).
- Enable the scraping DAG and run on schedule or trigger manually.

### Important Scrapy Configuration

See `pidana/pidana/settings.py` for options like:
- `DOWNLOAD_DELAY`, `CONCURRENT_REQUESTS`, `RETRY_TIMES`
- Middlewares: `pidana/pidana/middlewares.py`
- Items/Fields: `pidana/pidana/items.py`

Use the CLI parameter `-s KEY=VALUE` for quick overrides, e.g.:
```bash
scrapy crawl list_pidana -s DOWNLOAD_DELAY=1.0 -s CONCURRENT_REQUESTS=8
```

### Official Data Source

MA Decision Directory: `https://putusan3.mahkamahagung.go.id/direktori/index/kategori/pidana-umum-1.html`

Please respect robots.txt, terms of use, and reasonable rate limits. Use throttling/delay options to avoid putting excessive load on the server.

### Troubleshooting
- Ensure your virtualenv is active before running `scrapy`.
- If modules are not found, run commands from the project root or set the correct `PYTHONPATH`.
- If DB connection fails, verify credentials/URI in `db/util.py` or your environment variables.
- On Windows PowerShell, use `python` and `pip` from the virtualenv (`.\.venv\Scripts\Activate.ps1`).

### License and Contributions
- Use responsibly for research/analysis purposes.
- Contributions are welcome via pull requests. Please include a clear description of your changes.