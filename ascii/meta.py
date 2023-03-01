import pyexiv2
import json

metadata = pyexiv2.ImageMetadata('./test/test.jpg')
metadata.read()
userdata={'Category':'Human',
          'Physical': {
              'skin_type':'smooth',
              'complexion':'fair'
              },
          'Location': {
              'city': 'london'
              }
          }
metadata['Exif.Photo.UserComment']=json.dumps(userdata)
metadata.write()