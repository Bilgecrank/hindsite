"""
Class definition for the password table
"""

from src.main import db, intpk


class Password(db.Model):
    """
    Defines the password table to include password hashes and last changed passwords.
    """
