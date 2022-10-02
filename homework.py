# -*- coding: utf-8 -*-
class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str, duration: float, distance: float,
                 speed: float, calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories
        pass

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type};'
                f' Длительность: {self.duration:.3f} ч.;'
                f' Дистанция: {self.distance:.3f} км;'
                f' Ср. скорость: {self.speed:.3f} км/ч;'
                f' Потрачено ккал: {self.calories:.3f}.')
    pass


class Training:
    """Базовый класс тренировки."""
    type = 'Training'
    LEN_STEP: float = 0.65  # 0.65m/1.38m - for swimming
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        pass

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP / self.M_IN_KM)
        pass

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.get_distance() / self.duration)
        pass

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        msg = (InfoMessage(self.type, self.duration, self.get_distance(),
               self.get_mean_speed(), self.get_spent_calories()))
        return msg
        pass


class Running(Training):
    """Тренировка: бег."""
    type: str = 'Running'

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)
    pass

    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        return ((coeff_calorie_1 * self.get_mean_speed() - coeff_calorie_2)
                * self.weight / self.M_IN_KM * self.duration * self.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    type: str = 'SportsWalking'

    def __init__(self, action: int, duration: float, weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height
    pass

    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 0.029
        return ((coeff_calorie_1 * self.weight + (self.get_mean_speed()**2
                // self.height) * coeff_calorie_2 * self.weight)
                * self.duration * self.MIN_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""
    type: str = 'Swimming'
    LEN_STEP: float = 1.38

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
    pass

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 1.1
        coeff_calorie_2 = 2
        return ((self.get_mean_speed() + coeff_calorie_1)
                * coeff_calorie_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    if workout_type in dict.keys():
        return dict[workout_type](*data)
    else:
        print('workout_type error')
        exit()
    pass


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())
    pass


if __name__ == '__main__':
    """Имитация получения данных от блока датчиков фитнес-трекера."""
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
