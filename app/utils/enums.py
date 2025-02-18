from enum import Enum


class POProcessingStatusEnum(str, Enum):
    RECEIVED = "RECEIVED"
    PARTIALLY_FULFILLED = "PARTIALLY_FULFILLED"
    FULFILLED = "FULFILLED"
    OPEN = "OPEN"
    IN_PROGRESS_PARTIAL = "IN_PROGRESS_PARTIAL"
    IN_PROGRESS_FULL = "IN_PROGRESS_FULL"
    CLOSED = "CLOSED"

class POLineItemProcessingStatusEnum(str, Enum):
    OPEN = "OPEN"
    FULFILLED = "FULFILLED"
    PARTIALLY_FULFILLED = "PARTIALLY_FULFILLED"

class InvoiceStatusEnum(str, Enum):
    RAISED = "RAISED"
    DUE = "DUE"
    OVER_DUE = "OVER_DUE"
    SETTLED = "SETTLED"
    TO_BE_GENERATED = "TO_BE_GENERATED"
    NOT_RAISED = "NOT_RAISED"
