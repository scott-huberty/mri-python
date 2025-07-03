from pathlib import Path

import mri


def test_bpath_constructor():
    """Test BIDS path construction."""
    prefix_data = dict(
        subject="one",
        session="two",
        task="three",
        acquisition="four",
        run=1,
        processing="six",
        recording="seven",
        suffix="T1w",
        extension=".json",
        datatype="anat",
    )
    expected_str = (
        "sub-one_ses-two_task-three_acq-four_run-1_proc-six_recording-seven_T1w.json"
    )
    bpath = mri.io.BIDSPath(**prefix_data)
    assert bpath.basename == expected_str
    assert bpath == (Path("sub-one") / "ses-two" / "anat" / expected_str).as_posix()
    # subsets of keys works
    bpath_subset = mri.io.BIDSPath(subject="one", task="three", run=4)
    assert bpath_subset.basename == "sub-one_task-three_run-4"
    bpath_subset.update(run=None, suffix="T1w", extension=".json")
    assert bpath_subset.basename == "sub-one_task-three_T1w.json"
