from core.plugins_manager import PluginsManager


class BaseModule:

    def log_stream(http_stream):
        pass

    @classmethod
    def help(cls):
        return "BaseModule!!!"


# Registering the plugin in the plugin manager
PluginsManager.register(BaseModule, 'BaseModule')
