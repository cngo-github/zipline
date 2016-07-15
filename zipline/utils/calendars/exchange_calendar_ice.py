from datetime import time

from pandas.tseries.holiday import AbstractHolidayCalendar, GoodFriday
from pytz import timezone

from zipline.utils.calendars import TradingCalendar
from zipline.utils.calendars.us_holidays import USNewYearsDay, Christmas


class ICEExchangeCalendar(TradingCalendar):
    """
    Exchange calendar for ICE US.

    Open Time: 8pm, US/Eastern
    Close Time: 6pm, US/Eastern
    """
    name = "ICE"
    tz = timezone('US/Eastern')

    open_time = time(20)
    close_time = time(18)

    open_offset = -1
    close_offset = 0

    holidays_calendar = ICEHolidayCalendar()


class ICEHolidayCalendar(AbstractHolidayCalendar):
    # https://www.theice.com/publicdocs/futures_us/exchange_notices/NewExNot2016Holidays.pdf # noqa
    rules = [
        USNewYearsDay,
        GoodFriday,
        Christmas
    ]
