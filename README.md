# HackerNews API Test Suite

API test suite for the HackerNews Firebase API.

## Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv)

## Installing uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip
pip install uv
```

## Setup

From the project root directory:

```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv sync
```

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_top_stories.py

# Run by marker
pytest -m acceptance      # Core requirement tests
pytest -m edge_case       # Edge case tests
pytest -m security        # Security tests
pytest -m items           # Items API tests
pytest -m top_stories     # Top Stories API tests
```

## Project Structure

```
src/
  client.py         # Generic HTTP client
  top_stories.py    # Top Stories API wrapper
  items.py          # Items API wrapper

tests/
  conftest.py       # Pytest fixtures
  test_client.py    # Client/security tests
  test_items.py     # Items API tests
  test_top_stories.py  # Top Stories API tests
```

## Test Coverage

### Acceptance Tests (Core Requirements)
1. Retrieving top stories with the Top Stories API
2. Using Top Stories API to retrieve the current top story from Items API
3. Using Top Stories API to retrieve a top story's first comment

### Edge Case Tests
- Invalid item IDs (0, negative, non-existent, text)
- Deleted comments
- Nested comments
- Text stories (Ask HN, Show HN)
- Max 500 top stories

### Security Tests
- HTTP connections rejected (HTTPS only)
- Invalid endpoints return 401
- Empty item ID returns 401

## Test Markers

| Marker | Description |
|--------|-------------|
| `acceptance` | Core requirement tests |
| `edge_case` | Edge case tests |
| `security` | Security tests |
| `items` | Items API tests |
| `top_stories` | Top Stories API tests |
| `story` | Story-related tests |
| `comment` | Comment-related tests |
