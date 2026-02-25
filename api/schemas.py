from pydantic import BaseModel, Field

class CustomerData(BaseModel):
    Income: float = Field(..., description="Jahreseinkommen in Euro")
    Credit_Score: float = Field(..., description="Schufa Score")
    Age: int = Field(..., description="Alter in Jahren")

class PredictResponse(BaseModel):
    Approved: int = Field(..., description="1 = Genehmigt, 0 = Abgelehnt")

class ExplainResponse(BaseModel):
    status: str
    shap_explanation: dict
