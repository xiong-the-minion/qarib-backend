# Qarib Backend

A Django REST API backend for managing transcript data with automatic file import capabilities.

## Quick Start

```bash
python start.py
```

That's it! One command does everything.

## What the startup script does:

1. ✅ **Checks Python version** (requires 3.8+)
2. ✅ **Installs dependencies** from `requirements.txt`
3. ✅ **Runs database migrations** (creates tables)
4. ✅ **Imports transcript files** automatically (via migration)
5. ✅ **Starts the Django development server** on port 8000

## After Starting

Once the server starts, you can access:

- **Main API**: http://127.0.0.1:8000/api/
- **Admin Interface**: http://127.0.0.1:8000/admin/
- **API Documentation**: http://127.0.0.1:8000/api/docs/ (if available)

## Features

- **Automatic Transcript Import**: Transcript files from `public/assets/` are automatically imported when migrations run
- **Speaker Analysis**: Automatically extracts and analyzes speaker contributions
- **REST API**: Full REST API for transcript management
- **Admin Interface**: Django admin for easy data management
- **One-Command Setup**: Everything runs with a single `python start.py` command

## Project Structure

```
qarib-backend/
├── config/                 # Django project settings
├── transcript/             # Main app for transcript management
│   ├── management/commands/
│   │   └── import_transcripts.py  # Command to import transcript files
│   ├── migrations/         # Database migrations (includes auto-import)
│   ├── models.py          # Transcript, Speaker, Tag models
│   └── views.py           # API views
├── public/assets/         # Transcript files to be imported
├── start.py              # One-command startup script
└── requirements.txt      # Python dependencies
```

## Troubleshooting

### Python not found
- Make sure Python 3.8+ is installed
- On Windows, you might need to add Python to your PATH
- Try using `python3` instead of `python`

### Virtual Environment
- It's recommended to use a virtual environment
- Create one with: `python -m venv venv`
- Activate it: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Unix)

### Port already in use
- Stop the process using port 8000
- Or modify the script to use a different port

### Database issues
- Delete `db.sqlite3` and run `python start.py` to start fresh
- The script will automatically recreate the database and import transcripts

## Development

### Adding New Transcript Files
1. Place `.txt` files in the `public/assets/` directory
2. Run `python start.py` - the files will be automatically imported

### Manual Import
If you need to manually import transcripts:
```bash
python manage.py import_transcripts
```

### API Endpoints
- `GET /api/transcripts/` - List all transcripts
- `GET /api/transcripts/{id}/` - Get specific transcript