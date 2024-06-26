import pkgutil
from get_doc_scripts import tools

# Iterate over all modules in the 'tools' package
for importer, modname, ispkg in pkgutil.iter_modules(tools.__path__, tools.__name__ + '.'):
    module = __import__(modname, fromlist="dummy")
    if hasattr(module, 'scraper'):
        print(f"Running {modname}")
        try:
            module.scraper.run()
        except Exception as e:
            print(f"Error running {modname}: {e}")
        print(f"Finished running {modname} -----------------")
        print()
