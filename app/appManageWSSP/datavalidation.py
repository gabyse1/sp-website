from django.core.exceptions import ValidationError
import re

# data validation
def validate_text(value):
    value = strim(value)
    value = stripslashes(value)
    value = htmlspecialchars(value)
    value = escape_special_chars(value)
    return value

def strim(value):
    return str(value).strip('')

def stripslashes(value):
    return re.sub(r'[\\(\'|\")]','',value)

def htmlspecialchars(value): 
    return (
     value.replace("&", "&amp;"). 
     replace('"', "&quot;"). 
     replace("<", "&lt;"). 
     replace(">", "&gt;").
     replace("'", "&#39;")
    )

def escape_special_chars(value):
    return (
        value.replace("ñ","&ntilde;").
        replace("Ñ","&Ntilde;").
        replace("á","&aacute;").
        replace("é","&eacute;").
        replace("í","&iacute;").
        replace("ó","&oacute;").
        replace("ú","&uacute;").
        replace("Á","&Aacute;").
        replace("É","&Eacute;").
        replace("Í","&Iacute;").
        replace("Ó","&Oacute;").
        replace("Ú","&Uacute;").
        replace("€","&euro;")
    )

def is_alphanumeric_space(value):
    if re.fullmatch(r'[a-zA-ZñÑÀ-ÿ0-9-\'&_\s]+', value):
        return True
    else:
        return False

def is_email(value):
    if re.fullmatch(r'[a-z0-9_\.-]+@[a-z0-9_\.-]+\.[a-z\.]{2,6}', value):
        return True
    else:
        return False

def is_url(value):
    if re.fullmatch(r'http[s]{0,1}:\/\/){0,1}[a-z0-9\.-]+\.[a-z\.]{2,6}[/a-zA-Z0-9_\.\%\&-]+[/]{0,1}', value):
        return True
    else:
        return False

def is_image(value):
    if (not value.name.endswith('.png') and
        not value.name.endswith('.jpeg') and 
        not value.name.endswith('.gif') and
        not value.name.endswith('.bmp') and 
        not value.name.endswith('.jpg') and
        not value.name.endswith('.ico')):
        return False
    else:
        return True

def is_integer(value):
    try:
        if int(value):
            return True
    except ValueError:
        return False

def is_positive_integer(value):
    try:
        if int(value) > 0:
            return True
        else:
            return False
    except ValueError:
        return False

def is_positive_number(value):
    try:
        if float(value) > 0:
            return True
        else:
            return False
    except ValueError:
        return False

# Valid image field and svg file field
def valid_file_name(value):
    if not re.fullmatch(r'[a-zA-ZñÑÀ-ÿ0-9-\'\/&._\s]+', str(value)):
        raise ValidationError("File names allow: alphanumeric characters, spaces, single quote, ampersand, hyphens, underscores, and periods.")

def valid_image_file_size(value): # add this to some file where you can import it from
    limit = 1 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 1 MB.')

def valid_image_extension(value):
    if (not value.name.endswith('.png') and
        not value.name.endswith('.jpeg') and 
        not value.name.endswith('.gif') and
        not value.name.endswith('.bmp') and 
        not value.name.endswith('.jpg') and
        not value.name.endswith('.JPG') and 
        not value.name.endswith('.ico') and
        not value.name.endswith('.svg')):
 
        raise ValidationError("Allowed files: .jpg, .jpeg, .png, .gif, .bmp, .svg")

def valid_video_file_size(value): # add this to some file where you can import it from
    limit = 100 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 100 MB.')

def valid_video_extension(value):
    if not value.name.endswith('.mp4'):
        raise ValidationError("Allowed files: .mp4")

def valid_html_file_size(value):
    limit = 1 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 1 MB.')

def valid_html_extension(value):
    if not value.name.endswith('.html'):
        raise ValidationError("Allowed files: .html")