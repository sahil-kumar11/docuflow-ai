class OrgScopedMixin:
    def get_queryset(self):
        queryset = super().get_queryset()

        org_id = self.kwargs["org_id"]

        return queryset.filter(
            organization_id=org_id
        )