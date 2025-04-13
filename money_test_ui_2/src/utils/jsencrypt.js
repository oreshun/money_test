//密码加密、解密处理
import JSEncrypt from 'jsencrypt/bin/jsencrypt.min'

//公匙
const publicKey = 'MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEApSGlVcQrKKFeyodmSIcP\n' +
    'FmqiRvhotfHrGOfsxO6PD9eoZlvD38o9CFPBtHw5DGcLLoTAi6orPelAKRZHYiqd\n' +
    'RDX9kbrIv+pgIwLURav4xDTplHQCp3D+iEOw+fjnjifBIMNsjHvHZm2kCREdzmky\n' +
    'WrGkO0SxWCSzLMWWDmttTWAP5WYGJT+IH+FI0ZWnpUHC86j4kJKjn7dJhQTe8Gdq\n' +
    '4q+9y7AwY5Coc6M25SxKV02aoFRgXWwg1ifRhFJTvnsCblSQXPxT53JlkJ/8MVYz\n' +
    'E/VREU+Ox7DYPax8IVY1YyZtRBKYbTTtgedZsfAsOtal241wyOjgYY5V0ibxzpl4\n' +
    'igs2ejD59FNvvZuM5UGZ2hv85DRanqY37oRvBF/EK87A8eGrxQkZhVJktUt6VV7H\n' +
    'Oyr8rVAvrKNjHbUZj3LxptzIfqob8zLpNRYnBozh+6QwXzrG4ZSV9h3vDqnWpEj0\n' +
    'GvSXMTS8/2AMu2wVaLejXJJJTkK/dNg4wXZrg9SQNmLfFHfBQG59VqJGu/Ayn/u2\n' +
    'QVzdILRm7m98KooCqJ91u4u1OqC9XpnMe/p5gm1VikSw/6OYzt2eYF12ivEIbfRq\n' +
    'wRKVSqxE1yAgHg5fy5CgqcLD/CbFYGpR6QPmpuVqapq0hCv3bu1lJEsf4dsIvBXf\n' +
    '/UpLdAH5eMGl1Nv+/drTwsUCAwEAAQ=='

//私匙
const privateKey = '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\n' +
    'FLGkvvfDDGKwOSIRsqLwJvdJisrKpQo='

//密码加密
export function encrypt(txt) {
    const encryptor = new JSEncrypt()
    encryptor.setPublicKey(publicKey) // 设置公钥
    return encryptor.encrypt(txt) // 对数据进行加密
}

//密码解密
export function decrypt(txt) {
    const encryptor = new JSEncrypt()
    encryptor.setPrivateKey(privateKey) // 设置私钥
    return encryptor.decrypt(txt) // 对数据进行解密
}
