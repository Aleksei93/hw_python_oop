from typing import Dict, List, Type


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        """Создать объекты класса InfoMessage."""
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Вернуть информационное сообщение."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MIN_IN_HOUR: float = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        """Создать объекты базового класса."""
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
        message = InfoMessage(self.__class__.__name__,
                              self.duration,
                              self.get_distance(),
                              self.get_mean_speed(),
                              self.get_spent_calories()
                              )
        return message


class Running(Training):
    """Тренировка: бег."""

    COEF_RUN_1: int = 18
    COEF_RUN_2: int = 20

    def get_spent_calories(self) -> float:
        """Получить колличество потраченных калории при беге."""
        return ((self.COEF_RUN_1 * self.get_mean_speed()
                - self.COEF_RUN_2) * self.weight
                / self.M_IN_KM * self.duration * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEF_WLK_1: float = 0.035
    COEF_WLK_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        """Создать объекты дочернего класса SportsWalking."""
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить колличество потраченных калории при спортивной хотьбе."""
        return((self.COEF_WLK_1 * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * self.COEF_WLK_2 * self.weight)
               * (self.duration * self.MIN_IN_HOUR))


class Swimming(Training):
    """Тренировка: плавание."""

    COEF_SWIM_1: float = 1.1
    COEF_SWIM_2: int = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        """Создать объекты дочернего класса Swimming."""
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self) -> float:
        """Получить колличество потраченных калории при плавании."""
        return ((self.get_mean_speed() + self.COEF_SWIM_1)
                * self.COEF_SWIM_2 * self.weight)

    def get_mean_speed(self) -> float:
        """Расчет средней скорости при плавании"""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return training_type[workout_type](*data)


def main(training: Training) -> str:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: Dict[str, List[int]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
