from __future__ import annotations

from models import AgentDefinition, AgentStatus, AgentType

from .exceptions import AgentNotFoundError, AgentRegistrationError


class AgentRegistry:
    """Registry for executable agent definitions and capability discovery."""

    def __init__(self) -> None:
        self._agents: dict[str, AgentDefinition] = {}
        self._name_versions: set[tuple[str, str]] = set()

    def register(self, agent: AgentDefinition) -> None:
        identity = (agent.name, agent.version)
        if agent.agent_id in self._agents:
            raise AgentRegistrationError(f"Duplicate agent_id: {agent.agent_id}")
        if identity in self._name_versions:
            raise AgentRegistrationError(f"Agent name/version already registered: {agent.name} {agent.version}")
        self._agents[agent.agent_id] = agent
        self._name_versions.add(identity)

    def get(self, agent_id: str) -> AgentDefinition:
        try:
            return self._agents[agent_id]
        except KeyError as exc:
            raise AgentNotFoundError(f"Unknown agent_id: {agent_id}") from exc

    def list_agents(self, *, active_only: bool = False) -> list[AgentDefinition]:
        agents = list(self._agents.values())
        if active_only:
            agents = [agent for agent in agents if agent.status == AgentStatus.ACTIVE]
        return agents

    def find_by_capability(self, capability: str, *, agent_type: AgentType | None = None) -> list[AgentDefinition]:
        normalized = capability.strip()
        if not normalized:
            return []
        matches = []
        for agent in self._agents.values():
            if agent.status != AgentStatus.ACTIVE:
                continue
            if agent_type is not None and agent.agent_type != agent_type:
                continue
            if normalized in agent.capabilities:
                matches.append(agent)
        return matches
