# app/core/units/exceptions.py
from typing import Any, Dict, Optional
from datetime import datetime

class QuantityError(Exception):
    """Base exception class for all quantity-related errors."""
    
    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None
    ):
        self.message = message
        self.details = details or {}
        self.timestamp = timestamp or datetime.utcnow()
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary format."""
        return {
            "error_type": self.__class__.__name__,
            "message": self.message,
            "details": self.details,
            "timestamp": self.timestamp.isoformat()
        }

class UnitError(QuantityError):
    """Exception raised for errors related to unit conversions or invalid units."""
    
    def __init__(
        self,
        message: str,
        invalid_unit: str,
        valid_units: set,
        **kwargs
    ):
        details = {
            "invalid_unit": invalid_unit,
            "valid_units": list(valid_units)
        }
        super().__init__(message, details, **kwargs)

class ConversionError(QuantityError):
    """Exception raised when conversion between units fails."""
    
    def __init__(
        self,
        message: str,
        from_unit: str,
        to_unit: str,
        quantity_type: str,
        **kwargs
    ):
        details = {
            "from_unit": from_unit,
            "to_unit": to_unit,
            "quantity_type": quantity_type
        }
        super().__init__(message, details, **kwargs)

class OperationalLimitError(QuantityError):
    """Exception raised when a quantity exceeds operational limits."""
    
    def __init__(
        self,
        message: str,
        current_value: float,
        limit_value: float,
        parameter: str,
        unit: str,
        **kwargs
    ):
        details = {
            "parameter": parameter,
            "current_value": current_value,
            "limit_value": limit_value,
            "unit": unit
        }
        super().__init__(message, details, **kwargs)

class SafetyLimitError(OperationalLimitError):
    """Exception raised when a safety limit is exceeded."""
    
    def __init__(
        self,
        message: str,
        current_value: float,
        limit_value: float,
        parameter: str,
        unit: str,
        safety_factor: float,
        **kwargs
    ):
        details = {
            "parameter": parameter,
            "current_value": current_value,
            "limit_value": limit_value,
            "unit": unit,
            "safety_factor": safety_factor
        }
        super().__init__(message, current_value, limit_value, parameter, unit, **kwargs)

class ValidationError(QuantityError):
    """Exception raised when quantity validation fails."""
    
    def __init__(
        self,
        message: str,
        field_name: str,
        invalid_value: Any,
        validation_criteria: Dict[str, Any],
        **kwargs
    ):
        details = {
            "field": field_name,
            "invalid_value": invalid_value,
            "validation_criteria": validation_criteria
        }
        super().__init__(message, details, **kwargs)

class CalculationError(QuantityError):
    """Exception raised when a calculation involving quantities fails."""
    
    def __init__(
        self,
        message: str,
        calculation_type: str,
        input_values: Dict[str, Any],
        error_details: str,
        **kwargs
    ):
        details = {
            "calculation_type": calculation_type,
            "input_values": input_values,
            "error_details": error_details
        }
        super().__init__(message, details, **kwargs)

class IncompatibleUnitsError(QuantityError):
    """Exception raised when trying to operate on quantities with incompatible units."""
    
    def __init__(
        self,
        message: str,
        first_quantity: Dict[str, Any],
        second_quantity: Dict[str, Any],
        operation: str,
        **kwargs
    ):
        details = {
            "first_quantity": first_quantity,
            "second_quantity": second_quantity,
            "operation": operation
        }
        super().__init__(message, details, **kwargs)

class RangeError(QuantityError):
    """Exception raised when a quantity is outside its valid range."""
    
    def __init__(
        self,
        message: str,
        value: float,
        min_value: float,
        max_value: float,
        unit: str,
        **kwargs
    ):
        details = {
            "value": value,
            "min_value": min_value,
            "max_value": max_value,
            "unit": unit
        }
        super().__init__(message, details, **kwargs)

class EquipmentLimitError(OperationalLimitError):
    """Exception raised when equipment limits are exceeded."""
    
    def __init__(
        self,
        message: str,
        current_value: float,
        equipment_rating: float,
        parameter: str,
        unit: str,
        equipment_type: str,
        **kwargs
    ):
        details = {
            "parameter": parameter,
            "current_value": current_value,
            "equipment_rating": equipment_rating,
            "unit": unit,
            "equipment_type": equipment_type
        }
        super().__init__(message, current_value, equipment_rating, parameter, unit, **kwargs)

class WellControlError(SafetyLimitError):
    """Exception raised for well control related issues."""
    
    def __init__(
        self,
        message: str,
        current_value: float,
        limit_value: float,
        parameter: str,
        unit: str,
        safety_factor: float,
        well_condition: str,
        **kwargs
    ):
        details = {
            "well_condition": well_condition
        }
        super().__init__(
            message, current_value, limit_value, parameter, unit, safety_factor,
            details=details, **kwargs
        )

# Example usage:
"""
try:
    # Unit conversion error
    raise UnitError(
        message="Invalid pressure unit provided",
        invalid_unit="bar",
        valid_units={"psi", "kPa", "MPa"}
    )
except UnitError as e:
    print(e.to_dict())

try:
    # Operational limit error
    raise OperationalLimitError(
        message="Maximum pressure exceeded",
        current_value=16000,
        limit_value=15000,
        parameter="Pressure",
        unit="psi"
    )
except OperationalLimitError as e:
    print(e.to_dict())

try:
    # Safety limit error
    raise SafetyLimitError(
        message="Casing safety factor below minimum",
        current_value=1.1,
        limit_value=1.2,
        parameter="Safety Factor",
        unit="ratio",
        safety_factor=1.2
    )
except SafetyLimitError as e:
    print(e.to_dict())

try:
    # Well control error
    raise WellControlError(
        message="Insufficient mud weight for well control",
        current_value=12.5,
        limit_value=13.2,
        parameter="Mud Weight",
        unit="ppg",
        safety_factor=1.1,
        well_condition="Gas influx detected"
    )
except WellControlError as e:
    print(e.to_dict())
"""

# Error handler for FastAPI:
"""
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(QuantityError)
async def quantity_error_handler(request: Request, exc: QuantityError):
    return JSONResponse(
        status_code=400,
        content=exc.to_dict()
    )
"""

# Example middleware for logging quantity errors:
"""
from fastapi import Request
import logging

logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_quantity_errors(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except QuantityError as e:
        logger.error(f"Quantity Error: {e.to_dict()}")
        raise
"""

# Example utility function for handling quantity errors:
"""
from typing import Callable, TypeVar, Any

T = TypeVar('T')

def handle_quantity_error(
    func: Callable[..., T],
    error_handler: Optional[Callable[[QuantityError], Any]] = None
) -> Callable[..., T]:
    '''Decorator to handle quantity errors.'''
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except QuantityError as e:
            if error_handler:
                return error_handler(e)
            raise
    return wrapper

# Usage:
@handle_quantity_error
def calculate_pressure(depth: float, mud_weight: float) -> float:
    if mud_weight > 22:
        raise OperationalLimitError(
            message="Mud weight exceeds maximum limit",
            current_value=mud_weight,
            limit_value=22,
            parameter="Mud Weight",
            unit="ppg"
        )
    return depth * mud_weight * 0.052
"""