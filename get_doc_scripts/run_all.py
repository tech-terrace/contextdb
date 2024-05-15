import pkgutil
from get_doc_scripts import tools

# Iterate over all modules in the 'tools' package
for importer, modname, ispkg in pkgutil.iter_modules(tools.__path__, tools.__name__ + '.'):
    module = __import__(modname, fromlist="dummy")
    if hasattr(module, 'scraper'):
        module.scraper.run()
