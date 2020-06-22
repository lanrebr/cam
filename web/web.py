#!/usr/bin/env python
import os
from app import app, db, routes

if __name__ == '__main__':
    with app.app_context():
        if app.config.get('DROP_DB') is True:
            db.drop_all()
            db.create_all()
            db.session.commit()
        else:
            db.create_all()
            
    app.run()