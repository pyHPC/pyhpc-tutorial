#!/usr/bin/env -S sudo -u ubuntu -- /bin/bash

cd ~

# Install CUDA Toolkit
curl -s -S -L -O https://developer.download.nvidia.com/compute/cuda/12.9.0/local_installers/cuda-repo-debian12-12-9-local_12.9.0-575.51.03-1_amd64.deb
sudo dpkg -i cuda-repo-debian12-12-9-local_12.9.0-575.51.03-1_amd64.deb
sudo cp /var/cuda-repo-debian12-12-9-local/cuda-*-keyring.gpg /usr/share/keyrings/
sudo apt-get update
sudo apt-get -y install cuda-toolkit-12-9
rm cuda-repo-debian12-12-9-local_12.9.0-575.51.03-1_amd64.deb

# Install Python
curl -s -S -L https://astral.sh/uv/install.sh | sh
source ~/.local/bin/env
uv python install 3.13 --default --preview-features python-install-default
uv venv ~/pyhpc-tutorial/.venv
echo "VIRTUAL_ENV_DISABLE_PROMPT=1 source ~/pyhpc-tutorial/.venv/bin/activate" >> ~/.bashrc
source ~/pyhpc-tutorial/.venv/bin/activate

# Install Python packages
uv pip install -r ~/pyhpc-tutorial/build/requirements.txt

# Create a Jupyter service
cat >/etc/systemd/system/jupyterlab.service <<'EOF'
[Unit]
Description=JupyterLab
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/pyhpc-tutorial
Environment=HOME=/home/ubuntu
ExecStart=/bin/bash -lc 'source /home/ubuntu/pyhpc-tutorial/.venv/bin/activate; exec python -m jupyter lab --allow-root --ip=0.0.0.0 --no-browser --NotebookApp.token="" --NotebookApp.password="" --NotebookApp.default_url=""'
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now jupyterlab.service
