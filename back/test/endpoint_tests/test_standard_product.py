from datetime import date

from boxtribute_server.enums import ProductGender
from utils import assert_successful_request

today = date.today().isoformat()


def test_standard_product_query(read_only_client, default_standard_product):
    # Test case 8.1.41
    query = f"""query {{
                standardProduct(id: {default_standard_product['id']}) {{
                ... on StandardProduct {{
                    id
                    name
                    category {{ id }}
                    sizeRange {{ id }}
                    gender
                    version
                    addedBy {{ id }}
                    deprecatedBy {{ id }}
                    deprecatedOn
                }} }} }}"""
    product = assert_successful_request(read_only_client, query)
    assert product == {
        "id": str(default_standard_product["id"]),
        "name": default_standard_product["name"],
        "category": {"id": str(default_standard_product["category"])},
        "gender": ProductGender(default_standard_product["gender"]).name,
        "sizeRange": {"id": str(default_standard_product["size_range"])},
        "version": default_standard_product["version"],
        "addedBy": {"id": str(default_standard_product["added_by"])},
        "deprecatedBy": None,
        "deprecatedOn": None,
    }


def test_standard_products_query(read_only_client, standard_products):
    # Test case 8.1.40
    query = """query { standardProducts {
                ...on StandardProductPage { elements { name } } } }"""
    products = assert_successful_request(read_only_client, query)["elements"]
    assert products == [{"name": p["name"]} for p in standard_products]
