import random
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import APIRouter, HTTPException, Form, Depends , Header
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.security import validate_token
from datetime import datetime, timedelta
from app.models import User, user_nameAndOTP  # Ensure models are correctly imported

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# SMTP Configuration
SMTP_SERVER = "email-smtp.ap-south-1.amazonaws.com"  # Change to Mumbai region
SMTP_PORT = 587  # Keep the same port
SMTP_user_name = "AKIA2NPZE34AIL52QD44"  # Change to new SMTP user_name
SMTP_PASSWORD = "BGG7nhwb8doIy52V/wvA/wjl1fUU0QA12p7tcQLthCXG"  # Change to new SMTP password
sender_email = "prakash.n@samyudhi.com"  # Sender's email address

# Create a router instance
router = APIRouter()

# **Step 1: Forgot Password - Generate otp and Send Email**
@router.post("/ForgOTPassword")
def forgot_password(
    user_name: str = Form(...),
    db: Session = Depends(get_db)
):
    logging.info(f"Received forgot password request for user_name: {user_name}")

    # Query to check if the user exists and is active
    user = db.query(User).filter(User.user_login_id == user_name, User.active_flag == 1).first()
    if not user:
        logging.warning(f"User {user_name} not found or inactive.")
        raise HTTPException(status_code=404, detail="User not found")
    logging.debug(f"User {user_name} found and active.")

    # Generate otp
    otp = random.randint(100000, 999999)
    generated_at = datetime.now()
    valid_until = generated_at + timedelta(minutes=25)
    logging.debug(f"Generated otp for {user_name}: {otp}, valid until {valid_until}")

    # Check if otp already exists for the user, and update if necessary
    existing_entry = db.query(user_nameAndOTP).filter(user_nameAndOTP.user_name == user_name).first()
    if existing_entry:
        existing_entry.otp = otp
        existing_entry.generated_at = generated_at
        existing_entry.valid_until = valid_until
        logging.debug(f"Updated existing otp entry for {user_name}.")
    else:
        new_entry = user_nameAndOTP(user_name=user_name, otp=otp, generated_at=generated_at, valid_until=valid_until)
        db.add(new_entry)
        logging.debug(f"Created new otp entry for {user_name}.")

    db.commit()
    logging.info(f"Stored otp for {user_name} with expiration time: {valid_until}.")

    # Send email with the otp
    try:
        send_email_ses(user.user_e_mail_id, otp, db)  # Pass user email and otp
        logging.info(f"otp sent to {user_name}'s email.")
    except Exception as e:
        logging.error(f"Failed to send otp email to {user_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to send otp email.")

    return {
        "user_name": user_name,
        "message": "otp sent to your email."
    }


# **Step 2 & 3: Verify otp & Reset Password in One API**
@router.post("/VerifyAndResetPassword")
def verify_and_reset_password(
    user_name: str = Form(...),
    otp: int = Form(...),
    new_password: str = Form(...),
    db: Session = Depends(get_db)
):
    logging.info(f"Received otp verification & password reset request for user_name: {user_name}")

    otp_entry = db.query(user_nameAndOTP).filter(user_nameAndOTP.user_name == user_name).first()
    if not otp_entry:
        logging.warning(f"No otp found for user {user_name}.")
        raise HTTPException(status_code=400, detail="otp not found")

    if datetime.now() > otp_entry.valid_until:
        logging.warning(f"otp for user {user_name} has expired.")
        raise HTTPException(status_code=400, detail="otp expired")

    if otp_entry.otp != otp:
        logging.warning(f"Incorrect otp for user {user_name}.")
        raise HTTPException(status_code=400, detail="Invalid otp")

    logging.info(f"User {user_name} successfully verified with otp.")

    user = db.query(User).filter(User.user_login_id == user_name).first()
    if not user:
        logging.warning(f"User {user_name} not found for password reset.")
        raise HTTPException(status_code=404, detail="User not found")

    user.user_password = new_password
    db.commit()
    logging.info(f"Password reset successfully for user {user_name}")

    db.query(user_nameAndOTP).filter(user_nameAndOTP.user_name == user_name).delete()
    db.commit()
    logging.info(f"Cleaned up otp records for {user_name}")

    return {"message": "Password reset successful. You may now log in with your new password."}


def send_email_ses(recipient_email, otp, db):
    user = db.query(User).filter(User.user_e_mail_id == recipient_email).first()
    
    if not user:
        logging.warning(f"User with email {recipient_email} not found.")
        return
    
    full_name = f"{user.user_first_name} {user.user_last_name}"
    
    subject = "Your otp for Password Reset"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    body = f"""
    Hi {full_name},

    Your otp is {otp}. Please use it to reset your password.

    Thank you!
    """
    msg.attach(MIMEText(body, "plain"))

    try:
        logging.info("Connecting to SMTP server...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        logging.info("Logging in to SMTP server...")
        server.login(SMTP_user_name , SMTP_PASSWORD)
        server.login(SMTP_user_name , SMTP_PASSWORD)
        server.login(SMTP_user_name , SMTP_PASSWORD)
        server.login(SMTP_user_name , SMTP_PASSWORD)
        logging.info(f"Sending email to {recipient_email}...")
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        logging.info("Email sent successfully!")

    except Exception as e:
        logging.error(f"Error sending email: {e}")
        raise HTTPException(status_code=500, detail="Failed to send otp email.")
    
