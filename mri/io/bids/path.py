from pathlib import Path

from mri.utils._checks import check_type
from mri.io.bids.utils import _check_key_val, _check_non_sub_ses_entity
from mri.io.bids.config import (
    ALLOWED_DATATYPES, 
    ENTITY_VALUE_TYPE,
    ALLOWED_PATH_ENTITIES,
    ALLOWED_PATH_ENTITIES_SHORT,
    ALLOWED_FILENAME_SUFFIX,
    ALLOWED_FILENAME_EXTENSIONS,
    ALLOWED_SPACES,
)

class BIDSPath:
    """A BIDS path object.

    BIDS filename prefixes have one or more pieces of metadata in them. They
    must follow a particular order, which is followed by this function. This
    will generate the *prefix* for a BIDS filename that can be used with many
    subsequent files, or you may also give a suffix that will then complete
    the file name.

    BIDSPath allows dynamic updating of its entities in place, and operates
    similar to `pathlib.Path`. In addition, it can query multiple paths
    with matching BIDS entities via the ``match`` method.

    Note that not all parameters are applicable to each suffix of data. For
    example, electrode location TSV files do not need a "task" field.

    Parameters
    ----------
    subject : str | None
        The subject ID. Corresponds to "sub" [1]_.
    session : str | None
        The acquisition session. Corresponds to "ses" [2]_.
    task : str | None
        The experimental task. Corresponds to "task" [3]_.
    acquisition: str | None
        The acquisition parameters. Corresponds to "acq" [4]_.
    run : int | None
        The run number. Corresponds to "run" [5]_.
    processing : str | None
        The processing label. Corresponds to "proc" [6]_.
    recording : str | None
        The recording name. Corresponds to "recording" [7]_.
    space : str | None
        The coordinate space that the data has been aligned to (e.g. `'Talairach'`,
        `'MNI305'`, `'MNI152NLin2009cAsym_desc-preproc_T1w'`). Note that valid values
        for ``space`` must come from a list
        of BIDS keywords as described in the BIDS specification [8]_ [9]_.
        Corresponds to "space". 
    split : int | None
        The split of the continuous recording file for ``.fif`` data.
        Corresponds to "split".
    description : str | None
        This corresponds to the BIDS entity ``desc``. It is used to provide
        additional information for derivative data, e.g., preprocessed data
        may be assigned ``description='cleaned'``. Corresponds to "desc" [10]_.

        .. versionadded:: 0.11
    suffix : str | None
        The filename suffix. This is the entity after the
        last ``_`` before the extension. E.g., ``'channels'``.
        The following filename suffix's are accepted:
        'meg', 'markers', 'eeg', 'ieeg', 'T1w',
        'participants', 'scans', 'electrodes', 'coordsystem',
        'channels', 'events', 'headshape', 'digitizer',
        'beh', 'physio', 'stim'
    extension : str | None
        The extension of the filename. E.g., ``'.json'``.
    datatype : str
        The BIDS data type, e.g., ``'anat'``, ``'func'``, ``'eeg'``, ``'meg'``,
        ``'ieeg'``.
    root : path-like | None
        The root directory of the BIDS dataset.
    check : bool
        If ``True``, enforces BIDS conformity. Defaults to ``True``.

    Attributes
    ----------
    entities : dict
        A dictionary of the BIDS entities and their values:
        ``subject``, ``session``, ``task``, ``acquisition``,
        ``run``, ``processing``, ``space``, ``recording``,
        ``split``, ``description``, ``suffix``, and ``extension``.
    datatype : str | None
        The data type, i.e., one of ``'anat'``, ``'func'``, ``'fmap'``.
    basename : str
        The basename of the file path. Similar to `os.path.basename(fpath)`.
    root : pathlib.Path
        The root of the BIDS path.
    directory : pathlib.Path
        The directory path.
    fpath : pathlib.Path
        The full file path.
    check : bool
        Whether to enforce BIDS conformity.

    Examples
    --------
    Generate a BIDSPath object and inspect it

    >>> bids_path = BIDSPath(subject='test', session='two', task='mytask',
    ...                      suffix='T1w', extension='.nii.gz', datatype='T1w')
    >>> print(bids_path.basename)
    sub-test_ses-two_task-mytask_ieeg.edf
    >>> bids_path
    BIDSPath(
    root: None
    datatype: ieeg
    basename: sub-test_ses-two_task-mytask_ieeg.edf)

    Copy and update multiple entities at once

    >>> new_bids_path = bids_path.copy().update(subject='test2',
    ...                                         session='one')
    >>> print(new_bids_path.basename)
    sub-test2_ses-one_task-mytask_ieeg.edf

    Printing a BIDSPath will show a relative path when `root` is not set

    >>> print(new_bids_path)
    sub-test2/ses-one/ieeg/sub-test2_ses-one_task-mytask_ieeg.edf

    Setting `suffix` without an identifiable datatype will make
    BIDSPath try to guess the datatype

    >>> new_bids_path = new_bids_path.update(suffix='channels',
    ...                                      extension='.tsv')
    >>> print(new_bids_path)
    sub-test2/ses-one/ieeg/sub-test2_ses-one_task-mytask_channels.tsv

    You can set a new root for the BIDS dataset. Let's see what the
    different properties look like for our object:

    >>> new_bids_path = new_bids_path.update(root='/bids_dataset')
    >>> print(new_bids_path.root.as_posix())
    /bids_dataset
    >>> print(new_bids_path.basename)
    sub-test2_ses-one_task-mytask_channels.tsv
    >>> print(new_bids_path)
    /bids_dataset/sub-test2/ses-one/ieeg/sub-test2_ses-one_task-mytask_channels.tsv
    >>> print(new_bids_path.directory.as_posix())
    /bids_dataset/sub-test2/ses-one/ieeg

    Notes
    -----
    BIDS entities are generally separated with a ``"_"`` character, while
    entity key/value pairs are separated with a ``"-"`` character.
    There are checks performed to make sure that there are no ``'-'``, ``'_'``,
    or ``'/'`` characters contained in any entity keys or values.

    To represent a filename such as ``dataset_description.json``,
    one can set ``check=False``, and pass ``suffix='dataset_description'``
    and ``extension='.json'``.

    References
    ----------
    .. [1] https://bids-specification.readthedocs.io/en/stable/appendices/entities.html#sub
    .. [2] https://bids-specification.readthedocs.io/en/stable/appendices/entities.html#ses
    .. [3] https://bids-specification.readthedocs.io/en/stable/appendices/entities.html#task
    .. [4] https://bids-specification.readthedocs.io/en/stable/appendices/entities.html#acq
    .. [5] https://bids-specification.readthedocs.io/en/stable/appendices/entities.html#run
    .. [6] https://bids-specification.readthedocs.io/en/stable/appendices/entities.html#proc
    .. [7] https://bids-specification.readthedocs.io/en/stable/appendices/entities.html#recording
    .. [8] https://bids-specification.readthedocs.io/en/stable/appendices/entities.html#space
    .. [9] https://bids-specification.readthedocs.io/en/stable/appendices/coordinate-systems.html
    .. [1] https://bids-specification.readthedocs.io/en/stable/appendices/entities.html#desc
    """

    def __init__(
        self,
        subject=None,
        session=None,
        task=None,
        acquisition=None,
        run=None,
        processing=None,
        recording=None,
        space=None,
        split=None,
        description=None,
        root=None,
        suffix=None,
        extension=None,
        datatype=None,
        check=True,
    ):
        if all(
            ii is None
            for ii in [
                subject,
                session,
                task,
                acquisition,
                run,
                processing,
                recording,
                space,
                description,
                root,
                suffix,
                extension,
            ]
        ):
            raise ValueError("At least one parameter must be given.")

        self.check = check

        self.update(
            subject=subject,
            session=session,
            task=task,
            acquisition=acquisition,
            run=run,
            processing=processing,
            recording=recording,
            space=space,
            split=split,
            description=description,
            root=root,
            datatype=datatype,
            suffix=suffix,
            extension=extension,
        )

    def update(self, *, check=None, **kwargs):
        """Update inplace BIDS entity key/value pairs in object.

        ``run`` and ``split`` are auto-converted to have two
        digits. For example, if ``run=1``, then it will nbecome ``run='01'``.

        Also performs error checks on various entities to
        adhere to the BIDS specification. Specifically:
        - ``datatype`` should be one of: ``anat``, ``eeg``, ``ieeg``, ``meg``
        - ``extension`` should be one of the accepted file
        extensions in the file path: ``.nii``, ``.nii.gz``, ``.json``, ``.tsv``.
        - ``suffix`` should be one of the acceptable file suffixes in: ``T1w``,
        ``T2w``, ``func``, ``beh``, ``physio``, ``stim``
        - Depending on the modality of the data (EEG, MEG, iEEG),
        ``space`` should be a valid string according to Appendix VIII
        in the BIDS specification [1]_ [2]_.

        Parameters
        ----------
        check : None | bool
            If a boolean, controls whether to enforce BIDS conformity. This
            will set the ``.check`` attribute accordingly. If ``None``, rely on
            the existing ``.check`` attribute instead, which is set upon
            :class:`mne_bids.BIDSPath` instantiation. Defaults to ``None``.
        **kwargs : dict
            It can contain updates for valid BIDSPath entities:
            'subject', 'session', 'task', 'acquisition', 'processing', 'run',
            'recording', 'space', 'suffix', 'split', 'extension',
            or updates for 'root' or 'datatype'.

        Returns
        -------
        bidspath : BIDSPath
            The updated instance of BIDSPath.

        Examples
        --------
        If one creates a bids basename using
        :func:`mne_bids.BIDSPath`:

        >>> bids_path = BIDSPath(subject='test', session='two',
        ...                      task='mytask', suffix='channels',
        ...                      extension='.tsv')
        >>> print(bids_path.basename)
        sub-test_ses-two_task-mytask_channels.tsv
        >>> # Then, one can update this `BIDSPath` object in place
        >>> bids_path.update(acquisition='test', suffix='t1w',
        ...                  datatype='t1w',
        ...                  extension='.nii.gz', task=None)
        BIDSPath(
        root: None
        datatype: t1w
        basename: sub-test_ses-two_acq-test_t1w.nii.gz)
        >>> print(bids_path.basename)
        sub-test_ses-two_acq-test_t1w.nii.gz

        References
        ----------
        .. [1] https://bids-specification.readthedocs.io/en/stable/appendices/entities.html#space
        .. [2] https://bids-specification.readthedocs.io/en/stable/appendices/coordinate-systems.html
        """
        # Update .check attribute
        if check is not None:
            self.check = check

        for key, val in kwargs.items():
            if key == "root":
                check_type(val, types=("path-like", None), item_name=key)
                continue
            if key == "datatype":
                if val is not None and val not in ALLOWED_DATATYPES and self.check:
                    raise ValueError(
                        f"datatype ({val}) is not valid. "
                        f"Should be one of "
                        f"{ALLOWED_DATATYPES}"
                    )
                else:
                    continue
            if key not in ENTITY_VALUE_TYPE:
                raise ValueError(
                    f"Key must be one of {ALLOWED_PATH_ENTITIES}, got {key}"
                )
            if ENTITY_VALUE_TYPE[key] == "label":
                check_type(val, types=(None, str), item_name=key)
            else:
                assert ENTITY_VALUE_TYPE[key] == "index"
                check_type(val, types=(int, str, None), item_name=key)
                if isinstance(val, str) and not val.isdigit():
                    raise ValueError(f"{key} is not an index (Got {val})")
                elif isinstance(val, int):
                    kwargs[key] = f"{val}"

        # ensure extension starts with a '.'
        extension = kwargs.get("extension")
        if extension is not None and not extension.startswith("."):
            kwargs["extension"] = f".{extension}"
        del extension

        # error check entities
        old_kwargs = dict()
        for key, val in kwargs.items():
            # check if there are any characters not allowed
            if val is not None and key != "root":
                if key == "suffix" and not self.check:
                    # suffix may skip a check if check=False to allow
                    # things like "dataset_description.json"
                    pass
                else:
                    _check_key_val(key, val)
            # set entity value, ensuring `root` is a Path
            if val is not None and key == "root":
                val = Path(val).expanduser()
            old_kwargs[key] = (
                getattr(self, key) if hasattr(self, f"_{key}") else None
            )
            setattr(self, f"_{key}", val)

        # Perform a check of the entities and revert changes if check fails
        try:
            self._check()
        except Exception as e:
            old_check = self.check
            self.check = False
            self.update(**old_kwargs)
            self.check = old_check
            raise e
        return self

    def _check(self):
        """Deep check or not of the instance."""
        self.basename  # run basename to check validity of arguments

        # perform error check on scans
        if (
            self.suffix == "scans" and self.extension == ".tsv"
        ) and _check_non_sub_ses_entity(self):
            raise ValueError(
                "scans.tsv file name can only contain "
                "subject and session entities. BIDSPath "
                f"currently contains {self.entities}."
            )

        # perform deeper check if user has it turned on
        if self.check:
            # ensure extension starts with a '.'
            extension = self.extension
            if extension is not None:
                # check validity of the extension
                if extension not in ALLOWED_FILENAME_EXTENSIONS:
                    raise ValueError(
                        f"Extension {extension} is not "
                        f"allowed. Use one of these extensions "
                        f"{ALLOWED_FILENAME_EXTENSIONS}."
                    )

            # labels from space entity must come from list (appendix VIII)
            space = self.space
            if space is not None:
                datatype = getattr(self, "datatype", None)
                if datatype is None:
                    raise ValueError(
                        "You must define datatype if you want to "
                        "use space in your BIDSPath."
                    )

                allowed_spaces_for_dtype = ALLOWED_SPACES.get(datatype, None)
                if allowed_spaces_for_dtype is None:
                    raise ValueError(
                        f"space entity is not valid for datatype {self.datatype}"
                    )
                elif space not in allowed_spaces_for_dtype:
                    raise ValueError(
                        f"space ({space}) is not valid for "
                        f"datatype ({self.datatype}).\n"
                        f"Should be one of "
                        f"{allowed_spaces_for_dtype}"
                    )
                else:
                    pass

            # error check suffix
            suffix = self.suffix
            if suffix is not None and suffix not in ALLOWED_FILENAME_SUFFIX:
                raise ValueError(
                    f"Suffix {suffix} is not allowed. "
                    f"Use one of these suffixes "
                    f"{ALLOWED_FILENAME_SUFFIX}."
                )

    @property
    def basename(self):
        """Path basename."""
        basename = []
        for key, val in self.entities.items():
            if val is not None and key != "datatype":
                # convert certain keys to shorthand
                long_to_short_entity = {
                    val: key for key, val in ALLOWED_PATH_ENTITIES_SHORT.items()
                }
                key = long_to_short_entity[key]
                basename.append(f"{key}-{val}")

        if self.suffix is not None:
            if self.extension is not None:
                basename.append(f"{self.suffix}{self.extension}")
            else:
                basename.append(self.suffix)

        basename = "_".join(basename)
        return basename

    @property
    def subject(self) -> str | None:
        """The subject ID."""
        return self._subject

    @subject.setter
    def subject(self, value):
        self.update(subject=value)

    @property
    def session(self) -> str | None:
        """The acquisition session."""
        return self._session

    @session.setter
    def session(self, value):
        self.update(session=value)

    @property
    def task(self) -> str | None:
        """The experimental task."""
        return self._task

    @task.setter
    def task(self, value):
        self.update(task=value)

    @property
    def run(self) -> str | None:
        """The run number."""
        return self._run

    @run.setter
    def run(self, value):
        self.update(run=value)

    @property
    def acquisition(self) -> str | None:
        """The acquisition parameters."""
        return self._acquisition

    @acquisition.setter
    def acquisition(self, value):
        self.update(acquisition=value)

    @property
    def processing(self) -> str | None:
        """The processing label."""
        return self._processing

    @processing.setter
    def processing(self, value):
        self.update(processing=value)

    @property
    def recording(self) -> str | None:
        """The recording name."""
        return self._recording

    @recording.setter
    def recording(self, value):
        self.update(recording=value)

    @property
    def space(self) -> str | None:
        """The coordinate space for an anatomical or sensor position file."""
        return self._space

    @space.setter
    def space(self, value):
        self.update(space=value)

    @property
    def description(self) -> str | None:
        """The description entity."""
        return self._description

    @description.setter
    def description(self, value):
        self.update(description=value)

    @property
    def suffix(self) -> str | None:
        """The filename suffix."""
        return self._suffix

    @suffix.setter
    def suffix(self, value):
        self.update(suffix=value)

    @property
    def root(self) -> Path | None:
        """The root directory of the BIDS dataset."""
        return self._root

    @root.setter
    def root(self, value):
        self.update(root=value)

    @property
    def datatype(self) -> str | None:
        """The BIDS data type, e.g. ``'anat'``, ``'meg'``, ``'eeg'``."""
        return self._datatype

    @datatype.setter
    def datatype(self, value):
        self.update(datatype=value)

    @property
    def split(self) -> str | None:
        """The split of the continuous recording file for ``.fif`` data."""
        return self._split

    @split.setter
    def split(self, value):
        self.update(split=value)

    @property
    def extension(self) -> str | None:
        """The extension of the filename, including a leading period."""
        return self._extension

    @extension.setter
    def extension(self, value):
        self.update(extension=value)

    @property
    def entities(self):
        """Return dictionary of the BIDS entities."""
        return {
            "subject": self.subject,
            "session": self.session,
            "task": self.task,
            "acquisition": self.acquisition,
            "run": self.run,
            "processing": self.processing,
            "space": self.space,
            "recording": self.recording,
            "split": self.split,
            "description": self.description,
        }

    def __str__(self):
        """Return the string representation of the path."""
        return str(self.fpath.as_posix())

    def __repr__(self):
        """Representation in the style of `pathlib.Path`."""
        root = self.root.as_posix() if self.root is not None else None

        return (
            f"{self.__class__.__name__}(\n"
            f"root: {root}\n"
            f"datatype: {self.datatype}\n"
            f"basename: {self.basename})"
        )

    def __fspath__(self):
        """Return the string representation for any fs functions."""
        return str(self.fpath)

    def __eq__(self, other):
        """Compare str representations."""
        return str(self) == str(other)

    def __ne__(self, other):
        """Compare str representations."""
        return str(self) != str(other)

    
