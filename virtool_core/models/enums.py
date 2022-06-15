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
