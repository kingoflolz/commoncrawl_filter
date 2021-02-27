import subprocess
import multiprocessing
from multiprocessing import set_start_method
from functools import partial
from tqdm import tqdm

import sys
import pathlib

set_start_method("spawn")

def process_wat(url, output_path):
    output_name = url.split("/")[-1].replace(".warc.wat.gz", ".jsonl.wat.gz")
    dir_name = url.split("/")[1]

    pathlib.Path(f"{output_path}/{dir_name}/").mkdir(parents=True, exist_ok=True)
    subprocess.run(["./commoncrawl_filter", "http://commoncrawl.s3.amazonaws.com/" + url, f"{output_path}/{dir_name}/{output_name}".strip()], timeout=3600)


assert len(sys.argv) == 4

f = open(sys.argv[2])
p = multiprocessing.Pool(int(sys.argv[1]))
process = partial(process_wat, output_path=sys.argv[3])

list(tqdm(p.imap_unordered(process, f)))