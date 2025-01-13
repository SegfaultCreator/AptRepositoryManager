Python scripts to generate the files necessary to deploy custom apt-packages on a local-mirror.

Default Usage (Pack all new files in source directoy and deploy on repository) 
```
python3 AptRepositoryManager.py --new
```

Rebuild all packages folder from source folder and deploy to repository
```
python3 AptRepositoryManager.py --all
```

Build single packages 
```
python3 AptRepositoryManager.py example-package example-package2
```
