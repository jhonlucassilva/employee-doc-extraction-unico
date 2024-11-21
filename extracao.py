import os
import time
import requests
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Configurações
API_BASE_URL = "https://api.acessorh.com.br/v1"
JWT_TOKEN = ""   # Substitua pelo seu token JWT
HEADERS = {"Authorization": f"Bearer {JWT_TOKEN}"}


def get_positions(skip=2, limit=2):
    url = f"{API_BASE_URL}/positions?skip={skip}&limit={limit}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro na requisição: {response.status_code}")
        return None

def get_position_details(position_id):
    url = f"{API_BASE_URL}/positions/{position_id}?includes=persons&includes=attachments"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro na requisição: {response.status_code}")
        return None

def download_file(file_path, save_path):
    url = f"{API_BASE_URL}/r/{file_path}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            file.write(response.content)
        print(f"Arquivo baixado e salvo em: {save_path}")
    else:
        print(f"Erro ao baixar arquivo: {response.status_code} - URL: {url}")

def save_employee_info(employee_data, folder_name):
    """
    Salva as informações pessoais do funcionário em um arquivo .txt
    """
    if 'profile' not in employee_data:
        print("Dados de perfil não encontrados no funcionário")
        return
    
    profile = employee_data['profile']
    employee_name = profile.get('name', 'Nome não disponível')
    matricula = employee_data.get('num_matricula', 'Não disponível')
    email = profile.get('email', 'Não disponível')
    mobile = profile.get('mobile', 'Não disponível')
    
    info_content = f"Nome: {employee_name}\n"
    info_content += f"Matrícula: {matricula}\n"
    info_content += f"Email: {email}\n"
    info_content += f"Celular: {mobile}\n"
    
    # Caminho do arquivo .txt
    info_file_path = os.path.join(folder_name, "informacoes_pessoais.txt")
    
    # Escreve as informações no arquivo .txt
    with open(info_file_path, "w") as info_file:
        info_file.write(info_content)

def save_documents_comprovantes(documents, folder_name):
    """
    Baixa todos os comprovantes dos documentos de um funcionário.
    """
    for document in documents:
        title = document['title']['pt_BR']
        
        # Verificação se 'data' não é None
        data = document.get('data')
        if data is None:
            print(f"Nenhum dado disponível para o documento: {title}")
            continue
        
        comprovantes = data.get('comprovantes', [])
        
        # Verifica se há comprovantes
        if not comprovantes:
            print(f"Nenhum comprovante encontrado para {title}")
            continue
        
        for comprovante in comprovantes:
            file_info = comprovante['file']
            file_name = f"{title}_{file_info['name']}".encode('utf-8').decode('utf-8')  # Forçando UTF-8
            file_path = file_info['path']
            save_path = os.path.join(folder_name, file_name)
            
            print(f"Baixando comprovante {file_name}")
            download_file(file_path, save_path)
            print(f"Comprovante {file_name} salvo em {save_path}")

def save_employee_documents(employee_data):
    profile = employee_data['profile']
    employee_name = profile.get('name', 'Desconhecido')
    matricula = employee_data.get('num_matricula', 'Sem_matricula')

    # Formato da pasta: "nome-matricula"
    employee_folder = f"./employees/{employee_name}_{matricula}"
    os.makedirs(employee_folder, exist_ok=True)

    # Salva a foto do perfil
    if 'photo' in employee_data['profile']:
        photo = employee_data['profile']['photo']
        if 'path' in photo:
            file_name = photo.get('filename', 'foto_desconhecida.jpg')
            file_path = photo['path']
            save_path = os.path.join(employee_folder, file_name)
            
            print(f"Baixando foto de perfil para {employee_name}")
            download_file(file_path, save_path)
        else:
            print(f"Nenhum caminho de foto encontrado para {employee_name}")
    
    # Salva os comprovantes de todos os documentos
    if 'persons' in employee_data:
        for person in employee_data['persons']:
            person_documents = person.get('documents', [])  # Corrigido para acessar documentos diretamente
            if person_documents:
                print(f"Documentos encontrados para {employee_name}")
                save_documents_comprovantes(person_documents, employee_folder)
            else:
                print(f"Nenhum documento encontrado para {employee_name}")
    
    # Salva as informações pessoais em um arquivo .txt
    save_employee_info(employee_data, employee_folder)

def process_employees(batch_size):
    skip = 2
    total_downloaded = 0

    while total_downloaded < batch_size:
        positions_data = get_positions(skip=skip, limit=batch_size)
        if positions_data and 'positions' in positions_data:
            for position in positions_data['positions']:
                position_details = get_position_details(position['id'])
                if position_details:
                    save_employee_documents(position_details)
                
                total_downloaded += 1
                if total_downloaded >= batch_size:
                    break
                time.sleep(5)  # Pausa de 5 segundos entre requisições
        else:
            print("Erro ou nenhuma posição encontrada")
            break

        skip += batch_size

if __name__ == "__main__":
    batch_size = 2  # Ajuste o número de funcionários por lote
    process_employees(batch_size)