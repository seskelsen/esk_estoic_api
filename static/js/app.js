// Formatar e exibir a data atual
function formatDate() {
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    const today = new Date();
    return today.toLocaleDateString('pt-BR', options);
}

// Atualiza a data na página
function updateDate() {
    document.getElementById('current-date').textContent = formatDate();
}

// Configuração inicial
let currentLanguage = 'pt'; // 'pt' para português, 'en' para inglês
let favorites = JSON.parse(localStorage.getItem('favoriteQuotes')) || [];

// Obtém a URL base para as requisições à API
function getApiBaseUrl() {
    return window.location.origin; // Usando origin que combina protocolo, hostname e porta
}

// Busca a citação do dia ou uma citação aleatória da API
async function fetchQuote(type = 'today', language = currentLanguage) {
    try {
        const baseUrl = getApiBaseUrl();
        const endpoint = language === 'pt' 
            ? `${baseUrl}/quote/${type}` 
            : `${baseUrl}/quote/${type}/en`;
        
        console.log(`Fazendo requisição para: ${endpoint}`); // Log para depuração
        
        const response = await fetch(endpoint, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Cache-Control': 'no-cache'
            },
            // Credentials: 'same-origin' pode ajudar em alguns casos
            credentials: 'same-origin'
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Dados recebidos:', data); // Log para depuração
        
        displayQuote(data);
        return data;
    } catch (error) {
        console.error('Erro ao buscar citação:', error);
        const quoteElement = document.getElementById('quote');
        quoteElement.textContent = 'Erro ao carregar a citação. Por favor, tente novamente mais tarde.';
        quoteElement.classList.remove('loading');
        document.getElementById('author').textContent = '';
    }
}

// Exibe a citação na página
function displayQuote(quoteData) {
    const quoteElement = document.getElementById('quote');
    quoteElement.textContent = quoteData.text;
    quoteElement.classList.remove('loading');
    quoteElement.dataset.id = quoteData.date; // Armazena a data como ID da citação
    
    document.getElementById('author').textContent = `— ${quoteData.author}`;
    
    // Verifica se esta citação está nos favoritos
    updateFavoriteButton(isFavorite(quoteData));
}

// Verifica se uma citação está nos favoritos
function isFavorite(quoteData) {
    return favorites.some(fav => fav.date === quoteData.date);
}

// Atualiza o botão de favoritos
function updateFavoriteButton(isFav) {
    const favButton = document.getElementById('favorite-button');
    if (favButton) {
        favButton.innerHTML = isFav ? '★' : '☆';
        favButton.title = isFav ? 'Remover dos favoritos' : 'Adicionar aos favoritos';
    }
}

// Alterna entre português e inglês
function toggleLanguage() {
    currentLanguage = currentLanguage === 'pt' ? 'en' : 'pt';
    const langButton = document.getElementById('language-toggle');
    if (langButton) {
        langButton.textContent = currentLanguage === 'pt' ? 'EN' : 'PT';
    }
    fetchQuote('today', currentLanguage);
}

// Compartilha a citação atual
function shareQuote() {
    const quote = document.getElementById('quote').textContent;
    const author = document.getElementById('author').textContent;
    
    // Se a API de compartilhamento está disponível no navegador
    if (navigator.share) {
        navigator.share({
            title: 'Citação Estoica',
            text: `"${quote}" ${author}\n\n`,
            url: window.location.href
        })
        .catch(error => console.error('Erro ao compartilhar:', error));
    } else {
        // Fallback para navegadores que não suportam a API de compartilhamento
        const textArea = document.createElement('textarea');
        textArea.value = `"${quote}" ${author}`;
        document.body.appendChild(textArea);
        textArea.select();
        
        try {
            document.execCommand('copy');
            alert('Citação copiada para a área de transferência!');
        } catch (err) {
            console.error('Erro ao copiar citação:', err);
            alert('Não foi possível copiar a citação. Por favor, copie manualmente.');
        }
        
        document.body.removeChild(textArea);
    }
}

// Adiciona ou remove uma citação dos favoritos
function toggleFavorite() {
    const quoteElement = document.getElementById('quote');
    const authorElement = document.getElementById('author');
    
    const quoteId = quoteElement.dataset.id;
    const quoteText = quoteElement.textContent;
    const author = authorElement.textContent.replace('— ', '');
    
    const quoteData = {
        text: quoteText,
        author: author,
        date: quoteId,
        language: currentLanguage
    };
    
    const index = favorites.findIndex(fav => fav.date === quoteId);
    
    if (index === -1) {
        // Adicionar aos favoritos
        favorites.push(quoteData);
        updateFavoriteButton(true);
    } else {
        // Remover dos favoritos
        favorites.splice(index, 1);
        updateFavoriteButton(false);
    }
    
    // Salvar no localStorage
    localStorage.setItem('favoriteQuotes', JSON.stringify(favorites));
}

// Função para alternar o tema entre claro e escuro
function toggleTheme() {
    const body = document.body;
    const themeButton = document.getElementById('theme-toggle');
    
    // Alternar a classe dark-mode
    body.classList.toggle('dark-mode');
    
    // Atualizar o ícone do botão
    const isDarkMode = body.classList.contains('dark-mode');
    themeButton.textContent = isDarkMode ? '☀️' : '🌙';
    themeButton.title = isDarkMode ? 'Mudar para tema claro' : 'Mudar para tema escuro';
    
    // Salvar a preferência do usuário no localStorage
    localStorage.setItem('darkMode', isDarkMode ? 'enabled' : 'disabled');
}

// Função para aplicar o tema preferido do usuário (salvo anteriormente)
function applyTheme() {
    // Verificar se o usuário já tem uma preferência salva
    const savedTheme = localStorage.getItem('darkMode');
    
    // Se o tema escuro estiver salvo como preferência, aplicá-lo
    if (savedTheme === 'enabled') {
        document.body.classList.add('dark-mode');
        if (document.getElementById('theme-toggle')) {
            document.getElementById('theme-toggle').textContent = '☀️';
            document.getElementById('theme-toggle').title = 'Mudar para tema claro';
        }
    }
}

// Criar e adicionar o botão de alternância de tema
function createThemeToggle() {
    const themeButton = document.createElement('button');
    themeButton.id = 'theme-toggle';
    themeButton.className = 'theme-toggle';
    themeButton.textContent = document.body.classList.contains('dark-mode') ? '☀️' : '🌙';
    themeButton.title = document.body.classList.contains('dark-mode') ? 'Mudar para tema claro' : 'Mudar para tema escuro';
    themeButton.addEventListener('click', toggleTheme);
    
    // Adicionar o botão ao body
    document.body.appendChild(themeButton);
}

// Cria e adiciona os botões de controle à interface
function createControls() {
    const controlsDiv = document.createElement('div');
    controlsDiv.className = 'quote-controls';
    
    // Botão de citação aleatória
    const randomButton = document.createElement('button');
    randomButton.id = 'random-button';
    randomButton.textContent = '🔄';
    randomButton.title = 'Citação aleatória';
    randomButton.addEventListener('click', () => fetchQuote('random', currentLanguage));
    
    // Botão de alternar idioma
    const languageButton = document.createElement('button');
    languageButton.id = 'language-toggle';
    languageButton.textContent = currentLanguage === 'pt' ? 'EN' : 'PT';
    languageButton.title = 'Alternar idioma';
    languageButton.addEventListener('click', toggleLanguage);
    
    // Botão de compartilhar
    const shareButton = document.createElement('button');
    shareButton.id = 'share-button';
    shareButton.textContent = '📤';
    shareButton.title = 'Compartilhar citação';
    shareButton.addEventListener('click', shareQuote);
    
    // Botão de favorito
    const favoriteButton = document.createElement('button');
    favoriteButton.id = 'favorite-button';
    favoriteButton.textContent = '☆';
    favoriteButton.title = 'Adicionar aos favoritos';
    favoriteButton.addEventListener('click', toggleFavorite);
    
    // Adiciona os botões ao div de controles
    controlsDiv.appendChild(randomButton);
    controlsDiv.appendChild(languageButton);
    //controlsDiv.appendChild(shareButton);
    controlsDiv.appendChild(favoriteButton);
    
    // Adiciona os controles após o autor
    const authorElement = document.getElementById('author');
    authorElement.parentNode.insertBefore(controlsDiv, authorElement.nextSibling);
}

// Inicializa a página
function init() {
    updateDate();
    applyTheme();
    fetchQuote().then(() => {
        createControls();
        createThemeToggle();
    });
}

// Executa a função init quando a página for carregada
document.addEventListener('DOMContentLoaded', init);