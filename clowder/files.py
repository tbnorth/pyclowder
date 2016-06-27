"""Clowder API

This module provides simple wrappers around the clowder Files API
"""

import json
import logging
import os
import tempfile

import requests


def download_file(connector, host, key, fileid, intermediatefileid, ext=""):
    """Download file to be processed from Clowder.

    Keyword arguments:
    connector -- connector information, used to get missing parameters and send status updates
    host -- the clowder host, including http and port, should end with a /
    key -- the secret key to login to clowder
    fileid -- the file that is currently being processed
    intermediatefileid -- either same as fileid, or the intermediate file to be used
    ext -- the file extension, the downloaded file will end with this extension
    """

    connector.status_update(fileid=fileid, status="Downloading file.")

    url = '%sapi/files/%s?key=%s' % (host, intermediatefileid, key)
    result = requests.get(url, stream=True, verify=connector.ssl_verify)
    result.raise_for_status()
    (inputfile, inputfilename) = tempfile.mkstemp(suffix=ext)
    with os.fdopen(inputfile, "w") as outputfile:
        for chunk in result.iter_content(chunk_size=10*1024):
            outputfile.write(chunk)
    return inputfilename


def upload_file_metadata_jsonld(connector, host, key, fileid, metadata):
    """Upload file JSON-LD metadata to Clowder.

    Keyword arguments:
    connector -- connector information, used to get missing parameters and send status updates
    host -- the clowder host, including http and port, should end with a /
    key -- the secret key to login to clowder
    fileid -- the file that is currently being processed
    metadata -- the metadata to be uploaded
    """

    connector.status_update(fileid=fileid, status="Uploading file metadata.")

    headers = {'Content-Type': 'application/json'}
    url = '%sapi/files/%s/metadata.jsonld?key=%s' % (host, fileid, key)
    result = requests.post(url, headers=headers, data=json.dumps(metadata),
                           verify=connector.ssl_verify)
    result.raise_for_status()


def upload_file_thumbnail(connector, host, key, fileid, thumbnail):
    """Upload thumbnail to Clowder.

    Keyword arguments:
    connector -- connector information, used to get missing parameters and send status updates
    host -- the clowder host, including http and port, should end with a /
    key -- the secret key to login to clowder
    fileid -- the file that the thumbnail should be associated with
    thumbnail -- the file containing the thumbnail
    """

    logger = logging.getLogger(__name__)
    url = host + 'api/fileThumbnail?key=' + key

    # upload preview
    with open(thumbnail, 'rb') as inputfile:
        files = {"File": inputfile}
        result = requests.post(url, files=files, verify=connector.ssl_verify)
        result.raise_for_status()
    thumbnailid = result.json()['id']
    logger.debug("preview id = [%s]", thumbnailid)

    # associate uploaded preview with orginal file/dataset
    if fileid:
        headers = {'Content-Type': 'application/json'}
        url = host + 'api/files/' + fileid + '/thumbnails/' + thumbnailid + '?key=' + key
        result = requests.post(url, headers=headers, data=json.dumps({}),
                               verify=connector.ssl_verify)
        result.raise_for_status()

    return thumbnailid