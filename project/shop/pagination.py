from rest_framework.pagination import PageNumberPagination


class StandartResultSetPagination(PageNumberPagination):
    page_size = 5
    page_zise_query_param = 'page'
    max_page_size = 5
