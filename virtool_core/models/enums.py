from enum import Enum


class Permission(Enum):
    cancel_job = "cancel_job"
    create_ref = "create_ref"
    create_sample = "create_sample"
    modify_hmm = "modify_hmm"
    modify_subtraction = "modify_subtraction"
    remove_file = "remove_file"
    remove_job = "remove_job"
    upload_file = "upload_file"


class HistoryMethod(Enum):
    add_isolate = "add_isolate"
    create = "create"
    create_sequence = "create_sequence"
    clone = "clone"
    edit = "edit"
    edit_sequence = "edit_sequence"
    edit_isolate = "edit_isolate"
    remove = "remove"
    remote = "remote"
    remove_isolate = "remove_isolate"
    remove_sequence = "remove_sequence"
    import_otu = "import"
    set_as_default = "set_as_default"
    update = "update"


class QuickAnalyzeWorkflow(str, Enum):
    aodp = "aodp"
    nuvs = "nuvs"
    pathoscope_bowtie = "pathoscope_bowtie"
