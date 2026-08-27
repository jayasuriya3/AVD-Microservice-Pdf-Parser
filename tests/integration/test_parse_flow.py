from decimal import Decimal

from app.classifier.cams_rules import CAMSRules
from app.classifier.provider_classifier import ProviderClassifier
from app.models.document import ExtractedDocument, ExtractedPage
from app.models.enums import Provider


def test_cams_provider_flow_without_fixture_parser_claim() -> None:
    document = ExtractedDocument(pages=[ExtractedPage(page_number=1, raw_text="CAMS Consolidated Account Statement")])
    detection = ProviderClassifier([CAMSRules()]).classify(document)
    assert detection.name == Provider.CAMS
    assert detection.confidence == Decimal("0.8")
