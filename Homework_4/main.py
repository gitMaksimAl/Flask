from file_downloader import AsyncFileDownloader, FileDownloader
from file_downloader import ThreadsFileDownloader, ProcessFileDownloader
import argparse


def parse():
    parser = argparse.ArgumentParser(
        prog=__name__,
        description="Files downloader with different approaches :),"
                    " Save files to work directory."
    )
    parser.add_argument("--method", default="async",
                        choices=["async", "thread", "process"],
                        help="download method")
    parser.add_argument("--urls", nargs='+', help="list of urls")
    args = parser.parse_args()
    return args.method, args.urls


def create_downloader(method: str) -> FileDownloader:
    match method:
        case "async":
            return AsyncFileDownloader()
        case "thread":
            return ThreadsFileDownloader()
        case "process":
            return ProcessFileDownloader()


if __name__ == '__main__':
    method, urls = parse()
    downloader = create_downloader(method)
    downloader.create_tasks(urls)
    downloader.run(downloader.tasks)
    downloader.exit()
