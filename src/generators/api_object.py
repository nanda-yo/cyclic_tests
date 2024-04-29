from faker import Faker
from uuid import uuid4
from src.baseclasses.builder import BuilderBaseClass

fake = Faker()


class ApiObjectBuilder(BuilderBaseClass):
    def update_key(self, key):
        method_name = 'generate_' + key
        fn = getattr(self, method_name)
        if callable(fn):
            return fn()
        else:
            return 'not_callable'

    @classmethod
    def generate_pk(cls):
        return str(uuid4())

    @classmethod
    def generate_sk(cls):
        # returns fixed value to ease up the cleaning in case something goes wrong :O
        return str("test")

    @classmethod
    def generate_title(cls):
        return fake.paragraph(nb_sentences=2)

    @classmethod
    def generate_author(cls):
        return fake.name()

    @classmethod
    def generate_description(cls):
        return fake.text(max_nb_chars=300)

    @classmethod
    def build(cls):
        pk = cls.generate_pk()
        sk = cls.generate_sk()
        title = cls.generate_title()
        author = cls.generate_author()
        description = cls.generate_description()
        var1 = fake.isbn10()
        var2 = fake.isbn10()
        var3 = fake.pyfloat()
        params = [
     {
       "var1": var1,
       "var2": var2,
       "var3": var3
     }
   ]

        valid_item_object = {
          "pk": pk,
          "sk": sk,
          "title": title,
          "author": author,
          "description": description,
          "params": params
        }

        return valid_item_object
