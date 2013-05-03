import trans
from hashlib import md5
from datetime import date, datetime


def image_path(instance, filename):
    """
    Returns a file path where to save a photo
    """
    ext = filename.rsplit('.')[-1].lower()
    hash = md5(filename.encode('trans') + '%s' % datetime.now())
    new_filename = '%s.%s' % (hash.hexdigest()[3:10], ext)

    return u'upload/%s/%d/%d/%s' % (date.today().year, date.today().month,
                                    date.today().day, new_filename)
