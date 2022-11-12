"""Utilities for handling authorization"""
import os

from flask import g

from .exceptions import Forbidden
from .models.definitions.base import Base
from .models.definitions.transfer_agreement import TransferAgreement

BASE_AGNOSTIC_RESOURCES = (
    "box_state",
    "category",
    "gender",
    "history",
    "language",
    "organisation",
    "qr",
    "size",
    "size_range",
    "tag_relation",
    "transaction",
    "unboxed_items_collection",  # temporary
    "user",
)


def authorize(*args, **kwargs):
    """Check whether the current user (default: `g.user`) is authorized to access the
    specified resource.
    The god user is authorized to access anything.
    This function is supposed to be used in resolver functions. It may raise a Forbidden
    exception which ariadne handles by extending the 'errors' field of the response.
    There are no HTTP 4xx status codes associated with the error since a GraphQL
    response is returned as 200 acc. to specification.
    """
    kwargs["ignore_missing_base_info"] = False
    return _authorize(*args, **kwargs)


def _authorize(
    current_user=None,
    *,
    user_id=None,
    organisation_id=None,
    organisation_ids=None,
    base_id=None,
    base_ids=None,
    permission=None,
    ignore_missing_base_info=False,
):
    """Function for internal use that acts like authorize() but allows for ignoring
    missing base information.
    """
    if current_user is None:
        current_user = g.user
    if current_user.is_god:
        return True

    authorized = False
    if permission is not None:
        resource = permission.split(":")[0]
        if (
            resource not in BASE_AGNOSTIC_RESOURCES
            and base_id is None
            and base_ids is None
            and not ignore_missing_base_info
        ):
            raise ValueError(f"Missing base_id for base-related resource '{resource}'.")

        try:
            # Look up base IDs for given permission. If the user does not have the
            # permission at all, the look-up will result in a KeyError.
            # It is not distinguished between base-related and base-agnostic permissions
            # when decoding the JWT (CurrentUser.from_jwt()), instead base IDs are
            # mapped to every permission.
            authzed_base_ids = current_user.authorized_base_ids(permission)
        except KeyError:
            # Permission not granted for user
            authzed_base_ids = []

        if authzed_base_ids:
            # Permission field exists and access for at least one base granted.
            # Enforce base-specific permission
            if base_id is not None:
                # User is authorized for specified base
                authorized = int(base_id) in authzed_base_ids
            elif base_ids is not None:
                # User is authorized for at least one of the specified bases
                authorized = any([int(b) in authzed_base_ids for b in base_ids])
            elif resource in BASE_AGNOSTIC_RESOURCES or ignore_missing_base_info:
                authorized = True

    elif organisation_id is not None:
        authorized = organisation_id == current_user.organisation_id
    elif organisation_ids is not None:
        authorized = current_user.organisation_id in organisation_ids
    elif user_id is not None:
        authorized = user_id == current_user.id
    else:
        raise ValueError("Missing argument.")

    if authorized:
        return authorized
    else:
        for value, resource in zip(
            [user_id, organisation_id, base_id, permission],
            ["user", "organisation", "base", "permission"],
        ):
            if value is not None:
                break
        raise Forbidden(resource, value, current_user.__dict__)


def authorized_bases_filter(model=Base, *, base_fk_field_name="base"):
    """Derive base filter condition for given resource model depending the current
    user's base-specific permissions. The resource model must have a FK field referring
    to the Base model named 'base_fk_field_name'.
    The lower-case model name must match the permission resource name.
    See also `auth.requires_auth()`.
    """
    if g.user.is_god:
        return True

    permission = f"{model.__name__.lower()}:read"
    _authorize(permission=permission, ignore_missing_base_info=True)
    base_ids = g.user.authorized_base_ids(permission)
    pattern = Base.id if model is Base else getattr(model, base_fk_field_name)
    return pattern << base_ids


def agreement_organisation_filter_condition():
    """Derive filter condition for accessing transfer agreements depending on the user's
    organisation. The god user may access any agreement.
    """
    if g.user.is_god:
        return True
    _authorize(permission="transfer_agreement:read", ignore_missing_base_info=True)
    return (TransferAgreement.source_organisation == g.user.organisation_id) | (
        TransferAgreement.target_organisation == g.user.organisation_id
    )


def authorize_for_organisation_bases():
    """This is an exceptional use for ignoring missing base info. It must be possible to
    read organisations' bases information for anyone. The resolvers for base fields
    (e.g. beneficiaries, products) are guarded with base-specific permission
    enforcement.
    """
    _authorize(permission="base:read", ignore_missing_base_info=True)


def check_beta_feature_access(payload, *, current_user=None):
    """Check whether the current user wants to execute a beta-feature mutation, and
    whether they have sufficient beta-feature scope to run it.
    """
    if os.getenv("CI") == "true" or os.getenv("ENVIRONMENT") == "development":
        # Skip check when running tests in CircleCI, or during local development
        return True

    current_user = current_user or g.user
    if current_user.is_god:
        return True

    if "mutation" not in payload:
        return True

    all_allowed_mutations = {
        0: [],
        1: ["createQrCode"],
    }
    allowed_mutations = all_allowed_mutations[current_user.beta_feature_scope]
    return any([m in payload for m in allowed_mutations])
