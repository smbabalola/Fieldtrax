# app/core/business_rules.py
from typing import Optional, List
from datetime import datetime, timedelta

class JobBusinessRules:
    """Business rules for job operations"""
    
    @staticmethod
    def can_update_job(job: dict, user: dict) -> bool:
        """Check if user can update job"""
        if job.get('status') == 'completed':
            return False
        if user.get('role') not in ['admin', 'supervisor']:
            return False
        return True

    @staticmethod
    def can_approve_timesheet(timesheet: dict, user: dict) -> bool:
        """Check if user can approve timesheet"""
        if timesheet.get('employee_id') == user.get('id'):
            return False  # Cannot approve own timesheet
        if user.get('role') not in ['admin', 'supervisor']:
            return False
        return True

    @staticmethod
    def validate_daily_report(report: dict, previous_reports: List[dict]) -> bool:
        """Validate daily report"""
        if not previous_reports:
            return True
            
        last_report = previous_reports[-1]
        last_report_date = last_report.get('report_date')
        current_report_date = report.get('report_date')
        
        if current_report_date <= last_report_date:
            return False  # Reports must be in chronological order
        
        return True

class FluidBusinessRules:
    """Business rules for fluid operations"""
    
    @staticmethod
    def calculate_mixing_requirements(current_volume: float, 
                                   target_properties: dict,
                                   available_products: List[dict]) -> Optional[dict]:
        """Calculate mixing requirements to achieve target properties"""
        # Implement mixing calculations
        pass

    @staticmethod
    def validate_fluid_properties(properties: dict, well_conditions: dict) -> bool:
        """Validate fluid properties against well conditions"""
        # Implement validation logic
        pass
