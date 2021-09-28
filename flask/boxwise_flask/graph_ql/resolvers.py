"""GraphQL resolver functionality"""
from ariadne import (
    EnumType,
    MutationType,
    ObjectType,
    ScalarType,
    convert_kwargs_to_snake_case,
    gql,
    make_executable_schema,
    snake_case_fallback_resolvers,
)
from boxwise_flask.auth_helper import authorization_test
from boxwise_flask.graph_ql.mutation_defs import mutation_defs
from boxwise_flask.graph_ql.query_defs import query_defs
from boxwise_flask.graph_ql.type_defs import type_defs
from boxwise_flask.models.base import Base
from boxwise_flask.models.box import Box, create_box, update_box
from boxwise_flask.models.location import Location
from boxwise_flask.models.organisation import Organisation
from boxwise_flask.models.product import Product
from boxwise_flask.models.product_category import ProductCategory
from boxwise_flask.models.qr_code import QRCode
from boxwise_flask.models.size import Size
from boxwise_flask.models.user import User

from flask import g

query = ObjectType("Query")
box = ObjectType("Box")
location = ObjectType("Location")
organisation = ObjectType("Organisation")
product = ObjectType("Product")
product_category = ObjectType("ProductCategory")
qr_code = ObjectType("QrCode")
user = ObjectType("User")
mutation = MutationType()

datetime_scalar = ScalarType("Datetime")
date_scalar = ScalarType("Date")


@datetime_scalar.serializer
def serialize_datetime(value):
    return value.isoformat()


@date_scalar.serializer
def serialize_date(value):
    return value.isoformat()


@user.field("bases")
@query.field("bases")
def resolve_bases(_, info):
    return Base.select().where(Base.id.in_(g.user["base_ids"]))


@query.field("base")
def resolve_base(_, info, id):
    authorization_test("bases", base_id=id)
    return Base.get_by_id(id)


@query.field("users")
def resolve_users(_, info):
    return User.select()


@query.field("user")
def resolve_user(_, info, email):
    return User.get(User.email == email)


@query.field("qrExists")
@convert_kwargs_to_snake_case
def resolve_qr_exists(_, info, qr_code):
    try:
        QRCode.get_id_from_code(qr_code)
    except QRCode.DoesNotExist:
        return False
    return True


@query.field("qrCode")
@convert_kwargs_to_snake_case
def resolve_qr_code(_, info, qr_code):
    return QRCode.get(QRCode.code == qr_code)


@query.field("product")
def resolve_product(_, info, id):
    product = Product.get_by_id(id)
    authorization_test("bases", base_id=str(product.base.id))
    return product


@query.field("box")
@convert_kwargs_to_snake_case
def resolve_box(_, info, box_id):
    return Box.get(Box.box_label_identifier == box_id)


@query.field("location")
def resolve_location(_, info, id):
    location = Location.get_by_id(id)
    authorization_test("bases", base_id=str(location.base.id))
    return location


@query.field("organisation")
def resolve_organisation(_, info, id):
    authorization_test("organisation", organisation_id=id)
    return Organisation.get_by_id(id)


@query.field("productCategory")
def resolve_product_category(_, info, id):
    return ProductCategory.get_by_id(id)


@query.field("productCategories")
def resolve_product_categories(_, info):
    return ProductCategory.select()


@query.field("organisations")
def resolve_organisations(_, info):
    return Organisation.select()


@query.field("locations")
def resolve_locations(_, info):
    return Location.select()


@query.field("products")
def resolve_products(_, info):
    return Product.select()


@box.field("state")
@location.field("boxState")
def resolve_box_state(obj, info):
    # Instead of a BoxState instance return an integer for EnumType conversion
    return obj.box_state.id


@mutation.field("createBox")
@convert_kwargs_to_snake_case
def resolve_create_box(_, info, box_creation_input):
    user_id = User.get(User.email == g.user["email"]).id
    box_creation_input["created_by"] = user_id
    return create_box(box_creation_input)


@mutation.field("updateBox")
@convert_kwargs_to_snake_case
def resolve_update_box(_, info, box_update_input):
    user_id = User.get(User.email == g.user["email"]).id
    box_update_input["last_modified_by"] = user_id
    return update_box(box_update_input)


@location.field("boxes")
def resolve_location_boxes(location_obj, info):
    return Box.select().where(Box.location == location_obj.id)


@organisation.field("bases")
def resolve_organisation_bases(organisation_obj, info):
    return Base.select().where(Base.organisation_id == organisation_obj.id)


@product.field("gender")
def resolve_product_gender(obj, info):
    return obj.id


@product.field("sizes")
def resolve_product_sizes(product_id, info):
    product = Product.get_by_id(product_id)
    sizes = Size.select(Size.label).where(Size.seq == product.size_range.seq)
    return [size.label for size in sizes]


@product_category.field("products")
def resolve_product_category_products(product_category_obj, info):
    return Product.select().where(Product.category == product_category_obj.id)


@qr_code.field("box")
def resolve_qr_code_box(qr_code_obj, info):
    return Box.get(Box.qr_code == qr_code_obj.id)


@user.field("organisation")
def resolve_user_organisation(obj, info):
    return Organisation.get_by_id(g.user["organisation_id"])


# Translate GraphQL enum into id field of database table
product_gender_type_def = EnumType(
    "ProductGender",
    {
        "Women": 1,
        "UnisexAdult": 3,
    },
)
box_state_type_def = EnumType(
    "BoxState",
    {
        "InStock": 1,
    },
)


schema = make_executable_schema(
    gql(type_defs + query_defs + mutation_defs),
    [
        query,
        mutation,
        date_scalar,
        datetime_scalar,
        box,
        location,
        organisation,
        product,
        product_category,
        qr_code,
        user,
        product_gender_type_def,
        box_state_type_def,
    ],
    snake_case_fallback_resolvers,
)
