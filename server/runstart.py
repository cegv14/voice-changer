Token = '2qaJOZxCQpo9rgvRN5LtY6ZPtoG_5vphrWnTCzLXiXWHBJFLK' # @param {type:"string"}
# @markdown **4** - *(optional)* Change to a region near to you or keep at United States if increase latency\
# @markdown `Default Region: us - United States (Ohio)`
Region = "us - United States (Ohio)" # @param ["ap - Asia/Pacific (Singapore)", "au - Australia (Sydney)","eu - Europe (Frankfurt)", "in - India (Mumbai)","jp - Japan (Tokyo)","sa - South America (Sao Paulo)", "us - United States (Ohio)"]

#@markdown **5** - *(optional)* Other options:
ClearConsole = True  # @param {type:"boolean"}

# ---------------------------------
# DO NOT TOUCH ANYTHING DOWN BELOW!
# ---------------------------------

from pyngrok import conf, ngrok

MyConfig = conf.PyngrokConfig()
MyConfig.auth_token = Token
MyConfig.region = Region[0:2]
#conf.get_default().authtoken = Token
#conf.get_default().region = Region
conf.set_default(MyConfig);

import subprocess, threading, time, socket, urllib.request
PORT = 8000

from pyngrok import ngrok
ngrokConnection = ngrok.connect(PORT)
public_url = ngrokConnection.public_url
print("conectado")
print(public_url)
def wait_for_server():
    print("Entro funcion")
    while True:
        time.sleep(0.5)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', PORT))
        if result == 0:
            break
        sock.close()
    if ClearConsole:
        clear_output()
    print("--------- SERVER READY! ---------")
    print("Your server is available at:")
    print(public_url)
    print("---------------------------------")

threading.Thread(target=wait_for_server, daemon=True).start()

python MMVCServerSIO.py \
  -p {PORT} \
  --https False \
  --content_vec_500 pretrain/checkpoint_best_legacy_500.pt \
  --content_vec_500_onnx pretrain/content_vec_500.onnx \
  --content_vec_500_onnx_on true \
  --hubert_base pretrain/hubert_base.pt \
  --hubert_base_jp pretrain/rinna_hubert_base_jp.pt \
  --hubert_soft pretrain/hubert/hubert-soft-0d54a1f4.pt \
  --nsf_hifigan pretrain/nsf_hifigan/model \
  --crepe_onnx_full pretrain/crepe_onnx_full.onnx \
  --crepe_onnx_tiny pretrain/crepe_onnx_tiny.onnx \
  --rmvpe pretrain/rmvpe.pt \
  --model_dir model_dir \
  --samples samples.json

ngrok.disconnect(ngrokConnection.public_url)
