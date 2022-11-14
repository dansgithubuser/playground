from aiosmtpd.controller import Controller

class Handler:
    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        if not address.endswith('@example.com'):
            return '550 not relaying to that domain'
        envelope.rcpt_tos.append(address)
        return '250 OK'

    async def handle_DATA(self, server, session, envelope):
        print('Message from %s' % envelope.mail_from)
        print('Message for %s' % envelope.rcpt_tos)
        print('Message data:\n')
        for ln in envelope.content.decode('utf8', errors='replace').splitlines():
            print(f'> {ln}'.strip())
        print('-'*40)
        return '250 Message accepted for delivery'

controller = Controller(Handler())
controller.start()
print('Server started.')
print(f'hostname: {controller.hostname}')
print(f'port    : {controller.port}')
print('Press enter to quit.')
print('-'*40)
input()
controller.stop()
