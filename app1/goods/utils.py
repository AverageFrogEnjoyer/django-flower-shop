from django.db.models import Q
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
    SearchHeadline,
)

from goods.models import Products


def q_search(query):
    vector = SearchVector("name", "description")
    query = SearchQuery(query)

    result = (
        Products.objects.annotate(rank=SearchRank(vector, query))
        .filter(rank__gt=0)
        .order_by("-rank")
    )

    result = result.annotate(
        headline=SearchHeadline(
            "name",
            query,
            start_sel='<span style="background-color: green;">',
            stop_sel="</span>",
        )
    )
    return result 