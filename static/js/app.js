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

// Busca a citação do dia da API
async function fetchQuote() {
    try {
        const response = await fetch('http://localhost:8000/quote/today');
        const data = await response.json();
        
        const quoteElement = document.getElementById('quote');
        quoteElement.textContent = data.text;
        quoteElement.classList.remove('loading');
        
        document.getElementById('author').textContent = `— ${data.author}`;
    } catch (error) {
        console.error('Erro ao buscar citação:', error);
        const quoteElement = document.getElementById('quote');
        quoteElement.textContent = 'Erro ao carregar a citação do dia. Por favor, tente novamente mais tarde.';
        quoteElement.classList.remove('loading');
    }
}

// Inicializa a página
function init() {
    updateDate();
    fetchQuote();
}

// Executa a função init quando a página for carregada
document.addEventListener('DOMContentLoaded', init);