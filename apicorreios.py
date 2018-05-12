import configparser
import requests
import status

config = configparser.ConfigParser()
config.sections()
config.read('bot.conf')

usuario = config['CORREIOS']['usuario']
senha = config['CORREIOS']['senha']
token = config['CORREIOS']['token']


async def get(code, session, retries):
    print("correios")
    try:
        request_xml = '''
            <rastroObjeto>
                <usuario>{}</usuario>
                <senha>{}</senha>
                <tipo>L</tipo>
                <resultado>T</resultado>
                <objetos>{}</objetos>
                <lingua>101</lingua>
                <token>{}</token>
            </rastroObjeto>
        '''.format(usuario, senha, code, token)
        headers = {
            'Content-Type': 'application/xml',
            'Accept': 'application/json',
            'User-Agent': 'Dalvik/1.6.0 (' +
            'Linux; U; Android 4.2.1; LG-P875h Build/JZO34L)'
        }
        url = (
            'http://webservice.correios.com.br/service/rest/rastro/rastroMobile'
        )
        response = await session.post(
            url, data=request_xml, headers=headers, timeout=3
        )
        response = await response.text()
    except Exception:
        if retries > 0:
            return await get(code, retries - 1, session)
        return status.OFFLINE
    if len(str(response)) < 10:
        return status.OFFLINE
    elif 'ERRO' in str(response):
        return status.NOT_FOUND
    return response
