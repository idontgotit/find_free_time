import os
import sys
from datetime import datetime

import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
django.setup()
from datetime import timedelta

START_DATETIME = 'start'
END_DATETIME = 'end'


def rebuild_busy_time(input_array_busy):
    busy_time = []
    for item in input_array_busy:
        busy_time.append((item[START_DATETIME], item[END_DATETIME]))
    return busy_time


def find_free_time(input_array_available, input_array_busy):
    results = []
    busy_time = rebuild_busy_time(input_array_busy)
    for item in input_array_available:
        free_time = find_really_free_time(item, busy_time)
        for item_free in free_time:
            temp = {
                START_DATETIME: item_free.get(START_DATETIME),
                END_DATETIME: item_free.get(END_DATETIME)
            }
            if temp not in results:
                results.append(temp)
    return merge_time(results)


def find_really_free_time(item_available, busy_time):
    free_time = []
    time_start = item_available.get(START_DATETIME)
    time_stop = item_available.get(END_DATETIME)
    tp = [(time_start, time_start)]
    tp.extend(busy_time)
    tp.append((time_stop, time_stop))
    for i, v in enumerate(tp):
        if i > 0:
            if (tp[i][0] - tp[i - 1][1]) > timedelta(seconds=0):
                tf_start = tp[i - 1][1]
                tf_end = tp[i][0]
                if tf_end > time_stop:
                    tf_end = time_stop
                if tf_start < time_start:
                    tf_start = time_start
                if time_start <= tf_start <= tf_end <= time_stop:
                    free_time.append({
                        START_DATETIME: tf_start,
                        END_DATETIME: tf_end
                    })
    return free_time


def merge_time(input_array_time):
    results = []
    for item in input_array_time:
        data_start = item.get(START_DATETIME)
        data_stop = item.get(END_DATETIME)
        for child_item in input_array_time:
            child_time_start = child_item.get(START_DATETIME)
            child_time_stop = child_item.get(END_DATETIME)
            if item == child_item:
                continue
            if data_start <= child_time_start <= data_stop <= child_time_stop:
                data_start = data_start
                data_stop = child_time_stop
            elif child_time_start <= data_start <= child_time_stop <= data_stop:
                data_start = child_time_start
                data_stop = data_stop

            elif child_time_start <= data_start <= data_stop <= child_time_stop:
                data_start = child_time_start
                data_stop = child_time_stop

            elif data_start <= child_time_start <= child_time_stop <= data_stop:
                data_start = data_start
                data_stop = data_stop

        temp = {
            START_DATETIME: data_start,
            END_DATETIME: data_stop
        }
        if temp not in results:
            results.append(temp)

    return sorted(results, key=lambda i: i[START_DATETIME])


if __name__ == "__main__":
    array_available = [
        {
            'start': datetime.fromisoformat('2011-11-04T16:00:00'),
            'end': datetime.fromisoformat('2011-11-04T23:50:00')
        },

        {
            'start': datetime.fromisoformat('2011-11-04T02:00:00'),
            'end': datetime.fromisoformat('2011-11-04T05:50:00')
        },

        {
            'start': datetime.fromisoformat('2011-11-04T15:00:00'),
            'end': datetime.fromisoformat('2011-11-04T18:50:00')
        },

    ]
    array_busy = [

        {'start': datetime.fromisoformat('2011-11-04T16:00:00'),
         'end': datetime.fromisoformat('2011-11-04T22:00:00')},

        {'start': datetime.fromisoformat('2011-11-04T16:00:00'),
         'end': datetime.fromisoformat('2011-11-04T23:00:00')},

        {'start': datetime.fromisoformat('2011-11-04T18:00:00'),
         'end': datetime.fromisoformat('2011-11-04T20:00:00')},
    ]

    merge_array_busy = merge_time(array_busy)
    merge_array_available = merge_time(array_available)
    result = find_free_time(merge_array_available, merge_array_busy)
    print(result)
