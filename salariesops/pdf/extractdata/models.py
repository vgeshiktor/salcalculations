from typing import Optional

from pydantic import BaseModel


class PersonalInfo(BaseModel):
    employee_name: str
    address: str
    employee_number: Optional[int]
    identity_number: Optional[int]
    resident: Optional[str]
    main_job: Optional[str]
    job_unit: Optional[str]
    seniority: Optional[str]
    job_fraction: Optional[str]
    salary_basis: Optional[str]
    job_start_date: Optional[str]
    department: Optional[str]
    marital_status: Optional[str]
    rank: Optional[str]
    rating: Optional[str]
    bank_account_number: Optional[int]
    bank_number: Optional[str]


class SalaryDetails(BaseModel):
    national_insurance: Optional[float]
    health_tax: Optional[float]
    rounding_bl: Optional[float]
    harel: Optional[float]
    mandatory_deductions: Optional[float]
    salary: Optional[float]
    travel: Optional[float]
    gross_salary: Optional[float]
    net_salary: Optional[float]


class WorkDetails(BaseModel):
    work_days: Optional[int]
    work_hours: Optional[float]
    absence_hours: Optional[float]
    daily_hours: Optional[float]
    regular_points: Optional[float]
    marginal_tax_rate: Optional[int]
    edition_code: Optional[float]
    cumulative_calculation: Optional[str]
    payment_method: Optional[str]


class InsuranceTaxDetails(BaseModel):
    company_hours: Optional[float]
    taxable_salary: Optional[float]
    national_insurance: Optional[float]
    insured_salary: Optional[float]
    base_insurance: Optional[float]
    pension_employer: Optional[float]
    severance_pay_exempt: Optional[float]
    employer_national_ins: Optional[float]
    monthly_minimum_salary: Optional[float]
    hourly_minimum_salary: Optional[float]
    accumulated_taxable_salary: Optional[float]
    national_ins_accumulated: Optional[float]
    national_ins_payment: Optional[float]
    health_tax_payment: Optional[float]
    harel: Optional[float]


class VacationBalance(BaseModel):
    previous_balance: Optional[float]
    accrued_vacation: Optional[float]
    used_vacation: Optional[float]
    new_balance: Optional[float]


class SickLeaveBalance(BaseModel):
    previous_balance: Optional[float]
    accrued_sick_leave: Optional[float]
    used_sick_leave: Optional[float]
    new_balance: Optional[float]


class Employee(BaseModel):
    personal_info: PersonalInfo
    salary_details: SalaryDetails
    work_details: WorkDetails
    insurance_tax_details: InsuranceTaxDetails
    vacation_balance: VacationBalance
    sick_leave_balance: SickLeaveBalance
