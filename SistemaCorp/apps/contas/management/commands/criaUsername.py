import re
from django.core.management.base import BaseCommand
from contas.models import MyUser

class Command(BaseCommand):
    help = "Atualizar o Cadastro de usuario adicionando username"
    
    def handle(self, *args, **options):
        myuser = MyUser.objects.all()
        for user in myuser:
             
            get_email = user.email.split("@")[0]
            username = re.sub(r"[^a-zA-Z0-9]","",get_email)
            user.username = username
            user.save()

            self.stdout.write(
                self.style.SUCCESS('username Atualizado com sucesso "%s"' % user.username)
            )