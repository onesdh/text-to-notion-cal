conda deactivate&&
conda env remove -n text_to_cal -y&&
conda create -n text_to_cal python=3.12 -y&&
conda activate text_to_cal&&
pip install -r requirements.txt
