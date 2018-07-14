import tornado.ioloop
import tornado.web
import rsa
from yaml import load

from db.repository import Repository
from server_admin.main import WordsHandler, UrlsHandler

# should be replaced with any conf system
with open('public.pem', 'rb') as public:
    public_key = rsa.PublicKey.load_pkcs1_openssl_pem(public.read())
with open('private.pem', 'rb') as private:
    private_key = rsa.PrivateKey.load_pkcs1(private.read())
with open('salt', 'rb') as file:
    salt = file.read()
with open('settings.yml') as file:
    settings = load(file)
repository = Repository(public_key, settings.get('dbUrl'), salt, private_key)


def make_app():
    return tornado.web.Application([
        (r'/adminApi/getWords', WordsHandler, {'repository': repository}),
        (r'/adminApi/getUrls', UrlsHandler, {'repository': repository})
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8889)
    tornado.ioloop.IOLoop.current().start()
