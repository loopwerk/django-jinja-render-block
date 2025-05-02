# django-jinja-render-block

[![pypi](https://img.shields.io/pypi/v/django-jinja-render-block.svg)](https://pypi.org/project/django-jinja-render-block/)

This project aims to bring the super ergomomic partial template rendering of [django-template-partials](https://github.com/carltongibson/django-template-partials) to [django-jinja](https://github.com/niwinz/django-jinja). It's a bit more limited in scope though: instead of allowing you to define reusable (inline) template partials using `{% partialdef partial-name %}`, it limits itself to rendering a block within a template, ala [django-render-block](https://github.com/clokep/django-render-block).

TL;DR: you can render just a block using a template name such as `template-name.jinja#block-name`.

## Installation

```shell
uv add django-jinja-render-block
```

Then use its template backend, instead of the one from django-ninja:

```python
TEMPLATES = [
    {
        "BACKEND": "render_block.backend.Jinja2", # <- instead of "django_jinja.jinja2.Jinja2"
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            # ...
        },
    },
]
```

## Usage

Define a block in your Jinja template:

```jinja
{% extends "base.jinja" %}

{% block body %}
<h1>HOME</h1>

{% block test-partial %}
<p>Partial block content</p>
{% endblock %}

<p>Lorum ipsum</p>
{% endblock %}
```

And in your view code you use the template name plus the partial block name, like so:

```python
# In view handler...
self.template_name = "example.jinja#test-partial"
```

This is extremely useful in combination with HTMX:

```python
def partial_rendering(request: HtmxHttpRequest) -> HttpResponse:
    template_name = "example.jinja"
    if request.htmx:
        template_name += "#test-partial"

    return TemplateResponse(request, template_name)
```

## Thanks to

- https://github.com/carltongibson/django-template-partials for the initial idea. I love the way it allows you to render a partial template just by appending the partial name to the template name. It only works with the Django Template Language though.
- https://github.com/clokep/django-render-block for showing me how to render a single block out of a template.
