from datetime import datetime


def get_current_datetime() -> str:
    """
    Get current time formatted in dd/MM/yyyy HH:MM:SS.
    :return: String value of current time formatted in dd/MM/yyyy HH:MM:SS.
    """
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
