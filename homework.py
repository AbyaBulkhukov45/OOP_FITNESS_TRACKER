class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        message = (f'Тип тренировки: {self.training_type}; '
                   f'Длительность: {self.duration:.3f} ч.; '
                   f'Дистанция: {self.distance:.3f} км; '
                   f'Ср. скорость: {self.speed:.3f} км/ч; '
                   f'Потрачено ккал: {self.calories:.3f}.')
        return message

    def show_message(self) -> None:
        print(self.get_message())


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = self.__class__.__name__
        return InfoMessage(training_type, self.duration, self.get_distance(),
                           self.get_mean_speed(), self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1 = 18
    coeff_calorie_2 = 20

    def get_spent_calories(self):
        first = self.coeff_calorie_1 * self.get_mean_speed()
        second = self.duration * 60
        third = first - self.coeff_calorie_2
        return (third * self.weight / self.M_IN_KM * second)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_calorie_1 = 0.035
    coeff_calorie_2 = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        first_step = self.coeff_calorie_1 * self.weight
        second_step = (self.get_mean_speed()**2 // self.height)
        third_step = self.coeff_calorie_2 * self.weight
        fourth_step = self.duration * 60
        return ((first_step + second_step * third_step) * fourth_step)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    coeff_calorie_1 = 1.1
    coeff_calorie_2 = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self) -> float:
        calorie_weight = self.coeff_calorie_2 * self.weight
        return (self.get_mean_speed() + self.coeff_calorie_1) * calorie_weight

    def get_mean_speed(self) -> float:
        multiplic = self.length_pool * self.count_pool
        return multiplic / self.M_IN_KM / self.duration


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    prime = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    if workout_type in prime.keys():
        return prime[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    info.show_message()


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for training_type, data in packages:
        training = read_package(training_type, data)
        main(training)
''