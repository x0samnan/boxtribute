/* eslint-disable no-console */
import { gql, useMutation } from "@apollo/client";
import { SHIPMENT_FIELDS_FRAGMENT } from "queries/fragments";
import { useCallback, useState } from "react";
import {
  AssignBoxToShipmentMutation,
  AssignBoxToShipmentMutationVariables,
  BoxState,
} from "types/generated/graphql";
import { IBoxBasicFields } from "types/graphql-local-only";
import { useErrorHandling } from "./useErrorHandling";

export enum IAssignBoxToShipmentResultKind {
  SUCCESS = "success",
  FAIL = "fail",
  NETWORK_FAIL = "networkFail", // ERROR
  NOT_AUTHORIZED = "notAuthorized", // FORBIDDEN
  WRONG_SHIPMENT_STATE = "wrongShipmentState", // BAD_USER_INPUT
  BOX_FAIL = "BoxFail", // detail does not include box
}

export interface IAssignBoxToShipmentResult {
  kind: IAssignBoxToShipmentResultKind;
  requestedBoxes: IBoxBasicFields[];
  assignedBoxes?: IBoxBasicFields[];
  failedBoxes?: IBoxBasicFields[];
  error?: any;
}

export const ASSIGN_BOX_TO_SHIPMENT = gql`
  ${SHIPMENT_FIELDS_FRAGMENT}
  mutation AssignBoxToShipment($id: ID!, $labelIdentifiers: [String!]) {
    updateShipmentWhenPreparing(
      updateInput: {
        id: $id
        preparedBoxLabelIdentifiers: $labelIdentifiers
        removedBoxLabelIdentifiers: []
      }
    ) {
      ...ShipmentFields
    }
  }
`;

export const useAssignBoxesToShipment = () => {
  const { triggerError } = useErrorHandling();
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const [assignBoxesToShipmentMutation] = useMutation<
    AssignBoxToShipmentMutation,
    AssignBoxToShipmentMutationVariables
  >(ASSIGN_BOX_TO_SHIPMENT);

  const assignBoxesToShipment = useCallback(
    (shipmentId: string, boxes: IBoxBasicFields[]) => {
      setIsLoading(true);
      const inStockLabelIdentifiers = boxes
        .filter((box) => box.state === BoxState.InStock)
        .map((box) => box.labelIdentifier);
      assignBoxesToShipmentMutation({
        variables: {
          id: shipmentId,
          labelIdentifiers: inStockLabelIdentifiers,
        },
      })
        .then(({ data, errors }) => {
          setIsLoading(false);
          if ((errors?.length || 0) > 0) {
            const errorCode = errors ? errors[0].extensions.code : undefined;
            // Example: the user is not of the sending base
            if (errorCode === "FORBIDDEN") {
              triggerError({
                message: "You don't have the permissions to assign boxes to this shipment.",
              });
              return {
                kind: IAssignBoxToShipmentResultKind.NOT_AUTHORIZED,
                requestedBoxes: boxes,
                error: errors ? errors[0] : undefined,
              } as IAssignBoxToShipmentResult;
            }
            // The shipment is not in the preparing state
            if (errorCode === "BAD_USER_INPUT") {
              triggerError({
                message: "The shipment is not in the Preparing state.",
              });
              return {
                kind: IAssignBoxToShipmentResultKind.WRONG_SHIPMENT_STATE,
                requestedBoxes: boxes,
                error: errors ? errors[0] : undefined,
              } as IAssignBoxToShipmentResult;
            }
            triggerError({
              message: "Could not assign boxes to shipment. Try again?",
            });
            // General error
            return {
              kind: IAssignBoxToShipmentResultKind.FAIL,
              requestedBoxes: boxes,
              error: errors ? errors[0] : undefined,
            } as IAssignBoxToShipmentResult;
          }
          const boxesInShipment: IBoxBasicFields[] =
            data?.updateShipmentWhenPreparing?.details.map((detail) => detail.box) ?? [];
          const failedBoxes: IBoxBasicFields[] = boxes.filter(
            (box) =>
              !boxesInShipment.some(
                (boxInShipment) => boxInShipment.labelIdentifier === box.labelIdentifier,
              ),
          );
          const assignedBoxes: IBoxBasicFields[] = boxes.filter((box) =>
            boxesInShipment.find(
              (boxInShipment) => boxInShipment.labelIdentifier === box.labelIdentifier,
            ),
          );
          // Not all Boxes were assigned
          if (failedBoxes.length) {
            return {
              kind: IAssignBoxToShipmentResultKind.BOX_FAIL,
              requestedBoxes: boxes,
              assignedBoxes,
              failedBoxes,
            } as IAssignBoxToShipmentResult;
          }
          // all Boxes were assigned
          return {
            kind: IAssignBoxToShipmentResultKind.SUCCESS,
            requestedBoxes: boxes,
            error: errors ? errors[0] : undefined,
          } as IAssignBoxToShipmentResult;
        })
        .catch(
          // Network error
          (err) => {
            setIsLoading(false);
            triggerError({
              message: "Could not assign boxes to shipment. Try again?",
            });
            return {
              kind: IAssignBoxToShipmentResultKind.NETWORK_FAIL,
              requestedBoxes: boxes,
              error: err,
            } as IAssignBoxToShipmentResult;
          },
        );
    },
    [assignBoxesToShipmentMutation, triggerError],
  );

  return {
    assignBoxesToShipment,
    isLoading,
  };
};
