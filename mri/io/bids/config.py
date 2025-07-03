ALLOWED_DATATYPES = ["anat"]

# See: https://bids-specification.readthedocs.io/en/latest/appendices/entity-table.html#encephalography-eeg-ieeg-and-meg  # noqa: E501
ENTITY_VALUE_TYPE = {
    "subject": "label",
    "session": "label",
    "task": "label",
    "run": "index",
    "processing": "label",
    "recording": "label",
    "space": "label",
    "acquisition": "label",
    "split": "index",
    "description": "label",
    "suffix": "label",
    "extension": "label",
}

# allowed BIDSPath entities
ALLOWED_PATH_ENTITIES = (
    "subject",
    "session",
    "task",
    "run",
    "processing",
    "recording",
    "space",
    "acquisition",
    "split",
    "description",
    "suffix",
    "extension",
)
ALLOWED_PATH_ENTITIES_SHORT = {
    "sub": "subject",
    "ses": "session",
    "task": "task",
    "acq": "acquisition",
    "run": "run",
    "proc": "processing",
    "space": "space",
    "recording": "recording",
    "split": "split",
    "desc": "description",
}

# allowed BIDS extensions (extension in the BIDS filename)
ALLOWED_FILENAME_EXTENSIONS = (
    [".json", ".tsv", ".tsv.gz", ".nii", ".nii.gz"]
)

# allowed suffixes (i.e. last "_" delimiter in the BIDS filenames before
# the extension)
ALLOWED_FILENAME_SUFFIX = [
    "markers",
    "T1w",
    "FLASH",  # datatype
    "participants",
    "scans",
    "sessions",
    "coordsystem",
    "events",  # sidecars
    "headshape",
    "beh",
    "physio",
    "stim",  # behavioral
]

BIDS_STANDARD_TEMPLATE_COORDINATE_SYSTEMS = [
    "ICBM452AirSpace",
    "ICBM452Warp5Space",
    "IXI549Space",
    "fsaverage",
    "fsaverageSym",
    "fsLR",
    "MNIColin27",
    "MNI152Lin",
    "MNI152NLin2009aSym",
    "MNI152NLin2009bSym",
    "MNI152NLin2009cSym",
    "MNI152NLin2009aAsym",
    "MNI152NLin2009bAsym",
    "MNI152NLin2009cAsym",
    "MNI152NLin6Sym",
    "MNI152NLin6ASym",
    "MNI305",
    "NIHPD",
    "OASIS30AntsOASISAnts",
    "OASIS30Atropos",
    "Talairach",
    "UNCInfant",
]

coordsys_standard_template_deprecated = [
    "fsaverage3",
    "fsaverage4",
    "fsaverage5",
    "fsaverage6",
    "fsaveragesym",
    "UNCInfant0V21",
    "UNCInfant1V21",
    "UNCInfant2V21",
    "UNCInfant0V22",
    "UNCInfant1V22",
    "UNCInfant2V22",
    "UNCInfant0V23",
    "UNCInfant1V23",
    "UNCInfant2V23",
]

coordsys_wildcard = ["Other"]


BIDS_SHARED_COORDINATE_FRAMES = (
    BIDS_STANDARD_TEMPLATE_COORDINATE_SYSTEMS
    + coordsys_standard_template_deprecated
    + coordsys_wildcard
)
# accepted BIDS formats, which may be subject to change
# depending on the specification
ALLOWED_SPACES = dict()
ALLOWED_SPACES["anat"] = None
ALLOWED_SPACES["beh"] = None

allowed_extension_anat = [".nii", ".nii.gz"]
ALLOWED_DATATYPE_EXTENSIONS = dict()
ALLOWED_DATATYPE_EXTENSIONS["anat"] = allowed_extension_anat