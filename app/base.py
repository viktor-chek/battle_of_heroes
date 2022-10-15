from unit import BaseUnit


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1
    player = None
    enemy = None
    game_is_running = False
    battle_result = None

    def start_game(self, player: BaseUnit, enemy: BaseUnit) -> None:
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self):
        """Проверка уровня здоровья и расчёт результатов битвы"""
        if self.player.health_points > 0 and self.enemy.health_points > 0:
            return None

        if self.player.health_points <= 0:
            self.battle_result = "Игрок проиграл битву"

        elif self.player.health_points <= 0 and self.enemy.health_points <= 0:
            self.battle_result = "Ничья"

        else:
            self.battle_result = "Игрок выиграл битву"
        return self._end_game()

    def _stamina_regeneration(self):
        """ Регенерация здоровья и стамины для игрока и врага за ход """
        if self.player.stamina + self.STAMINA_PER_ROUND > self.player.unit_class.max_stamina:
            self.player.stamina = self.player.unit_class.max_stamina
        else:
            self.player.stamina += self.STAMINA_PER_ROUND

        if self.enemy.stamina + self.STAMINA_PER_ROUND > self.enemy.unit_class.max_stamina:
            self.enemy.stamina = self.enemy.unit_class.max_stamina
        else:
            self.enemy.stamina += self.STAMINA_PER_ROUND

    def next_turn(self):
        """Функция следующего хода.
        Срабатывает когда игрок пропускает ход или наносит удар
        """

        if self.game_is_running:
            result = self.enemy.hit(self.player)
            self._check_players_hp()
            self._stamina_regeneration()
            return result

    def _end_game(self) -> str:
        """Кнопка завершения игры"""
        self._instances = {}
        self.game_is_running = False
        return self.battle_result

    def player_hit(self):
        """Кнопка удара игрока"""
        result = self.player.hit(self.enemy)
        result_enemy = self.next_turn()
        return f"{result}<br>{result_enemy}"

    def player_use_skill(self):
        """Кнопка использования умения"""
        result = self.player.use_skill(self.enemy)
        result_enemy = self.next_turn()
        return f"{result}<br>{result_enemy}"