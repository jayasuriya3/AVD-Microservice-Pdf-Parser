from collections.abc import Sequence
from decimal import Decimal

from app.classifier.base import ProviderRule
from app.classifier.provider_classifier import ProviderClassifier
from app.models.document import ExtractedDocument
from app.models.enums import Provider
from app.models.statement import ProviderDetection


class MLProviderClassifier(ProviderClassifier):
    """Optional ML-backed classifier that keeps the rule engine as safe fallback."""

    def __init__(self, rules: Sequence[ProviderRule], minimum_confidence: float = 0.5) -> None:
        super().__init__(list(rules), minimum_confidence=minimum_confidence)

    def classify(self, document: ExtractedDocument) -> ProviderDetection:
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.linear_model import LogisticRegression
        except ImportError:
            return super().classify(document)

        text = document.text.strip()
        if not text:
            return super().classify(document)

        labels = [Provider.CAMS.value, Provider.KFINTECH.value]
        training_text = [
            "CAMS Consolidated Account Statement registrar and transfer agent",
            "KFintech Consolidated Account Statement registrar and transfer agent",
        ]

        vectorizer = TfidfVectorizer(lowercase=True, ngram_range=(1, 2))
        X = vectorizer.fit_transform(training_text)
        model = LogisticRegression(max_iter=1000)
        model.fit(X, labels)

        features = vectorizer.transform([text])
        predicted = model.predict(features)[0]
        probability = float(model.predict_proba(features).max())

        if probability < self.minimum_confidence:
            return super().classify(document)

        if predicted == Provider.CAMS.value:
            return ProviderDetection(
                name=Provider.CAMS,
                confidence=Decimal(str(probability)),
                signals=["ml_provider_prediction"],
            )

        return ProviderDetection(
            name=Provider.KFINTECH,
            confidence=Decimal(str(probability)),
            signals=["ml_provider_prediction"],
        )
