from smtplib import SMTP

print(
    SMTP('::1', 8025)
        .sendmail(
            'dog@example.com',
            ['bird@example.com'],
            'woof!',
        )
)
