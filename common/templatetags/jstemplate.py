from django import template
from django.template.loader_tags import do_include
import re

register = template.Library()


class JsTemplateBaseNode(template.Node):

    LEFT_PATTERN = re.compile(r'{!')
    RIGHT_PATTERN = re.compile(r'!}')

    LEFT_TARGET = '{{'
    RIGHT_TARGET = '}}'

    def __init__(self, inner_node):
        """
        Instantiated with a inner_node as an argument
        This node comes from the from the do_include function
        """
        self.inner_node = inner_node

        # attempting to get the tmplate name
        # depends whether it is an IncludeNode or ConstantIncludeNode
        try:
            self.template_name = inner_node.template_name
        except AttributeError:
            self.template_name = inner_node.template.name

    def top(self):
        """
        for subclasses - what comes before the rendered meta templates
        defaults to ''
        """
        return ''

    def bottom(self):
        """
        for subclasses - what comes after the rendered meta template
        defaults = ''
        """
        return ''

    def render(self, context):
        """
        renders the inner node (the included template)
        then replaces the js delimiters with the actual delimiters

        then returns top() + js_template + bottom()!
        """
        js_template = self.inner_node.render(context)
        left_replaced_js_template = self.LEFT_PATTERN.sub(
            self.LEFT_TARGET, js_template)
        left_right_replaced_js_template = self.RIGHT_PATTERN.sub(
            self.RIGHT_TARGET, left_replaced_js_template)

        return "%s\n%s\n%s" % (
            self.top(),
            left_right_replaced_js_template,
            self.bottom(),
        )


class IchTemplateNode(JsTemplateBaseNode):

    """
    implements the wrapper for icanhaz
    """

    def top(self):
        return "<script type='text/html' id='%s'>" % self.template_name

    def bottom(self):
        return "</script>"

#########
# registering stuff

register_hash = {
    'basejstemplate': JsTemplateBaseNode,
    'ichtemplate': IchTemplateNode,
}

TAG_NAME_TEMPLATE = "include_%s"


def compilation_function_factory(node_klass):
    """
    returns a compilation function that
    will use the builtin do_include to generate
    a node containing the rendered meta template,
    then pass it to the constuctor of the given
    node_klass to be wrapped somehow.
    """
    def compilation_function(parser, token):
        returned_node = do_include(parser, token)
        return node_klass(returned_node)

    return compilation_function


for tag_type, node_klass in register_hash.items():
    tag_name = TAG_NAME_TEMPLATE % tag_type
    compilation_function = compilation_function_factory(node_klass)
    register.tag(tag_name, compilation_function)
