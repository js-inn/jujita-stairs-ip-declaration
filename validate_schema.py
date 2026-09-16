from typing import List, Optional
from pydantic import BaseModel, Field, ValidationInfo, field_validator, ConfigDict


class TransmitterType(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    submitter_acct_num: str = Field(
        default="MM1234560000001",
        alias="TransmitterNumber"
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
        default="780-555-0199", 
        alias="ContactPhone"
    )
    language_code: str = Field(
        default="E", 
        alias="LanguageCode", 
        pattern=r"^[EF]$"
    )

    @field_validator("contact_phone", mode="before")
    @classmethod
    def format_phone(cls, v: str) -> str:
        if len(v) == 8 and v[3] == "-":
            return f"780-{v}"
        return v

    @field_validator("submitter_acct_num", mode="before")
    @classmethod
    def pad_transmitter_num(cls, v: str) -> str:
        if len(v) < 15:
            return v.zfill(15)
        return v


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

    @property
    def T4A_OASSummary(self) -> T4AOASSummary:
        return self.summary

    @property
    def T4A_OASSlip(self) -> List[T4AOASSlip]:
        return self.slips

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

    @property
    def T4A_OAS(self) -> Optional[T4AOASReturnType]:
        return self.t4a_oas


class Submission(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    t619: TransmitterType = Field(..., alias="T619")
    returns: List[T4AOASReturnChoiceType] = Field(default_factory=list, alias="Return")

    @property
    def T619(self) -> TransmitterType:
        return self.t619

    @property
    def Return(self) -> List[T4AOASReturnChoiceType]:
        return self.returns


SubmissionModel = Submission
