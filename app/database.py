# database.py
import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import pyodbc
from sqlalchemy.engine import URL


Base = declarative_base()


# Database Models
class PortfolioItem(Base):
    __tablename__ = 'portfolio_items'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(Text)
    image_url = Column(String(200))
    project_url = Column(String(200))

class BlogPost(Base):
    __tablename__ = 'blog_posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    content = Column(Text)
    author = Column(String(100))
    created_at = Column(DateTime, default=datetime.now)

class ContactMessage(Base):
    __tablename__ = 'contact_messages'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))
    subject = Column(String(200), nullable=True)
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    email_sent = Column(Boolean, default=False)


module_dir = os.path.dirname(__file__)
env_path = os.path.join(module_dir, ".env")

load_dotenv(env_path)


db_server = os.getenv("DB_SERVER")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_driver = os.getenv("DB_DRIVER") 


connection_string = f"""
    DRIVER={{{db_driver}}};
    SERVER={db_server};
    DATABASE={db_name};
    UID={db_user};
    PWD={db_password};
    Encrypt=No;
    TrustServerCertificate=no;
    Connection Timeout=30;
"""

connection_url = URL.create(
    "mssql+pyodbc",
    query={"odbc_connect": connection_string}
)
engine = create_engine(connection_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(engine)
    session = SessionLocal()
    
    # Add sample data if empty
    if not session.query(PortfolioItem).count():
        portfolio_items = [
            PortfolioItem(
                title="Personal Website",
                description="A personal website showcasing my portfolio and blog.",
                image_url="https://via.placeholder.com/150",
                project_url="https://mywebsite.com"
            ),
            # Add other items...
        ]
        session.add_all(portfolio_items)
    
    if not session.query(BlogPost).count():
        blog_post = BlogPost(
            title="How I Built My Website",
            content="Lorem ipsum dolor sit amet...",
            author="Sai Sri Harsha Guddati"
        )
        session.add(blog_post)
    
    session.commit()
    session.close()

def send_email_notification(message):
    try:
        from pathlib import Path
        module_dir = Path(__file__).parent
        env_path = module_dir / ".env"

        load_dotenv(env_path)
        smtp_server = os.getenv("SMTP_SERVER")
        smtp_port = os.getenv("SMTP_PORT")
        smtp_user = os.getenv("SMTP_USER")
        smtp_password = os.getenv("SMTP_PASSWORD")
        if None in [smtp_server, smtp_port, smtp_user, smtp_password]:
            raise ValueError("Missing email configuration in environment variables")


        smtp_port = int(smtp_port)


        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = os.getenv("NOTIFICATION_EMAIL")
        msg['Subject'] = "New Contact Message Received"
        
        body = f"""Name: {message['name']}
Email: {message['email']}
Message: {message['message']}

Received at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        msg.attach(MIMEText(body, 'plain'))

        # Establish connection based on port
        if smtp_port == 465:
            # SSL Connection
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(smtp_user, smtp_password)
                server.send_message(msg)
        elif smtp_port == 587:
            # STARTTLS Connection
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(msg)
        else:
            raise ValueError(f"Unsupported SMTP port: {smtp_port}")

        return True

    except Exception as e:
        print(f"Email error: {str(e)}")
        return False

def get_db():
    db = SessionLocal()  # Use SessionLocal for creating a session
    try:
        yield db
    finally:
        db.close()


# Database operations
def get_portfolio_items():
    session = SessionLocal()
    items = session.query(PortfolioItem).all()
    session.close()
    return items

def get_blog_posts():
    session = SessionLocal()
    posts = session.query(BlogPost).all()
    session.close()
    return posts

def add_contact_message(name, email, message):
    session = SessionLocal()
    try:
        # Create a new message entry
        new_message = ContactMessage(
            name=name,
            email=email,
            message=message
        )
        session.add(new_message)

        # Send email notification
        try:
            email_sent = send_email_notification({
                'name': name,
                'email': email,
                'message': message
            })
        except Exception as e:
            # Log the email sending failure and handle accordingly
            print(f"Error sending email: {e}")
            email_sent = False  # Or any default value you'd like to set

        # Store the result of email sent
        new_message.email_sent = email_sent
        new_message.subject = None
        new_message.created_at = datetime.now()
        
        # Commit the session to the database
        session.commit()
        return new_message

    except Exception as e:
        # Log the error and rollback in case of failure
        print(f"Error occurred while adding contact message: {e}")
        session.rollback()  # Rollback to prevent partial commits
        return False

    finally:
        session.close()  # Close the session to free up resources


# Initialize database
init_db()