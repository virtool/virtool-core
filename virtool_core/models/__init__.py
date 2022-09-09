from virtool_core.models import user
from virtool_core.models import group
from virtool_core.models import samples
from virtool_core.models import subtraction


group.Group.update_forward_refs(UserNested=user.UserNested)
samples.Sample.update_forward_refs(SubtractionNested=subtraction.SubtractionNested)
subtraction.Subtraction.update_forward_refs(SampleNested=samples.SampleNested)
