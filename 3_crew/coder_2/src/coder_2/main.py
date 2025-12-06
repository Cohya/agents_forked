#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from coder_2.crew import Coder2

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

assignment = "Write a python program to calculate the first 10,000 terms \
    of this series, multiplying the total by 4: 1 - 1/3 + 1/5 - 1/7 + ..."


def run():
   inputs = {"assignment": assignment}
   results = Coder2().crew().kickoff(inputs=inputs)
   print(results.raw)

