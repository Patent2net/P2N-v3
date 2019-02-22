# -*- coding: utf-8 -*-
# (c) 2017-2018 The Patent2Net Developers
import os
import json
import logging
from P2N_Lib import LoadBiblioFile, RenderTemplate
from P2N_Config import LoadConfig
from p2n.config import label_from_prefix
from p2n.util import boot_logging, to_png

logger_name = os.path.basename(__file__).replace('.py', '')
logger = logging.getLogger(logger_name)


# Configure designated size of generated thumbnails
THUMBNAIL_SIZE = 128, 128


def get_patent_label(patent):
    if isinstance(patent['label'], list):
        return patent['label'][0]
    return patent['label']


def generate_thumbnails(img_path):

    # Compute filenames and paths
    img_path = os.path.normpath(img_path)
    base_path, img_fname = os.path.split(img_path)
    filename, ext = os.path.splitext(img_fname)

    png_large_name = filename + '.png'
    png_thumb_name = filename + '.tb.png'

    png_large_path = os.path.normpath(os.path.join(base_path, png_large_name))
    png_thumb_path = os.path.normpath(os.path.join(base_path, png_thumb_name))

    # Convert original TIFF file to PNG format and also create a thumbnailed version.
    # Use Pillow, ImageMagick or other tooling.
    logger.info('Processing image "{}"'.format(img_path))
    with open(img_path, 'rb') as tiff:

        # Write original image in PNG format
        # Only process image if not already exists
        if not os.path.exists(png_large_path):
            png_large = to_png(tiff)
            with open(png_large_path, 'wb') as f:
                f.write(png_large.read())

        tiff.seek(0)

        # Write thumbnail image in PNG format
        # Only process image if not already exists
        if not os.path.exists(png_thumb_path):
            width, height = THUMBNAIL_SIZE
            png_thumb = to_png(tiff, width=width, height=height)
            with open(png_thumb_path, 'wb') as f:
                f.write(png_thumb.read())

    return png_thumb_name, png_large_name, img_fname


def run():

    # Bootstrap logging
    boot_logging()

    # Load configuration
    config = LoadConfig()

    # Run this only if enabled
    if not config.GatherImages:
        return

    # Get some information from configuration
    expression = config.requete
    storage_basedir = config.ResultBiblioPath
    storage_dirname = config.ndf
    output_path = config.ResultPathImages

    # Compute prefixes
    prefixes = [""]
    if config.GatherFamilly:
        prefixes.append("Families")

    # Build maps for all prefixes
    for prefix in prefixes:

        # Status message
        label = label_from_prefix(prefix)
        logger.info("Generating gallery of drawings for {}. ".format(label))

        # Compute storage slot using prefix and DataDirectory
        # e.g. "Lentille" vs. "FamiliesLentille"
        storage_name = prefix + storage_dirname

        # Load bibliographic data
        biblio_file = LoadBiblioFile(storage_basedir, storage_name)

        # Generate thumbnails
        gallery = []
        patents = biblio_file['brevets']
        for patent in patents:
            patent_label = get_patent_label(patent)
            i = 1
            logger.info('Processing patent {}'.format(patent_label))
            path_img_base = '{}//{}-{}.tiff'.format(output_path, patent_label, '{}')
            path = path_img_base.format(i)
            while os.path.exists(path):
                thumb, orig, tiff = generate_thumbnails(path)
                gallery.append({
                    "_id": '{}-{}'.format(patent_label, i),
                    'thumb': thumb,
                    'orig': orig,
                    'label': patent['title'],
                    'ipcr7': patent['IPCR7'],
                    'code': patent_label,
                    'tiff': tiff,
                })
                i += 1
                path = path_img_base.format(i)

        # Render gallery
        RenderTemplate(
            'ModeleImages.html',
            output_path + '/index' + prefix + '.html',
            request=expression.replace('"', ''),
            gallery=gallery,
            json=json.dumps(gallery),
        )


if __name__ == '__main__':
    run()
