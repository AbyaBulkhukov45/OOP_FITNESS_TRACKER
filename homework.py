from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    DURATION_COEFF: int = 60

    def __init__(self, action: int, duration: float, weight: float) -> None:
        """
        Конструктор класса, инициализирующий новый
        экземпляр класса с заданными параметрами.
    
        Параметры:
        action - номер действия
        duration - длительность действия в секундах
        weihgt - вес в килограммах
        """
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> None:
        """Получить количество затраченных калорий.
        Метод не реализован и нужно переопределить в наследниках
        """
        raise NotImplementedError("Метод не реализован")

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight
                / self.M_IN_KM
                * (self.duration
                   * self.DURATION_COEFF))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_MEAN_SPEED_MULTIPLIER: float = 0.035
    CALORIES_MEAN_SPEED_SHIFT: float = 0.029
    KM_H_TO_M_S: float = 0.278
    SM_TO_M: int = 100

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * self.weight
                 + ((self.get_mean_speed() * self.KM_H_TO_M_S)**2
                    / (self.height / self.SM_TO_M))
                * self.CALORIES_MEAN_SPEED_SHIFT
                * self.weight)
                * self.duration
                * self.DURATION_COEFF)
        """
        Рассчитывает количество калорий, сожженных во время выполнения
        упражнения, исходя из веса, роста, продолжительности и средней скорости
        """


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    SHIFT_SPEED: float = 1.1
    MULTIPLIER_SPEED: int = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ):
        """
        Конструктор класса, инициализирующий
        объект класса с заданными параметрами.

        Параметры:
            action (int): совершенные действия
            duration (float): длительность выполнения
            weight (float): вес
            length_pool (float): длина бассейна
            count_pool (float): сколько раз проплыл туда и обратно
        """
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        """Рассчитывает среднюю скорость плавания в км/ч."""
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self):
        """Вычисляет количество затраченных калорий"""
        return ((self.get_mean_speed()
                + self.SHIFT_SPEED)
                * self.MULTIPLIER_SPEED
                * self.weight
                * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    training_types: dict[str, Training] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type not in training_types:
        raise ValueError('Набор входных данных некорректный.')

    return training_types[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
