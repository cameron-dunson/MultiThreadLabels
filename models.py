from dataclasses import dataclass
from typing import List, Optional

from dotenv import load_dotenv

load_dotenv()


@dataclass
class ShipFromAddress:
    name: str
    phone: str
    company_name: Optional[str]
    address_line1: str
    address_line2: Optional[str]
    city_locality: str
    state_province: str
    postal_code: str
    country_code: str
    address_residential_indicator: str = "unknown"
    address_line3: Optional[str] = ""

    def __post_init__(self):
        valid_residential_indicators = ("yes", "no", "unknown")
        if self.address_residential_indicator not in valid_residential_indicators:
            raise ValueError(
                f"address_residential_indicator must be on of {valid_residential_indicators}"
            )


@dataclass
class ShipToAddress:
    name: str
    phone: str
    company_name: Optional[str]
    address_line1: str
    address_line2: Optional[str]
    city_locality: str
    state_province: str
    postal_code: str
    country_code: str
    address_residential_indicator: str = "unknown"  # Might change to ENUM
    address_line3: Optional[str] = ""

    def __post_init__(self):
        valid_residential_indicators = ("yes", "no", "unknown")
        if self.address_residential_indicator not in valid_residential_indicators:
            raise ValueError(
                f"address_residential_indicator must be on of {valid_residential_indicators}"
            )


@dataclass
class ReturnAddress:
    name: str
    phone: str
    company_name: Optional[str]
    address_line1: str
    address_line2: Optional[str]
    city_locality: str
    state_province: str
    postal_code: str
    country_code: str
    address_residential_indicator: str = "unknown"  # Might change to ENUM
    address_line3: Optional[str] = ""

    def __post_init__(self):
        valid_residential_indicators = ("yes", "no", "unknown")
        if self.address_residential_indicator not in valid_residential_indicators:
            raise ValueError(
                f"address_residential_indicator must be on of {valid_residential_indicators}"
            )


@dataclass
class PackageWeight:
    value: float
    unit: str = "ounce"

    def __post_init__(self):
        valid_units = ("pound", "ounce", "gram", "kilogram")
        if self.unit not in valid_units:
            raise ValueError(f"weight unit must be one of {valid_units}.")


@dataclass
class PackageDimensions:
    length: float = 0.0
    width: float = 0.0
    height: float = 0.0
    unit: str = "inch"

    def __post_init__(self):
        valid_units = ("inch", "centimeter")
        if self.unit not in valid_units:
            raise ValueError(f"dimension unit must be one of {valid_units}.")


@dataclass
class Package:
    weight: PackageWeight
    dimensions: Optional[PackageDimensions]
    package_code: Optional[str] = ""
    external_package_id: Optional[str] = ""


@dataclass
class Shipment:
    carrier_id: str
    service_code: str
    ship_date: str
    ship_to: ShipToAddress
    ship_from: ShipFromAddress
    packages: List[Package]
    insurance_provider: str = "none"
    confirmation: str = "none"
    is_return_label: bool = True
    charge_event: str = "on_carrier_acceptance"  # Enables POUR if enabled on the Stamps.com account being used
    validate_address: Optional[str] = "no_validation"

    def __post_init__(self):
        confirmation_options = (
            "none",
            "delivery",
            "signature",
            "adult_signature",
            "direct_signature",
            "delivery_mailed",
        )
        if self.confirmation not in confirmation_options:
            return ValueError(f"confirmation must be one of {confirmation_options}")
