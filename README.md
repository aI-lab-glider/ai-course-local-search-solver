# Lab 04 - local search solvers

Local search solvers are algorithms used for optimization problems where it is impractical to explore the entire search space 🔍. Instead, they focus on finding a good solution by making small incremental changes to an initial solution 💡. They are commonly used in transportation and logistics 🚛, manufacturing and production 🏭, telecommunications and networking 📡. Current research in this area include the use of hybrid algorithms, metaheuristics, constraint satisfaction, parallelization, and machine learning applications for neighborhood estimation to improve the efficiency and effectiveness of local search solvers 🤖.

# TODO: 

Search for `TODO` text in the repository with CTRL+F and replace it with you code written according to it.


## How To Submit Solutions

* [ ] Clone repository: git clone:
    ```bash
    git clone <repository url>
    ```
* [ ] Complete TODOS the exercises
* [ ] Commit your changes
    ```bash
    git add <path to the changed files>
    git commit -m <commit message>
    ```
* [ ] Push changes to your repository main branch
    ```bash
    git push -u origin master
    ```

The rest will be taken care of automatically. You can check the `GRADE.md` file for your grade / test results. Be aware that it may take some time (up to one hour) till this file

## How To Run

### Linux
```bash
pip install -e .
local_search_solver solve -c [PATH_TO_CONFIG]
```

## Config

Every entity (solver/algorithm/problem) gets its corespondig config class constainning all necessary parametrs, e.g.:
- algorithm_config.py
- solver_config.py

The default values can be overridden by configuration file, please look into *_config.json files for reference.

### config file structure:

```jsonc
{
  "problem": {
     ...
   },
   "algorithm": {
     ...
   },
   "solver_config": {
     ...
   },
   "visualization": {
     ...
   }
  "save_solution": ...
}

```


## CLI 

Course provides you with a command line interface, to facilitate developing and debugging of algorithms.
You can check commands by running:

```bash
python run.py --help
```

If you are interested in how some concrete command works you can check it by running:

```bash
python run.py COMMAND_NAME --help
```
