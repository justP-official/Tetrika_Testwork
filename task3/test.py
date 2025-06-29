import pytest

from solution import appearance, merge_intervals, process_intervals


def test_process_intervals():
    lesson = [1000, 2000]
    
    # Тест 1: Интервалы внутри урока
    intervals = [1100, 1200, 1300, 1400]
    assert process_intervals(intervals, lesson) == [(1100, 1200), (1300, 1400)]
    
    # Тест 2: Интервал выходит за границы урока
    intervals = [900, 1500, 1800, 2500]
    assert process_intervals(intervals, lesson) == [(1000, 1500), (1800, 2000)]
    
    # Тест 3: Интервал полностью вне урока
    intervals = [500, 800, 2100, 3000]
    assert process_intervals(intervals, lesson) == []
    
    # Тест 4: Некорректный интервал (начало > конца)
    intervals = [1500, 1400]
    assert process_intervals(intervals, lesson) == []
    
    # Тест 5: Граничные значения
    intervals = [1000, 1001, 1999, 2000]
    assert process_intervals(intervals, lesson) == [(1000, 1001), (1999, 2000)]
    
    # Тест 6: Интервал касается границ
    intervals = [500, 1000, 2000, 2500]
    assert process_intervals(intervals, lesson) == []
    
    # Тест 7: Нечетное количество элементов
    intervals = [1100, 1200, 1300]
    with pytest.raises(IndexError):
        process_intervals(intervals, lesson)


def test_merge_intervals():
    # Тест 1: Пересекающиеся интервалы
    intervals = [(100, 200), (150, 250)]
    assert merge_intervals(intervals) == [(100, 250)]
    
    # Тест 2: Соприкасающиеся интервалы
    intervals = [(100, 200), (200, 300)]
    assert merge_intervals(intervals) == [(100, 300)]
    
    # Тест 3: Непересекающиеся интервалы
    intervals = [(100, 200), (300, 400)]
    assert merge_intervals(intervals) == [(100, 200), (300, 400)]
    
    # Тест 4: Несколько интервалов
    intervals = [(100, 200), (150, 250), (300, 400), (350, 450)]
    assert merge_intervals(intervals) == [(100, 250), (300, 450)]
    
    # Тест 5: Полное поглощение
    intervals = [(100, 400), (200, 300)]
    assert merge_intervals(intervals) == [(100, 400)]
    
    # Тест 6: Пустой ввод
    assert merge_intervals([]) == []
    
    # Тест 7: Один интервал
    intervals = [(100, 200)]
    assert merge_intervals(intervals) == [(100, 200)]
    
    # Тест 8: Неупорядоченные интервалы
    intervals = [(300, 400), (100, 200), (150, 250)]
    assert merge_intervals(intervals) == [(100, 250), (300, 400)]


def test_appearance():
    # Тест 1: Простое пересечение
    intervals1 = {
        'lesson': [1000, 2000],
        'pupil': [1100, 1500],
        'tutor': [1200, 1300]
    }
    assert appearance(intervals1) == 100  # 1300 - 1200 = 100
    
    # Тест 2: Два интервала пересечения
    intervals2 = {
        'lesson': [1000, 2000],
        'pupil': [900, 1200, 1300, 1700],
        'tutor': [1100, 1400]
    }
    assert appearance(intervals2) == 200  # (1200-1100) + (1400-1300) = 200
    
    # Тест 3: Полное совпадение
    intervals3 = {
        'lesson': [1000, 2000],
        'pupil': [1000, 2000],
        'tutor': [1000, 2000]
    }
    assert appearance(intervals3) == 1000
    
    # Тест 4: Пересечение на границах
    intervals4 = {
        'lesson': [1000, 2000],
        'pupil': [900, 1000, 2000, 2100],
        'tutor': [900, 1000, 2000, 2100]
    }
    assert appearance(intervals4) == 0