from typing import Annotated
from pydantic import AfterValidator, Field
from app.utils.validators import (
    validate_phone_number,
    validate_email,
    validate_password,
)

PhoneNumber = Annotated[
    str, AfterValidator(validate_phone_number), Field(examples=["+996500500500"])
]

EmailField = Annotated[
    str, AfterValidator(validate_email), Field(examples=["example@mail.com"])
]

PasswordField = Annotated[
    str, AfterValidator(validate_password), Field(examples=["P@sSw0rd911"])
]
