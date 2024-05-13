import pkgutil
from get_doc_scripts import tools

# Iterate over all modules in the 'tools' package
for importer, modname, ispkg in pkgutil.iter_modules(tools.__path__, tools.__name__ + '.'):
    print("Found submodule %s (is a package: %s)" % (modname, ispkg))
    module = __import__(modname, fromlist="dummy")
    if hasattr(module, 'scraper'):
        print(f"Running scraper for {modname}")
        module.scraper.run()
