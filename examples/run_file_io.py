# Copyright 2017 The Vispek Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==========================================================================
""" Example code about how to run file_io

python3 -m vispeck.examples.run_filo_io \
        --in_path /Users/huaminli/Downloads/data \
        --out_path /Users/huaminli/Desktop/vispek/data
"""

import argparse

from vispek.lib.io.file_io import FileIO

def run_file_io(args):
    my_file_io = FileIO(args.in_path, args.out_path)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(
        description='Example code about how tun run file_io')
    parser.add_argument(
        '--in_path', type=str,
        help='absolute path to the directories that contains raw csv files')

    parser.add_argument(
        '--out_path', type=str,
        help='absolute path to the directories that contains ' + 
             'preproceed files')
    args = parser.parse_args()
    
    print(args.in_path)
    print(args.out_path)

    run_file_io(args)
