#!/usr/bin/env python3
"""Offline, read-only ScanChat ZIP intake. Never writes to GitHub."""
import argparse
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

class IntakeError(ValueError):
    pass

def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise IntakeError("duplicate JSON key: " + key)
        result[key] = value
    return result

def parse(raw, name):
    try:
        value = json.loads(raw, object_pairs_hook=unique_object)
    except (UnicodeError, ValueError) as exc:
        raise IntakeError(f"{name}: invalid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise IntakeError(f"{name}: expected JSON object")
    return value

def read_archive(path):
    with zipfile.ZipFile(path) as archive:
        infos = archive.infolist()
        if len(infos) > 20000:
            raise IntakeError("too many ZIP entries")
        files = {}
        size = 0
        for info in infos:
            if info.is_dir():
                continue
            name = info.filename
            if not name or name.startswith("/") or "\\" in name or ".." in Path(name).parts or name in files:
                raise IntakeError(f"unsafe or duplicate ZIP entry: {name}")
            size += info.file_size
            if info.file_size > 30000000 or size > 200000000:
                raise IntakeError("ZIP size limit exceeded")
            files[name] = archive.read(info)
    return files

def validate_checksums(files):
    if "checksums.sha256" not in files:
        raise IntakeError("missing checksums.sha256")
    try:
        lines = files["checksums.sha256"].decode("utf-8").splitlines()
    except UnicodeError as exc:
        raise IntakeError("invalid checksum encoding") from exc
    indexed = {}
    for line in lines:
        match = re.fullmatch(r"([0-9a-fA-F]{64})  (.+)", line)
        if not match or match.group(2) in indexed:
            raise IntakeError("malformed or duplicated checksums")
        indexed[match.group(2)] = match.group(1).lower()
    if set(indexed) != set(files) - {"checksums.sha256"}:
        raise IntakeError("checksum inventory mismatch")
    for path, digest in indexed.items():
        if hashlib.sha256(files[path]).hexdigest() != digest:
            raise IntakeError("checksum mismatch: " + path)

def convert(files):
    validate_checksums(files)
    manifest = parse(files["manifest.json"], "manifest.json")
    version = manifest.get("schema_version")
    if version == "scanchat-archive/1.1":
        names = ["conversation.json"]
    elif version == "scanchat-project-archive/1.2":
        names = sorted(name for name in files if name.endswith("/conversation.json"))
    else:
        raise IntakeError("unsupported ScanChat archive version")
    if not names:
        raise IntakeError("no conversations")
    conversations = []
    for name in names:
        if name not in files:
            raise IntakeError("missing conversation: " + name)
        payload = parse(files[name], name)
        if payload.get("schema_version") != "scanchat-conversation/1.1":
            raise IntakeError("unsupported conversation schema")
        messages = payload.get("messages")
        if not isinstance(messages, list):
            raise IntakeError("messages must be array")
        seen = set()
        normalized = []
        for index, item in enumerate(messages):
            if not isinstance(item, dict):
                raise IntakeError("invalid message object")
            key, role, text = item.get("message_key"), item.get("role"), item.get("text")
            attachments = item.get("attachments", [])
            if not isinstance(key, str) or not key or key in seen:
                raise IntakeError("missing or duplicate message key")
            if not isinstance(role, str) or not isinstance(text, str) or not isinstance(attachments, list):
                raise IntakeError("invalid role, text or attachments")
            seen.add(key)
            normalized.append({"index": index, "source_message_key": key, "role": role,
                               "text": text, "native_message_id": item.get("native_message_id"),
                               "turn_id": item.get("turn_id"), "timestamp": None,
                               "timestamp_status": "NOT_AVAILABLE_IN_SOURCE",
                               "attachment_count": len(attachments),
                               "attachment_bytes_verified": False,
                               "collapsed_content_detected": bool(item.get("collapsed_content_detected"))})
        conversations.append({"source_entry": name,
                              "source_sha256": hashlib.sha256(files[name]).hexdigest(),
                              "completeness": "NOT_PROVEN", "messages": normalized})
    return {"schema_version": "cos-scanchat-intake/0.1",
            "profile": "PRIVATE_SINGLE_USER_ANALYSIS_ONLY",
            "read_only": True, "archive_integrity": "SHA256_MANIFEST_VERIFIED",
            "global_completeness": "NOT_PROVEN", "ai_analysis_performed": False,
            "conversation_count": len(conversations), "conversations": conversations,
            "warnings": ["No complete export guarantee", "Attachment bytes not available",
                         "Cross-chat links and message dates are not reconstructed",
                         "No AI conclusions or DONE claims generated"]}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        result = convert(read_archive(args.archive))
        result["source_archive_sha256"] = hashlib.sha256(args.archive.read_bytes()).hexdigest()
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except (OSError, ValueError, zipfile.BadZipFile, KeyError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(f"PASS: {result['conversation_count']} conversations, offline SHA-256 verified")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
