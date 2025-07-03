import nibabel as nib
import xarray as xr


def read_raw_niifti(bids_path, extra_params=None):
    """Read raw data in BIDS format.

    Parameters
    ----------
    bids_path : BIDSPath
        The BIDS entity key-value pairs.
    extra_params : dict | None
        Extra parameters to pass to the reader.

    Returns
    -------
    raw : instance of mri.io.Raw
        The raw data.
    """
    img = nib.load(bids_path.fpath)
    data = img.get_fdata()
    header = img.header

    # Create a DataArray
    dims = ["x", "y", "z"]
    assert len(dims) == data.ndim
    coords = {dim: range(size) for dim, size in zip(dims, data.shape)}
    data_array = xr.DataArray(data, dims=dims, coords=coords)

    # Add metadata
    voxel_sizes = header.get_zooms()
    units = header.get_xyzt_units()
    metadata = {
        "voxel_sizes": voxel_sizes,
        "units": units,
    }
    data_array.attrs.update(metadata)
    return data_array
