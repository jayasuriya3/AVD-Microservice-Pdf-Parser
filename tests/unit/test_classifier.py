from decimal import Decimal

from app.classifier.cams_rules import CAMSRules
from app.classifier.kfintech_rules import KFintechRules
from app.classifier.ml_classifier import MLProviderClassifier
from app.classifier.provider_classifier import ProviderClassifier
from app.models.document import ExtractedDocument, ExtractedPage
from app.models.enums import Provider


def test_classifier_uses_weighted_cams_signals() -> None:
    document = ExtractedDocument(pages=[ExtractedPage(page_number=1, raw_text="CAMS Consolidated Account Statement")])
    detection = ProviderClassifier([CAMSRules(), KFintechRules()]).classify(document)
    assert detection.name == Provider.CAMS
    assert detection.confidence == Decimal("0.8")


def test_classifier_rejects_unknown_text() -> None:
    document = ExtractedDocument(pages=[ExtractedPage(page_number=1, raw_text="Unrelated document")])
    assert ProviderClassifier([CAMSRules(), KFintechRules()]).classify(document).name == Provider.UNKNOWN


def test_ml_classifier_falls_back_to_rule_based_detection_when_sklearn_missing() -> None:
    document = ExtractedDocument(pages=[ExtractedPage(page_number=1, raw_text="CAMS Consolidated Account Statement")])
    detection = MLProviderClassifier([CAMSRules(), KFintechRules()]).classify(document)
    assert detection.name == Provider.CAMS
    assert detection.confidence >= 0.5
