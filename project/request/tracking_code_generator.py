import uuid
from datetime import datetime
from flask_security import current_user


def generate_code():
    date = datetime.utcnow()
    formatted_date = date.strftime('%y%m')
    id = uuid.uuid4().hex[:5]
    code = f"{formatted_date}{id.upper()}{current_user.id}"
    return code
