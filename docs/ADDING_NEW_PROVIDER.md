# Adding a Provider

1. Add a `Provider` enum value.
2. Implement weighted `ProviderRule` signals.
3. Add a provider package implementing `BaseCASParser`.
4. Register the parser in `app/api/dependencies.py`.
5. Add anonymized PDF fixtures and expected JSON.
6. Add classifier, parser, validation, and integration tests.
7. Document layout assumptions and confidence limits.

Do not add provider-specific logic to extraction or API modules.
