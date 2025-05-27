from rest_framework import pagination


class CommonPageNumberPagination(pagination.PageNumberPagination):
    page_size = 20
