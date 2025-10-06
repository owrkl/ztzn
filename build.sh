apt-get update
apt-get install -y --no-install-recommends gcc libxml2-dev libxslt1-dev
rm -rf /var/lib/apt/lists/*
python -m pip install --upgrade pip
pip install lxml --only-binary :all:
pip install -r requirements.txt
