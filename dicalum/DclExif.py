__all__ = ['fr2fl','read_exif_tags']
import exifread
from dicalum.coeffs import *
def fr2fl(frac_str):
    try:
        return float(frac_str)
    except ValueError:
        try:
            num, denom = frac_str.split('/')
        except ValueError:
            return None
        try:
            leading, num = num.split(' ')
        except ValueError:
            return float(num) / float(denom)        
        if float(leading) < 0:
            sign_mult = -1
        else:
            sign_mult = 1
        return float(leading) + sign_mult * (float(num) / float(denom))

def read_exif_tags(filename):
    f = open(filename, 'rb')
    tags = exifread.process_file(f)
    aperture=fr2fl(str(tags['EXIF FNumber']))
    shutter=fr2fl(str(tags['EXIF ExposureTime']))
    iso=fr2fl(str(tags['EXIF ISOSpeedRatings']))
    dclex = DclExpo(iso,aperture,shutter)
    return dclex

def exif2b(tags):
    brand = tags['Image Make']
    model = tags['Image Model']
    date = tags['Image DateTime']
    focallength = tags['EXIF FocalLength']
    lens = tags['EXIF LensModel']
    return str(brand)
