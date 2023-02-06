from datetime import datetime

from django.core.exceptions import ValidationError


def min_date_validator(date):
    """Check that the date is not less than now"""
    now = datetime.today()
    if date < now:
        raise ValidationError('Wrong date.')
