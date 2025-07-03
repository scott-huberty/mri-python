from pathlib import Path


def check_openneuro_installed():
    """Check if openneuro is installed."""
    try:
        import openneuro
    except ImportError:
        raise ImportError("openneuro is not installed. Please install it by running:\n"
                          "`pip install openneuro`.")
    return openneuro


def fetch_pixar_data(
        dataset="ds000228", subject="pixar001", bids_root=None):
    """Fetch a dataset from OpenNeuro."""
    openneuro = check_openneuro_installed()

    if bids_root is None:
        bids_root = Path(__file__).parent / dataset
    if not bids_root.is_dir():
        bids_root.mkdir()

    openneuro.download(
        dataset=dataset,
        target_dir=bids_root,
        include=[f"sub-{subject}"],
    )
    return bids_root
