from typing import List, Optional
from pydantic import BaseModel, Field, ValidationInfo, field_validator, ConfigDict


class TransmitterType(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    submitter_acct_num: str = Field(
        ..., 
        alias="TransmitterNumber", 
        pattern=r"^[A-Za-z0-9]{15}$"
    )
    transmitter_name: str = Field(
        ..., 
        alias="TransmitterName", 
        max_length=30
    )
    contact_name: str = Field(
        ..., 
        alias="ContactName", 
        max_length=30
    )
    contact_phone: str = Field(
        ..., 
        alias="ContactPhone", 
        pattern=r"^\d{3}-\d{3}-\d{4}$"
    )
    language_code: str = Field(
        ..., 
        alias="LanguageCode", 
        pattern=r"^[EF]$"
    )


class T4AOASSlip(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    recipient_sin: str = Field(..., alias="RecipientSIN", pattern=r"^\d{9}$")
    bn: str = Field(..., alias="BusinessNumber", pattern=r"^\d{9}RP\d{4}$")
    gross_pay: float = Field(default=0.0, alias="GrossPay", ge=0.0)
    tax_deducted: float = Field(default=0.0, alias="TaxDeducted", ge=0.0)

    @field_validator("recipient_sin")
    @classmethod
    def mask_sin_for_audit(cls, v: str) -> str:
        if len(v) == 9 and v.isdigit():
            return f"***-***-{v[-3:]}"
        return v


class T4AOASSummary(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    bn: str = Field(..., alias="BusinessNumber", pattern=r"^\d{9}RP\d{4}$")
    total_slips: int = Field(..., alias="TotalSlips", ge=0)
    total_gross_pay: float = Field(..., alias="TotalGrossPay", ge=0.0)
    total_tax_deducted: float = Field(..., alias="TotalTaxDeducted", ge=0.0)


class T4AOASReturnType(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    summary: T4AOASSummary = Field(..., alias="T4A_OASSummary")
    slips: List[T4AOASSlip] = Field(default_factory=list, alias="T4A_OASSlip")

    @field_validator("slips")
    @classmethod
    def validate_bn_keyref(cls, slips: List[T4AOASSlip], info: ValidationInfo) -> List[T4AOASSlip]:
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
    model_config = ConfigDict(populate_by_name=True)

    t4a_oas: Optional[T4AOASReturnType] = Field(default=None, alias="T4A_OAS")


class Submission(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    t619: TransmitterType = Field(..., alias="T619")
    returns: List[T4AOASReturnChoiceType] = Field(default_factory=list, alias="Return")


SubmissionModel = Submission
