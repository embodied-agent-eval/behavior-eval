from igibson.utils.assets_utils import show_progress,download_assets,download_ig_dataset
import argparse
import json
import logging
import os
import subprocess
import tempfile
from collections import defaultdict
from urllib.request import urlretrieve
import fire
import progressbar
import yaml
import behavior
import igibson

if os.name == "nt":
    import win32api
    import win32con

log = logging.getLogger(__name__)

pbar = None

def download_igibson_key():
    """
    Download iGibson key
    """
    while (
        input(
            "Do you agree to the terms for using iGibson key (http://svl.stanford.edu/igibson/assets/GDS_agreement.pdf)? [y/n]"
        )
        != "y"
    ):
        print("You need to agree to the terms for using iGibson key.")
        
    key_path = igibson.key_path  # Assuming igibson.key_path is defined elsewhere in the config
    url = "https://storage.googleapis.com/gibson_scenes/igibson.key"

    # Ensure the parent directory of key_path exists
    if not os.path.exists(os.path.dirname(key_path)):
        os.makedirs(os.path.dirname(key_path))

    # Download the file
    print("Downloading iGibson key from {}".format(url))
    urlretrieve(url, key_path,show_progress)
    print("iGibson key downloaded to {}".format(key_path))

def download_vr_demos():
    """
    Download behavior100 VR demos
    """
    if not os.path.exists(behavior.vr_demo_path):
        log.info("Creating iGibson dataset folder at {}".format(behavior.vr_demo_path))
        os.makedirs(behavior.vr_demo_path)

    url = "https://download.cs.stanford.edu/downloads/behavior/behavior_virtual_reality_v0.5.0.tar.gz"
    file_name = url.split("/")[-1]
    tmp_file = os.path.join(tempfile.gettempdir(), file_name)
    log.info("Downloading the behavior100 VR demos from {}".format(url))
    urlretrieve(url, tmp_file, show_progress)
    log.info("Decompressing the behavior100 VR demos into {}".format(behavior.vr_demo_path))
    os.system("tar -zxf {} --strip-components=1 --directory {}".format(tmp_file, behavior.vr_demo_path))
    # These datasets come as folders; in these folder there are scenes, so --strip-components are needed.

from typing import Optional
def main(download_option: Optional[str] = "all"):
    if download_option=="all":
        download_igibson_key()
        download_ig_dataset()
        download_assets()
        download_vr_demos()
    elif download_option=="igibson_key":
        download_igibson_key()
    elif download_option=="ig_dataset":
        download_ig_dataset()
    elif download_option=="assets":
        download_assets()
    elif download_option=="vr_demos":
        download_vr_demos()
        
if __name__ == "__main__":
    fire.Fire(main)