# Bluesky Posts Export Tool

Export public Bluesky posts to clean JSON format. No authentication required.

## Quick Start

```bash
git clone https://github.com/symmetricalboy/bsky-to-gem.git
cd bsky-to-gem

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate    # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Export posts
python export_posts.py your_handle.bsky.social
```

## Output

Creates timestamped JSON files: `{handle}_posts_YYYYMMDD_HHMMSS.json`

```json
[
  {
    "created_at": "2025-01-15T10:30:45.123Z",
    "text": "Your post content here...",
    "images": [
      {
        "url": "https://cdn.bsky.app/img/feed_fullsize/plain/...",
        "alt_text": "Description of the image"
      }
    ]
  }
]
```

## Creating AI Writing Style Models

1. Export your posts: `python export_posts.py your_handle.bsky.social`
2. Use the prompt template in `gemini_prompt_template.md` with your JSON export
3. Feed the result to Gemini Custom Gems for personalized AI writing

## Use Cases

- AI training data
- Personal backups
- Writing style analysis
- Custom AI personas
- Platform migration

## License

MIT - see [LICENSE](LICENSE) file.
