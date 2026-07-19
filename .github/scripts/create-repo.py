import gzip
import html
import json
import os
import re
import shutil
import struct
import subprocess
from pathlib import Path
from typing import cast
from zipfile import ZipFile

from google.protobuf import json_format

import index_pb2

APK_BASE_URL = f"https://cdn.jsdelivr.net/gh/MajorTanya/mihon-dummyextension@repo/apk"
ICON_BASE_URL = f"https://cdn.jsdelivr.net/gh/MajorTanya/mihon-dummyextension@repo/icon"


PACKAGE_NAME_REGEX = re.compile(r"package: name='([^']+)'")
VERSION_CODE_REGEX = re.compile(r"versionCode='([^']+)'")
VERSION_NAME_REGEX = re.compile(r"versionName='([^']+)'")
APPLICATION_LABEL_REGEX = re.compile(r"^application-label:'([^']+)'", re.MULTILINE)
APPLICATION_ICON_320_REGEX = re.compile(
    r"^application-icon-320:'([^']+)'", re.MULTILINE
)
LANGUAGE_REGEX = re.compile(r"tachiyomi-([^.]+)")

*_, ANDROID_BUILD_TOOLS = (Path(os.environ["ANDROID_HOME"]) / "build-tools").iterdir()
REPO_DIR = Path("repo")
REPO_APK_DIR = REPO_DIR / "apk"
REPO_ICON_DIR = REPO_DIR / "icon"

REPO_ICON_DIR.mkdir(parents=True, exist_ok=True)

try:
    shutil.rmtree(REPO_APK_DIR)
except FileNotFoundError:
    pass

REPO_APK_DIR.mkdir(parents=True, exist_ok=True)

for apk in (Path.home() / "apk-artifacts").glob("**/*.apk"):
    apk_name = apk.name.replace("-release.apk", ".apk")

    shutil.move(apk, REPO_APK_DIR / apk_name)

extensions: list[index_pb2.Extension] = []

for apk in REPO_APK_DIR.iterdir():
    apk_name = apk.name.replace("-release.apk", ".apk")
    (REPO_APK_DIR / apk_name).write_bytes(apk.read_bytes())

    badging = subprocess.check_output(
        [
            ANDROID_BUILD_TOOLS / "aapt",
            "dump",
            "--include-meta-data",
            "badging",
            apk,
        ]
    ).decode()

    badging_lines = badging.splitlines()

    package_info: str | None = None
    content_warning: int | None = None
    extension_lib_version: str | None = None

    for line in badging_lines:
        if line.startswith("package: "):
            package_info = line
        elif line.startswith("meta-data: "):
            key = line.removeprefix("meta-data: name='")
            key, value = key.split("'", maxsplit=1)
            value = value.removeprefix(" value='").removesuffix("'")

            if key == "tachiyomix.extensionLib":
                # untwiddle the IEEE-754 float from the hex representation
                value = str(
                    cast(
                        float,
                        round(
                            struct.unpack(
                                "!f",
                                struct.pack("!I", int(value, base=16) & 0xFFFFFFFF),
                            )[0],
                            ndigits=1,
                        ),
                    )
                )
                extension_lib_version = value

            elif key == "tachiyomix.contentWarning":
                value = int(value)
                if value == 0:
                    content_warning = index_pb2.CONTENT_WARNING_UNSPECIFIED
                elif value == 1:
                    content_warning = index_pb2.CONTENT_WARNING_SAFE
                elif value == 2:
                    content_warning = index_pb2.CONTENT_WARNING_MIXED
                elif value == 3:
                    content_warning = index_pb2.CONTENT_WARNING_NSFW
                else:
                    raise ValueError(f"Unknown ContentWarning: {value}")

            print(f"{key, value=}")

    if package_info is None:
        raise ValueError("Could not find package_info")
    if content_warning is None:
        raise ValueError("Could not find ContentWarning")
    if extension_lib_version is None:
        raise ValueError("Could not find extensionLib version")

    package_name = PACKAGE_NAME_REGEX.search(package_info).group(1)
    application_icon = APPLICATION_ICON_320_REGEX.search(badging).group(1)
    name = APPLICATION_LABEL_REGEX.search(badging).group(1)
    version_name = VERSION_NAME_REGEX.search(package_info).group(1)
    version_code = int(VERSION_CODE_REGEX.search(package_info).group(1))

    with (
        ZipFile(apk) as z,
        z.open(application_icon) as i,
        (REPO_ICON_DIR / f"{package_name}.png").open("wb") as f,
    ):
        f.write(i.read())

    extensions.append(
        index_pb2.Extension(
            name=name,
            packageName=package_name,
            resources=index_pb2.Resources(
                apkUrl=f"{APK_BASE_URL}/{apk_name}",
                iconUrl=f"{ICON_BASE_URL}/{package_name}.png",
            ),
            extensionLib=extension_lib_version,
            versionCode=version_code,
            versionName=version_name,
            contentWarning=index_pb2.CONTENT_WARNING_SAFE,
            sources=[
                index_pb2.Source(
                    id=7326071459150356677,
                    name=name,
                    language="all",
                    homeUrl="https://example.com",
                    mirrorUrls=[],
                )
            ],
        )
    )

index = index_pb2.Index(
    name="Dummy Extension Repo",
    badgeLabel="DUMMY",
    signingKey="debefdf6a48f69a10ed908b5185b111926cf9487f3e17149ca9a2baf10153106",
    contact=index_pb2.Contact(
        website="https://github.com/MajorTanya/mihon-dummyextension",
    ),
    extensionList=index_pb2.ExtensionList(extensions=extensions),
)

with open(REPO_DIR / "index.json", mode="w", encoding="utf8") as f:
    f.write(
        json_format.MessageToJson(
            index,
            always_print_fields_with_no_presence=False,
            preserving_proto_field_name=True,
        )
    )

with open(REPO_DIR / "index.pb", mode="wb") as f:
    f.write(gzip.compress(index.SerializeToString()))


def get_legacy_lang(ext: index_pb2.Extension) -> str:
    apk_filename = ext.resources.apkUrl.split("/")[-1]
    lang = LANGUAGE_REGEX.search(apk_filename).group(1)
    if len(ext.sources) == 1:
        source_language = ext.sources[0].language
        if (
            source_language != lang
            and source_language not in {"all", "other"}
            and lang not in {"all", "other"}
        ):
            lang = source_language
    return lang


legacy_json_index = [
    {
        "name": f"Tachiyomi: {ext.name}",
        "pkg": ext.packageName,
        "apk": ext.resources.apkUrl.split("/")[-1],
        "lang": get_legacy_lang(ext),
        "code": ext.versionCode,
        "version": ext.versionName,
        "nsfw": 1 if ext.contentWarning > 2 else 0,
        "sources": [
            {
                "name": source.name,
                "lang": source.language,
                "id": str(source.id),
                "baseUrl": source.homeUrl,
            }
            for source in ext.sources
        ],
    }
    for ext in extensions
]

with open(REPO_DIR / "index.min.json", mode="w", encoding="utf8") as f:
    json.dump(legacy_json_index, f, ensure_ascii=False, separators=(",", ":"))

with open(REPO_DIR / "index.html", mode="w", encoding="utf8") as f:
    f.write(
        "<!DOCTYPE html>\n"
        "<html>\n"
        "<head>\n"
        '<meta charset="UTF-8">\n'
        "<title>apks</title>\n"
        "</head>\n"
        "<body>\n"
        "<pre>\n"
    )
    for ext in extensions:
        apk_escaped = html.escape(ext.resources.apkUrl)
        name_escaped = html.escape(f"Tachiyomi: {ext.name}")
        f.write(f'<a href="{apk_escaped}">{name_escaped}</a>\n')
    f.write("</pre>\n</body>\n</html>\n")
