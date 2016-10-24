#!/usr/bin/env python

"""
Super simple persistency.

This actually writes to two SQLite3 databases, one using SQLite3
directly, the other using the SQLAlchemy ORB.
"""

import os
import sqlite3

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String


def store_sqlite3(ip, port):
    """
    Insert one row into a SQLite database.
    """
    path = 'hma1.db'

    # create table if needed
    if not os.path.exists(path):
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cmd = '''
            CREATE TABLE proxies (
                id INTEGER PRIMARY KEY, 
                ip TEXT, 
                port INT
            )
        '''
        cursor.execute(cmd)
        conn.commit()

    # add entry
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cmd = "INSERT INTO proxies(ip, port) VALUES('%s', '%d')" % (ip, port)
    cursor.execute(cmd)
    conn.commit()


def store_sqlalchemy(ip, port):
    """
    Insert one row into a SQLite database using SQLAlchemy ORB.
    """
    path = 'hma2.db'
    db = create_engine('sqlite:///%s' % path)
    db.echo = False
    metadata = MetaData(db)

    # create table if needed
    if not os.path.exists(path):
        proxies = Table('proxies', metadata,
            Column('id', Integer, primary_key=True),
            Column('ip', String(40)),
            Column('port', Integer),
        )
        proxies.create()
    else:
        proxies = Table('proxies', metadata, autoload=True)

    # add entry
    i = proxies.insert()
    i.execute(ip=ip, port=port)
