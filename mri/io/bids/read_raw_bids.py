from copy import deepcopy
from pathlib import Path

import xarray as xr


class BIDSPath:
    """Class for representing paths to BIDS data.

    Parameters
    ----------
    root : str | pathlib.Path
        Path to the root of the BIDS dataset.
    subject : str
        Subject label. Corresponds to sub-<subject_label>.
    session : str | None
        Session label. Corresponds to ses-<session_label>.
    task : str | None
        Task label. Corresponds to task-<task_label>.
    acquisition : str | None
        Acquisition parameters. Corresponds to acq-<acquisition_label>.
    run : str | None
        Run entity. Corresponds to run-<run_label>.
    space : str | None
        Space entity, i.e., the spatial reference to which the file has been aligned
        to. For example, ``'T1w'``. Corresponds to space-<space_label>.
    datatype : str
        The BIDS datatype, which is the subdirectory that the file is stored in. For
        example, ``'anat'``, ``'func'``, ``'dwi'``, ``'fmap'``, ``'meg'``, ``'ieeg'``,
        ``'eeg'``, ``'ieeg'``, ``'beh'``, etc.
    suffix : str | None
        The file suffix, e.g., 'T1w', 'bold', 'events', 'physio'. This is the last part
        of the filename (before the extension). The following suffixes are accepted:
        ``'T1w'``, ``'T2w'``.
    """

    def __init__(
        self,
        *,
        root=None,
        subject=None,
        session=None,
        task=None,
        acquisition=None,
        run=None,
        space=None,
        datatype=None,
        suffix=None,
        extension=None,
    ):
        self.root = root
        self.subject = subject
        self.session = session
        self.task = task
        self.acquisition = acquisition
        self.run = run
        self.space = space
        self.datatype = datatype
        self.suffix = suffix
        self.extension = extension

        self.update(
            root=root,
            subject=subject,
            session=session,
            task=task,
            acquisition=acquisition,
            run=run,
            space=space,
            datatype=datatype,
            suffix=suffix,
            extension=extension,
        )

    def update(self, *, check=None, **kwargs):
        """Update the entity key-value pairs, in-place.

        ``'run'`` is automatically converted to have a leading zero if it is a single
        digit. For example, ``run='1'`` is converted to ``run='01'``.

        Parameters
        ----------
        check : bool | None
            If True, check that each entity conforms to BIDS specification.
        **kwargs : dict
            Key-value pairs to update for valid BIDS entities: ``'root'``,
            ``'subject'``, ``'session'``, ``'task'``, ``'acquisition'``, ``'run'``,
            ``'space'``, ``'datatype'``, ``'suffix'``.

        Returns
        -------
        self : instance of BIDSPath
            The updated BIDSPath instance.
        """
        # TODO: This is a simple implementation. Align with MNE-BIDS version
        for key, value in kwargs.items():
            if value is not None:
                if key == "root":
                    value = Path(value).expanduser().resolve()
                if key == "run" and len(value) == 1:
                    value = f"0{value}"
                setattr(self, key, value)

        if check:
            raise NotImplementedError("Check not implemented yet.")
        return self

    ######################
    ### Dunder methods ###
    ######################
    def __repr__(self):
        """Return the BIDSPath in a format that is easy to read."""
        # TODO: This is a simple implementation. Align with MNE-BIDS version
        entities = [
            f"{key}: {value!r}" for key, value in self.__dict__.items()
        ]
        entities = [f"\n    {entity}" for entity in entities]
        name = self.fpath.name if hasattr(self, "fpath") else None
        if name is not None:
            entities.append(f"\n    filename: {name!r}")
        return f"{self.__class__.__name__}({', '.join(entities)})"

    #######################
    ### Utility methods ###
    #######################
    def copy(self):
        """Return a copy of the BIDSPath instance.

        Returns
        -------
        bids_path : instance of BIDSPath
            The copied BIDSPath instance.
        """
        return deepcopy(self)

    #########################
    ### Path-like methods ###
    #########################
    @property
    def fpath(self):
        """Return the full file path."""
        # TODO: This is a simple implementation. Align with MNE-BIDS version
        fpath = Path(self.root) # / "bids" / f"sub-{self.subject}"
        if list(fpath.glob("bids")):
            fpath /= "bids"
        fpath /= f"sub-{self.subject}"
        if self.session:
            fpath /= f"ses-{self.session}"
        fpath /= self.datatype
        fname = f"sub-{self.subject}"
        if self.session:
            fname += f"_ses-{self.session}"
        if self.task:
            fname += f"_task-{self.task}"
        if self.acquisition:
            fname += f"_acq-{self.acquisition}"
        if self.run:
            fname += f"_run-{self.run}"
        if self.space:
            fname += f"_space-{self.space}"
        if self.suffix:
            fname += f"_{self.suffix}"
        if self.extension:
            fname += self.extension
        fpath /= fname
        return fpath

    @property
    def directory(self):
        """Get the parent directory of the BIDS file.

        If ``subject``, ``session``, and ``datatype`` are provided, the directory
        location will be ``bids_root/sub-<subject>/ses-<session>/<datatype>``.

        Returns
        -------
        directory : pathlib.Path
            The parent directory.
        """
        return self.fpath.parent

    def find_matching_sidecar(self, *, suffix=None, extension=None):
        """Try to Get the path to a sidecar JSON file with a given suffix.

        Parameters
        ----------
        suffix : str | None
            The suffix of the sidecar file. This is the entity after the last ``'_'``.
            For example, ``'bold'`` for a BOLD run, ``'events'`` for an events file.
            Default is ``None``.
        extension : str | None
            The extension of the sidecar file, for example ``'.json'``. If ``None``,
            the extension is assumed to be ``'.json'``. Default is ``None``.

        Returns
        -------
        sidecar_path : pathlib.Path | None
            The path to the sidecar file if it exists. ``None`` otherwise.
        """
        return self._find_matching_sidecar(suffix=suffix, extension=extension)

    #######################
    ### Private methods ###
    #######################
    def _find_matching_sidecar(self, *, suffix=None, extension=None):
        """Get the path to a sidecar JSON filepath.

        Parameters
        ----------
        suffix : str | None
            The suffix of the sidecar file. This is the entity after the last ``'_'``.
            For example, ``'bold'`` for a BOLD run, ``'events'`` for an events file.
            Default is ``None``.
        extension : str | None
            The extension of the sidecar file, for example ``'.json'``. If ``None``,
            the extension is assumed to be ``'.json'``. Default is ``None``.
        """
        if suffix is None and self.suffix is not None:
            suffix = self.suffix
        elif suffix is None and self.suffix is None:
            raise ValueError("suffix must be provided if BIDSPath.suffix is None.")

        if extension is None:
            extension = ".json"
        search_suffix = suffix + extension

        # We only use subject and session as identifier, because all other
        # parameters are potentially not binding for metadata sidecar files
        # XXX: Is the above comment correct?
        search_str_filename = f"sub-{self.subject}"
        if self.session is not None:
            search_str_filename += f"_ses-{self.session}"

        # Find all potential sidecar files, doing a recursive glob
        # from bids_root/sub-*, potentially taking into account the data type
        # and suffix
        search_dir = self.root / "bids" / search_str_filename
        if self.datatype is not None:
            search_dir /= self.datatype # e.g., 'anat', 'func', 'meg', etc.
            search_dir /= "**"
        else:
            search_dir /= "**" # Search all data types
        search_str_complete = search_dir / f"{search_str_filename}*{search_suffix}"
        sidecar_files = list(search_str_complete.parent.rglob(search_str_complete.name))
        return sidecar_files[0] if sidecar_files else None


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
    import nibabel as nib
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
