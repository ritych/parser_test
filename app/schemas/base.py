# THIRDPARTY
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    """Pydantic model for describing a referral event.

    Used for validation of event data.

    - directionId (int): Direction identifier (mandatory positive number).
    - directionName (str): The name of the direction (non-empty string).
    - topicVersion (int): The version of the topic (mandatory non-negative
        number).
    - status (str): The status of the event (one of the allowed statuses).
    """
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        from_attributes=True
    )
