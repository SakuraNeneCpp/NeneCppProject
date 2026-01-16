#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from datetime import datetime


def _is_yes(v: str) -> bool:
    return str(v).strip().lower() in ("y", "yes", "true", "1", "on")


def _rm(path: Path) -> None:
    if not path.exists():
        return
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()


def _run(cmd: list[str], cwd: Path) -> None:
    subprocess.run(cmd, cwd=str(cwd), check=True)


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _render_license(license_name: str, author: str, email: str) -> str:
    year = datetime.now().year

    if license_name == "MIT":
        return f"""MIT License

Copyright (c) {year} {author} <{email}>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    if license_name == "Apache-2.0":
        return f"""Apache License
Version 2.0, January 2004
http://www.apache.org/licenses/

Copyright {year} {author} <{email}>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
    if license_name == "BSD-3-Clause":
        return f"""BSD 3-Clause License

Copyright (c) {year}, {author} <{email}>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
    if license_name == "Proprietary":
        return f"""All Rights Reserved

Copyright (c) {year} {author} <{email}>

This software is proprietary and confidential. Unauthorized copying, distribution,
modification, or use is prohibited.
"""
    return ""


def main() -> int:
    root = Path.cwd()

    # Cookiecutter variables are injected as strings at template render time.
    use_tests = _is_yes("{{ cookiecutter.use_tests }}")
    test_framework = "{{ cookiecutter.test_framework }}"
    use_subtree = _is_yes("{{ cookiecutter.use_subtree }}")
    use_assets = _is_yes("{{ cookiecutter.use_assets }}")
    use_documents = _is_yes("{{ cookiecutter.use_documents }}")
    add_readme_for_users = _is_yes("{{ cookiecutter.add_readme_for_users }}")
    license_name = "{{ cookiecutter.license }}"
    use_package_init = _is_yes("{{ cookiecutter.use_package_init }}")

    init_git = _is_yes("{{ cookiecutter.init_git }}")
    git_config_local = _is_yes("{{ cookiecutter.git_config_local }}")

    author = "{{ cookiecutter.author_name }}"
    email = "{{ cookiecutter.author_email }}"

    # --- remove optional folders/files ---
    if not use_tests:
        _rm(root / "tests")

    if not use_subtree:
        _rm(root / "subtree")

    if not use_assets:
        _rm(root / "assets")

    if not use_documents:
        _rm(root / "documents")

    if not use_package_init:
        _rm(root / "cmake")  # cmake/Config.cmake.in is only needed for packaging

    # --- README behavior ---
    # If enabled, create an empty README.md (as requested).
    if add_readme_for_users:
        readme_path = root / "README.md"
        if not readme_path.exists():
            _write_text(readme_path, "")
    else:
        _rm(root / "README.md")

    # --- LICENSE ---
    if license_name != "none":
        lic_text = _render_license(license_name, author, email).strip()
        if lic_text:
            _write_text(root / "LICENSE.txt", lic_text + "\n")
            if use_documents:
                _write_text(root / "documents" / "LICENSE.txt", lic_text + "\n")
    else:
        _rm(root / "LICENSE.txt")
        _rm(root / "documents" / "LICENSE.txt")

    # --- git init / local config ---
    if init_git:
        try:
            _run(["git", "init"], cwd=root)
            if git_config_local:
                if author.strip():
                    _run(["git", "config", "--local", "user.name", author], cwd=root)
                if email.strip():
                    _run(["git", "config", "--local", "user.email", email], cwd=root)
        except FileNotFoundError:
            print("git not found; skipping git init")
        except subprocess.CalledProcessError as e:
            print(f"git command failed: {e}")

    print("Project generation complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
