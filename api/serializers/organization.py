from importlib.metadata import MetadataPathFinder
from rest_framework.serializers import ModelSerializer
from organization.models import Branch, Organization


class OrganizationSerializer(ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            "id",
            "org_name",
            "org_logo",
            "tax_number",
            "website",
            "company_contact_number",
            "company_contact_email",
            "contact_person_number",
            "company_address",
            "company_bank_qr",
            "current_fiscal_year"
        ]


class BranchSerializer(ModelSerializer):
    class Meta:
        model = Branch
        fields = [
            "id",
            "name",
            "address",
            "contact_number",
            "branch_manager",
            "organization",
            "branch_code",
        ]
