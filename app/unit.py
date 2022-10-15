from __future__ import annotations
from abc import ABC, abstractmethod
from equipment import Weapon, Armor
from classes import UnitClass
from random import randint


class BaseUnit(ABC):
    """Базовый класс юнита"""
    def __init__(self, name: str, unit_class: UnitClass):
        """При инициализации класса Unit используем свойства класса UnitClass"""
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = None
        self.armor = None
        self._is_skill_used = False

    @property
    def health_points(self):
        return round(self.hp, 1)

    @property
    def stamina_points(self):
        return round(self.stamina, 1)

    def equip_weapon(self, weapon: Weapon):
        """Присваиваем нашему герою новое оружие"""
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor):
        """Одеваем новую броню"""
        self.armor = armor
        return f"{self.name} экипирован броней {self.armor}"

    def _count_damage(self, target: BaseUnit) -> int:
        """Нанесение урона"""
        self.stamina -= self.weapon.stamina_per_hit
        damage = self.weapon.damage * self.unit_class.attack

        target_stamina = target.armor.stamina_per_turn * target.unit_class.stamina
        if target.stamina > target_stamina:
            damage -= target.armor.defence * target.unit_class.armor

        damage = round(damage, 1)
        target.get_damage(damage=damage)

        return damage

    def get_damage(self, damage: int) -> None:
        """Получение урона"""
        if damage > 0:
            self.hp -= damage
            if self.hp < 0:
                self.hp = 0

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """Этот метод будет переопределен ниже"""
        pass

    def use_skill(self, target: BaseUnit) -> str:
        """Использование умения"""
        if self._is_skill_used:
            return "Навык уже был использован"

        self._is_skill_used = True
        return self.unit_class.skill.use(self, target)


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """функция удар игрока:"""

        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        damage = self._count_damage(target)
        if damage > 0:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {damage} урона."

        return f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """функция удар соперника"""
        if not self._is_skill_used and self.stamina >= self.unit_class.stamina and randint(0, 100) < 10:
            return self.use_skill(target)

        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        damage = self._count_damage(target)
        if damage > 0:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} и наносит Вам {damage} урона."

        return f"{self.name} используя {self.weapon.name} наносит удар, но Ваш(а) {target.armor.name} его останавливает."
