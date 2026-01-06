import fnmatch
import os
import shutil
import sys
from pathlib import Path
from shutil import copyfile, copytree, rmtree

from mkdocs.config import config_options
from mkdocs.config.base import Config
from mkdocs.plugins import BasePlugin, get_plugin_logger

log = get_plugin_logger(__name__)


class IncludeFilesPluginConfig(Config):
    temp_location = config_options.Type(str, default="includes")
    search_syntax = config_options.Type(list, default=[])
    search_paths = config_options.Type(list, default=["."])


class IncludeFilesPlugin(BasePlugin[IncludeFilesPluginConfig]):
    def on_pre_build(self, config):
        "runs before files are loaded so its a good time to copy the include files over"

        # get directory containing mkdocs.yml
        mkdocs_yml_dir = Path(config.config_file_path)

        # get path to include directory
        include_dir = (
            Path(config.docs_dir) / config.plugins["include-files"].config.temp_location
        )

        # search the search path for files that match the search syntax
        for search_pattern in config.plugins["include-files"].config.search_syntax:
            for dir in config.plugins["include-files"].config.search_paths:
                for filename in Path(dir).glob(search_pattern):
                    # copy file to include dir
                    dest = include_dir.joinpath(filename.relative_to(dir))
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    copyfile(filename, str(dest))
                    log.info(f"Copying {filename} to {dest}")

    def on_post_build(self, config):
        include_dir = (
            Path(config.docs_dir) / config.plugins["include-files"].config.temp_location
        )
        rmtree(include_dir)
        ...
