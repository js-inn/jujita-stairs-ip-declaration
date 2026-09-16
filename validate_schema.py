import xml.etree.ElementTree as ET
from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, EmailStr, Field, ValidationInfo, field_validator

# 1. Base XSD SimpleTypes
ProvinceType = Literal[
    "Sa", "AB", "ab", "Ab", "AL", "al", "Al", "BC", "bc", "Bc",
    "NT", "nt", "Nt", "YT", "yt", "Yt", "NL", "nl", "Nl", "NF",
    "nf", "Nf", "LB", "lb", "Lb", "PQ", "pq", "Pq", "QU", "qu",
    "Qu", "NU", "nu", "Nu", "NN", "nn", "Nn", "US", "us", "Us",
    "ZZ", "zz", "Zz"
]

StateType = Literal[
    "AL", "al", "NV", "nv", "AK", "ak", "NH", "nh", "AZ", "az",
    "NJ", "nj", "AR", "ar", "NM", "nm", "CA", "ca", "NY", "ny",
    "CO", "co", "NC", "nc", "CT", "ct", "ND", "nd", "DE", "de",
    "OH", "oh", "DC", "dc", "OK", "ok", "FL", "fl", "OR", "or",
    "GA", "ga", "PA", "pa", "HI", "hi", "RI", "ri", "ID", "id",
    "SC", "sc", "IL", "il", "SD", "sd", "IN", "in", "TN", "tn",
    "IA", "ia", "TX", "tx", "KS", "ks", "UT", "ut", "KY", "ky",
    "VT", "vt", "LA", "la", "VA", "va", "ME", "me", "WA", "wa",
    "MD", "md", "WV", "wv", "MA", "ma", "WI", "wi", "MI", "mi",
    "WY", "wy", "MN", "mn", "MS", "ms", "MO", "mo", "MT", "mt",
    "NE", "ne", "PR", "pr", "AS", "as", "FM", "fm", "GU", "gu",
    "MH", "mh", "MP", "mp", "PW", "pw", "VI", "vi", "ZZ", "zz"
]

Char22Type = Annotated[str, Field(min_length=1, max_length=22)]
Char60Type = Annotated[str, Field(min_length=1, max_length=60)]
Numeric3Type = Annotated[str, Field(pattern=r"^\d{3}$")]
PhoneType = Annotated[str, Field(pattern=r"^\d{3}-\d{4}$")]
Int7Type = Annotated[str, Field(pattern=r"^\d{1,7}$")]

# 2. Pydantic Models
class TransmitterType(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    TransmitterNumber: Numeric3Type
    TransmitterName: Char60Type
    ContactName: Char60Type
    ContactPhone: PhoneType
    ContactEmail: EmailStr


class T550SlipType(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    RecipientName: Char60Type
    RecipientSIN: Annotated[str, Field(pattern=r"^\d{9}$")]
    Amount: Annotated[float, Field(ge=0.0)]


class T550SummaryType(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    PayorName: Char60Type
    PayorAccountableNumber: Char22Type
    TotalSlips: Annotated[int, Field(ge=1)]
    TotalAmount: Annotated[float, Field(ge=0.0)]


class T550Return(BaseModel):
    Summary: T550SummaryType
    Slips: list[T550SlipType]

    @field_validator("Slips")
    @classmethod
    def validate_totals(cls, slips: list[T550SlipType], info: ValidationInfo) -> list[T550SlipType]:
        if "Summary" in info.data:
            summary: T550SummaryType = info.data["Summary"]
            if len(slips) != summary.TotalSlips:
                raise ValueError(
                    f"Slip count mismatch: Summary specifies {summary.TotalSlips}, "
                    f"but {len(slips)} slips were provided."
                )
            calculated_total = sum(slip.Amount for slip in slips)
            if round(calculated_total, 2) != round(summary.TotalAmount, 2):
                raise ValueError(
                    f"Total amount mismatch: Summary states {summary.TotalAmount}, "
                    f"but calculated total of slips is {calculated_total:.2f}."
                )
        return slips


class SubmissionModel(BaseModel):
    T619: TransmitterType
    T550: T550Return


if __name__ == "__main__":
    valid_data = {
        "T619": {
            "TransmitterNumber": "001",
            "TransmitterName": "Systems & Integration Corp",
            "ContactName": "Alex Mercer",
            "ContactPhone": "555-0199",
            "ContactEmail": "alex@example.com",
        },
        "T550": {
            "Summary": {
                "PayorName": "Enterprise Logistics Ltd",
                "PayorAccountableNumber": "ACC-9988776655",
                "TotalSlips": 2,
                "TotalAmount": 350.50,
            },
            "Slips": [
                {"RecipientName": "Jane Doe", "RecipientSIN": "123456789", "Amount": 150.25},
                {"RecipientName": "John Smith", "RecipientSIN": "987654321", "Amount": 200.25},
            ],
        },
    }

    try:
        submission = SubmissionModel.model_validate(valid_data)
        print("Validation Successful!")
        print(f"Transmitter: {submission.T619.TransmitterName}")
        print(f"Total Slips Validated: {len(submission.T550.Slips)}")
        print(f"Validated JSON Output:\n{submission.model_dump_json(indent=2)}")
    except Exception as e:
        print(f"Validation Error: {e}")
