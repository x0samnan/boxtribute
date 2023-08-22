from ariadne import QueryType

from .crud import (
    compute_beneficiary_demographics,
    compute_created_boxes,
    compute_top_products_checked_out,
)

query = QueryType()


@query.field("beneficiaryDemographics")
def resolve_beneficiary_demographics(*_, base_ids=None):
    return compute_beneficiary_demographics(base_ids)


@query.field("createdBoxes")
def resolve_created_boxes(*_, base_id=None):
    return compute_created_boxes(base_id)


@query.field("topProductsCheckedOut")
def resolve_top_products_checked_out(*_, base_id):
    return compute_top_products_checked_out(base_id)
