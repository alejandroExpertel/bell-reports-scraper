import calendar
import datetime


def get_driver_path(system: str):
    if system == 'macOS':
        return "./drivers/mac/chromedriver"
    if system == 'windows':
        return "./drivers/windows/chromedriver_win32.zip/chromedriver.exe"


def get_month_name_folder(date: str = None):
    if date is not None:
        dt = datetime.datetime.strptime(date, '%Y-%m-%d')
    else:
        dt = datetime.datetime.now()

    name_actual_month = calendar.month_name[dt.month]
    anio_actual = dt.year

    return f"{name_actual_month}_{anio_actual}"


def get_date_ranges():
    base_month = datetime.datetime.now().month - 1
    base_year = datetime.datetime.now().year - 1
    options_dict = {}
    for _ in range(1, 15):
        if base_month > 12:
            base_month = 1
            base_year = base_year + 1
        month_name = calendar.month_name[base_month]
        if base_month > 9:
            formatted_value = f"{base_year}-{base_month}-21"
        else:
            formatted_value = f"{base_year}-0{base_month}-21"

        options_dict[f"{month_name[:3]} {base_year}"] = formatted_value
        base_month = base_month + 1

    return options_dict


def get_key_date_from_value(value):
    for k, v in get_date_ranges():
        if v == value:
            return k
    return None


def get_date_from_text(key):
    return get_date_ranges()[key]
