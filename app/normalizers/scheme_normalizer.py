from app.services.scheme_resolver import SchemeResolver


class SchemeNormalizer:
    def __init__(self, resolver: SchemeResolver) -> None:
        self.resolver = resolver
