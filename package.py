# -*- coding: utf-8 -*-
# © 2018 WE Technology
# Authored by: Zhi Li (zealiemai@gmail.com)
import base64
import os
import shutil
import time
import zipfile

from config import IGNORE_FILES, AK, SK, FUNCTION_NAME
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.cfc.cfc_client import CfcClient

CFC_ZIP_NAME = 'cfc_pack.zip'
IGNORE_FILES.append(CFC_ZIP_NAME)
HOST = 'http://cfc.bj.baidubce.com'
config = BceClientConfiguration(credentials=BceCredentials(AK, SK), endpoint=HOST)
current_dirname = os.path.dirname(os.path.realpath(__file__))


def crypto_release():
    f = zipfile.ZipFile("Crypto.zip", 'r')
    for file in f.namelist():
        f.extract(file)
    f.close()


def delete_crypto():
    shutil.rmtree('Crypto')


def cfc_zip():
    crypto_release()

    f = zipfile.ZipFile(CFC_ZIP_NAME, 'w', zipfile.ZIP_DEFLATED)
    filelists = []
    get_dir_file(current_dirname, filelists, IGNORE_FILES)
    for file in filelists:
        file = '.%s' % file.replace(current_dirname, '')
        f.write(file)

    f.close()

    with open(CFC_ZIP_NAME, "rb") as f:
        bytes = f.read()
        base64_file_with_args = base64.b64encode(bytes)
        f.close()

    delete_crypto()

    print u'CFC zip packaging successful.'
    return base64_file_with_args


def get_dir_file(input_path, result, IGNORE_FILES=()):
    #
    files = os.listdir(input_path)
    for file in files:
        if file not in IGNORE_FILES:

            if os.path.isdir(input_path + '/' + file):
                get_dir_file(input_path + '/' + file, result, ())
            else:
                result.append(input_path + '/' + file)


def update_function_code():
    base64_file_with_args = cfc_zip()
    if base64_file_with_args:
        os.remove(CFC_ZIP_NAME)
        cfc_client = CfcClient(config)

        response = cfc_client.update_function_code(FUNCTION_NAME,
                                                   zip_file=base64_file_with_args,
                                                   publish=True)
        if response.status == 200:
            print u'CFC zip update successful.'
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


if __name__ == "__main__":
    update_function_code()
