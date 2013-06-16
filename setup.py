# -*- coding: utf-8 -*-
from distutils.core import setup
import py2exe,os

def add_path_tree( base_path, path, skip_dirs=[ '.svn', '.git' ]):

    path = os.path.join( base_path, path )

    partial_data_files = []

    for root, dirs, files in os.walk( os.path.join( path )):

        sample_list = []

        for skip_dir in skip_dirs:

            if skip_dir in dirs:

                dirs.remove( skip_dir )

        if files:

            for filename in files:

                sample_list.append( os.path.join( root, filename ))

        if sample_list:

            partial_data_files.append((

                root.replace(

                    base_path + os.sep if base_path else '',

                    '',

                    1

                ),

                sample_list

                ))

    print partial_data_files

    return partial_data_files

py2exe_data_files = add_path_tree( '', 'templates' )

setup(
    console=[{"script":"bootstrap.py"}],
    options={'py2exe':{'packages':['django','email']}},
    data_files=py2exe_data_files,
)