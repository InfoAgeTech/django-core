# -*- coding: utf-8 -*-


# TODO: I no longer think I have a need for this since i'm using django's querysets
def paging(query_set, page=1, page_size=25, select_related=False):
    """
    Database helper that figures out paging logic for you.
    
    :param query_set: QuerySet
    :param page_size: if None, just the objects will be returned.  If a 
        page_size is explicitly defined, a Paginator object for all objects and 
        the current page will be returned.
    :param select_related: boolean indicator that will query for all existing 
        referenced objects on the queryset.
    :return: a tuple. First part is the list of instances returned.  If no 
        instances are found, this will be an empty list.  The second part is a 
        boolean indicating if there's more instances to retrieve.
    """
    if select_related:
        docs = query_set.skip((page - 1) * page_size).limit(page_size + 1).select_related(max_depth=1)

    has_more = query_set.count() > page * page_size

    return docs, has_more
