# -*- coding: utf-8 -*-
# (c) 2017-2018 The Patent2Net Developers
import os
import sys
import time
import types
import where
import logging
import operator
import functools
import itertools
import traceback
import subprocess
from six import StringIO, BytesIO
from json.encoder import JSONEncoder
from collections import OrderedDict

logger = logging.getLogger(__name__)


def setup_logging(level=logging.INFO):
    log_format = '%(asctime)-15s [%(name)-25s] %(levelname)-7s: %(message)s'
    logging.basicConfig(
        format=log_format,
        stream=sys.stderr,
        level=level)


def boot_logging(options=None):
    log_level = logging.INFO
    if options and options.get('--debug'):
        log_level = logging.DEBUG
    setup_logging(level=log_level)


def normalize_docopt_options(options):
    normalized = {}
    for key, value in options.items():
        key = key.strip('--<>')
        normalized[key] = value
    return normalized


def run_script(script, configfile, directory='Patent2Net'):

    # Compute command
    command = 'python {script} {configfile}'.format(script=script, configfile=configfile)
    logger.info('Running command "{}"'.format(command))

    # Run process
    process = subprocess.Popen(command, shell=True, bufsize=1, cwd=directory)

    # Poll process for new output until finished
    while True:

        try:
            outcome = process.poll()

            if outcome is not None:
                returncode = process.returncode
                if returncode != 0:
                    logger.error(
                        'Command "{command}" failed with return code {returncode}'.format(**locals()))
                return returncode

            time.sleep(1)

        except KeyboardInterrupt:
            logger.warning('Terminating script {}'.format(script))
            process.terminate()
            process.wait()
            return process.returncode


def memoize(obj):
    """
    https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
    """
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]

    return memoizer


def to_list(obj):
    """Convert an object to a list if it is not already one"""
    if not isinstance(obj, (list, tuple)):
        obj = [obj, ]
    return obj


def filterdict(dct, keys=None):
    """Filter dictionaries using specified keys"""
    keys = keys or []
    dct = {key: value for (key, value) in dct.iteritems() if key in keys}
    return dct


def dictproduct(dct):
    """
    Compute combinations from dictionary with list values
    by calculating the cartesian product.
    """
    # https://stackoverflow.com/questions/3873654/combinations-from-dictionary-with-list-values-using-python/41870264#41870264

    # Bring dictionary into a form suitable for computing the cartesian product
    for key, value in dct.iteritems():

        # Use empty string for empty values
        if value is None or value == [] or value == [None]:
            value = ''

        # Let's make everything a list
        value = to_list(value)

        dct[key] = value

    # Yield dictionaries making up all combinations of multiple values
    # reduced to dictionaries containing single scalar values only.
    for t in itertools.product(*dct.itervalues()):
        yield dict(zip(dct.iterkeys(), t))


class JsonObjectEncoder(JSONEncoder):
    """
    Serialize nested object compositions to JSON
    """

    def default(self, o):
        # TODO: Maybe use "o.asdict()"?
        return o.__dict__


def unique(data):
    return list(set(data))


def object_to_dictionary(obj, rules):
    """
    Transform object to dictionary according to set of rules.
    For an example, see ``p2n.formatter.tables.pivottables_data_documents``.

    TODO: Provide examples of rule format, input and output data.
    """

    data = OrderedDict()

    for rule in rules:
        key = value = None

        if isinstance(rule, types.StringType):
            key = rule
            try:
                value = operator.attrgetter(rule)(obj)
            except AttributeError:
                pass

        elif isinstance(rule, types.DictionaryType):
            key = rule['name']
            value = rule['getter'](obj)

            if 'recipe' in rule:
                recipe = rule['recipe']
                value = recipe(value)

        if key:
            data[key] = value

    return data


def exception_traceback(exc_info=None):
    """
    Return a string containing a traceback message for the given
    exc_info tuple (as returned by sys.exc_info()).

    from setuptools.tests.doctest
    """

    if not exc_info:
        exc_info = sys.exc_info()

    # Get a traceback message.
    excout = StringIO()
    exc_type, exc_val, exc_tb = exc_info
    traceback.print_exception(exc_type, exc_val, exc_tb, file=excout)
    return excout.getvalue()


@memoize
def find_convert():
    """
    Debian: aptitude install imagemagick
    /usr/bin/convert

    Mac OS X with Homebrew
    /usr/local/bin/convert

    Mac OS X with Macports
    /opt/local/bin/convert

    Self-compiled
    /opt/imagemagick/bin/convert
    /opt/imagemagick-7.0.2/bin/convert
    """

    # Some nailed location candidates
    candidates = [
        '/opt/imagemagick-7.0.2/bin/convert',
        '/opt/imagemagick/bin/convert',
        '/usr/local/bin/convert',
        '/opt/local/bin/convert',
        '/usr/bin/convert',
    ]

    # More location candidates from the system
    candidates += where.where('convert')

    # Find location of "convert" program
    convert_path = find_program_candidate(candidates)

    logger.info('Found "convert" program at {}'.format(convert_path))
    return convert_path


def find_program_candidate(candidates):
    for candidate in candidates:
        if os.path.isfile(candidate):
            return candidate


def to_png(tiff, width=None, height=None):
    """
    Convert image to PNG format with optional resizing.

    :param tiff: A stream buffer object like BytesIO
    :param width: The width of the image in pixels (optional)
    :param height: The height of the image in pixels (optional)
    :return: A BytesIO object instance containing image data
    """

    """
    The PIL module didn't properly support TIFF images with G4 compression::

        Failure: exceptions.IOError: decoder group4 not available
        Maybe patch: http://mail.python.org/pipermail/image-sig/2003-July/002354.html

    Nowadays, this should be supported by Pillow on recent platforms:
    https://pillow.readthedocs.io/en/latest/releasenotes/5.0.0.html#compressed-tiff-images
    """
    try:
        from PIL import Image

        # Read image
        image = Image.open(tiff)

        if width and height:

            # Convert image to grayscale
            image = image.convert('L')

            # Resize image
            image.thumbnail((width, height), Image.LANCZOS)

        # Save image into a stream buffer
        png = BytesIO()
        image.save(png, 'PNG')

        # Readers should start reading at the beginning of the stream
        png.seek(0)

        return png

    except Exception as ex:
        logger.warning('Image conversion using "Pillow" failed: {}'.format(ex))

    """
    However, if the conversion using "Pillow" fails for some reason,
    let's try to use the "convert" utility from ImageMagick.


    Instructions for installing ImageMagick on Debian::
        apt install imagemagick
    Instructions for installing ImageMagick on Windows::
        https://www.imagemagick.org/script/download.php#windows
    Instructions for building ImageMagick on Debian::
        # https://packages.debian.org/source/wheezy/imagemagick
        aptitude install build-essential checkinstall ghostscript libbz2-dev libexif-dev fftw-dev libfreetype6-dev libjasper-dev libjpeg-dev liblcms2-dev liblqr-1-0-dev libltdl-dev libpng-dev librsvg2-dev libtiff-dev libx11-dev libxext-dev libxml2-dev zlib1g-dev liblzma-dev libpango1.0-dev
        ./configure --prefix=/opt/imagemagick-7.0.2
        wget http://www.imagemagick.org/download/ImageMagick.tar.gz
        # untar and cd
        make -j6 && make install
    """

    more_args = []

    # Compute value for "resize" parameter
    size = ''
    if width or height:

        if width:
            size += str(width)

        # Use "x" for separating "width" and "height" when resizing
        size += 'x'

        if height:
            size += str(height)

        more_args += ['-resize', size]

    convert = find_convert()
    if not convert:
        message = 'Could not find ImageMagick program "convert", please install from e.g. https://imagemagick.org/'
        logger.error(message)
        raise AssertionError(message)

    command = [
        convert,
        '+set', 'date:create', '+set', 'date:modify',
        '-define', 'stream:buffer-size=0',
        '-colorspace', 'rgb', '-flatten', '-depth', '8',
        '-antialias', '-quality', '100', '-density', '300',
        # '-level', '30%,100%',

        # Debugging
        # (see "convert -list debug")
        #'-verbose',
        #'-debug', 'All',

    ] \
        + more_args + \
        [

        # Convert from specific format
        #'{0}:-'.format(format),

        # Convert from any format
        '-',

        # Convert to PNG format
        'png:-',
    ]

    command_string = ' '.join(command)
    try:
        logger.debug('Converting image using "{}"'.format(command_string))
        return run_imagemagick(command, tiff.read())

    except Exception as ex:
        logger.error('Image conversion using ImageMagicks "convert" program failed: {}'.format(ex))
        raise


def run_imagemagick(command, input=None):
    output = run_command(command, input)
    if 'ImageMagick' in output.read()[:200]:
        command_string = ' '.join(command)
        message = 'Image conversion failed, found "ImageMagick" in STDOUT. Command was "{}"'.format(
            command_string)
        logger.error(message)
        raise RuntimeError(message)
    output.seek(0)
    return output


def run_command(command, input=None):

    command_string = ' '.join(command)

    proc = subprocess.Popen(
        command,
        #shell = (os.name == 'nt'),
        #shell = True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    stdout = stderr = ''
    try:
        stdout, stderr = proc.communicate(input)
        if proc.returncode is not None and proc.returncode != 0:
            message = 'Command "{}" failed, returncode={}, stderr={}'.format(
                command_string, proc.returncode, stderr)
            logger.error(message)
            raise RuntimeError(message)

    except Exception as ex:
        if isinstance(ex, RuntimeError):
            raise
        else:
            message = 'Command "{}" failed, returncode={}, exception={}, stderr={}'.format(
                command_string, proc.returncode, ex, stderr)
            logger.error(message)
            raise RuntimeError(message)

    return BytesIO(stdout)

    """
    # Use Delegator.py for process execution

    # Currently, there seem to be problems using both binary STDIN and STDOUT:
    # https://github.com/kennethreitz/delegator.py/issues/51
    # Let's try again soon.

    #proc = delegator.run(command)
    #proc = delegator.run(command, block=True, binary=True)
    proc = delegator.run(command, block=False, binary=True)

    # https://github.com/kennethreitz/delegator.py/issues/50
    #proc.blocking = False
    proc.send(tiff.read())
    #proc.subprocess.send(tiff.read() + b"\n")
    proc.block()
    #print 'out:', proc.out
    print 'self.blocking:', proc.blocking
    print 'self._uses_subprocess:', proc._uses_subprocess
    print 'self.subprocess:', proc.subprocess

    print 'stdout-1:', proc.std_out
    stdout = proc.std_out.read()
    print 'stdout-2:', stdout
    #if 'ImageMagick' in stdout[:200]:
    #    raise ValueError('Image conversion failed, found "ImageMagick" in STDOUT')

    return BytesIO(stdout)
    """
