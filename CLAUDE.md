# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development
```bash
# Install dependencies
uv sync

# Run linting
uv run ruff check .
uv run ruff format .

# Run type checking
uv run mypy .

# Run tests
uv run pytest

# Build the package
uv build
```

## Architecture

This is a Django/Jinja2 template backend extension that enables partial template rendering by appending `#block-name` to template names.

### Core Components

1. **`render_block/backend.py`** - Main implementation
   - `TemplateWithPartial`: Custom template class that overrides render() to extract and render specific Jinja2 blocks
   - `Jinja2`: Custom backend extending django-jinja that parses `template.jinja#block-name` syntax

### How It Works

When a template name like `example.jinja#test-partial` is requested:
1. The backend splits the template name at `#` 
2. Loads the full template file
3. Extracts and renders only the named block content
4. Returns the partial HTML without the surrounding template structure

This enables efficient partial template updates for HTMX and similar patterns without duplicating template code.