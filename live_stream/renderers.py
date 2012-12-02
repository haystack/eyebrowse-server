from django.template.loader import render_to_string

from common.pagination import paginator

def history_renderer(user, history, return_type, page=None):
    """ 
    Can render a history as html block or list of
    html items. User is the user requesting the view.
    """
    if return_type == "html":
        template_values =  {
            'history' : paginator(page, history),
            'user' : user,
        }

        return render_to_string('live_stream/timeline.html',template_values)

    elif return_type == "list":
        history_list = []
        for h_item in history:
           history_list.append(str(render_to_string('live_stream/history_item_template.html', 
                {
                    'history' : history,
                }))
            )

        return history_list