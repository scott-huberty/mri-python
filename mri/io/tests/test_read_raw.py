from mri.datasets import fetch_pixar_data
from mri.io import BIDSPath, read_raw_niifti

import pytest

@pytest.mark.skip(reason="Need to finish dataset fetching")
def test_read_raw(tmp_path):
    """Test reading raw data."""
    # Fetch the data
    subject = "pixar001"
    bids_root = fetch_pixar_data(subject=subject, bids_root=tmp_path)

    suffix = "T1w"
    extension = ".nii.gz"
    datatype = "anat"

    # Create a BIDSPath object
    bids_path = BIDSPath(
        root=bids_root,
        subject=subject,
        datatype=datatype,
        suffix=suffix,
        extension=extension,
    )

    want_path = bids_root / f"sub-{subject}" / datatype
    want_path /= f"sub-{subject}_{suffix}{extension}"
    assert bids_path.fpath == want_path
    assert bids_path.fpath.exists()
    want_entities = {
        "root": bids_root,
        "subject": subject,
        "session": None,
        "task": None,
        "acquisition": None,
        "run": None,
        "space": None,
        "datatype": datatype,
        "suffix": suffix,
        "extension": extension,
    }
    assert bids_path.__dict__ == want_entities

    # Read the raw data
    raw = read_raw_niifti(bids_path)
    assert raw is not None
