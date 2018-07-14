import tornado.ioloop
import tornado.web
import rsa

from db.repository import Repository
from server.main import MainHandler

# should be replaced with any conf system
with open('public.pem', 'rb') as public:
    public_key = rsa.PublicKey.load_pkcs1_openssl_pem(public.read())
repository = Repository(public_key, 'mysql+mysqlconnector://root:password@localhost/dict')


def make_app():
    return tornado.web.Application([
        (r"/api/generateWordCloud", MainHandler, {'repository': repository}),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
