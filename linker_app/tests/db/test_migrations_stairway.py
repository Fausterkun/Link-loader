from flask import current_app

import pytest
from alembic.command import downgrade, upgrade

from alembic.script import ScriptDirectory, Script

from linker_app import migrate


def get_revisions():
    """Get revision list from first to last"""

    # Get alembic config
    config = migrate.get_config()

    # get revision directory
    revision_dir = ScriptDirectory.from_config(config)
    revisions = list(revision_dir.walk_revisions("base", "heads"))
    revisions.reverse()

    return revisions


@pytest.mark.parametrize("revision", get_revisions())
def test_migrations_stairway(app, revision: Script):
    # alembic_config = app.extensions["migrate"].migrate.get_config()
    with app.app_context():
        # TODO: change it to flask-migrate upgrade/downgrade
        alembic_config = current_app.extensions["migrate"].migrate.get_config()
        upgrade(alembic_config, revision.revision)

        downgrade(alembic_config, revision.down_revision or "-1")
        upgrade(alembic_config, revision.revision)
