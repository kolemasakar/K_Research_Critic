class SupervisorError(Exception):
    """Base exception for Supervisor orchestration errors."""


class TaskNotFoundError(SupervisorError):
    pass


class DuplicateTaskError(SupervisorError):
    pass


class WorkflowNotFoundError(SupervisorError):
    pass


class WorkflowAlreadyActiveError(SupervisorError):
    pass


class InvalidStateTransitionError(SupervisorError):
    pass


class AgentRegistrationError(SupervisorError):
    pass


class AgentNotFoundError(SupervisorError):
    pass


class ProfileNotFoundError(SupervisorError):
    pass


class ProfileStateError(SupervisorError):
    pass
