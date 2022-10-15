from dataclasses import dataclass
from typing import List
from random import uniform
import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass
class Weapon:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    @property
    def damage(self):
        return round(uniform(self.min_damage, self.max_damage), 1)


@dataclass
class EquipmentData:
    weapons: List[Weapon]
    armors: List[Armor]


class Equipment:

    def __init__(self):
        self.equipment = self.__get_equipment_data()

    def get_weapon(self, weapon_name: str) -> Weapon | None:
        for i in self.equipment.weapons:
            if i.name == weapon_name:
                return i
        return None

    def get_armor(self, armor_name) -> Armor | None:
        for i in self.equipment.armors:
            if i.name == armor_name:
                return i
        return None

    def get_weapons_names(self) -> list:
        res = []
        for i in self.equipment.weapons:
            res.append(i.name)
        return res

    def get_armors_names(self) -> list:
        res = []
        for i in self.equipment.armors:
            res.append(i.name)
        return res

    @staticmethod
    def __get_equipment_data() -> EquipmentData:
        """Этот метод загружает json в переменную EquipmentData"""
        with open("../data/equipment.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
        try:
            return equipment_schema().load(data)
        except marshmallow.exceptions.ValidationError:
            raise ValueError
