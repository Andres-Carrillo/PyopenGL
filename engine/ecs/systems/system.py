from typing import Protocol


class System(Protocol):
    def update(self,entities:list,dt:float) ->None: ...

class SystemManager:
    def __init__(self):
        self._systems: list[System] = []

    def register(self,system:System) ->None:
        self._systems.append(system)

    def update(self,entities:list,dt:float) -> None:
        for system in self._systems:
            system.update(entities,dt)


