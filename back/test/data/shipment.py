import pytest
from boxtribute_server.enums import ShipmentState
from boxtribute_server.models.definitions.shipment import Shipment
from boxtribute_server.models.utils import utcnow

from .base import data as base_data
from .transfer_agreement import data as transfer_agreement_data
from .user import default_user_data

TIME = utcnow().replace(tzinfo=None)


def data():
    return [
        {
            "id": 1,
            "source_base": base_data()[0]["id"],
            "target_base": base_data()[2]["id"],
            "transfer_agreement": transfer_agreement_data()[0]["id"],
            "state": ShipmentState.Preparing,
            "started_by": default_user_data()["id"],
            "started_on": TIME,
            "canceled_by": None,
            "canceled_on": None,
            "sent_by": None,
            "sent_on": None,
            "receiving_started_by": None,
            "receiving_started_on": None,
        },
        {
            "id": 2,
            "source_base": base_data()[0]["id"],
            "target_base": base_data()[2]["id"],
            "transfer_agreement": transfer_agreement_data()[1]["id"],
            "state": ShipmentState.Canceled,
            "started_by": default_user_data()["id"],
            "started_on": TIME,
            "canceled_by": default_user_data()["id"],
            "canceled_on": TIME,
            "sent_by": None,
            "sent_on": None,
            "receiving_started_by": None,
            "receiving_started_on": None,
        },
        {
            "id": 3,
            "source_base": base_data()[2]["id"],
            "target_base": base_data()[0]["id"],
            "transfer_agreement": transfer_agreement_data()[3]["id"],
            "state": ShipmentState.Preparing,
            "started_by": default_user_data()["id"],
            "started_on": TIME,
            "canceled_by": None,
            "canceled_on": None,
            "sent_by": None,
            "sent_on": None,
            "receiving_started_by": None,
            "receiving_started_on": None,
        },
        {
            "id": 4,
            "source_base": base_data()[0]["id"],
            "target_base": base_data()[2]["id"],
            "transfer_agreement": transfer_agreement_data()[0]["id"],
            "state": ShipmentState.Sent,
            "started_by": default_user_data()["id"],
            "started_on": TIME,
            "canceled_by": None,
            "canceled_on": None,
            "sent_by": default_user_data()["id"],
            "sent_on": TIME,
            "receiving_started_by": None,
            "receiving_started_on": None,
        },
        {
            "id": 5,
            "source_base": base_data()[1]["id"],
            "target_base": base_data()[2]["id"],
            "transfer_agreement": transfer_agreement_data()[0]["id"],
            "state": ShipmentState.Preparing,
            "started_by": default_user_data()["id"],
            "started_on": TIME,
            "canceled_by": None,
            "canceled_on": None,
            "sent_by": None,
            "sent_on": None,
            "receiving_started_by": None,
            "receiving_started_on": None,
        },
        {
            "id": 6,
            "source_base": base_data()[0]["id"],
            "target_base": base_data()[2]["id"],
            "transfer_agreement": transfer_agreement_data()[0]["id"],
            "state": ShipmentState.Receiving,
            "started_by": default_user_data()["id"],
            "started_on": TIME,
            "canceled_by": None,
            "canceled_on": None,
            "sent_by": default_user_data()["id"],
            "sent_on": TIME,
            "receiving_started_by": default_user_data()["id"],
            "receiving_started_on": TIME,
        },
    ]


@pytest.fixture
def default_shipment():
    return data()[0]


@pytest.fixture
def canceled_shipment():
    return data()[1]


@pytest.fixture
def another_shipment():
    return data()[2]


@pytest.fixture
def sent_shipment():
    return data()[3]


@pytest.fixture
def receiving_shipment():
    return data()[5]


@pytest.fixture
def shipments():
    return data()


def create():
    Shipment.insert_many(data()).execute()
