import argparse
import json
import os
import pathlib
import sys
from importlib import resources
import urllib.parse
from typing import Any

from megalania import Megalania, MegalaniaError


class Usage(Exception):
    pass


def host(name: str, default: str) -> str:
    url = os.environ.get(name) or default
    parts = urllib.parse.urlsplit(url)
    if parts.scheme != "https" and not (parts.scheme == "http" and parts.hostname in ("localhost", "127.0.0.1", "::1")):
        raise Usage(f"{name} must be an https URL, so the key never travels in clear text")
    return url


def client_factory() -> Megalania:
    return Megalania(base_url=host("MEG_BASE_URL", "https://get.megalania.io"),
                     api_url=host("MEG_API_URL", "https://api.megalania.io"))


def body(args: argparse.Namespace) -> dict:
    raw = getattr(args, "json", None)
    extra = json.loads(sys.stdin.read() if raw == "-" else raw) if raw else {}
    if not isinstance(extra, dict):
        raise Usage("--json must be a JSON object")
    flags = {k: v for k, v in vars(args).items()
             if k in ("response_types", "engine", "proxy_tier", "country_code", "max_credits") and v is not None}
    if getattr(args, "crawl", None):
        flags["crawl"] = json.loads(args.crawl)
    return {**extra, **flags}


def out(value: Any) -> None:
    print(json.dumps(value, indent=2))


def install_skill(args: argparse.Namespace) -> None:
    target = pathlib.Path(args.dir).expanduser() / "megalania"
    source = resources.files("megalania") / "skill"
    names = ("SKILL.md", "reference.md")
    for name in names:
        dest = target / name
        if dest.exists() and dest.read_text() != (source / name).read_text() and not args.force:
            raise Usage(f"{dest} was changed; pass --force to overwrite it")
    target.mkdir(parents=True, exist_ok=True)
    for name in names:
        (target / name).write_text((source / name).read_text())
    print(target)


def run(args: argparse.Namespace) -> None:
    if args.cmd == "skill":
        return install_skill(args)
    with client_factory() as meg:
        if args.cmd == "scrape":
            r = meg.scrape(args.url, **body(args))
            if args.output:
                pathlib.Path(args.output).write_bytes(r.content)
            else:
                sys.stdout.buffer.write(r.content)
            print(f"credits_charged={r.headers.credits_charged} request_id={r.headers.request_id}", file=sys.stderr)
        elif args.cmd == "tier":
            out(meg.get_tier(args.host))
        elif args.cmd == "map":
            out(meg.map_site(args.url, **body(args)))
        elif args.cmd == "batch":
            if args.action == "create":
                urls = list(args.urls)
                if args.file:
                    urls += [u.strip() for u in pathlib.Path(args.file).read_text().splitlines() if u.strip()]
                if not urls:
                    raise Usage("batch create needs URLs or --file")
                out(meg.create_batch(urls, **body(args)))
            elif args.action == "wait":
                out(meg.wait_batch(args.id, timeout=args.timeout))
            elif args.action == "results":
                folder = pathlib.Path(args.dir)
                folder.mkdir(parents=True, exist_ok=True)
                n = 0
                for item, data in meg.batch_results(args.id):
                    name = str(item.get("id") or "")
                    if not name or "/" in name or "\\" in name or ".." in name:
                        raise Usage(f"the API sent an item id that is not a safe file name: {name!r}")
                    (folder / name).write_bytes(data)
                    n += 1
                print(f"{n} results in {folder}", file=sys.stderr)
            else:
                out({"get": meg.get_batch, "cancel": meg.cancel_batch}[args.action](args.id))
        elif args.cmd == "monitor":
            a = args.action
            if a == "create":
                out(meg.create_monitor(**body(args)))
            elif a == "list":
                out(meg.list_monitors())
            elif a == "update":
                out(meg.update_monitor(args.id, **body(args)))
            elif a == "delete":
                meg.delete_monitor(args.id)
            else:
                out({"get": meg.get_monitor, "run": meg.run_monitor, "checks": meg.list_monitor_checks}[a](args.id))


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="megalania", description="The Megalania scraping API. The key comes from MEG_API_KEY.")
    sub = p.add_subparsers(dest="cmd", required=True)

    def page_flags(q: argparse.ArgumentParser) -> None:
        q.add_argument("--response-types", dest="response_types")
        q.add_argument("--engine", choices=["http", "browser"])
        q.add_argument("--proxy-tier", dest="proxy_tier", choices=["datacenter", "residential", "mobile"])
        q.add_argument("--country-code", dest="country_code")
        q.add_argument("--max-credits", dest="max_credits", type=int)
        q.add_argument("--json", help="more fields, as a JSON object, or - for stdin")

    s = sub.add_parser("scrape", help="one page; the body goes to stdout")
    s.add_argument("url")
    s.add_argument("-o", "--output")
    page_flags(s)
    t = sub.add_parser("tier", help="what one page of a host costs on each route, free, as JSON")
    t.add_argument("host")
    m = sub.add_parser("map", help="a site's URLs, as JSON")
    m.add_argument("url")
    m.add_argument("--json")
    b = sub.add_parser("batch", help="many pages or a crawl").add_subparsers(dest="action", required=True)
    c = b.add_parser("create")
    c.add_argument("urls", nargs="*")
    c.add_argument("--file")
    c.add_argument("--crawl", help='crawl one site, for example {"max_pages": 50}')
    page_flags(c)
    w = b.add_parser("wait")
    w.add_argument("id")
    w.add_argument("--timeout", type=float, default=3600.0)
    r = b.add_parser("results")
    r.add_argument("id")
    r.add_argument("--dir", required=True)
    for name in ("get", "cancel"):
        b.add_parser(name).add_argument("id")
    mon = sub.add_parser("monitor", help="watch pages for changes").add_subparsers(dest="action", required=True)
    mon.add_parser("create").add_argument("--json", required=True)
    mon.add_parser("list")
    u = mon.add_parser("update")
    u.add_argument("id")
    u.add_argument("--json", required=True)
    for name in ("get", "delete", "run", "checks"):
        mon.add_parser(name).add_argument("id")
    k = sub.add_parser("skill", help="install the agent skill").add_subparsers(dest="action", required=True)
    i = k.add_parser("install")
    i.add_argument("--dir", default="~/.claude/skills")
    i.add_argument("--force", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    p = parser()
    args = p.parse_args(argv)
    try:
        run(args)
    except Usage as e:
        print(f"megalania: {e}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"megalania: bad JSON: {e.msg}", file=sys.stderr)
        return 2
    except ValueError as e:
        print(f"megalania: {e}", file=sys.stderr)
        return 2
    except MegalaniaError as e:
        print(f"error {e.code or e.status}: {e.message} (request {e.request_id})", file=sys.stderr)
        return 1
    except TimeoutError as e:
        print(f"megalania: {e}", file=sys.stderr)
        return 1
    return 0
