from typing import Optional
from pydantic import BaseModel, validator, root_validator, ValidationError


class User(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    age: Optional[int]
    # @validator("phone_number")
    # def parse_phone_number(cls, phone_number: str):
    #     """
    #     Change phone number after parsing
    #     """
    #     return f'Phone number {phone_number} XXX '

    # @validator("phone_number")
    # def parse_phone_number(cls, phone_number:str, values, **kwargs):
    #     """
    #     print dict_keys(['first_name', 'last_name'])
    #     all required values names except phone_number it put
    #     into method directly
    #     """
    #     print(values.keys())
    #     return phone_number

    @root_validator
    def parse_user(cls, values: dict):
        """Validate all User parameters"""
        if values['age'] is not None:
            if int(values['age']) < 0:
                raise ValidationError('Age should be positive')
            if int(values['age']) > 150:
                raise ValidationError('Age should be less than 150')
        print(values.keys())
        return values

    class Config:
        orm_mode = True

