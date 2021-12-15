from ariadne import EnumType

from ..enums import (
    BoxState,
    HumanGender,
    Language,
    ProductGender,
    TransferAgreementState,
    TransferAgreementType,
)

enum_types = [
    EnumType("ProductGender", ProductGender),
    EnumType("BoxState", BoxState),
    EnumType("HumanGender", HumanGender),
    EnumType("Language", Language),
    EnumType("TransferAgreementState", TransferAgreementState),
    EnumType("TransferAgreementType", TransferAgreementType),
]
