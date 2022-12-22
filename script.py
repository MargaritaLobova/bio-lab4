import os
import re
from os.path import abspath

from toil.common import Toil
from toil.job import Job
import subprocess

minimap_path = abspath("./minimap2")
samtools_path = abspath("../samtools-1.9/samtools")
stats_file = abspath("stats.txt")
index_file = abspath("ref.index")
alignment_file = abspath("alignment.sam")

def index_ref_genom(ref_path):
    print("IM IN1")
    subprocess.call(f"{minimap_path} -d {index_file} {ref_path}", shell=True)


def compute_alignment(job, ref_path, actual_path):
    print("IM IN2")
    print(os.getcwd())
    subprocess.call(f"{minimap_path} -a {index_file} {actual_path} > {alignment_file}", shell=True)


def extract_stats(job):
    print("IM IN3")
    subprocess.call(f"{samtools_path} flagstat {alignment_file} > {stats_file}", shell=True)


def find_stat_accuracy(job):
    with open(stats_file) as f:
        file = " ".join(f.readlines())
        print(file)
        accuracy = float(re.findall(r"\d+\.\d+", file)[0])
        threshold = 90
        if accuracy > threshold:
            print("OK")
        else:
            print("NOT OK")



if __name__ == "__main__":
    parser = Job.Runner.getDefaultArgumentParser()
    options = parser.parse_args()
    options.clean = "always"
    ref_path = abspath(input("provide ref path: "))
    actual_path = abspath(input("provide actual path: "))
    with Toil(options) as toil:
        main_job = Job.wrapFn(index_ref_genom, ref_path)
        jobs = main_job\
            .addFollowOnJobFn(compute_alignment, ref_path, actual_path)\
            .addFollowOnJobFn(extract_stats)\
            .addFollowOnJobFn(find_stat_accuracy)

        output = toil.start(main_job)
    print(output)