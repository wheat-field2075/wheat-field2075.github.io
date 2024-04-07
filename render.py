import yaml
from jinja2 import Environment
import base64
import hashlib


def template_authors(data):
    people = {}
    # replace authors with markdown with link to profiles
    for person in data["people"]:
        assert person["name"] not in people
        people[person["name"]] = person["link"]

    for publication in data["publications"]:
        publication["authors"] = ", ".join(
            [people[author] for author in publication["authors"]]
        )
def get_hash(name):
    hasher = hashlib.sha1(name.encode("utf-8"))
    hash = base64.urlsafe_b64encode(hasher.digest()[:5])
    hash = [x for x in hash.decode("utf-8") if x.isalnum()]
    hash = "".join(hash)
    hash = "_" + hash # since function names can't start with a number
    return hash

def template_hash(data):
    hashes = set()
    for publication in data["publications"]:
        hash = get_hash(publication["name"])
        assert hash not in hashes, "hash collision"
        publication["hash"] = hash


data = yaml.load(open("data.yaml"), Loader=yaml.FullLoader)
template_authors(data)
template_hash(data)

env = Environment(extensions=['jinja_markdown.MarkdownExtension'])

template = env.from_string(
    open("template.html").read(),
)

output = template.render(**data)
open("index.html", "w").write(output)

print("done")
