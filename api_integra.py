import requests

def obter_dica_do_dia():# Obter e traduzir dica do dia

    try:
        # Dica em inglês
        response_en = requests.get("https://api.adviceslip.com/advice") ##(API-AdviceSlip)
        if response_en.status_code != 200:
            return False, "Não foi possível obter a dica do dia (API Advice Slip indisponível)."
        
        dica_en = response_en.json()["slip"]["advice"]

        # Parâmetros para a API de tradução
        params = {
            "q": dica_en,
            "langpair": "en|pt-br"
        }

        # Tradução da dica
        response_pt = requests.get("https://api.mymemory.translated.net/get", params=params) ##(API-MyMemory)

        if response_pt.status_code == 200:
            data_pt = response_pt.json()
            dica_pt = data_pt.get("responseData", {}).get("translatedText")
            
            if dica_pt:
                return True, dica_pt
            else:
                return True, f"{dica_en} (Tradução falhou)"
        else:
            # Se a tradução falhar, retorna em inglês mesmo
            return True, f"{dica_en} (Serviço de tradução indisponível)"

    except Exception as e:
        return False, f"Erro ao obter dica: {str(e)}"