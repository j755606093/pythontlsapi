#! /usr/bin/python
# coding:utf-8

__author__ = "tls@tencent.com"
__date__ = "$Mar 3, 2016 03:00:43 PM"

import OpenSSL
import base64
import zlib
import json
import time
import falcon


def list_all_curves():
    list = OpenSSL.crypto.get_elliptic_curves()
    for element in list:
        print element


def get_secp256k1():
    print OpenSSL.crypto.get_elliptic_curve('secp256k1')


def base64_encode_url(data):
    base64_data = base64.b64encode(data)
    base64_data = base64_data.replace('+', '*')
    base64_data = base64_data.replace('/', '-')
    base64_data = base64_data.replace('=', '_')
    return base64_data


def base64_decode_url(base64_data):
    base64_data = base64_data.replace('*', '+')
    base64_data = base64_data.replace('-', '/')
    base64_data = base64_data.replace('_', '=')
    raw_data = base64.b64decode(base64_data)
    return raw_data


class TLSSigAPI:
    """"""
    __acctype = 11893
    __identifier = ""
    __appid3rd = "1400028505"
    __sdkappid = 1400028505
    __version = 20170410
    __expire = 3600 * 24 * 30        # 默认一个月，需要调整请自行修改
    __pri_key = """
-----BEGIN EC PARAMETERS-----
BgUrgQQACg==
-----END EC PARAMETERS-----
-----BEGIN EC PRIVATE KEY-----
MIGEAgEAMBAGByqGSM49AgEGBSuBBAAKBG0wawIBAQQg0f4hJOci0wlo1VCZdBX9
MOLqy8HSnoMOLmluvSnMrW6hRANCAATuErpKeqT3iLekbq/dch2kAQKXgRAJ7Dgs
86lEimO9atnbFe4oyJYAyWaqNgVO0vQ5vNVwzpxy+FXGZczWoOC6
-----END EC PRIVATE KEY-----
"""
    __pub_key = "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE7hK6Snqk94i3pG6v3XIdpAECl4EQCew4LPOpRIpjvWrZ2xXuKMiWAMlmqjYFTtL0ObzVcM6ccvhVxmXM1qDgug=="
    _err_msg = "ok"

    def on_get(self, req, resp, identifier):
        """Handles GET requests"""
        self.__identifier = identifier
        sig = self.tls_gen_sig()
        resp.status = falcon.HTTP_200
        resp.body = sig

    def __get_pri_key(self):
        return OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, self.__pri_key)

    def __create_dict(self):
        m = {}
        m["TLS.account_type"] = "%d" % self.__acctype
        m["TLS.identifier"] = "%s" % self.__identifier
        m["TLS.appid_at_3rd"] = "%s" % self.__appid3rd
        m["TLS.sdk_appid"] = "%d" % self.__sdkappid
        m["TLS.expire_after"] = "%d" % self.__expire
        m["TLS.time"] = "%d" % time.time()
        return m

    def __encode_to_fix_str(self, m):
        fix_str =  "TLS.appid_at_3rd:"+m["TLS.appid_at_3rd"]+"\n" \
                  + "TLS.account_type:" + m["TLS.account_type"] + "\n" \
                  + "TLS.identifier:" + m["TLS.identifier"] + "\n" \
                  + "TLS.sdk_appid:" + m["TLS.sdk_appid"] + "\n" \
                  + "TLS.time:" + m["TLS.time"] + "\n" \
                  + "TLS.expire_after:" + m["TLS.expire_after"] + "\n"
        return fix_str

    def tls_gen_sig(self):
        m = self.__create_dict()
        fix_str = self.__encode_to_fix_str(m)
        pk_loaded = self.__get_pri_key()
        sig_field = OpenSSL.crypto.sign(pk_loaded, fix_str, "sha256")
        sig_field_base64 = base64.b64encode(sig_field)
        m["TLS.sig"] = sig_field_base64
        json_str = json.dumps(m)
        sig_cmpressed = zlib.compress(json_str)
        base64_sig = base64_encode_url(sig_cmpressed)
        return base64_sig


app = falcon.API()
things = TLSSigAPI()
app.add_route('/getsig/{identifier}', things)
