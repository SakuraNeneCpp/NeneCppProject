# コマンド一覧

## CMake 初期化（configure）

### 基本（単一構成: Ninja / Makefiles など）
```sh
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
```

### Release で初期化
```sh
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
```

### 生成器を指定（例: Ninja）
```sh
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Debug
```

### マルチ構成（Visual Studio など）の例
```sh
cmake -S . -B build
```

---

## ビルド

### 基本
```sh
cmake --build build -j
```

### 構成指定（Visual Studio 等）
```sh
cmake --build build --config Debug -j
cmake --build build --config Release -j
```

---

## 実行

### 生成物を直接実行（例）
```sh
./build/src/{{cookiecutter.project_slug}}
```

### マルチ構成（Visual Studio 等）の例
```sh
./build/src/Debug/{{cookiecutter.project_slug}}.exe
./build/src/Release/{{cookiecutter.project_slug}}.exe
```

### CTest（tests 有効時）
```sh
ctest --test-dir build -V
```

---

## クリーン

### build ディレクトリごと消す（確実）
```sh
rm -rf build
```

### CMake の clean ターゲット（使える場合）
```sh
cmake --build build --target clean
```

---

## git subtree を追加する（例）

> 先に「subtree を置くディレクトリ」を決める（例: `subtree/somelib`）

### 追加（初回）
```sh
git subtree add --prefix=subtree/somelib https://github.com/OWNER/REPO.git main --squash
```

### 更新（pull）
```sh
git subtree pull --prefix=subtree/somelib https://github.com/OWNER/REPO.git main --squash
```

### こちらの変更を upstream に返す（push）
```sh
git subtree push --prefix=subtree/somelib https://github.com/OWNER/REPO.git main
```

---

## Git の基本操作

### 状態確認
```sh
git status
git diff
```

### 追加 / コミット
```sh
git add .
git commit -m "message"
```

### ブランチ
```sh
git branch
git switch -c feature/xxx
git switch main
```

### リモート設定
```sh
git remote -v
git remote add origin <REMOTE_URL>
```

### push / pull
```sh
git push -u origin main
git pull
```

### ログ
```sh
git log --oneline --graph --decorate -n 30
```

### 一時退避（stash）
```sh
git stash
git stash pop
```

### タグ
```sh
git tag v0.1.0
git push --tags
```

## その他の操作

### フォルダ構成を可視化
```sh
tree
```
フォルダに含まれるファイルまで表示するなら,
```Powershell
tree /F
```