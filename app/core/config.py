"""
Configuração centralizada da aplicação.
Carrega configurações de variáveis de ambiente, arquivo .env ou config.cfg.
"""
import os
from pathlib import Path
from configparser import ConfigParser
from dotenv import load_dotenv
from typing import Optional


def get_config_paths() -> tuple[Path, Path, Path]:
    """Retorna os caminhos dos arquivos de configuração."""
    current_dir = Path(__file__).parent.parent.parent
    env_path = current_dir / '.env'
    cfg_path = current_dir / 'config.cfg'
    return current_dir, env_path, cfg_path


def load_config() -> dict:
    """
    Carrega as configurações com a seguinte prioridade:
    1. Variáveis de ambiente do sistema (usadas no Docker com -e ou --env-file)
    2. Arquivo .env (usado em desenvolvimento local)
    3. Arquivo config.cfg (usado quando não há variáveis de ambiente)
    
    Returns:
        dict: Dicionário com as configurações carregadas
        
    Raises:
        ValueError: Se variáveis obrigatórias estiverem faltando
    """
    current_dir, env_path, cfg_path = get_config_paths()
    config = {}
    required_vars = ['AUTH_TOKEN', 'EMAIL_WIPLAY_TOPICO', 'SERVER_IP']
    
    # 1. Tenta carregar de variáveis de ambiente primeiro
    for var in required_vars:
        config[var] = os.getenv(var)
    
    config['PORT'] = os.getenv('PORT')
    config['LOG_LEVEL'] = os.getenv('LOG_LEVEL')
    
    # 2. Se não encontrou nas variáveis de ambiente, tenta arquivo .env
    if not all(config.get(var) for var in required_vars):
        if env_path.exists():
            load_dotenv(env_path, override=False)
            # Atualiza config com valores do .env
            for var in required_vars:
                if not config.get(var):
                    config[var] = os.getenv(var)
            
            if not config.get('PORT'):
                config['PORT'] = os.getenv('PORT')
            
            if not config.get('LOG_LEVEL'):
                config['LOG_LEVEL'] = os.getenv('LOG_LEVEL')
    
    # 3. Se ainda não encontrou, tenta arquivo config.cfg
    if not all(config.get(var) for var in required_vars):
        if cfg_path.exists():
            parser = ConfigParser()
            parser.read(cfg_path)
            
            # Lê valores do arquivo config.cfg
            if parser.has_section('DEFAULT'):
                for var in required_vars:
                    if not config.get(var):
                        config[var] = parser.get('DEFAULT', var, fallback=None)
                
                if not config.get('PORT'):
                    config['PORT'] = parser.get('DEFAULT', 'PORT', fallback='8500')
                
                if not config.get('LOG_LEVEL'):
                    config['LOG_LEVEL'] = parser.get('DEFAULT', 'LOG_LEVEL', fallback='info')
    
    # Valida variáveis obrigatórias
    missing_vars = [var for var in required_vars if not config.get(var)]
    
    if missing_vars:
        error_msg = (
            f"Variáveis obrigatórias não encontradas: {', '.join(missing_vars)}\n"
            f"Configure via variáveis de ambiente, arquivo .env ou config.cfg em: {current_dir}"
        )
        raise ValueError(error_msg)
    
    return {
        'AUTH_TOKEN': config['AUTH_TOKEN'],
        'EMAIL_WIPLAY_TOPICO': config['EMAIL_WIPLAY_TOPICO'],
        'SERVER_IP': config['SERVER_IP'],
        'PORT': config.get('PORT') or '8500',
        'LOG_LEVEL': config.get('LOG_LEVEL') or 'info'
    }


# Carrega configurações uma única vez ao importar o módulo
_config = load_config()

# Variáveis de configuração
AUTH_TOKEN: str = _config['AUTH_TOKEN']
EMAIL_WIPLAY_TOPICO: str = _config['EMAIL_WIPLAY_TOPICO']
SERVER_IP: str = _config['SERVER_IP']
PORT: int = int(_config['PORT'])
LOG_LEVEL: str = _config['LOG_LEVEL']

