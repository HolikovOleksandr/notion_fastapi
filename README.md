# Just trying Notion like database

This project is a lightweight implementation of a Notion-like database system, designed to manage and organize data efficiently. It provides a simple API for creating, reading, updating, and deleting records.

## 1. Installation

```
git clone https://github.com/HolikovOleksandr/notion_fastapi.git
```
```
cd notion_fastapi
```
```
py -m venv .venv
```

Unix
```
source .venv/bin/activate
touch .env
```

Windows
```
.venv\Scripts\activate
echo. > .env
```

```
pip install -r requirements.txt
```

Set `NOTION_TOKEN` and `NOTION_DB_ID` in `.env` file
[YouTube tutorial link](https://www.youtube.com/watch?v=7mo4XrjRFv0&t=187s&ab_channel=Whalesync)

Start FastApi server
```
uvicorn app.main:app --reload
```