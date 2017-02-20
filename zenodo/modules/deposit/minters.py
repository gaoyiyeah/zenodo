# -*- coding: utf-8 -*-
#
# This file is part of Zenodo.
# Copyright (C) 2016 CERN.
#
# Zenodo is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Zenodo is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Zenodo; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Persistent identifier minters."""

from __future__ import absolute_import

from invenio_pidstore.models import (PersistentIdentifier, PIDStatus,
                                     RecordIdentifier)

from invenio_pidrelations.contrib.records import RecordDraft, versioned_minter


def zenodo_deposit_minter(record_uuid, data):
    """Mint deposit identifier."""

    # Reserve the record pid
    recid = zenodo_reserved_record_minter(data=data)

    # Create depid with same pid_value of the recid
    depid = PersistentIdentifier.create(
        'depid',
        str(recid.pid_value),
        object_type='rec',
        object_uuid=record_uuid,
        status=PIDStatus.REGISTERED,
    )

    data.update({
        '_deposit': {
            'id': depid.pid_value,
            'status': 'draft',
        },
    })

    RecordDraft.link(recid, depid)

    return depid


# NOTE: We only add the decorator here since we only want to version the recid
@versioned_minter(pid_type='recid', object_type='rec')
def zenodo_reserved_record_minter(record_uuid=None, data=None):
    id_ = RecordIdentifier.next()
    recid = PersistentIdentifier.create(
        'recid', id_, status=PIDStatus.RESERVED
    )
    data['recid'] = recid.pid_value

    return recid
