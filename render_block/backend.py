import os
import sys

import jinja2
from django.template import TemplateDoesNotExist, TemplateSyntaxError
from django_jinja import utils
from django_jinja.backend import Jinja2 as Jinja2Base
from django_jinja.backend import Template, get_exception_info


class TemplateWithPartial(Template):
    partial_name = ""

    def render(self, context=None, request=None):
        if self.partial_name:
            context = self.template.new_context(context)
            gen = self.template.blocks[self.partial_name](context)
            return "".join([s for s in gen])

        return super().render(context=context, request=request)


class Jinja2(Jinja2Base):
    def get_template(self, template_name):
        template_name, _, partial_name = template_name.partition("#")

        if not self.match_template(template_name):
            message = f"Template {template_name} does not exists"
            raise TemplateDoesNotExist(message)

        try:
            template = TemplateWithPartial(self.env.get_template(template_name), self)
            template.partial_name = partial_name
            return template
        except jinja2.TemplateNotFound as exc:
            # Unlike django's template engine, jinja2 doesn't like windows-style path separators.
            # But because django does, its docs encourage the usage of os.path.join().
            # Rather than insisting that our users switch to posixpath.join(), this try block
            # will attempt to retrieve the template path again with forward slashes on windows:
            if os.name == "nt" and "\\" in template_name:
                try:
                    return self.get_template(template_name.replace("\\", "/"))
                except jinja2.TemplateNotFound:
                    pass

            exc = TemplateDoesNotExist(exc.name, backend=self)

            utils.reraise(
                TemplateDoesNotExist,
                exc,
                sys.exc_info()[2],
            )
        except jinja2.TemplateSyntaxError as exc:
            new = TemplateSyntaxError(exc.args)
            new.template_debug = get_exception_info(exc)
            utils.reraise(TemplateSyntaxError, new, sys.exc_info()[2])
