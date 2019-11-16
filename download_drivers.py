"""
This utility downloads the Selenium browser drivers (Chromedriver and Geckodriver). Enjoy!
The drivers will be downloaded in the directory where this file is present.

Usage:
from download_drivers import ChromeDriver, GeckoDriver
cd = ChromeDriver()  # For chrome driver, it automatically identifies your browser version and downloads the matching driver.
cd.download_chromedriver()

cd = ChromeDriver('78')  # Alternatively, you can also download any specific version by passing the MAJOR version number (ex: 78)
cd.download_chromedriver()

# For Firefox driver
gd = GeckoDriver('0.26.0')
gd.download_geckodriver()

Supported browsers:
Chrome, Firefox, Safari (selenium works without safaridriver)

Supported operating systems:
Mac OS, Windows, Linux
"""
import os
import platform
import stat
import tarfile
import urllib.request
import zipfile

pwd = os.path.abspath(os.path.dirname(__file__))
cdriver_latest_release_url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
cdriver_download_url = 'https://chromedriver.storage.googleapis.com/{}/chromedriver_{}.zip'
gdriver_download_url = 'https://github.com/mozilla/geckodriver/releases/download/v{}/geckodriver-v{}-{}'


class Utils:
    def download_file(self, url, file):
        """
        :param url:
        :param file: file along with the format to be saved as. Ex: chromedriver.zip
        :return:
        """
        urllib.request.urlretrieve(url, os.path.abspath(os.path.join(pwd, file)))

    def unzip(self, file, path):
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(path)

    def untar(self, file, path):
        tf = tarfile.open(file)
        tf.extractall(path)

    def cleanup(self, file):
        os.remove(file)


class ChromeDriver(Utils):
    def __init__(self, version='LATEST_RELEASE'):
        self.version = self.get_version(version)
        self.cdriver_url = self.get_cdriver_download_url(self.version)
        self.cdriver_path = os.path.abspath(pwd + '/chromedriver')  # chromedriver path in your system
        self.cdriver_zip_path = self.cdriver_path + '.zip'  # append .zip to the chromedriver path in your system

    def download_chromedriver(self):
        """
        Download the chromedriver.zip, unzip the file, set permissions, clean up the zip file and keep only chromedriver
        :return: None
        """
        self.download_file(self.cdriver_url, 'chromedriver.zip')
        self.unzip(self.cdriver_zip_path, pwd)
        if not platform.system() == 'Windows':
            os.chmod(self.cdriver_path, os.stat(self.cdriver_path).st_mode | stat.S_IXUSR)
        self.cleanup(self.cdriver_zip_path)

    def get_version(self, version):
        """
        :param version:
        :return: the full version number of the chromedriver using cdriver_latest_release_url
        """
        r = urllib.request.urlopen(
            cdriver_latest_release_url) if version == 'LATEST_RELEASE' else urllib.request.urlopen(
            cdriver_latest_release_url + '_{}'.format(version))
        return r.read().decode()

    def get_cdriver_download_url(self, version):
        """
        :param version: chromedriver full version (ex: 78.0.3904.70)
        :return: the complete download url from cdriver_download_url above
        """
        if platform.system() == 'Darwin':
            cdriver_type = 'mac64'
        elif platform.system() == 'Linux':
            cdriver_type = 'linux64'
        elif platform.system() == 'Windows':
            cdriver_type = 'win32'
        else:
            raise NotImplementedError('This OS is not implemented yet.')
        return cdriver_download_url.format(version, cdriver_type)


class GeckoDriver(Utils):
    def __init__(self, version):
        self.version = version
        self.gdriver_url = self.get_gdriver_download_url(self.version)
        self.gdriver_path = os.path.abspath(pwd + '/geckodriver')  # geckodriver path in your system
        # append .zip or .tar.gz to the geckodriver path in your system based on the OS
        self.gdriver_tar_gz_path = self.gdriver_path + '.tar.gz'
        self.gdriver_zip_path = self.gdriver_path + '.zip'

    def download_geckodriver(self):
        """
        Download the geckodriver.zip/tar.gz, unzip/untar the file, clean up the zip/tar file and keep only geckodriver
        :return: None
        """
        if platform.system() == 'Windows':
            self.download_file(self.gdriver_url, 'geckodriver.zip')
            self.unzip(self.gdriver_zip_path, pwd)
            self.cleanup(self.gdriver_zip_path)
        else:
            self.download_file(self.gdriver_url, 'geckodriver.tar.gz')
            self.untar(self.gdriver_tar_gz_path, pwd)
            self.cleanup(self.gdriver_tar_gz_path)

    def get_gdriver_download_url(self, version):
        """
        :param version: geckodriver full version (ex: 0.26.0)
        :return: the complete download url from gdriver_download_url above
        """
        if platform.system() == 'Darwin':
            gdriver_type = 'macos.tar.gz'
        elif platform.system() == 'Linux':
            if '64' in platform.uname()[4]:
                gdriver_type = 'linux64.tar.gz'
            else:
                gdriver_type = 'linux32.tar.gz'
        elif platform.system() == 'Windows':
            if '64' in platform.uname()[4]:
                gdriver_type = 'win64.zip'
            else:
                gdriver_type = 'win32.zip'
        else:
            raise NotImplementedError('This OS is not implemented yet.')
        return gdriver_download_url.format(version, version, gdriver_type)
