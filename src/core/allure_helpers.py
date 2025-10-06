from __future__ import annotations
import os
from pathlib import Path
import allure


def attach_file(path: Path | str, name: str | None = None, attachment_type: "allure.attachment_type" | None = None):
    """
    Attach an existing file to Allure if it exists.
    """
    p = Path(path)
    if not p.exists():
        return
    display_name = name or p.name
    # Guess type if not provided
    if attachment_type is None:
        if p.suffix.lower() in {".png", ".jpg", ".jpeg"}:
            attachment_type = allure.attachment_type.PNG
        elif p.suffix.lower() in {".txt", ".log"}:
            attachment_type = allure.attachment_type.TEXT
        elif p.suffix.lower() in {".mp4"}:
            attachment_type = allure.attachment_type.MP4
        else:
            attachment_type = allure.attachment_type.TEXT
    with p.open("rb") as f:
        allure.attach(f.read(), name=display_name, attachment_type=attachment_type)


class step:
    """
    `with step("message"): ...` alias around allure.step but resilient if allure not enabled.
    """
    def __init__(self, title: str):
        self.title = title
        self.ctx = None

    def __enter__(self):
        try:
            self.ctx = allure.step(self.title)
            return self.ctx.__enter__()
        except Exception:
            # Allure not initialized or disabled; noop
            return self

    def __exit__(self, exc_type, exc, tb):
        try:
            if self.ctx:
                return self.ctx.__exit__(exc_type, exc, tb)
        except Exception:
            return False
        return False


def add_link(url: str, name: str | None = None):
    """
    Add an external link to the report (visible in Allure).
    """
    try:
        allure.dynamic.link(url, name=name or url)
    except Exception:
        pass


def add_label(name: str, value: str):
    """
    Set custom labels (e.g., suite, epic).
    """
    try:
        allure.dynamic.label(name, value)
    except Exception:
        pass


def add_feature(value: str):
    add_label("feature", value)


def add_suite(value: str):
    add_label("suite", value)
