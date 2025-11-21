"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Literal

# Example schemas (kept for reference):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Rhetorix MUN schemas

class Delegate(BaseModel):
    """
    Delegate registrations for Rhetorix MUN
    Collection name: "delegate"
    """
    full_name: str = Field(..., min_length=2, description="Delegate's full name")
    email: EmailStr = Field(..., description="Contact email")
    phone: str = Field(..., min_length=7, max_length=20, description="Contact phone number")
    institution: str = Field(..., description="School/College/Organization")
    grade_or_year: Optional[str] = Field(None, description="Grade/Year")
    committee: str = Field(..., description="Preferred committee")
    role: Literal["Delegate", "International Press", "Executive Board"] = Field("Delegate")
    country_preferences: Optional[List[str]] = Field(default=None, description="Preferred countries in order")
    experience: Optional[str] = Field(None, description="Past MUN experience (optional)")
    notes: Optional[str] = Field(None, description="Any additional notes or accommodations")
