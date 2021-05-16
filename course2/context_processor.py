from django.http import HttpRequest


def filter_query_context_processor(request: HttpRequest) -> dict:
    """

    :param request:
    :return:
    """
    return {'FILTER_QUERY': request.GET.get('q', '')}
