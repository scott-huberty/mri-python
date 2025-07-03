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
