import logging
import os
import pickle
import shutil
import traceback

from debuggingbook.bookutils import show_ast

from ast import NodeTransformer, parse
import ast
from debuggingbook.Slicer import (
    TrackGetTransformer, TrackSetTransformer, 
    TrackReturnTransformer, TrackControlTransformer, 
    TrackParamsTransformer, TrackCallTransformer, Slicer, 
    dump_tree)
from pathlib import Path
from types import FrameType
from typing import List, Any, Set, Dict, Tuple

from debuggingbook.StatisticalDebugger import ContinuousSpectrumDebugger, Collector, RankingDebugger

DependencyDict = Dict[
    str,
    Set[
        Tuple[
            Tuple[str, Tuple[str, int]],
            Tuple[Tuple[str, Tuple[str, int]], ...]
        ]
    ]
]
def instrumentFile(fileUrl: Path, dest_directory: Path, parentDirectory: Path = None):
    filePath = str(fileUrl.absolute())
    fileName = str(fileUrl.name)

    with open(filePath) as file:
        newFile = open(fileName, "w")
        newFile.write("from lib import _data")
        sourceCode = ""
        
        for line in file:
            sourceCode += line.rstrip() +"\n"
        middle_tree = parse(sourceCode)
        s = Slicer()
        s.transform(middle_tree)
        sourceCodeInstrumented = (ast.unparse(middle_tree))
        newFile.write("\n")
        for line in sourceCodeInstrumented:
            newFile.write((line+ ""))
        newFile.close()

        if parentDirectory == None:
            entry = fileName
            newFile = open(dest_directory.absolute() / entry, "w")
            newFile.close()
            shutil.copy((entry), dest_directory / entry )
            
        else:
            entry = str(parentDirectory.name) +"\\"+ fileName
            os.makedirs((dest_directory.absolute() / str(parentDirectory.name)), exist_ok=True)
            newFile = open(dest_directory.absolute() / str(parentDirectory.name) / fileName, "w+")
            newFile.close()
            shutil.copy(fileName, dest_directory.absolute() / str(parentDirectory.name) / fileName)
            shutil.copy('lib.py', dest_directory / str(parentDirectory.name) / 'lib.py')
            
class Instrumenter(NodeTransformer):

    def instrument(self, source_directory: Path, dest_directory: Path, excluded_paths: List[Path], log=False) -> None:

        """
        TODO: implement this function, such that you get an input directory, instrument all python files that are
        TODO: in the source_directory whose prefix are not in excluded files and write them to the dest_directory.
        TODO: keep in mind that you need to copy the structure of the source directory.
        :param source_directory: the source directory where the files to instrument are located
        :param dest_directory:   the output directory to which to write the instrumented files
        :param excluded_paths:   the excluded path that should be skipped in the instrumentation
        :param log:              whether to log or not
        :return:
        """

        if log:
            logging.basicConfig(level=logging.INFO)

        assert source_directory.is_dir()

        if dest_directory.exists():
            shutil.rmtree(dest_directory)
        os.makedirs(dest_directory)

        shutil.copy('lib.py', dest_directory / 'lib.py')

        for directory, sub_directories, files in os.walk(source_directory):
            # Iterates directory and its subdirectories in the form of (directory, [sub_directories], [files])
            logging.info(f'Current dir: {directory}')
            logging.info(f'Current sub_dirs: {sub_directories}')
            logging.info(f'Current files: {files}')
            

        for entry in source_directory.iterdir():
            fileExcluded = False
            if entry in excluded_paths:
               fileExcluded = True
            if entry.is_file() and fileExcluded == False:
               instrumentFile(entry, dest_directory)
            elif entry.is_file() and fileExcluded == True:
                try: 
                    fileName = str(entry.name)
                    newFile = open(dest_directory.absolute() / fileName, "w")
                    newFile.close()
                    shutil.copy((entry), dest_directory / fileName )
                except:
                    print(traceback.format_exc())
            if entry.is_dir():
                fileExcluded = False
                for subEntry in entry.iterdir():
                    if subEntry in excluded_paths:
                        fileExcluded = True
                    if subEntry.is_file() and fileExcluded == False:
                        instrumentFile(subEntry, dest_directory, entry)
                    if subEntry.is_file() and fileExcluded == True:
                        try:
                            fileName = str(entry.name) +"\\"+ str(subEntry.name)
                            newFile = open(dest_directory.absolute() / fileName, "w")
                            newFile.close()
                            
                            shutil.copy((subEntry), dest_directory / fileName )                            
                        except:
                            print(traceback.format_exc())


class DependencyCollector(Collector):

    def __init__(self, dump_path: Path):
        super().__init__()
        self.dump_path = dump_path
        self.dependencies = []

    def traceit(self, frame: FrameType, event: str, arg: Any) -> None:
        pass  # deactivate tracing overall, not required.

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with open(self.dump_path, 'rb') as dump:
            deps = pickle.load(dump)
        self.collect(deps)

    def collect(self, dependencies: DependencyDict):
        """
        TODO: Collect the dependencies in the specified format.
        :param dependencies: The dependencies for a run
        :return:
        """
        self.dependencies = dependencies
    pass

    def events(self) -> Set[Any]:
        newDependencies = set()
        for dep in self.dependencies["data"]:
            newDependencies.add(dep)
        for dep in self.dependencies["control"]:
            newDependencies.add(dep)
        return newDependencies
    

def extractFunctions(data):
    newDependencies = set()
    for dep in data:
            for subDep in dep:
                if len(subDep) > 0:
                    for sSubDep in subDep:
                        #print(sSubDep)
                        if type(sSubDep) is tuple:
                            if any(isinstance(x, tuple) for x in sSubDep):
                                for sSSubDep in sSubDep:
                                    if type(sSSubDep) is tuple:
                                        newDependencies.add(sSSubDep)
                                        #print(sSSubDep)        
                            else:
                                newDependencies.add(sSubDep)
    return newDependencies
class CoverageDependencyCollector(DependencyCollector):

    def events(self) -> Set[Any]:
        newDependencies = set()
        first = (extractFunctions(self.dependencies["data"]))
        for ele in first:
            if ele in newDependencies:
                pass
            else:
                newDependencies.add(ele)
        
        first = (extractFunctions(self.dependencies["control"]))
        for ele in first:
            if ele in newDependencies:
                pass
            else:
                newDependencies.add(ele)
                    
        #for dep in newDependencies:
        #    print(dep)
        
        """ for dep in self.dependencies["control"]:
            for subDep in dep:
                if len(subDep) > 0:
                    for sSubDep in subDep:
                        #print(sSubDep)
                        if type(sSubDep) is tuple:
                            if any(isinstance(x, tuple) for x in sSubDep):
                                for sSSubDep in sSubDep:
                                    if type(sSSubDep) is tuple:
                                        newDependencies.add(sSSubDep)
                                        #print(sSSubDep)        
                            else:
                                newDependencies.add(sSubDep) """
                                #print(sSubDep)
                        #if len(sSubDep) == 2:
                        #    print("Special",sSubDep)
                        #    newDependencies.add(sSubDep)
                            

                            
#        for dep in newDependencies:
#            print(dep)
        return newDependencies


class DependencyDebugger(ContinuousSpectrumDebugger, RankingDebugger):
    def __init__(self, coverage=False, log: bool = True):
        super().__init__(CoverageDependencyCollector if coverage else DependencyCollector, log)
