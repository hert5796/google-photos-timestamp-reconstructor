# Google Photos Timestamp Reconstructor

This project is designed to fix the timestamps on photos taken from Google Photos. When exporting photos from Google Photos, the creation date is not retained; instead, they are dated at the time of export. However, a properly exported photo from Google Photos will usually produce a corresponding `.json` file that includes the correct date information, such as in the example below:

```json
{
  "title": "20130705_180833.jpg",
  "description": "",
  "imageViews": "31",
  "creationTime": {
    "timestamp": "1234567890",
    "formatted": "Jul 5, 2013, 4:56:30 PM UTC"
  },
  "photoTakenTime": {
    "timestamp": "1234567890",
    "formatted": "Mar 30, 2019, 5:08:33 PM UTC"
  },
  "geoData": {
    "latitude": 0.0,
    "longitude": 0.0,
    "altitude": 0.0,
    "latitudeSpan": 0.0,
    "longitudeSpan": 0.0
  },
  ...
}
```

This script attempts to fix the timestamps on each photo or video by extracting the necessary information from the `photoTakenTime` field in the corresponding `.json` file, if it exists. If the `.json` file is not present, the program will try to extract the [exif data](https://photographylife.com/what-is-exif-data) from the image, assuming it is in a format that supports exif. If exif data is also not available, the program will try to extract date information from the image filename.

Note: There are ways to manually fix the timestamps using free tools like [this one](https://legault.me/post/correctly-migrate-away-from-google-photos-to-icloud), or by using a paid service like [Metadata fixer](https://metadatafixer.com). This script was created as a quick and dirty solution that has worked well enough for the me.
