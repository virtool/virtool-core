# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import GenericRepr, Snapshot


snapshots = Snapshot()

snapshots['test_create[pyloop-paired] return'] = {
    'created_at': GenericRepr('datetime.datetime(2015, 10, 6, 20, 0)'),
    'files': [
    ],
    'hash': '68b60be51a667882d3aaa02a93259dd526e9c990',
    'id': '9pfsom1b',
    'legacy': False,
    'missing': False,
    'paired': True,
    'parameters': {
        'end_quality': '20',
        'max_error_rate': '0.1',
        'max_indel_rate': '0.03',
        'max_length': None,
        'mean_quality': '25',
        'min_length': '20',
        'mode': 'pe'
    },
    'program': 'skewer-0.2.2',
    'ready': False,
    'sample': {
        'id': 'foo'
    }
}

snapshots['test_create[pyloop-paired] db'] = {
    '_id': '9pfsom1b',
    'created_at': GenericRepr('datetime.datetime(2015, 10, 6, 20, 0)'),
    'files': [
    ],
    'hash': '68b60be51a667882d3aaa02a93259dd526e9c990',
    'legacy': False,
    'missing': False,
    'paired': True,
    'parameters': {
        'end_quality': '20',
        'max_error_rate': '0.1',
        'max_indel_rate': '0.03',
        'max_length': None,
        'mean_quality': '25',
        'min_length': '20',
        'mode': 'pe'
    },
    'program': 'skewer-0.2.2',
    'ready': False,
    'sample': {
        'id': 'foo'
    }
}

snapshots['test_create[pyloop-unpaired] return'] = {
    'created_at': GenericRepr('datetime.datetime(2015, 10, 6, 20, 0)'),
    'files': [
    ],
    'hash': '68b60be51a667882d3aaa02a93259dd526e9c990',
    'id': '9pfsom1b',
    'legacy': False,
    'missing': False,
    'paired': False,
    'parameters': {
        'end_quality': '20',
        'max_error_rate': '0.1',
        'max_indel_rate': '0.03',
        'max_length': None,
        'mean_quality': '25',
        'min_length': '20',
        'mode': 'pe'
    },
    'program': 'skewer-0.2.2',
    'ready': False,
    'sample': {
        'id': 'foo'
    }
}

snapshots['test_create[pyloop-unpaired] db'] = {
    '_id': '9pfsom1b',
    'created_at': GenericRepr('datetime.datetime(2015, 10, 6, 20, 0)'),
    'files': [
    ],
    'hash': '68b60be51a667882d3aaa02a93259dd526e9c990',
    'legacy': False,
    'missing': False,
    'paired': False,
    'parameters': {
        'end_quality': '20',
        'max_error_rate': '0.1',
        'max_indel_rate': '0.03',
        'max_length': None,
        'mean_quality': '25',
        'min_length': '20',
        'mode': 'pe'
    },
    'program': 'skewer-0.2.2',
    'ready': False,
    'sample': {
        'id': 'foo'
    }
}

snapshots['test_create_legacy[pyloop] return'] = {
    'created_at': GenericRepr('datetime.datetime(2015, 10, 6, 20, 0)'),
    'files': [
    ],
    'hash': '68b60be51a667882d3aaa02a93259dd526e9c990',
    'id': '9pfsom1b',
    'legacy': True,
    'missing': False,
    'paired': False,
    'parameters': {
        'end_quality': '20',
        'max_error_rate': '0.1',
        'max_indel_rate': '0.03',
        'max_length': None,
        'mean_quality': '25',
        'min_length': '20',
        'mode': 'pe'
    },
    'program': 'skewer-0.2.2',
    'ready': False,
    'sample': {
        'id': 'foo'
    }
}

snapshots['test_create_legacy[pyloop] db'] = {
    '_id': '9pfsom1b',
    'created_at': GenericRepr('datetime.datetime(2015, 10, 6, 20, 0)'),
    'files': [
    ],
    'hash': '68b60be51a667882d3aaa02a93259dd526e9c990',
    'legacy': True,
    'missing': False,
    'paired': False,
    'parameters': {
        'end_quality': '20',
        'max_error_rate': '0.1',
        'max_indel_rate': '0.03',
        'max_length': None,
        'mean_quality': '25',
        'min_length': '20',
        'mode': 'pe'
    },
    'program': 'skewer-0.2.2',
    'ready': False,
    'sample': {
        'id': 'foo'
    }
}

snapshots['test_create_program[pyloop] return'] = {
    'created_at': GenericRepr('datetime.datetime(2015, 10, 6, 20, 0)'),
    'files': [
    ],
    'hash': '68b60be51a667882d3aaa02a93259dd526e9c990',
    'id': '9pfsom1b',
    'legacy': False,
    'missing': False,
    'paired': False,
    'parameters': {
        'end_quality': '20',
        'max_error_rate': '0.1',
        'max_indel_rate': '0.03',
        'max_length': None,
        'mean_quality': '25',
        'min_length': '20',
        'mode': 'pe'
    },
    'program': 'trimmomatic-0.2.3',
    'ready': False,
    'sample': {
        'id': 'foo'
    }
}

snapshots['test_create_program[pyloop] db'] = {
    '_id': '9pfsom1b',
    'created_at': GenericRepr('datetime.datetime(2015, 10, 6, 20, 0)'),
    'files': [
    ],
    'hash': '68b60be51a667882d3aaa02a93259dd526e9c990',
    'legacy': False,
    'missing': False,
    'paired': False,
    'parameters': {
        'end_quality': '20',
        'max_error_rate': '0.1',
        'max_indel_rate': '0.03',
        'max_length': None,
        'mean_quality': '25',
        'min_length': '20',
        'mode': 'pe'
    },
    'program': 'trimmomatic-0.2.3',
    'ready': False,
    'sample': {
        'id': 'foo'
    }
}

snapshots['test_create_duplicate[pyloop] return'] = {
    'created_at': GenericRepr('datetime.datetime(2015, 10, 6, 20, 0)'),
    'files': [
    ],
    'hash': '68b60be51a667882d3aaa02a93259dd526e9c990',
    'id': GenericRepr("ObjectId('5f6e1f6e1ef823b67223a8a0')"),
    'legacy': False,
    'missing': False,
    'paired': False,
    'parameters': {
        'end_quality': '20',
        'max_error_rate': '0.1',
        'max_indel_rate': '0.03',
        'max_length': None,
        'mean_quality': '25',
        'min_length': '20',
        'mode': 'pe'
    },
    'program': 'skewer-0.2.2',
    'ready': False,
    'sample': {
        'id': 'foo'
    }
}

snapshots['test_create_duplicate[pyloop] db'] = {
    '_id': '9pfsom1b'
}
