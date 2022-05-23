import random
from faker import Faker
import click
from flask.cli import with_appcontext
from app.models import *
from app.models.role import Roles


@click.command('seeders')
@with_appcontext
def run():
    '''
    run all seeders to fill database with test data
    '''
    fake = Faker()

    roles = [Role.seeder(Roles.staff), Role.seeder(Roles.admin)]
    memberships = [Membership.seeder(fake) for i in range(3)]

    applications = [Applications.seeders(fake) for i in range(10)]
    members = [Member.seeder(fake) for i in range(5)]
    users = [User.seeders(fake) for i in range(6)]

    for member, user in zip(members, users):
        member.user = user

    for i in applications:
        i.membership = random.choice(memberships)
        i.member = random.choice(members)
        i.approvee = users[-1]
        i.approvee.role = roles[0]

    db.session.add_all(memberships)
    db.session.add_all(applications)
    db.session.commit()


def init_app(app):
    app.cli.add_command(run)
