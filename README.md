
# 📂 Employee Document Extraction Script

**Automated Document Extraction and Organization Using Python**

## 🛠️ Sobre o Projeto

Este repositório contém um script desenvolvido em Python para extrair e organizar documentos de funcionários armazenados no sistema Unico People. A ferramenta foi projetada para facilitar a migração e preservação de dados antes do encerramento do contrato com a plataforma, garantindo eficiência, segurança e organização.

## 🚀 Funcionalidades

- **Autenticação via API**: Conexão segura com a API do Unico People usando token JWT.
- **Download Automatizado**: Extração de documentos, fotos de perfil e comprovantes para cada funcionário.
- **Organização de Arquivos**: Criação de pastas individuais no formato `nome-matricula`, evitando duplicidade.
- **Salvamento de Informações Pessoais**: Armazenamento de dados importantes, como nome, matrícula e contatos, em arquivos `.txt`.
- **Resiliência**: Implementação de verificações para evitar falhas durante o processo.

## 📂 Estrutura do Projeto

```bash
├── employees/
│   ├── Nome_Funcionario-Matricula/
│   │   ├── foto_perfil.jpg
│   │   ├── documento_comprovante.pdf
│   │   ├── informacoes_pessoais.txt
│   │   └── ...
├── extracao_unico_people.py  # Script principal
└── README.md  # Documentação do projeto
```

## ⚙️ Como Utilizar

1. Clone este repositório:
   ```bash
   git clone https://github.com/jhonlucassilva/employee-doc-extraction-unico.git
   ```
2. Instale as dependências
3. Configure o token JWT no script `extracao_unico_people.py`.
4. Execute o script para iniciar a extração:
   ```bash
   python extracao_unico_people.py
   ```

## 🛡️ Considerações de Segurança

- Certifique-se de proteger seu token JWT e demais dados sensíveis.
- Este repositório não inclui informações confidenciais.

## 📜 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
