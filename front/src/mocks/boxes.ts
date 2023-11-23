import { BoxState } from "types/generated/graphql";
import { product1, productBasic1 } from "./products";
import { size1, size2 } from "./sizeRanges";
import { location1, generateMockLocationWithBase } from "./locations";
import { tag1, tag2 } from "./tags";
import { history1, history2 } from "./histories";

export const box123 = {
  labelIdentifier: "123",
  product: product1,
  size: size1,
  state: BoxState.InStock,
  shipmentDetail: null,
  numberOfItems: 62,
  location: location1,
  tags: [tag1],
  comment: "Test",
  __typename: "Box",
};

export const generateMockBox = ({
  labelIdentifier = "123",
  state = BoxState.InStock,
  numberOfItems = 31,
  location = generateMockLocationWithBase({}),
  comment = "Good Comment",
  product = productBasic1,
  shipmentDetail = null as any,
  size = size2,
  tags = [tag2],
  histories = [history1, history2],
}) => ({
  labelIdentifier,
  state,
  product,
  size,
  shipmentDetail,
  location,
  numberOfItems,
  tags,
  comment,
  history: histories,
  createdOn: "2023-11-09T17:24:29+00:00",
  distributionEvent: null,
  __typename: "Box",
});
