class BaseConfig:
    DEBUG = True
    SECRET_KEY = '192b9bdd22ab9eg4d12e236c78afcb9a393ec15f71abf5dc987d54727823bcbf'
    # SQLALCHEMY_DATABASE_URI = "postgresql://oleg:1234@localhost:5432/resume"
    SQLALCHEMY_DATABASE_URI = "sqlite:///resume.db"

        ### Flask security
    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_SALT = 'bcrypt'
