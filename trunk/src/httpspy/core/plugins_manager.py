class PluginsManager:
    """
    This class is in charge of managing the available plugins for the sniffer.
    """

    def __init__(self):
        self._plugins = {}
	self._initialed_plugins = []

    def register(self, plugin, plugin_name):
        """
        This method must be called by each plugin implementation
        in order to be registered by this manager.
        """
        self._plugins[plugin_name] = plugin

    def list_plugins(self):
        """
        Return a list with the names of all registered plugins.
        """
        return self._plugins.keys()

    def list_initialized_plugins(self):
        """
	    Return a list of those plugins which were initialized 
	    from a configuration files and are ready to be used.
	    """
        return self._initialed_plugins

    def get_plugin(self, plugin_name):
        """
        Given a name, if registered, returns the plugin with that name.
        """
        try:
            return self._plugins[plugin_name]
        except KeyError:
            raise PluginsManagerError(c)

    def init_plugins(self, plugins_conf):
        """
        Initializes each registered plugin with it corresponding
        configuration file.
        """
        for plugin_conf in plugins_conf:
            try:
                self._initialed_plugins.append(PluginsManager.get_plugin(plugin_conf['name'])(plugin_conf))
            except PluginsManagerError:
                print 'Plugin %s not registered. Not able to initialize it.' % plugin_name


class PluginsManagerError(Exception):
    pass


"""
Singleton class ofuscated
"""
PluginsManager = PluginsManager()
