import json
import hashlib
import datetime
import requests

import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class GreeApiClient:

  APP_ID: str = "4920681951525131286"
  APP_HASH: str = "0fa513124aa97781d1f3f40d61ca1a89"
  AES_KEY: bytes = b"#G$&^jgfujy6ujxt"

  def __init__(self, base_url: str, username: str, password: str) -> None:
    self.base_url = base_url
    self.username = username
    self.password = password

    self.token = None
    self.user_id = None

  def _md5(self, in_str: str) -> str:
    md5_hash = hashlib.md5()
    md5_hash.update(in_str.encode('utf-8'))
    return md5_hash.hexdigest()

  def _prep_body(self, payload: dict, date: datetime.date, hash_props: list[str]) -> dict:
    t = date.strftime("%Y-%m-%d %H:%M:%S")
    r = int(date.timestamp())

    vc = self._md5(f"{self.APP_ID}_{self.APP_HASH}_{t}_{r}")

    props: list = []
    for p in hash_props:
      props.append(str(payload[p]))

    datVc = self._md5(f"{self.APP_HASH}_{'_'.join(props)}")
    
    return {
      "api": {
        "appId": self.APP_ID,
        "r": r,
        "t": t,
        "vc": vc
      },
      "datVc": datVc
    } | payload
  
  def _encrypt_aes(self, data: str) -> bytes:
    data_bytes = data.encode('utf-8')
    cipher = AES.new(self.AES_KEY, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(data_bytes, AES.block_size))
    return ciphertext

  def _decrypt_aes(self, data: str) -> str:
    cipher = AES.new(self.AES_KEY, AES.MODE_ECB)
    decrypted_data = unpad(cipher.decrypt(data), AES.block_size)
    return decrypted_data.decode('utf-8')
  
  def _send_post_request(self, endpoint: str, data: str) -> str:
    url = f"{self.base_url}{endpoint}"
    
    c_body = self._encrypt_aes(data)
    enc_body = base64.b64encode(c_body)

    res = requests.post(url, enc_body, headers={
      "Content-Type": "application/x-www-form-urlencoded",
      "Gaen1": "5ac2bdf935bcca70",
      "Charset": "utf-8"
    })

    return res.json()
  
  def get_user_id(self):
    return self.user_id

  def login(self, endpoint = "/App/UserLoginV2"):
    d = datetime.datetime.now(datetime.timezone.utc)
    t = d.strftime("%Y-%m-%d %H:%M:%S")

    h = self._md5(self._md5(self.password) + self.password)
    psw = self._md5(h + t)

    body = json.dumps(self._prep_body({
      "psw": psw,
      "t": t,
      "user": self.username
    }, d, ["user", "psw", "t"]))

    res = self._send_post_request(endpoint, body)
    data = self._decrypt_aes(base64.b64decode(res["enRes"]))
    data = json.loads(data)

    self.user_id = data["uid"]
    self.token = data["token"]
  
  def get_homes(self, endpoint = "/App/GetHomes") -> dict:
    d = datetime.datetime.now(datetime.timezone.utc)

    body = json.dumps(self._prep_body({
      "token": self.token,
      "uid": self.user_id
    }, d, ["token", "uid"]))

    res = self._send_post_request(endpoint, body)
    data = self._decrypt_aes(base64.b64decode(res["enRes"]))
    data = json.loads(data)

    return data["home"]

  def get_devices(self, home_id: int, endpoint = "/App/GetDevsInRoomsOfHomeV2") -> dict:
    d = datetime.datetime.now(datetime.timezone.utc)

    body = json.dumps(self._prep_body({
      "token": self.token,
      "homeId": home_id,
      "uid": self.user_id
    }, d, ["token", "uid", "homeId"]))

    res = self._send_post_request(endpoint, body)
    data = self._decrypt_aes(base64.b64decode(res["enRes"]))
    data = json.loads(data)

    devices = []
    for room in data["rooms"]:
      devices.extend(room["devs"])
    
    return devices