from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError

class DataPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 50

    allowed_page_sizes = [5, 10, 15, 20]

    def get_page_size(self, request):
        page_size = request.query_params.get(self.page_size_query_param)

        if page_size:
            try:
                page_size = int(page_size)
            except ValueError:
                raise ValidationError("page_size debe ser un número")

            if page_size not in self.allowed_page_sizes:
                raise ValidationError(
                    f"Solo se permiten estos valores: {self.allowed_page_sizes}"
                )

            return page_size

        return self.page_size