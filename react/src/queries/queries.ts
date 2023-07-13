import { gql } from "@apollo/client";
import {
  SHIPMENT_FIELDS_FRAGMENT,
  BOX_FIELDS_FRAGMENT,
  PRODUCT_BASIC_FIELDS_FRAGMENT,
  TAG_FIELDS_FRAGMENT,
  DISTRO_EVENT_FIELDS_FRAGMENT,
  BOX_BASIC_FIELDS_FRAGMENT,
} from "./fragments";

export const BOX_DETAILS_BY_LABEL_IDENTIFIER_QUERY = gql`
  ${BOX_FIELDS_FRAGMENT}
  query BoxDetails($labelIdentifier: String!) {
    box(labelIdentifier: $labelIdentifier) {
      ...BoxFields
    }
  }
`;

export const GET_BOX_LABEL_IDENTIFIER_BY_QR_CODE = gql`
  ${BOX_BASIC_FIELDS_FRAGMENT}
  query GetBoxLabelIdentifierForQrCode($qrCode: String!) {
    qrCode(qrCode: $qrCode) {
      code
      box {
        ...BoxBasicFields
      }
    }
  }
`;

export const CHECK_IF_QR_EXISTS_IN_DB = gql`
  query CheckIfQrExistsInDb($qrCode: String!) {
    qrExists(qrCode: $qrCode)
  }
`;

export const ALL_SHIPMENTS_QUERY = gql`
  ${SHIPMENT_FIELDS_FRAGMENT}
  query Shipments {
    shipments {
      ...ShipmentFields
    }
  }
`;

export const BOX_BY_LABEL_IDENTIFIER_AND_ALL_SHIPMENTS_QUERY = gql`
  ${PRODUCT_BASIC_FIELDS_FRAGMENT}
  ${BOX_FIELDS_FRAGMENT}
  ${TAG_FIELDS_FRAGMENT}
  ${DISTRO_EVENT_FIELDS_FRAGMENT}
  ${SHIPMENT_FIELDS_FRAGMENT}
  query BoxByLabelIdentifier($labelIdentifier: String!) {
    box(labelIdentifier: $labelIdentifier) {
      ...BoxFields
      product {
        ...ProductBasicFields
      }
      tags {
        ...TagFields
      }
      distributionEvent {
        ...DistroEventFields
      }
      location {
        __typename
        id
        name
        ... on ClassicLocation {
          defaultBoxState
        }
        base {
          locations {
            id
            seq
            name
            ... on ClassicLocation {
              defaultBoxState
            }
          }
          distributionEventsBeforeReturnedFromDistributionState {
            id
            state
            distributionSpot {
              name
            }
            name
            plannedStartDateTime
            plannedEndDateTime
          }
        }
      }
    }
    shipments {
      ...ShipmentFields
    }
  }
`;
