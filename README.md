# RE_DENCHU
# kivyを使用したターン制バトルゲーム

kivyのインストール手順

% cd ソースを置いているディレクトリ
% /usr/bin/python3 -m venv venv
% source venv/bin/activate
(venv) % pip install --upgrade pip
(venv) % pip install kivy
(venv) % deactivate
%   <== (venv)の表示が消える

インストール後、以下で実行

% cd ソース（とvenv）を置いているディレクトリ
% source venv/bin/activate　　　　　＃実行時に一度だけ必要
(venv) % python kivyView.py　　　　＃venvがactiveの時はpython3ではなくpython
