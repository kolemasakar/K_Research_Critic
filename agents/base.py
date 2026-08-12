from __future__ import annotations

from abc import ABC, abstractmethod

from models import AgentDefinition, AgentResult, AgentRunRequest


class Agent(ABC):
    """Common executable agent boundary."""

    @property
    @abstractmethod
    def definition(self) -> AgentDefinition:
        raise NotImplementedError

    @abstractmethod
    def run(self, request: AgentRunRequest) -> AgentResult:
        raise NotImplementedError
