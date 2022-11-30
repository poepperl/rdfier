from datetime import datetime


def get_datetime_postfix() -> str:
    """
    Generates a postfix from the current datetime. This postfix
    can be used for traning run ids oder file versioning.

    Returns:
        str: The generate postfix in format yyyymmdd_hhmmss
    """
    return (
        str(datetime.now())
        .replace("-", "")
        .replace(" ", "_")
        .replace(":", "")
        .split(".")[0]
    )

