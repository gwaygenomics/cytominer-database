"""

"""

import configparser
import glob
import odo
import os
import pandas as pd
import perturbation.ingest
import pytest
import subprocess
import tempfile

def test_seed(dataset):
    assert 1 == 1

    if dataset["munge"]:
        subprocess.call(["./munge.sh", dataset["data_dir"]])

    config_file = os.path.join(dataset["data_dir"], "config.ini")

    config = configparser.ConfigParser()

    config.read(config_file)

    with tempfile.TemporaryDirectory() as temp_dir:

        sqlite_file = os.path.join(temp_dir, "test.db")

        perturbation.ingest.seed(config=config, input=dataset["data_dir"], output="sqlite:///{}".format(str(sqlite_file)))

        image_csv = os.path.join(temp_dir, "image.csv")

        odo.odo("sqlite:///{}::{}".format(str(sqlite_file), "image"), image_csv)

        image_df = pd.read_csv(image_csv)

        assert image_df.shape[0] == dataset["ingest"]["image_nrows"]

        assert image_df.shape[1] == dataset["ingest"]["image_ncols"]