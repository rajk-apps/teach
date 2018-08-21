from django import template

register = template.Library()

@register.filter
def nested_list(nodes):
    if isinstance(nodes, list):
        yield {'start_nodes': True}
        for node in nodes:
            yield {'start_node': True}
            for i in nested_list(node):
                yield i
            yield {'end_node': True}
        yield {'end_nodes': True}
    else:
        yield {'data': nodes, 'is_data': True}