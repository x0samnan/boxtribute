import { InMemoryCache, makeVar } from "@apollo/client";
import { IScannedBoxesData } from "types/graphql-local-only";
import { GET_SCANNED_BOXES } from "./local-only";

export const cache = new InMemoryCache({
  typePolicies: {
    Box: {
      // Boxes should be normalized by labelIdentifier
      keyFields: ["labelIdentifier"],
    },
    QrCode: {
      // QR-Codes should be normalized by their hash
      keyFields: ["code"],
    },
  },
});

// initialize the query to return scanned Boxes in the cache
cache.writeQuery({
  query: GET_SCANNED_BOXES,
  data: {
    scannedBoxes: [],
  } as IScannedBoxesData,
});

// apollo reactive variable for BoxReconciliationOverlay
export interface IBoxReconciliationOverlayVar {
  isOpen: boolean;
  labelIdentifier: string | undefined;
  shipmentId: string | undefined;
}

export const boxReconciliationOverlayVar = makeVar<IBoxReconciliationOverlayVar>({
  isOpen: false,
  labelIdentifier: undefined,
  shipmentId: undefined,
});

// TODO: cache BoxReconciliation

// apollo reactive variable for QrReaderOverlay
export interface IQrReaderOverlayVar {
  isOpen: boolean;
  isMultiBox?: boolean;
  selectedShipmentId?: string;
}

export const qrReaderOverlayVar = makeVar<IQrReaderOverlayVar>({ isOpen: false });
