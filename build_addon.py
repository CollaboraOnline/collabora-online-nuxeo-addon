#!/usr/bin/env python3

import os
import shutil
import subprocess
from zipfile import ZipFile, ZIP_DEFLATED

def main():
    cwd = os.getcwd()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    productName = 'collaboraonline'

    workDir = 'workdir'
    if os.path.exists(workDir):
        shutil.rmtree(workDir)
    os.makedirs(workDir)

    destDir = 'dest'
    if os.path.exists(destDir):
        shutil.rmtree(destDir)
    os.makedirs(destDir)

    packageName = productName + '-nuxeo-wopi'
    jarBundleName = packageName + '.jar'
    jarBundlePath = os.path.join(workDir, jarBundleName)
    zipBundleName = packageName + '.zip'
    zipBundlePath = os.path.join(destDir, zipBundleName)

    # 1. Build JAR
    subprocess.run(['jar', 'cf', jarBundlePath, 'web', 'OSGI-INF']).check_returncode()

    # 2. Create ZIP
    with ZipFile(zipBundlePath, 'w') as myzip:
        myzip.write('package.xml', 'package.xml', ZIP_DEFLATED)
        myzip.write('install.xml', 'install.xml', ZIP_DEFLATED)
        for f in os.listdir('config'):
            myzip.write(os.path.join('config', f), 'install/config/' + f, ZIP_DEFLATED)
        for f in os.listdir('images'):
            myzip.write(os.path.join('images', f), 'install/images/' + f, ZIP_DEFLATED)
        myzip.write(jarBundlePath, 'install/bundles/' + jarBundleName, ZIP_DEFLATED)

    # Cleanup
    shutil.rmtree(workDir)
    os.chdir(cwd)

if __name__ == "__main__":
    main()

# vim:set shiftwidth=4 softtabstop=4 expandtab:
