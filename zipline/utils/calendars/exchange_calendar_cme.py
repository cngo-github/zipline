#
# Copyright 2016 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import time
from itertools import chain

from pandas.tseries.holiday import AbstractHolidayCalendar
from pytz import timezone

# Useful resources for making changes to this file:
# http://www.cmegroup.com/tools-information/holiday-calendar.html

from .trading_calendar import TradingCalendar, HolidayCalendar
from .us_holidays import (
    USNewYearsDay,
    Christmas,
    ChristmasEveBefore1993,
    ChristmasEveInOrAfter1993,
    FridayAfterIndependenceDayExcept2013,
    MonTuesThursBeforeIndependenceDay,
    USBlackFridayInOrAfter1993,
    # September11Closings,
    USNationalDaysofMourning
)

# US_CENTRAL = timezone('America/Chicago')
# CME_OPEN = time(17)
# CME_CLOSE = time(16)
#
#
# CME_STANDARD_EARLY_CLOSE = time(12)

#
# class CMEHolidayCalendar(AbstractHolidayCalendar):
#     """
#     Non-trading days for the CME.
#
#     See CMEExchangeCalendar for full description.
#     """
#     rules = [
#         USNewYearsDay,
#         Christmas,
#     ]
#

# class CMEEarlyCloseCalendar(AbstractHolidayCalendar):
#     """
#     Regular early close calendar for NYSE
#     """
#     rules = [
#         MonTuesThursBeforeIndependenceDay,
#         FridayAfterIndependenceDayExcept2013,
#         USBlackFridayInOrAfter1993,
#         ChristmasEveBefore1993,
#         ChristmasEveInOrAfter1993,
#     ]


class CMEExchangeCalendar(TradingCalendar):
    """
    Exchange calendar for CME

    Open Time: 5:00 PM, America/Chicago
    Close Time: 5:00 PM, America/Chicago

    Regularly-Observed Holidays:
    - New Years Day (observed on monday when Jan 1 is a Sunday)
    - Christmas (observed on nearest weekday to December 25)

    NOTE: For the following US Federal Holidays, part of the CME is closed
    (Foreign Exchange, Interest Rates) but Commodities, GSCI, Weather & Real
    Estate is open.  Thus, we don't treat these as holidays.
    - Columbus Day
    - Veterans Day

    Regularly-Observed Early Closes:
    - Martin Luther King Jr. Day (3rd Monday in January, only after 1998)
    - Washington's Birthday (aka President's Day, 3rd Monday in February)
    - Good Friday (two days before Easter Sunday)
    - Memorial Day (last Monday in May)
    - Independence Day (observed on the nearest weekday to July 4th)
    - Labor Day (first Monday in September)
    - Thanksgiving (fourth Thursday in November)
    - Christmas Eve (except on Fridays, when the exchange is closed entirely)
    - Day After Thanksgiving (aka Black Friday, observed from 1992 onward)

    Additional Irregularities:
    - Closed on 4/27/1994 due to Richard Nixon's death.
    - Closed on 6/11/2004 due to Ronald Reagan's death.
    - Closed on 1/2/2007 due to Gerald Ford's death.
    """
    @property
    def name(self):
        return "CME"

    @property
    def tz(self):
        return timezone('America/Chicago')

    @property
    def open_time(self):
        return time(17)

    @property
    def close_time(self):
        return time(16)

    @property
    def open_offset(self):
        return -1

    @property
    def regular_holidays(self):
        # The CME has different holiday rules depending on the type of
        # instrument. For example, http://www.cmegroup.com/tools-information/holiday-calendar/files/2016-4th-of-july-holiday-schedule.pdf # noqa
        # shows that Equity, Interest Rate, FX, Energy, Metals & DME Products
        # close at 1200 CT on July 4, 2016, while Grain, Oilseed & MGEX
        # Products and Livestock, Dairy & Lumber products are completely
        # closed.

        # For now, we will treat the CME as having a single calendar, and just
        # go with the most conservative hours - and treat July 4 as an early
        # close at noon.
        return HolidayCalendar([
            USNewYearsDay,
            Christmas,
        ])

    @property
    def adhoc_holidays(self):
        return USNationalDaysofMourning

    @property
    def early_closes(self):
        return HolidayCalendar([
            MonTuesThursBeforeIndependenceDay,
            FridayAfterIndependenceDayExcept2013,
            USBlackFridayInOrAfter1993,
            ChristmasEveBefore1993,
            ChristmasEveInOrAfter1993,
        ])

    @property
    def special_closes(self):
        return [(
            time(12),
            HolidayCalendar([
                MonTuesThursBeforeIndependenceDay,
                FridayAfterIndependenceDayExcept2013,
                USBlackFridayInOrAfter1993,
                ChristmasEveBefore1993,
                ChristmasEveInOrAfter1993,
            ])
        )]
