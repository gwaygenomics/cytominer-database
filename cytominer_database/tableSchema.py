import os
import csv
import click
import warnings
import zlib
import pandas as pd
import backports.tempfile
import sqlalchemy.exc
from sqlalchemy import create_engine
import pyarrow
import pyarrow.parquet as pq
import pyarrow.csv
import numpy as np
import collections
import numpy as np
import cytominer_database
import cytominer_database.utils
import cytominer_database.load

################################################################################
# Contains "open_writers()"" to generate the dictionary containing the
# reference data ("writer dictionary"), from which the table schemata will be generated.
# The reference tables can either be loaded directly from a designated folder,
# or sampled across all available data, as specified in the config_file.
#
# Also contains helper functions "get_grouped_table_paths()" and "get_dict_of_paths()"
# to generate a list of paths
# and the sampling function get_reference_paths().
################################################################################



def open_writers(source, target, config_file, skip_image_prefix=True):
    """
    Determines, loads reference tables and openes them as ParquetWriters.
    Returns a dictionary referencing the writers.
    :param source: path to directory containing all parent folders of .csv files
    :target: output file path
    :config_file: parsed configuration data (output from cytominer_database.utils.read_config(config_path))
    :skip_image_prefix: Boolean value specifying if the column headers of
     the image.csv files should be prefixed with the table name ("Image").
    """
    writers_dict = {}  # nested dictionary: dict in dict
    engine = config_file["ingestion_engine"]["engine"]
    reference = config_file["schema"]["reference_option"]

    print("engine = ", engine)
    print("reference = ", reference)

    if engine == "SQLite": # no reference table needed
        return writers_dict

    if reference == "sample": 
        # Idea: sample from all tables contained in the subdirectories of source.
        # Get all possible reference directories for each table kind, as stored in the dictionary
        directories = sorted(list(cytominer_database.utils.find_directories(source)))
        grouped_full_paths = get_grouped_table_paths_from_directory_list(directories)
        # get sample size (as fraction of all available files) from config file
        ref_fraction = float(config_file["schema"]["ref_fraction"])
        # build reference dictionary
        ref_dir = get_reference_paths(ref_fraction, grouped_full_paths)

        # ---------------- print statements ----------------
        # print("open_writers: reference == 'sample' ")
        # print("ref_fraction", ref_fraction)
        # print("grouped_full_paths", grouped_full_paths)
        # print("ref_dir", ref_dir)
        # --------------------------------------------------

    else: # elif os.path.isdir(os.path.join(source, reference))
        print("reference == ", reference)
        print("open_writers: reference != 'sample' ")
        #'reference' is a path to the folder containing all reference tables (no sampling)
        reference_folder = os.path.join(source, reference)
        assert os.path.isdir(reference_folder)
        ref_dir = get_dict_of_paths(
            reference_folder
        )  # returns values as single string in a dict
        print("------------- in open_writers(): --------------")
        print("ref_dir", ref_dir)

        
    refIdentifier = 999 & 0xFFFFFFFF
    # arbitrary identifier, will not be stored but used only as type template. (uint32 as in checksum())
    # Iterate over all table kinds:
    for name, path in ref_dir.items():  # iterates over keys of the dictionary ref_dir
        print("name", name)
        print("path", path)
        # unpack path from [path]
        if isinstance(path, list):
            path = path[0]
        print(
            ">>>>>>>>>>>>>>>> In open_writers(): ", name, " <<<<<<<<<<<<<<<<<<<<<<<<,"
        )
        # load dataframe
        ref_df = cytominer_database.load.get_and_modify_df(path, refIdentifier, skip_image_prefix)
            
  
        # ---------------------- temporary -------------------------------------
        #refPyTable_before_conversion = pyarrow.Table.from_pandas(ref_df)
        #ref_schema_before_conversion = refPyTable_before_conversion.schema[0]
        print("------ In open_writers(): ref_schema_before_conversion --------")
        # print(ref_schema_before_conversion)
        # ----------------------------------------------------------------------
        type_conversion = config_file["schema"]["type_conversion"]
        print(
            "------ In open_writers(): type_conversion: ", type_conversion, "--------"
        )
        if type_conversion == "int2float":
            ref_df = cytominer_database.utils.convert_cols_int2float(
                ref_df
            )  # converts all columns int -> float (except for "TableNumber")
            print("------ converted ref_pandas_df to float --------")
        elif type_conversion == "all2string":
            ref_df = cytominer_database.utils.convert_cols_2string(ref_df)
            print("------ converted ref_pandas_df to string --------")

        ref_table = pyarrow.Table.from_pandas(
            ref_df
        )
        ref_schema = ref_table.schema
        # print("------ In open_writers(): ref_schema (after conversion)")
        # ref_schema_after_conversion = ref_schema[0]
        # print(ref_schema_after_conversion)
        destination = os.path.join(
            target, name + ".parquet"
        )
        writers_dict[name] = {}
        writers_dict[name]["writer"] = pq.ParquetWriter(
            destination, ref_schema, flavor={"spark"}
        )
        writers_dict[name]["schema"] = ref_schema
        writers_dict[name]["pandas_dataframe"] = ref_df
    return writers_dict

def get_grouped_table_paths_from_directory_list(directories):
    """
    Returns a dictionary holding a list of all full paths (as value) for every table kind (key).
    Example: directories = ["path/plate_a/set_1" , "path/plate_a/set_2"] returns
     grouped_table_paths = {"Cells": ["path/plate_a/set_1" , "path/plate_a/set_2"], ...
     "Cytoplasm": ["path/plate_a/set_1" , "path/plate_a/set_2"]}
     if set_1 and set_2 both contain the files "Cells.csv" and "Cytoplasm.csv" (and no other files).

    :param directories: list of directories in which .csv files are stored, e.g. "path/plate_a/set_1" , "path/plate_a/set_2"].
    """
    # Notes:
    # - The argument "source" specifies the parent directory, from which all
    #  subdirectories will be read and sorted and used to get all full paths to
    #  all tables, separately for each table kind. This argument is used when
    #  the function is called from "open_writers()"", for the option 'sampling'.
    # - The function returns a dictionary to "open_writers()"". It is then passed to "get_reference_paths()",
    #   which samples paths from the lists and selects the reference table among them.
    # - Attention: returns a dictionary with value = list, even if there is only a single element
    # - Option: We could include the old csv-validation (cytominer_database.utils.validate_csv_set(config_file, directory))

    # initialize dictionary that will be returned
    grouped_table_paths = {}
    # iterate over all (sub)directories.
    for directory in directories:
        # Get the names of all files in that directory (e.g. Cells.csv)
        filenames = os.listdir(directory)
        for filename in filenames:
            # get full path
            fullpath = os.path.join(directory, filename)
            name = cytominer_database.utils.get_name(fullpath) 

            # initialize dictionary entry if it does not exist yet
            if name not in grouped_table_paths.keys():
                grouped_table_paths[name] = []
            # extend the list of paths by current path
            grouped_table_paths[name] += [fullpath]
    return grouped_table_paths





def get_dict_of_paths(folder):
    """
    Returns a dictionary with key: name (table kind), value = path string.
    :folder: path to folder that contains tables
    Example: "path/plate_a/special_set"
    """
    # Note: similar to get_grouped_table_paths(source, directories=None),
    # Difference: Dictionary values are a single table path for each table kind
    # that is contained in a single directory "folder".
    # Does not accept a list of directories as an input
    # and does not return a list of all table paths under a source directory.
    # We could include the old csv-validation (cytominer_database.utils.validate_csv_set(config_file, directory))
    return_dict = {}
    filenames = os.listdir(folder)
    for filename in filenames:
        fullpath = os.path.join(folder, filename)
        name = cytominer_database.utils.get_name(fullpath) # to prettify: check if name = cytominer_database.utils.get_name(filename) would also work
        return_dict[name] = fullpath  # attention: path may be overwritten here.
    return return_dict

def get_reference_paths(ref_fraction, full_paths):
    """
    Samples a subset of all existing full paths and determines the reference table among them.
    Returns a dictionary with key: name (table kind), value = full path to reference table.
    :ref_fraction: fraction of all paths to be compared (relative sample set size).
    :full_paths: dictionary containing a list of all full table paths for each table kind
    Example: {Image: [path/plate_a/set_1/image.csv, path/plate_a/set_2/image.csv,... ], Cells: [path/plate_a/set_1/Cells.csv, ...], ...}
    """
    print(" ------------------- Entering get_reference_paths() -------------------")
    # Note: returns full paths, not parent directories
    # -------------------------------------------------
    #  - samples only among directories in which that table kind exists.
    #  - sample by taking the first n element after permuting the list elements at random
    #  - option to pass a custom list of directories among which to sample
    #     (default is None, then the list of all existing directories is derived from source)
    # -------------------------------------------------
    # Note: if directories are passed
    # 0. initialize return dictionary
    ref_dirs = {}
    # print("full_paths: " , full_paths)
    # 1. iterate over table types
    for key, value in full_paths.items():  # iterate over table types
        # print("--------------------- In get_reference_paths(): Getting ref for table type : ", key, "---------------------")
        # 2. Permute the table list at random
        # print("dict value : ", np.random.shuffle(value))
        np.random.shuffle(value)  # alternative: assign to new list
        # print("Shuffled dict values : value = ", value)
        # 3. get first n items corresponding to fraction of files to be tested (among the number of all tables present for that table kind)
        # --------------------------- constants ----------------------------------
        sample_size = int(np.ceil(ref_fraction * len(value)))
        # print("sample_size", str(sample_size))
        # --------------------------- variables ----------------------------------
        max_width = 0
        # ------------------------------------------------------------------------
        for path in value[
            :sample_size
        ]:  # iterate over random selection of tables of that type
            # read first row of dataframe
            # check if path leads to a valid, non-empty file
            # if cytominer_database.utils.validate_csv(path) == "No errors.": ---> does not work
            if cytominer_database.utils.validate_csv(path):
                df_row = pd.read_csv(path, nrows=1)
                # print("df_row", df_row)
                # print("df_row.shape[1]", df_row.shape[1])
                # check if it beats current best (widest table)
                if df_row.shape[1] > max_width:  # note: .shape returns [length, width]
                    # update
                    # print("updated max_width = ", str(max_width))
                    max_width = df_row.shape[1]
                    # print("to max_width = ", str(max_width))
                    ref_dirs[key] = path
            elif sample_size < len(value) : # invalid file, but not all files were sampled yet
                sample_size += 1 # get a substitute sample file
    print(" ------------------- Leaving get_reference_paths() -------------------")
    return ref_dirs
