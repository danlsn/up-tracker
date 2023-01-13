"""
Enums models module for up_tracker app

Contains the models for:
    - TransactionStatusEnum
    - AccountType(Enum)
    - OwnershipType(Enum)
    - MoneyObject
    - CategoryResource
    - AccountResource
    - CashbackObject
    - RoundUpObject
    - HoldInfoObject
    - TransactionStatusResource
    - CardPurchaseMethodObject
    - CategoryInputResourceIdentifier
    - TransactionResource
    - TagResource
    - Attributes
    - Relationships
    - ErrorObject
    - WebhookResource
    - WebhookInputResource
    - WebhookEventResource
    - WebhookDeliveryLogResource
    - WebhookDeliveryStatus(Enum)
"""

# Standard Library Imports
from datetime import datetime
from enum import Enum
from http import HTTPStatus

# Third Party Imports
from dataclasses import dataclass
from typing import Optional, List, Any

from iso4217 import Currency
from pydantic import BaseModel, Field, validator, AnyUrl


class AccountType(Enum):
    """
    The bank account type for a transaction.
    Possible values are:
        - SAVER
        - TRANSACTIONAL
        - HOME_LOAN
    """
    SAVER = "SAVER"
    TRANSACTIONAL = "TRANSACTIONAL"
    HOME_LOAN = "HOME_LOAN"


class OwnershipType(Enum):
    """
    The ownership structure for an account.
    Possible values are:
        - INDIVIDUAL
        - JOINT
    """
    INDIVIDUAL = "INDIVIDUAL"
    JOINT = "JOINT"


class ResourceType(Enum):
    """
    The resource type for a response.
    Possible values are:
        - ACCOUNT
        - CATEGORY
        - TRANSACTION
        - WEBHOOK
    """
    ACCOUNT = "accounts"
    CATEGORY = "categories"
    TRANSACTION = "transactions"
    WEBHOOK = "webhooks"
    WEBHOOK_EVENT = "webhook-events"
    WEBHOOK_DELIVERY_LOG = "webhook-delivery-logs"


class ResourceIdentifier(BaseModel):
    """
    The resource identifier object.
    """
    id: str = Field(
        ...,
        description="The unique identifier for the resource."
    )
    type: str = Field(
        ...,
        description="The type of the resource."
    )


class MoneyObject:
    """
    An object containing the currency code, value and value in base units.
        - currency_code: str - The ISO 4217 currency code.
        - value: str - The value of the amount in the currency specified.
        - value_in_base_units: int - The amount of money in the smallest unit of the currency.
    """
    currency_code: Currency
    value: str
    value_in_base_units: int


class CategoryInput(ResourceIdentifier):
    """
    An object containing the category ID.
        - type: str - The type of the resource. This will always be categories.
        - id: str - The category ID.
    """
    type: str
    id: str


class Resource(BaseModel):
    """
    An object containing the resource type and ID.
        - type: str - The type of the resource.
        - id: str - The ID of the resource.
        - attributes:
    """
    type: str
    id: str


class Attribute(BaseModel):
    """
    An object containing the category ID.
        - name: str - The name of the attribute.
    """
    name: str


class Link(BaseModel):
    """
    An object containing the category ID.
        - href: str - The URL of the related resource.
        - meta: dict - A dictionary containing meta information about the link.
    """
    related: str


# TODO: Add the rest of the attributes for the Relationship class
class Relationship:
    """
    An object containing a relationship between resources.
        - data: Resource - The resource object.
        - links: list[Link] - The links object.
    """
    data: str
    links: list[Link]


# TODO: Add the rest of the attributes for the Link class
class Link:
    ...


class TransactionRelationships(Relationship):
    """
    An object containing the relationships for a transaction.
        - account: Relationship - The account relationship.
        - category: Relationship - The category relationship.
    """
    transactions: list[Relationship]


# Create Top Level Models
# TODO: Create Account class
class Account(BaseModel):
    """
    An object containing the account.
        - type: str - The type of the resource. This will always be accounts.
        - id: str - The unique identifier.
        - attributes: Attributes - An object containing the account attributes.
        - relationships: Relationships - An object containing the account relationships.
        - links: Links - An object containing the account links.
    """
    type: str
    attributes: Any
    relationships: Any
    links: Any


# TODO: Create CategoryResource
class Category(Resource):
    """
    An object containing the category ID.
        - type: str - The type of the resource. This will always be categories.
        - id: str - The category ID.
    """
    type: ResourceType = ResourceType.CATEGORY


# TODO: Create TagResource
class Tag(Resource):

    ...


# TODO: Create TransactionResource
class Transaction(Resource):
    type: str
    ...


# TODO: Create ErrorObject
class Source:
    parameter: Optional[str]
    pointer: Optional[str]


class ErrorObject:
    status: HTTPStatus
    title: str
    detail: str
    source: Optional[Source]
    ...


# TODO: Create WebhookResource
class WebhookAttribute(Attribute):
    url: AnyUrl
    description: Optional[str]
    secret_key: Optional[str]
    created_at: datetime


class Webhook(Resource):
    type: str
    id: str
    attributes: list[WebhookAttribute]

    ...
