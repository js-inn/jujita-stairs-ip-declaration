from typing import List, Optional
from pydantic import BaseModel, Field, FieldValidationInfo, field_validator


class TransmitterType(BaseModel):
    submitter_acct_num: str = Field(..., pattern=r"^[A-Za-z0-9]{15}$")
    transmitter_name: str = Field(..., max_length=30)
    contact_name: str = Field(..., max_length=30)
    contact_phone: str = Field(..., pattern=r"^\d{3}-\d{3}-\d{4}$")
    language_code: str = Field(..., pattern=r"^[EF]$")


class T4AOASSlip(BaseModel):
    recipient_sin: str = Field(..., pattern=r"^\d{9}$")
    bn: str = Field(..., pattern=r"^\d{9}RP\d{4}$")
    gross_pay: float = Field(default=0.0, ge=0.0)
    tax_deducted: float = Field(default=0.0, ge=0.0)

    @field_validator("recipient_sin")
    @classmethod
    def mask_sin_for_audit(cls, v: str) -> str:
        if len(v) == 9 and v.isdigit():
            return f"***-***-{v[-3:]}"
        return v


class T4AOASSummary(BaseModel):
    bn: str = Field(..., pattern=r"^\d{9}RP\d{4}$")
    total_slips: int = Field(..., ge=0)
    total_gross_pay: float = Field(..., ge=0.0)
    total_tax_deducted: float = Field(..., ge=0.0)


class T4AOASReturnType(BaseModel):
    summary: T4AOASSummary = Field(..., alias="T4A_OASSummary")
    slips: List[T4AOASSlip] = Field(default_factory=list, alias="T4A_OASSlip")

    @field_validator("slips")
    @classmethod
    def validate_bn_keyref(cls, slips: List[T4AOASSlip], info: FieldValidationInfo) -> List[T4AOASSlip]:
        summary: Optional[T4AOASSummary] = info.data.get("summary")
        if summary:
            summary_bn = summary.bn
            for idx, slip in enumerate(slips):
                if slip.bn != summary_bn:
                    raise ValueError(
                        f"Integrity Mismatch [KeyRef Error]: Slip index {idx} BN ({slip.bn}) "
                        f"does not match Summary BN ({summary_bn})."
                    )
        return slips


class T4AOASReturnChoiceType(BaseModel):
    t4a_oas: Optional[T4AOASReturnType] = Field(default=None, alias="T4A_OAS")


class Submission(BaseModel):
    t619: TransmitterType = Field(..., alias="T619")
    returns: List[T4AOASReturnChoiceType] = Field(default_factory=list, alias="Return")


if __name__ == "__main__":
    sample_payload = {
        "T619": {
            "submitter_acct_num": "MM1234560000001",
            "transmitter_name": "Edge Tax Engine Inc",
            "contact_name": "System Orchestrator",
            "contact_phone": "780-555-0199",
            "language_code": "E"
        },
        "Return": [
            {
                "T4A_OAS": {
                    "T4A_OASSummary": {
                        "bn": "123456789RP0001",
                        "total_slips": 1,
                        "total_gross_pay": 12500.00,
                        "total_tax_deducted": 1500.00
                    },
                    "T4A_OASSlip": [
                        {
                            "recipient_sin": "123456789",
                            "bn": "123456789RP0001",
                            "gross_pay": 12500.00,
                            "tax_deducted": 1500.00
                        }
                    ]
                }
            }
        ]
    }

    sub = Submission.model_validate(sample_payload)
    print("✅ Schema Validation Success!")
    print(sub.model_dump_json(indent=2))
