from typing import List, Optional, Any
from pydantic import BaseModel, Field, ValidationInfo, field_validator, ConfigDict


class TransmitterType(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    submitter_acct_num: str = Field(
        default="MM1234560000001",
        alias="TransmitterNumber"
    )
    transmitter_name: str = Field(
        default="Default Transmitter", 
        alias="TransmitterName", 
        max_length=30
    )
    contact_name: str = Field(
        default="Default Contact", 
        alias="ContactName", 
        max_length=30
    )
    contact_phone: str = Field(
        default="780-555-0199", 
        alias="ContactPhone"
    )
    contact_email: str = Field(
        default="admin@example.com",
        alias="ContactEmail"
    )
    language_code: str = Field(
        default="E", 
        alias="LanguageCode", 
        pattern=r"^[EF]$"
    )

    @property
    def TransmitterNumber(self) -> str:
        return self.submitter_acct_num

    @property
    def TransmitterName(self) -> str:
        return self.transmitter_name

    @property
    def ContactName(self) -> str:
        return self.contact_name

    @property
    def ContactPhone(self) -> str:
        return self.contact_phone

    @property
    def ContactEmail(self) -> str:
        return self.contact_email

    @property
    def LanguageCode(self) -> str:
        return self.language_code

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

    recipient_sin: str = Field(default="000000000", alias="RecipientSIN", pattern=r"^\d{9}$")
    bn: str = Field(default="000000000RP0001", alias="BusinessNumber", pattern=r"^\d{9}RP\d{4}$")
    gross_pay: float = Field(default=0.0, alias="GrossPay", ge=0.0)
    tax_deducted: float = Field(default=0.0, alias="TaxDeducted", ge=0.0)

    @property
    def RecipientSIN(self) -> str:
        return self.recipient_sin

    @property
    def BusinessNumber(self) -> str:
        return self.bn

    @property
    def GrossPay(self) -> float:
        return self.gross_pay

    @property
    def TaxDeducted(self) -> float:
        return self.tax_deducted

    @field_validator("recipient_sin")
    @classmethod
    def mask_sin_for_audit(cls, v: str) -> str:
        if len(v) == 9 and v.isdigit():
            return f"***-***-{v[-3:]}"
        return v


class T4AOASSummary(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    bn: str = Field(default="000000000RP0001", alias="BusinessNumber", pattern=r"^\d{9}RP\d{4}$")
    total_slips: int = Field(default=0, alias="TotalSlips", ge=0)
    total_gross_pay: float = Field(default=0.0, alias="TotalGrossPay", ge=0.0)
    total_tax_deducted: float = Field(default=0.0, alias="TotalTaxDeducted", ge=0.0)

    @property
    def BusinessNumber(self) -> str:
        return self.bn

    @property
    def TotalSlips(self) -> int:
        return self.total_slips

    @property
    def TotalGrossPay(self) -> float:
        return self.total_gross_pay

    @property
    def TotalTaxDeducted(self) -> float:
        return self.total_tax_deducted


class T4AOASReturnType(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    summary: T4AOASSummary = Field(default_factory=T4AOASSummary, alias="T4A_OASSummary")
    slips: List[T4AOASSlip] = Field(default_factory=list, alias="T4A_OASSlip")

    @property
    def Summary(self) -> T4AOASSummary:
        return self.summary

    @property
    def Slip(self) -> List[T4AOASSlip]:
        return self.slips

    @property
    def Slips(self) -> List[T4AOASSlip]:
        return self.slips

    @property
    def T4A_OASSummary(self) -> T4AOASSummary:
        return self.summary

    @property
    def T4A_OASSlip(self) -> List[T4AOASSlip]:
        return self.slips


class T4AOASReturnChoiceType(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    t4a_oas: Optional[T4AOASReturnType] = Field(default=None, alias="T4A_OAS")

    @property
    def T4A_OAS(self) -> Optional[T4AOASReturnType]:
        return self.t4a_oas


class Submission(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    t619: TransmitterType = Field(default_factory=TransmitterType, alias="T619")
    returns: List[Any] = Field(default_factory=list, alias="Return")

    @property
    def T619(self) -> TransmitterType:
        return self.t619

    @property
    def Return(self) -> List[Any]:
        return self.returns

    @property
    def T550(self) -> T4AOASReturnType:
        """Returns the inner T4A_OAS object if found, otherwise returns a default instance."""
        for ret in self.returns:
            if isinstance(ret, T4AOASReturnType):
                return ret
            if hasattr(ret, "t4a_oas") and ret.t4a_oas is not None:
                return ret.t4a_oas
            if isinstance(ret, dict):
                t4a_data = ret.get("T4A_OAS") or ret.get("t4a_oas")
                if t4a_data:
                    return T4AOASReturnType.model_validate(t4a_data)
        return T4AOASReturnType()


SubmissionModel = Submission
