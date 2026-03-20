class NetgridError(Exception):
    """Base class for all Netgrid errors."""
    pass

class DataLoadError(NetgridError):
    """Raised when JSON or data files fail to load."""
    pass

class SchemaValidationError(NetgridError):
    """Raised when data fails schema validation."""
    pass

class EngineStateError(NetgridError):
    """Raised when the engine enters an invalid state."""
    pass

class BattleError(NetgridError):
    """Raised for issues during battle calculations."""
    pass

class AIError(NetgridError):
    """Raised for AI scoring or decision issues."""
    pass
