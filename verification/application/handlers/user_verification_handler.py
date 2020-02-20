from common.constant import StatusCode, ResponseStatus
from common.exception_handler import exception_handler
from common.exceptions import BadRequestException
from common.logger import get_logger
from common.utils import validate_dict, generate_lambda_response
from verification.application.services.user_verification_service import UserVerificationService
from verification.config import SLACK_HOOK, NETWORK_ID, SUCCESS_REDIRECTION_DAPP_URL
from verification.exceptions import BadRequestException

logger = get_logger(__name__)

user_verification_service = UserVerificationService()


@exception_handler(logger, SLACK_HOOK, NETWORK_ID, BadRequestException)
def initiate(event):
    username = event["requestContext"]["authorizer"]["claims"]["email"]
    response = user_verification_service.initiate(username)
    return generate_lambda_response(StatusCode.OK, {"status": ResponseStatus.SUCCESS, "data": response})


@exception_handler(logger, SLACK_HOOK, NETWORK_ID, BadRequestException)
def submit(event):
    query_params = event["queryStringParameters"]
    transaction_id = query_params.get("customerInternalReference", None)
    jumio_reference = query_params.get("transactionReference", None)
    error_code = query_params.get("errorCode", None)
    user_verification_service.submit(transaction_id, jumio_reference, error_code)
    response_headers = {"location": SUCCESS_REDIRECTION_DAPP_URL}
    return generate_lambda_response(
        status_code=StatusCode.FOUND, message={}, headers=response_headers, cors_enabled=True)


@exception_handler(logger, SLACK_HOOK, NETWORK_ID, BadRequestException)
def complete(event):
    required_keys = ["callBackType", "jumioIdScanReference", "verificationStatus", "idScanStatus", "idScanSource",
                     "idCheckDataPositions", "idCheckDocumentValidation", "idCheckHologram", "idCheckMRZcode",
                     "idCheckMicroprint", "idCheckSecurityFeatures", "idCheckSignature", "transactionDate",
                     "callbackDate"]
    payload = event["body"]
    if not validate_dict(payload, required_keys):
        raise BadRequestException()
    response = user_verification_service.complete(payload)
    return generate_lambda_response(StatusCode.OK, {"status": ResponseStatus.SUCCESS, "data": response})


@exception_handler(logger, SLACK_HOOK, NETWORK_ID, BadRequestException)
def get_status(event):
    username = event["requestContext"]["authorizer"]["claims"]["email"]
    response = user_verification_service.get_status(username)
    return generate_lambda_response(StatusCode.OK, {"status": ResponseStatus.SUCCESS, "data": response})
