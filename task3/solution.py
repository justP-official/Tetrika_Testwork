"""
Когда пользователь заходит на страницу урока, мы сохраняем время его захода. Когда пользователь выходит с урока (или закрывает вкладку, браузер – в общем как-то разрывает соединение с сервером), мы фиксируем время выхода с урока. Время присутствия каждого пользователя на уроке хранится у нас в виде интервалов. В функцию передается словарь, содержащий три списка с таймстемпами (время в секундах):
lesson – начало и конец урока
pupil – интервалы присутствия ученика
tutor – интервалы присутствия учителя
Интервалы устроены следующим образом – это всегда список из четного количества элементов. Под четными индексами (начиная с 0) время входа на урок, под нечетными - время выхода с урока.
Нужно написать функцию appearance, которая получает на вход словарь с интервалами и возвращает время общего присутствия ученика и учителя на уроке (в секундах).
"""

def process_intervals(intervals: list[int], lesson: list[int]) -> list[tuple[int]]:
    """
    Функция для обработки интервалов.

    Убирает некорректные интервалы, оставляет только те, что в диапазоне урока.

    :param intervals: Список с интервалами.

    :param lesson: Список с интервалами урока

    :return result_intervals: Список кортежей с корректными интервалами.

    :rtype: list
    """
    lesson_start, lesson_end = lesson

    result_intervals = []

    for i in range(0, len(intervals), 2):
        start = intervals[i]
        end = intervals[i + 1]

        if start >= end:
            continue

        if start >= lesson_end or end <= lesson_start:
            continue

        start_clipped = max(start, lesson_start)
        end_clipped = min(end, lesson_end)

        if start_clipped >= end_clipped:
            continue

        result_intervals.append((start_clipped, end_clipped))

    return result_intervals


def merge_intervals(intervals: list[tuple[int]]) -> list[tuple[int]]:
    """
    Функция для слияния интервалов.

    Гарантирует корректность расчетов, устраняя перекрытия, упрощает логику поиска пересечений, 
    оптимизирует производительность, учитывает только реальное время присутствия

    :param intervals: Список кортежей с интервалами.

    :return result_intervals: Список кортежей с объединёнными интервалами.

    :rtype: list
    """
    result_intervals = []

    if intervals:
        intervals.sort(key=lambda x: x[0])

        current_start, current_end = intervals[0]

        for i in range(1, len(intervals)):
            start, end = intervals[i]

            if start <= current_end:
                current_end = max(current_end, end)
            else:
                result_intervals.append((current_start, current_end))
                current_start, current_end = start, end

        result_intervals.append((current_start, current_end))

    return result_intervals



def appearance(intervals: dict[str, list[int]]) -> int:
    """
    Функция для вычисления общего времени одновременного присутствия ученика и учителя на уроке.

    Функция обрабатывает временные интервалы урока, ученика и учителя для определения:
    1. Валидных интервалов присутствия в рамках урока
    2. Объединенных интервалов (с учётом перекрывающихся периодов для каждого участника)
    3. Пересекающихся периодов между учеником и учителем

    :param intervals: Словарь с интервалами.

    :return total_time: Суммарное время в секундах, когда ученик и учитель одновременно присутствовали на уроке.

    :rtype: int
    """
    lesson = intervals['lesson']
    
    pupil_intervals = intervals['pupil']
    tutor_intervals = intervals['tutor']
    
    # Обработка интервалов ученика
    pupil_intervals = process_intervals(pupil_intervals, lesson)
    
    # Объединение интервалов ученика
    pupil_intervals = merge_intervals(pupil_intervals)
    
    # Обработка интервалов учителя
    tutor_intervals = process_intervals(tutor_intervals, lesson)
    
    # Объединение интервалов учителя
    tutor_intervals = merge_intervals(tutor_intervals)
    
    # Поиск пересечений интервалов ученика и учителя
    total_time = 0
    pupil_index, tutor_index = 0, 0
    while pupil_index < len(pupil_intervals) and tutor_index < len(tutor_intervals):
        pupil_start, pupil_end = pupil_intervals[pupil_index]
        tutor_start, tutor_end = tutor_intervals[tutor_index]
        
        # Вычисление пересечения
        start_overlap = max(pupil_start, tutor_start)
        end_overlap = min(pupil_end, tutor_end)
        if start_overlap < end_overlap:
            total_time += end_overlap - start_overlap
        
        # Переход к следующему интервалу
        if pupil_end < tutor_end:
            pupil_index += 1
        else:
            tutor_index += 1
            
    return total_time


tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
             'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
             'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
    },
    {'intervals': {'lesson': [1594702800, 1594706400],
             'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
             'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
    'answer': 3577
    },
    {'intervals': {'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
             'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
    'answer': 3565
    },
]

if __name__ == '__main__':
   for i, test in enumerate(tests):
       test_answer = appearance(test['intervals'])
       assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'