# backend/app/core/constants.py
REGION_PRESETS = {
    "US": {
        "lengthUnit": "ft",
        "pressureUnit": "psi",
        "temperatureUnit": "f",
        "weightUnit": "lbs",
        "volumeUnit": "bbl",
        "densityUnit": "ppg",
        "torqueUnit": "ft-lbs",
        "rotationUnit": "rpm"
    },
    "METRIC": {
        "lengthUnit": "m",
        "pressureUnit": "bar",
        "temperatureUnit": "c",
        "weightUnit": "kg",
        "volumeUnit": "m3",
        "densityUnit": "kg/m3",
        "torqueUnit": "n-m",
        "rotationUnit": "rpm"
    }
}