#!/usr/bin/env python
import os
import xml.etree.ElementTree as ET
import shutil
import click


class SvnXml:
    """svn xml"""

    # svn log 命令
    EXEC_SVN_LOG = 'svn log %s -v -r %s --xml'

    # dist
    DIST = 'dist'

    # log
    LOG = 'log.txt'

    def __init__(self, svn_path, svn_revision):
        self.svn_path = svn_path
        self.svn_revision = svn_revision

        self.paths = []
        self.dist_path = []
        self.target_paths = []
        self.current_path = os.path.dirname(os.path.abspath(__file__))

        self.init_data()

    def init_data(self):
        """初始化相关数据"""
        svn_log_xml_str = ''.join(
            os.popen(self.EXEC_SVN_LOG % (self.svn_path, self.svn_revision))
        ).replace('\n', '')
        root = ET.fromstring(svn_log_xml_str)
        for paths in root.findall('./logentry/paths'):
            for path in paths:
                if path.attrib["kind"] == 'file':
                    self.paths.append(path.text)

                    self.dist_path.append(
                        self.current_path + os.path.sep + self.DIST + os.path.sep + self.svn_revision + os.path.sep + path.text
                    )
                    self.target_paths.append(
                        self.svn_path + path.text
                    )

    def copy_files(self):
        """copy file to dist"""
        log_txt_list = []
        for index, item in enumerate(self.target_paths):
            if os.path.exists(item):
                dist_path = self.dist_path[index]
                dist_dir = os.path.dirname(dist_path)
                if not os.path.exists(dist_dir):
                    os.makedirs(dist_dir)
                shutil.copyfile(item, self.dist_path[index])
                print('export:', item)
                log_txt_list.append(self.paths[index])
            else:
                print('file not found ：', item)

        f = open(self.current_path + os.path.sep + self.DIST + os.path.sep + self.svn_revision + os.path.sep + self.LOG, 'w+')
        f.write('\r\n'.join(log_txt_list))
        f.close()

@click.command()
@click.argument('dir')
@click.argument('revision')
def cli(dir, revision):
    svn_xml = SvnXml(dir, revision)
    svn_xml.copy_files()

cli()

