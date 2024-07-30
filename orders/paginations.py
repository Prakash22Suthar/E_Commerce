from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size" 

    def get_page_links(self):
        """create a list of multiple pages"""
        page_links = self.get_html_context()["page_links"]
        return [{"number": pl.number, "url": pl.url, "is_active": pl.is_active} for pl in page_links]


    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'current_page':self.page.number,
            'num_pages':self.page.paginator.num_pages,
            'page_links':self.get_page_links(),
            'start_index':self.page.start_index(),
            'end_index':self.page.end_index(),
            'count': self.page.paginator.count,
            'results': data
        })


