# -*- coding: utf-8 -*-


class PagingViewMixin(object):

    page_num_default = 1
    page_size_default = 15
    page_num = None
    page_size = None

    def dispatch(self, *args, **kwargs):
        self.page_num, self.page_size = self.get_paging()
        return super(PagingViewMixin, self).dispatch(*args, **kwargs)

    def get_paging(self, page_num_default=page_num_default,
                   page_size_default=page_size_default):
        """Gets the paging values passed through the query string params.

            * "p" for "page number" and
            * "ps" for "page size".

        :returns: tuple with the page being the first part and the page size
            being the second part.
        """

        try:
            page_num = int(self.request.GET.get('p', page_num_default))

            if page_num < 1:
                page_num = page_num_default
        except:
            page_num = page_num_default

        try:
            page_size = int(self.request.GET.get('ps', page_size_default))

            if page_size < 1:
                page_size = page_size_default
        except:
            page_size = page_size_default

        return page_num, page_size
