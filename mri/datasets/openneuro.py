from pathlib import Path


def data_path():
    """Return the default path for OpenNeuro datasets."""
    # This is a placeholder function to mimic the MNE data path function.
    # It returns a default path where OpenNeuro datasets can be stored.
    data_path = Path.home() / "mri_python_data" / "openneuro"
    if not data_path.exists():
        data_path.mkdir(parents=True, exist_ok=True)
    return data_path


def check_openneuro_installed():
    """Check if openneuro is installed."""
    try:
        import openneuro
    except ImportError:
        raise ImportError("openneuro is not installed. Please install it by running:\n"
                          "`pip install openneuro`.")
    return openneuro


def fetch_pixar_data(subject="pixar001"):
    """Fetch a dataset from OpenNeuro."""
    dataset = "ds000228"
    download_kwargs = dict(include=[f"sub-{subject}"])
    return fetch_dataset(dataset, download_kwargs=download_kwargs)


def fetch_dataset(dataset, download_kwargs=None):
    """Fetch a dataset from OpenNeuro."""
    if download_kwargs is None:
        download_kwargs = {}
    target_dir = data_path() / dataset
    openneuro = check_openneuro_installed()
    if target_dir.exists():
        return target_dir
    openneuro.download(
        dataset=dataset,
        target_dir=target_dir,
        **download_kwargs,
    )
    return target_dir
