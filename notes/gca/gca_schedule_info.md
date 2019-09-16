# GCA-Web `Schedule` description

Three main nested objects are supported: `session`, `tracks`, `events`

`events` can be nested within `tracks`
`tracks` can be nested within `sessions`

- `session` object has supported keys:
  `title`, `subtitle`, `tracks`
  - `title` and `subtitle` values are text
  - `tracks` value is an object array containing `track` objects

- `track` object has supported keys:
  `title`, `subtitle`, `chair`, `events`
  - `title` and `subtitle` values are text
  - `chair` value is an array of text
  - `events` value is an object array containing `event` objects

- `event` object has supported keys:
  `title`, `subtitle`, `start`, `end`, `date`, `location`, `authors`, `type`, `abstract`
  - all values are text
  - `start` and `end` time values have to be in format `HH:mm`.
  - `date` value has to be in format `YYYY-MM-DD`

## Minimal schedule json example

[
  {
    "title": "",
    "subtitle": "",
    "tracks": [
      {
        "title": "Session title",
        "subtitle": null,
        "chair": [""],
        "events": [
          {
            "title": "",
            "subtitle": null,
            "start": "",
            "end": "",
            "date": "",
            "location": "",
            "type": "",
            "authors": [""]
          }
        ]
      }
    }
  }
]
