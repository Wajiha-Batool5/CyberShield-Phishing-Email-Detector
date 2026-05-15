from email_check import predict_email

# Test email examples
test_emails = [

    # PHISHING EMAILS
    "Your bank account has been suspended. Click here immediately to verify your account.",

    "Congratulations! You have won a free iPhone. Submit your personal information now.",

    "Your PayPal account is at risk. Login now to secure your account.",

    "Urgent action required. Reset your password immediately using the link below.",

    "Your account will be permanently blocked within 24 hours if you do not verify your identity.",


    # SAFE EMAILS
    "The meeting is scheduled for tomorrow at 10 AM in the conference room.",

    "Please submit your assignment before Friday.",

    "Happy Birthday! Wishing you a wonderful day.",

    "Your food delivery order has been confirmed successfully.",

    "Dear students, the university portal has been updated with exam schedules."
]

# Loop through emails
for i, email in enumerate(test_emails, start=1):

    result = predict_email(email)

    print("\n" + "="*60)
    print(f"TEST CASE {i}")
    print("="*60)

    print("EMAIL:")
    print(email)

    print("\nPREDICTION:")
    print("Label :", result["label"])
    print("Risk  :", result["risk"])
    print("Score :", result["score"])