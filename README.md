# REL-Improvement



## Installation of REL

You can install REL via its [GitHub page](https://github.com/informagi/REL). Installing it using the second option, installation from source code is recommended. Then you should download the required data, for the experiments we have used the 2014 wiki database.

## Setting up the API

Even though REL is installed, you need an API. In the REL repository, it is also explained. A python script namely entlink.py is created for this purpose. It is not used in the experiments, but it is a crucial step to be sure that you have installed REL correctly. If you look at the script, it has two functions. The first one is for preprocessing, where an example input is given. The second function is for the entity linking operation. There are some important parameters you should be careful about. 

The first one is the wiki version, we have used **wiki_2014** but you can change it to **wiki_2019** (if you have installed the data) or your own data.
The second one is **base_url**. This is the location of your data, especially the location of the folders **wiki_2014**, **generic**, and **ed-wiki-2014**.
The third one is config. For the model path, you should enter the path for the model in wiki_2014. Alternatively again you can use your own model following the tutorial on the REL page.

After you set up the API, you can run it and see if it works. If it works, now you can adapt REL for the experiments.

## Adapting REL for the experiments

REL is installed as a python package. Some files must be changed / or replaced. The first file is **base.py**.  It is located in the folder **db**. You can either change it by yourself or replace the file with the code in **base_rep.py**. The same process must be applied to **generic.py**, located in the folder **db**. It may be changed with the code in **generic_rep.py**.

## Creating DuckDB datasets

DuckDB needs a proper DuckDB database, hence you should create a new database based on the current SQLite database. This can be done by using the functions in **create_duckdb_datasets.py** script. The first function is used to create a DuckDB dataset for common crawl in **generic** folder. The second function is used to create a DuckDB dataset for the embeddings in **wiki_2014** folder. You can move the script to these folders and run the functions, or you can change the paths in the functions that the path leads to the SQLite databases.

## Running the Experiments

The experiments are run by using SQLite and/or DuckDB. 

### Configuring REL to use SQLite

In **base.py**, in the function **initialize_db()** you should comment in lines **46,47,48** and you should comment out line **50**. Also in the functions **lookup_many(), lookup(), lookup_wik()** you should change the txt file names to a proper one, e.g. *wall_query_LOOKUP_results_sqlite_FSST_3.txt*.

In **generic.py**, in the function **__init__()** you should change the line **33** to *path_db = os.path.join(save_dir, f"{name}.db")* if it is not like this.


### Configuring REL to use DuckDB

In **base.py**, in the function **initialize_db()** you should comment out lines **46,47,48** (at least the line **46) and you should comment in line **50**. Also in the functions **lookup_many(), lookup(), lookup_wik()** you should change the txt file names to a proper one, e.g. *wall_query_LOOKUP_results_duckdb_FSST_3.txt*.

In **generic.py**, in the function **__init__()** you should change the line **33** to *path_db = os.path.join(save_dir, f"{name}.duckdb")* if it is not like this.


## Running the experiments

In **speed_analysis.py**, there are several functions : two preprocessing, two experiment methodologies and one entity-linking. The important one is entity-linking it is the same as API, so you should check about the **base_url** and the wiki version.

You can run either **speed_analysis_1()** (for the first methodology described in the paper) or **speed_analysis_2()** (for the other methodology). The name of the txt files must be the same with **base.py** 

After you run the experiments, you will see the created txt files. You should move them to the **Results** folder. After that change 
