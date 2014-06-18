"""
   Copyright 2013, 2014 Ricardo Tubio-Pardavila

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
__author__ = 'rtubiopa@calpoly.edu'

from datetime import datetime, timedelta
from pytz import utc as pytz_utc
from misc import get_today_utc


def define_interval(days=7):
    """
    Defines a tuple with the starting and ending dates for the interval
    of time that has to be used for the calculations of the available
    slots.
    :param days: Length of the interval for the calculations.
    :return: A tuple with the initial datetime and the final datetime for
    this interval.
    """
    utc_today = datetime.utcnow().date()
    begin_interval = pytz_utc.localize(
        datetime(utc_today.year, utc_today.month, utc_today.day)
    )
    end_interval = begin_interval + timedelta(days=days)
    return begin_interval, end_interval


def normalize_slots(slots):
    """
    This function "normalizes" a list of slots by merging all consecutive or
    overlapping slots into non-overlapping ones. IMPORTANT: the input slots
    array has to be sorted by initial datetime of the slot, this is, for a
    given slot at position 'i', it is always met the following condition:
    slots[i]['starting_date'] <= slots[i+1]['starting_date'].
    :param slots: The list of slots to be normalized.
    :return: The normalized list of slots.
    """
    if slots is None:
        return []
    slots_n = len(slots)
    if slots_n < 2:
        return slots

    normalized_s = []
    s = slots[0]
    t = slots[1]
    s_i = 0
    t_i = 1

    while s_i < slots_n:

        if s[1] < t[0]:
            # ### CASE A
            normalized_s.append(s)
            s = t

        if (s[0] <= t[0]) and (s[1] <= t[1]):
            # ### CASE B
            s = (s[0], t[1])

        # ### CASE C and next iteration
        if t_i < (slots_n - 1):
            t_i += 1
            t = slots[t_i]
            continue
        else:
            # ### last vectors
            normalized_s.append(s)
            break

    return normalized_s


def merge_slots(p_slots, m_slots):
    """
    This function  merges the slots that define the availability of the
    ground station with the slots that define the non-availability of a
    ground station. The result are the actual availability slots.
    IMPORTANT: input lists of slots must be order by starting datetime.
    :param p_slots: The list of (+) slots.
    :param m_slots: The list of (-) slots.
    :return: Resulting list with the actual available slots.
    """
    if p_slots is None or m_slots is None:
        return []
    if len(p_slots) < 1:
        return []

    # Algorithm initialization
    slots = []
    p_next = True  # ### indicates whether the 'p' vector has to be updated
    p_n = len(p_slots)
    p_i = 0
    m_i = 0
    m_n = len(m_slots)
    if m_n > 0:
        m = m_slots[0]
        m_i = 1
    else:
        # All slots will be generated from today on, so this will be the
        # "oldest" slot independently of the rest...
        m = (
            get_today_utc() - timedelta(days=1),
            get_today_utc() - timedelta(days=1)
        )

    # The algorithm is executed for all the add slots, since negative slots
    # do not generate actual slots at all, they only limit the range of the
    # add slots.
    while True:

        if p_next:
            # ### stop condition
            if p_i == p_n:
                break
            p = p_slots[p_i]
            p_i += 1
        else:
            p_next = True

        if p[1] <= m[0]:
            # ### CASE A:
            slots.append(p)
            continue

        if p[0] >= m[1]:
            # ### CASE F:
            if m_i < m_n:
                m = m_slots[m_i]
                m_i += 1
            else:
                slots.append(p)
            continue

        if p[0] < m[0]:

            if (p[1] > m[0]) and (p[1] <= m[1]):
                # ### CASE B:
                slots.append((p[0], m[0]))
            if p[1] > m[1]:
                # ### CASE C:
                slots.append((p[0], m[0]))
                p = (m[1], p[1])
                p_next = False

        else:

            # ### CASE D:
            if p[1] > m[1]:
                p = (m[1], p[1])
                p_next = False
                if m_i < m_n:
                    m = m_slots[m_i]
                    m_i += 1

    return slots
