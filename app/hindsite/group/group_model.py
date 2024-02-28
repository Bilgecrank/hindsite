"""
Allows the user to search for other users and send invites, while displaying user cards
for all users who belong to the current group.
"""
from app.hindsite.extensions import db
from app.hindsite.common_model import get_user, get_group
from app.hindsite.tables import User, Membership


class UserSearchError(Exception):
    """
    Definition for errors raised by the login function
    """

    message = None

    def __init__(self, message):
        self.message = message


def get_users(term: str):
    """
    Gets a single user record.

    :param term: **str** Email to check against the database
    :returns: **User** or **None**
    """
    users = None
    if term is not None:
        users = db.session.query(User) \
            .filter(User.display_name.icontains(term)
                    | User.email.icontains(term)
                    | User.first_name.icontains(term)
                    | User.last_name.icontains(term))
    return users


def send_invitation(group_id: int, email: str):
    """
    Creates a Membership that signals an invitation to a user, by default the membership
    is not an ownership membership and will have <code>invitation_accepted</code> set to False

    :param group_id: The id of the group attached to the membership.
    :param email: The email of the user to be added to the membership.
    :returns: **Membership** A reference to the membership object.
    """
    user = get_user(email)
    group = get_group(group_id)
    membership = Membership(user, group)
    db.session.add(membership)
    db.session.commit()
    return membership

def get_uninvited_users(group_id: int, term: str):
    """
    Gets all group records that a user hasn't been invited to.
    
    :param group_id: The id of the group being searched for uninvited users.
    :param term: The search term being used to populate the users.
    :returns **list** A list of user objects.
    """
    uninvited_users = []
    members = []
    users = get_users(term)
    group = get_group(group_id)
    #populates a list of members
    for member in group.users:
        members.append(member.user)
    #searches the list of members for users and only appends
    #the uninvited user list if the user isn't present in the list.
    for user in users:
        if user not in members:
            uninvited_users.append(user)
    return uninvited_users
