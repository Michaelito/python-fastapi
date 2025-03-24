
import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey

from db.model.base import DeclarativeBase


class UserModel(DeclarativeBase):
    __tablename__ = "tb_user"
    __table_args__ = {"schema": "user"}

    id_user = Column(Integer, primary_key=True, autoincrement=True)
    cd_company = Column(Integer, ForeignKey(
        "user.tb_company.id_company"), nullable=True)
    cd_role = Column(Integer, ForeignKey(
        "user.tb_role.id_role"), nullable=True)
    email = Column(String(200), unique=True, nullable=False)
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(128), nullable=False)
    nickname = Column(String(100), nullable=True)
    document = Column(String(14), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    token = Column(Text, nullable=True)
    token_refresh = Column(Text, nullable=True)
    is_active = Column(Boolean, nullable=True)
    dt_created = Column(DateTime(timezone=True),
                        nullable=False, default=datetime.datetime.utcnow)
    dt_updated = Column(DateTime(timezone=True), nullable=False,
                        default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # company = relationship(
    #     "CompanyModel", backref=backref("users", uselist=True))
    # role = relationship("RoleModel", backref=backref("users", uselist=True))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
