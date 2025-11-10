from collections import namedtuple

UrlComponents = namedtuple(
    typename="UrlComponents",
    field_names=["scheme", "netloc", "path", "params", "query", "fragment"],
)
