"""
Utility functions.
"""
import re
from decimal import Decimal
from typing import Optional


def format_document_number(doc_type: str, number: str) -> str:
    """
    Format Peruvian document numbers (DNI, RUC, Passport).

    Args:
        doc_type: Type of document (dni, ruc, passport)
        number: Document number

    Returns:
        Formatted document number
    """
    number = re.sub(r'[^0-9A-Z]', '', number.upper())

    if doc_type == 'dni':
        # DNI: 8 digits
        return number.zfill(8)
    elif doc_type == 'ruc':
        # RUC: 11 digits
        return number.zfill(11)
    else:
        # Passport: as is
        return number


def validate_ruc(ruc: str) -> bool:
    """
    Validate Peruvian RUC number.

    Args:
        ruc: RUC number to validate

    Returns:
        True if valid, False otherwise
    """
    if not ruc or len(ruc) != 11:
        return False

    if not ruc.isdigit():
        return False

    # Check digit validation
    factors = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
    total = sum(int(ruc[i]) * factors[i] for i in range(10))
    check_digit = 11 - (total % 11)

    if check_digit == 11:
        check_digit = 0
    elif check_digit == 10:
        check_digit = 1

    return int(ruc[10]) == check_digit


def calculate_igv(amount: Decimal, include_igv: bool = False) -> dict:
    """
    Calculate IGV (Peru's VAT - 18%).

    Args:
        amount: Base amount or total amount
        include_igv: If True, amount includes IGV; if False, IGV will be added

    Returns:
        Dict with base_amount, igv_amount, and total_amount
    """
    IGV_RATE = Decimal('0.18')

    if include_igv:
        # Amount includes IGV, extract it
        base_amount = amount / (1 + IGV_RATE)
        igv_amount = amount - base_amount
        total_amount = amount
    else:
        # Amount doesn't include IGV, add it
        base_amount = amount
        igv_amount = amount * IGV_RATE
        total_amount = amount + igv_amount

    return {
        'base_amount': base_amount.quantize(Decimal('0.01')),
        'igv_amount': igv_amount.quantize(Decimal('0.01')),
        'total_amount': total_amount.quantize(Decimal('0.01'))
    }


def generate_code(prefix: str, sequence: int, length: int = 6) -> str:
    """
    Generate a formatted code with prefix and sequence number.

    Args:
        prefix: Code prefix (e.g., 'GRP', 'PAX', 'INV')
        sequence: Sequence number
        length: Total length of sequence part (zero-padded)

    Returns:
        Formatted code (e.g., 'GRP-000123')
    """
    return f"{prefix}-{str(sequence).zfill(length)}"


def parse_phone_number(phone: str) -> Optional[str]:
    """
    Parse and format phone number.

    Args:
        phone: Raw phone number

    Returns:
        Formatted phone number or None if invalid
    """
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)

    if not digits:
        return None

    # Format based on length
    if len(digits) == 9:
        # Peru mobile: 9XX XXX XXX
        return f"{digits[0:3]} {digits[3:6]} {digits[6:9]}"
    elif len(digits) == 7:
        # Peru landline: XXX XXXX
        return f"{digits[0:3]} {digits[3:7]}"
    else:
        # International or other format
        return digits


def slugify_filename(filename: str) -> str:
    """
    Create a safe filename by removing special characters.

    Args:
        filename: Original filename

    Returns:
        Safe filename
    """
    # Get name and extension
    parts = filename.rsplit('.', 1)
    name = parts[0]
    ext = parts[1] if len(parts) > 1 else ''

    # Replace spaces and special chars
    name = re.sub(r'[^\w\s-]', '', name.lower())
    name = re.sub(r'[-\s]+', '-', name).strip('-')

    return f"{name}.{ext}" if ext else name
