from rest_framework.filters import SearchFilter, OrderingFilter


class CustomFilter(SearchFilter, OrderingFilter):
    def filter_queryset(self, request, queryset, view):
        search = request.GET.get("search","").strip()
        ordering = self.get_ordering(request, queryset, view)
        if search:
            queryset = queryset.filter(created_by__email=search)
            return queryset
        if ordering:
            pre = ""
            if "-" in ordering[0]:
                ordering = ordering[0].replace("-","")
                pre = "-"
            queryset = queryset.order_by(f"{pre}{ordering[0]}")
        return super().filter_queryset(request, queryset, view)