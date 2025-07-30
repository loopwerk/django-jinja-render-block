import pytest
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.test import RequestFactory


class TestBasicBlockRendering:
    """Test basic block rendering functionality."""

    def setup_method(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("/")

    def test_render_full_template_without_block_selector(self):
        """Test that rendering without # selector returns full template."""
        template = get_template("simple.jinja")
        result = template.render()

        assert "<html>" in result
        assert "<h1>Default Header</h1>" in result
        assert "<p>This is the main content block.</p>" in result
        assert "<footer>Default Footer</footer>" in result
        assert "</html>" in result

    def test_render_specific_block(self):
        """Test rendering a specific block using # selector."""
        template = get_template("simple.jinja#content")
        result = template.render()

        # Should only contain the content block
        assert "<p>This is the main content block.</p>" in result

        # Should not contain other parts
        assert "<html>" not in result
        assert "<h1>Default Header</h1>" not in result
        assert "<footer>Default Footer</footer>" not in result

    def test_render_block_with_context(self):
        """Test rendering blocks with context variables."""
        template = get_template("with_context.jinja#greeting")
        result = template.render({"name": "Alice"})

        assert "<h1>Hello Alice!</h1>" in result

    def test_render_block_with_loop(self):
        """Test rendering blocks containing loops."""
        template = get_template("with_context.jinja#loop_test")
        result = template.render({"items": ["apple", "banana", "orange"]})

        assert "<ul>" in result
        assert "<li>apple</li>" in result
        assert "<li>banana</li>" in result
        assert "<li>orange</li>" in result
        assert "</ul>" in result


class TestTemplateInheritance:
    """Test block rendering with template inheritance."""

    def test_render_inherited_block(self):
        """Test rendering a block that's overridden in child template."""
        template = get_template("child.jinja#title")
        result = template.render()

        # Should get the child's version, not the parent's
        assert "Child Title" in result
        assert "Base Title" not in result

    def test_render_nested_block_in_child(self):
        """Test rendering a nested block defined in child template."""
        template = get_template("child.jinja#nested_content")
        result = template.render()

        assert '<div class="nested">' in result
        assert "<p>This is nested content in child template.</p>" in result

    def test_render_entire_overridden_block(self):
        """Test rendering the entire body block from child."""
        template = get_template("child.jinja#body")
        result = template.render()

        assert "<h1>Child Page</h1>" in result
        assert '<div class="nested">' in result
        assert '<div class="another">' in result
        assert "<p>End of child body</p>" in result

        # Should not contain base template content
        assert "Base body content" not in result

    def test_render_block_only_in_child(self):
        """Test rendering a block that only exists in child template."""
        template = get_template("child.jinja#another_block")
        result = template.render()

        assert '<div class="another">' in result
        assert "<p>Another block in child template.</p>" in result


class TestErrorHandling:
    """Test error handling for invalid templates and blocks."""

    def test_nonexistent_template(self):
        """Test that requesting a non-existent template raises TemplateDoesNotExist."""
        with pytest.raises(TemplateDoesNotExist):
            get_template("nonexistent.jinja")

    def test_nonexistent_template_with_block(self):
        """Test that requesting a non-existent template with block raises TemplateDoesNotExist."""
        with pytest.raises(TemplateDoesNotExist):
            get_template("nonexistent.jinja#someblock")

    def test_nonexistent_block(self):
        """Test that requesting a non-existent block raises KeyError."""
        template = get_template("simple.jinja#nonexistent")

        # The error happens during render, not during template loading
        with pytest.raises(KeyError):
            template.render()

    def test_empty_block_name(self):
        """Test that empty block name renders full template."""
        # This should behave the same as not having a block selector
        template1 = get_template("simple.jinja#")
        template2 = get_template("simple.jinja")

        result1 = template1.render()
        result2 = template2.render()

        assert result1 == result2
