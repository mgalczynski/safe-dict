import tornado.ioloop
import tornado.web
import rsa

from db.repository import Repository
from server_admin.main import MainAdminHandler

# should be replaced with any conf system
with open('public.pem', 'rb') as public:
    public_key = rsa.PublicKey.load_pkcs1_openssl_pem(public.read())
with open('private.pem', 'rb') as private:
    private_key = rsa.PrivateKey.load_pkcs1(private.read())
with open('salt', 'rb') as file:
    salt = file.read()
repository = Repository(public_key, 'mysql+mysqlconnector://root:password@localhost/dict', salt, private_key)


def make_app():
    return tornado.web.Application([
        (r"/adminApi/getWords", MainAdminHandler, {'repository': repository}),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8889)
    tornado.ioloop.IOLoop.current().start()
