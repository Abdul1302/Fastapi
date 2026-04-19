from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    # Patient's name: max 50 characters, with title and description for docs/schema
    name: Annotated[str, Field(
        max_length=50,
        title='Name of the patient',
        description='Give the name of the patient in less than 50 chars',
        examples=['Nitish', 'Amit']
    )]

    # Validates that the email follows proper email format (e.g., abc@gmail.com)
    email: EmailStr

    # Validates that the URL is a properly formatted URL (e.g., https://linkedin.com/...)
    linkedin_url: AnyUrl

    # Age must be a positive integer and less than 120 (gt=0 means > 0, lt=120 means < 120)
    age: int = Field(gt=0, lt=120)

    # Weight must be a float strictly greater than 0
    # strict=True means no automatic type coercion (e.g., int 75 won't be accepted, must be 75.0)
    weight: Annotated[float, Field(gt=0, strict=True)]

    # Optional boolean field — defaults to None if not provided
    married: Annotated[bool, Field(default=None, description='Is the patient married or not')]

    # Optional list of allergy strings — defaults to None, and list can have at most 5 items
    allergies: Annotated[Optional[List[str]], Field(default=None, max_length=5)]

    # A dictionary where both keys and values are strings (e.g., {"phone": "1234567890"})
    contact_details: Dict[str, str]


def update_patient_data(patient: Patient):
    # Accepts a validated Patient object and prints its fields
    print(patient.name)
    print(patient.age)
    print(patient.allergies)   # Will print None if not provided
    print(patient.married)     # Will print None if not provided
    print('updated')


# Raw dictionary input — notice age is a string '30', Pydantic will auto-coerce it to int
# married and allergies are missing — they will default to None
patient_info = {
    'name': 'Abdul Rehman',
    'email': 'xyz@gmail.com',
    'linkedin_url': 'http://linkedin.com/132802',
    'age': '24',          # String '30' → Pydantic converts it to int 30 automatically
    'weight': 77.5,
    'contact_details': {'phone': '1234567890'}
}

# Pydantic validates all fields here — raises ValidationError if anything is invalid
patient1 = Patient(**patient_info)

# Pass the validated patient object to the function
update_patient_data(patient1)