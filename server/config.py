from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Mailer Agent"
    debug: bool = False

    # Database
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "maileragent"
    db_user: str = "postgres"
    db_password: str = "postgres"
    db_driver: str = "asyncpg"

    @property
    def database_url(self) -> str:
        return f"postgresql+{self.db_driver}://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    # JWT
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiry_hours: int = 24

    # Google OAuth
    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = "http://localhost:8000/api/v1/auth/google/callback"

    # Frontend
    frontend_url: str = "http://localhost:3000"

    # SMTP RSA keys
    rsa_private_key_path: str = ""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
