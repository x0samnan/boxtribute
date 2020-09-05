"""GraphQL type definitions"""
from ariadne import gql

type_defs = gql(
    """
    type Query {
        hello: String!
        allBases: [Base]
        orgBases(org_id: Int): [Base]
        base(id: String!): Base
        allUsers: [User]
        user(email: String): User
    }
    type Mutation {
        createBox(box_creation_input:CreateBoxInput):Box
    }
    type Base {
        id: Int
        name: String
        currencyname: String
        organisation_id: Int
    }
    type User{
        id: Int!
        organisation_id: Int
        name: String
        email: String!
        usergroups_id: Int
        valid_firstday: Date
        valid_lastday: Date
        base_id: [Int]
        lastlogin: Datetime
        lastaction: Datetime
    }
    type Box {
        id: Int
        box_id: String!
        product_id: String
        size_id: String
        items: String
        location_id: String
        comments: String
        qr_id: String
        created: String
        created_by: String
        box_state_id: String
    }

    input CreateBoxInput {
        box_id: Int #this is an output, but not an input
        product_id: Int! #this is a foreign key
        size_id: Int #this is a foreign key
        items: Int
        location_id: Int! #this is a foreign key
        comments: String!
        qr_barcode: String! #this will get looked up to turn into qr_id, which is a foreign key
        created: Datetime #this is an output, but not an input
        created_by: String #this is null in the table consistently
        box_state_id: Int  #this is an output, but not an input
    }

    scalar Datetime
    scalar Date
"""
)
