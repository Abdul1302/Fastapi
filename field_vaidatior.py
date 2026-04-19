from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    # Custom validator for 'email' field
    # Runs BEFORE type coercion (default mode='before') — but EmailStr already validates format
    # This adds extra business logic: only hdfc.com and icici.com domains are allowed
    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_domains = ['hdfc.com', 'icici.com']

        # Split email by '@' and take the last part to extract domain
        # e.g., 'abc@gmail.com'.split('@') → ['abc', 'gmail.com'] → [-1] → 'gmail.com'
        domain_name = value.split('@')[-1]

        # If domain is not in the allowed list, reject it with a clear error
        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')

        return value  # Return the original value if validation passes

    # Custom validator for 'name' field
    # Transforms the name to UPPERCASE before storing it in the model
    # No error is raised here — this is a transformation validator, not a constraint validator
    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        return value.upper()  # e.g., 'nitish' → 'NITISH'

    # Custom validator for 'age' field
    # mode='after' means this runs AFTER Pydantic has already coerced the type (str '30' → int 30)
    # So here we safely receive an int and apply our range check
    @field_validator('age', mode='after')
    @classmethod
    def validate_age(cls, value):
        if 0 < value < 100:
            return value  # Valid age — return as is
        else:
            raise ValueError('Age should be in between 0 and 100')


def update_patient_data(patient: Patient):
    # Receives a fully validated and transformed Patient object
    print(patient.name)           # Will print 'Abdul Rehman' (transformed by validator)
    print(patient.age)            # Will print 24 (coerced from string '30')
    print(patient.allergies)      # Will print ['pollen', 'dust']
    print(patient.married)        # Will print True
    print('updated')


# Raw input dictionary — notice:
# - 'age' is a string '30' → Pydantic will coerce it to int, then our validator runs (mode='after')
# - 'name' is lowercase → our transform_name validator will uppercase it
# - 'email' uses icici.com → passes our domain check
patient_info = {
    'name': 'Abdul Rehman',
    'email': 'xyz@icici.com',
    'age': '30',               # String → coerced to int 30 by Pydantic before mode='after' validator
    'weight': 75.2,
    'married': True,
    'allergies': ['pollen', 'dust'],
    'contact_details': {'phone': '123456789'}
}

# Pydantic runs: type coercion → field_validators → model is created
# If any validator raises ValueError, a ValidationError is thrown here
patient1 = Patient(**patient_info)

update_patient_data(patient1)