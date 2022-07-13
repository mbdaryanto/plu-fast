# PLU Fast

## Install python

di shell bash (ubuntu/debian)

    sudo apt update
    sudo apt install -y build-essential python3-dev python3-venv supervisor vim

## Building .whl

copykan file `companyLogo.png` ke folder `src`

di shell bash dalam, pastikan sudah ada yarn dan python dalam virtualenv

    yarn build
    python -m build

file .whl akan muncul di folder `dist`

## Installation

di shell bash

    mkdir -p ~/Projects/plu/
    cd ~/Projects/plu

copy file `PLU_Fast-x.x.x-py3-none-any.whl` ke folder ini

    python3 -m venv venv
    source venv/bin/activate

sekarang menggunakan virtual environment `venv` ditandai dengan prompt yang ada awalan `venv`

    python -m pip install -U pip setuptools wheel
    pip install -U PLU_Fast-x.x.x-py3-none-any.whl
    pip install "uvicorn[standard]" gunicorn
    python -m plu_app.create_config

isikan parameter untuk koneksi database sesuai dengan prompt.

untuk uji coba sementara bisa menggunakan uvicorn dengan port misal 8081, asumsi menggunakan session ssh <kbd>Enter</kbd> <kbd>~</kbd> <kbd>C</kbd> untuk masuk ke shell ssh lalu ketik (tanpa prompt)

    ssh> -L 1081:localhost:1081

keluar dari shell ssh dengan <kbd>Enter</kbd> x2 lalu jalankan uvicorn di port tersebut

    (venv) $ uvicorn petra_gl.main:app --host 0.0.0.0 --port 1081

test di browser dengan http://localhost:1081/

buat file configuration supervisor di `/etc/supervisor/conf.d/`, untuk listen ke port 80 user harus menggunakan root

    cat << EOF | sudo tee /etc/supervisor/conf.d/plu.conf
    [program:plu]
    command=/home/it/Projects/plu/venv/bin/gunicorn plu_appl.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80
    user=root
    EOF

check status supervisord dengan perintah

    sudo supervisorctl reload
    sudo supervisorctl status all

atau kalau sebelumnya sudah ada atau file baru diedit bisa update saja

    sudo supervisorctl update

cek hasilnya dengan perintah `curl http://localhost/`

