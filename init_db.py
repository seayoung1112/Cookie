# -*- coding: utf-8 -*-
from quqi.database import Base, engine
import quqi.models
Base.metadata.create_all(bind=engine)
