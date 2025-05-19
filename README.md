"# kavigai" 

App Folder Structure 

│
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   └── roadmap.py
│   ├── controllers/
│   │   └── roadmap_controller.py
│   ├── models/
│   │   ├── embedding_model.py
│   │   ├── vector_store.py
│   │   ├── web_search.py         ← 🔍 Search + URLs
│   │   └── web_scraper.py        ← 🧹 Scraper logic
│   └── templates/
│       └── roadmap_template.py
├── config.py
├── main.py
