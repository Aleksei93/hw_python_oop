from typing import Type, Dict
HOUR_TO_MIN: float = 60


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type,
                 duration,
                 distance,
                 speed,
                 ) -> None:
        self.traning_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed

    def get_message(self) -> str:
        return(f'Тип тренировки: {self.training_type};'
               f'Длительность: {self.duration}ч.;'
               f'Дистанция: {self.distance}км;'
               f'Ср. скорость: {self.speed} км/ч;'
               f'Потрачено ккал: {self.calories}ккал.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 calories: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.calories = calories

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * Training.LEN_STEP / Training.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        information_massage = InfoMessage(self,
                                          self.training_type,
                                          self.duration,
                                          self.get_distance(),
                                          self.get_mean_speed(),
                                          self.get_spent_calories()
                                          )
        return information_massage


class Running(Training):
    """Тренировка: бег."""
    training_type: str = 'RUN'
    coeff_calorie_1 = 18
    coeff_calorie_2 = 20

    def get_spent_calories(self) -> float:
        return ((Running.coeff_calorie_1 * self.get_mean_speed())
                - Running.coeff_calorie_2 * self.weight
                / Training.M_IN_KM * self.duration * 60)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CAL_WALK_1: float = 0.035
    CAL_WALK_2: int = 2
    CAL_WALK_3: float = 0.029

    def __init__(self,
                 action: int,
                 weight: float,
                 height: float,
                 duration: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((SportsWalking.CAL_WALK_1 * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * SportsWalking.CAL_WALK_3 * self.weight) * self.duration * 60)


class Swimming(Training):
    """Тренировка: плавание."""
    training_type: str = 'SWM'
    coeff_calorie_SWM1: float = 1.1
    coeff_calorie_SWM2: int = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 lenght_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(self, action, duration, weight)
        self.lenght_pool = lenght_pool
        self.count_pool = count_pool

    def get_spent_calories(self) -> float:
        return ((Swimming.get_mean_speed(self) + Swimming.coeff_calorie_SWM1)
                * Swimming.coeff_calorie_SWM2 * self.weight)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость при плавании."""
        return (self.lenght_pool * self.count_pool
                / Training.M_IN_KM / self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    all_trainings: Dict[str, Type[Training]] = {'RUN': Running,
                                                'WLK': SportsWalking,
                                                'SWM': Swimming
                                                }
    return all_trainings[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = Training.show_training_info()
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
