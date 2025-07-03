import glob
import os

from pathlib import Path
import mri
from mri.io.bids.config import ALLOWED_FILENAME_EXTENSIONS

def _check_key_val(key, val):
    """Validate the value of a BIDS entity to make sure it adheres to the spec."""
    if any(ii in val for ii in ["-", "_", "/"]):
        raise ValueError(
            f"Unallowed `-`, `_`, or `/` found in key/value pair {key}: {val}"
        )
    return key, val


def _check_non_sub_ses_entity(bids_path):
    """Check existence of non subject/session entities in BIDSPath."""
    if (
        bids_path.task
        or bids_path.acquisition
        or bids_path.run
        or bids_path.space
        or bids_path.recording
        or bids_path.split
        or bids_path.processing
    ):
        return True
    return False


def _get_matching_bidspaths_from_filesystem(bids_path):
    """Get matching file paths for a BIDSPath.

    Assumes suffix and/or extension is not provided.
    """
    # extract relevant entities to find filepath
    sub, ses = bids_path.subject, bids_path.session
    datatype = bids_path.datatype
    basename, bids_root = bids_path.basename, bids_path.root

    if datatype is None:
        datatype = _infer_datatype(root=bids_root, sub=sub, ses=ses)

    data_dir = mri.io.BIDSPath(
        subject=sub, session=ses, datatype=datatype, root=bids_root
    ).directory

    search_str = bids_root
    # parse down the BIDS directory structure
    if sub is not None:
        search_str = search_str / f"sub-{sub}"
    if ses is not None:
        search_str = search_str / f"ses-{ses}"
    if datatype is not None:
        search_str = search_str / datatype
    else:
        search_str = search_str / "**"
    search_str = str(search_str / f"{basename}*")

    # Find all matching files in all supported formats.
    valid_exts = ALLOWED_FILENAME_EXTENSIONS
    matching_paths = glob.glob(search_str)
    matching_paths = [p for p in matching_paths if _parse_ext(p)[1] in valid_exts]
    return matching_paths


def _infer_datatype(*, root, sub, ses):
    # Check which suffix is available for this particular
    # subject & session. If we get no or multiple hits, throw an error.

    modalities = _get_datatypes_for_sub(root=root, sub=sub, ses=ses)

    # We only want to handle imaging data here.
    allowed_recording_modalities = ["anat"]
    modalities = list(set(modalities) & set(allowed_recording_modalities))
    if not modalities:
        raise ValueError("No anatomical data found.")
    elif len(modalities) >= 2:
        msg = (
            f"Found data of more than one recording datatype. Please "
            f"pass the `suffix` parameter to specify which data to load. "
            f"Found the following modalitiess: {modalities}"
        )
        raise RuntimeError(msg)

    assert len(modalities) == 1
    return modalities[0]


def _get_datatypes_for_sub(*, root, sub, ses=None):
    """Retrieve data modalities for a specific subject and session."""
    subject_dir = root / f"sub-{sub}"
    if ses is not None:
        subject_dir = subject_dir/ f"ses-{ses}"

    # TODO We do this to ensure we don't accidentally pick up any "spurious"
    # TODO sub-directories. But is that really necessary with valid BIDS data?
    modalities_in_dataset = get_datatypes(root=root)
    subdirs = [f.name for f in os.scandir(subject_dir) if f.is_dir()]
    available_modalities = [s for s in subdirs if s in modalities_in_dataset]
    return available_modalities


# @verbose
def get_datatypes(root, verbose=None):
    """Get list of data types ("modalities") present in a BIDS dataset.

    Parameters
    ----------
    root : path-like
        Path to the root of the BIDS directory.
    %(verbose)s

    Returns
    -------
    modalities : list of str
        List of the data types present in the BIDS dataset pointed to by
        `root`.

    """
    # Take all possible data types from "entity" table
    # (Appendix in BIDS spec)
    # https://bids-specification.readthedocs.io/en/latest/appendices/entity-table.html
    datatype_list = ("anat")
    datatypes = list()
    for root, dirs, files in os.walk(root):
        for _dir in dirs:
            if _dir in datatype_list and _dir not in datatypes:
                datatypes.append(_dir)

    return datatypes

def _parse_ext(raw_fname):
    """Split a filename into its name and extension."""
    raw_fname = Path(raw_fname)
    fname, ext = raw_fname.stem, raw_fname.suffix
    # BTi data is the only file format that does not have a file extension
    if ext == "" or "c,rf" in fname:
        raise ValueError(f"Found no extension for raw file: {raw_fname}.")
    # If ending on .gz, check whether it is an .nii.gz file
    elif ext == ".gz" and raw_fname.name.endswith(".nii.gz"):
        ext = ".nii.gz"
        fname = fname[:-4]  # cut off the .nii
    return fname, ext

