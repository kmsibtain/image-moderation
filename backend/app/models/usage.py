from datetime import datetime
from pydantic import BaseModel, Field

class Usage(BaseModel):
    token: str
    endpoint: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }