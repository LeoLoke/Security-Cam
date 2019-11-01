# Author: Rodrigo Graca

from Constants import SEND_MESSAGE

import threading
import logging
import smtplib

carriers = {
    'att': '@mms.att.net',
    'tmobile': ' @tmomail.net',
    'verizon': '@vtext.com',
    'sprint': '@page.nextel.com'
}

threads = []


def send(message: str, number: str, email=False, carrier='att', blocking=False):
    if not SEND_MESSAGE:
        logging.info('Tried to send message when SMS messaging disabled')
        return

    if not blocking:
        thread = threading.Thread(target=send, args=(message, number, email, carrier, True), daemon=True)
        thread.start()

        threads.append(thread)
        return
    # Replace the number with your own, or consider using an argument\dict for multiple people.
    to_number = number + '{}'.format(carriers[carrier])
    auth = ('alertmesystem2056@gmail.com', 'GDrfe35N3Gu%$wD%')

    # Establish a secure session with gmail's outgoing SMTP server using your gmail account
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])

    # Send text message through SMS gateway of destination number
    server.sendmail(auth[0], to_number, message)

    if email:
        server.sendmail(auth[0], email, message)
