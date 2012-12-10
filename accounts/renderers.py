from django.template.loader import render_to_string

from common.pagination import paginator

def connection_table_renderer(connections, type, following):
    """
        Returns a rendered string of a following or followers table.
    """
    rendered_connections = connection_row_renderer(connections, type, following)
    template_values =  {
        'type' : type,
        'connections' : rendered_connections,
    }

    return render_to_string('accounts/connection_table.html',template_values)

def connection_row_renderer(connections, type, following):
    rows = []
    for connection in connections:
        follows = connection in following
        template_values = {
            'user' : connection.user,
            'follows' : str(follows)
        }
        rows.append(render_to_string('accounts/connection_row.html', template_values))
    return rows