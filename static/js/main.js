// static/js/main.js

const API_BASE_URL = '/api'; // Ajuste se a sua API estiver em outro caminho
let accessToken = localStorage.getItem('accessToken');
let refreshToken = localStorage.getItem('refreshToken');

const authSection = document.getElementById('auth-section');
const appSection = document.getElementById('app-section');
const loginForm = document.getElementById('loginForm');
const registerBtn = document.getElementById('registerBtn');
const logoutBtn = document.getElementById('logoutBtn');
const expenseForm = document.getElementById('expenseForm');
const categoryForm = document.getElementById('categoryForm');
const expenseList = document.getElementById('expenseList');
const categorySelect = document.getElementById('categorySelect');
const dailySummary = document.getElementById('dailySummary');
const monthlyChartCanvas = document.getElementById('monthlyChart');
let monthlyChart = null; // Para armazenar a instância do Chart.js

// --- Funções de Autenticação ---

async function login(username, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/token/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Falha no login');
        }
        const data = await response.json();
        accessToken = data.access;
        refreshToken = data.refresh;
        localStorage.setItem('accessToken', accessToken);
        localStorage.setItem('refreshToken', refreshToken);
        console.log('Login bem-sucedido!');
        showAppSection();
        await loadData();
    } catch (error) {
        console.error('Erro de login:', error);
        alert(`Erro de login: ${error.message}`);
    }
}

async function register(username, password) {
    try {
        // No Django, você precisaria de um endpoint de registro separado,
        // ou permitir que o admin crie usuários. Para este exemplo simples,
        // vamos apenas tentar criar via admin se o user for admin
        // ou você pode adicionar um endpoint de registro no views.py do expenses app.
        // Para um projeto real, você criaria um serializer e view para UserRegistration.
        // Por enquanto, vamos simular que o registro foi bem-sucedido e o usuário pode logar.
        alert('A funcionalidade de registro não está implementada via frontend neste exemplo. Por favor, crie um usuário via Django Admin.');
        // Exemplo de como seria se houvesse um endpoint:
        /*
        const response = await fetch('/api/register/', { // Você precisaria criar este endpoint
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.username ? errorData.username[0] : 'Falha no registro');
        }
        alert('Usuário registrado com sucesso! Faça login.');
        */
    } catch (error) {
        console.error('Erro de registro:', error);
        alert(`Erro de registro: ${error.message}`);
    }
}

async function logout() {
    accessToken = null;
    refreshToken = null;
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    console.log('Logout realizado.');
    showAuthSection();
}

async function getAuthenticatedHeaders() {
    if (!accessToken) {
        console.log("Token de acesso não encontrado. Redirecionando para login.");
        showAuthSection();
        return null;
    }

    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`
    };

    return headers;
}

// --- Funções para Interagir com a API de Despesas e Categorias ---

async function fetchCategories() {
    const headers = await getAuthenticatedHeaders();
    if (!headers) return [];
    try {
        const response = await fetch(`${API_BASE_URL}/categories/`, { headers });
        if (response.status === 401) { // Token expirado ou inválido
            console.log("Token expirado ou inválido. Tentando refresh...");
            if (await refreshAccessToken()) {
                return fetchCategories(); // Tenta novamente após o refresh
            } else {
                return [];
            }
        }
        if (!response.ok) throw new Error('Falha ao buscar categorias');
        return await response.json();
    } catch (error) {
        console.error('Erro ao buscar categorias:', error);
        return [];
    }
}

async function fetchExpenses() {
    const headers = await getAuthenticatedHeaders();
    if (!headers) return [];
    try {
        const response = await fetch(`${API_BASE_URL}/expenses/`, { headers });
        if (response.status === 401) {
            console.log("Token expirado ou inválido. Tentando refresh...");
            if (await refreshAccessToken()) {
                return fetchExpenses();
            } else {
                return [];
            }
        }
        if (!response.ok) throw new Error('Falha ao buscar despesas');
        return await response.json();
    } catch (error) {
        console.error('Erro ao buscar despesas:', error);
        return [];
    }
}

async function addExpense(amount, description, categoryId) {
    const headers = await getAuthenticatedHeaders();
    if (!headers) return;
    try {
        const response = await fetch(`${API_BASE_URL}/expenses/`, {
            method: 'POST',
            headers,
            body: JSON.stringify({ amount, description, category: categoryId }),
        });
        if (response.status === 401) {
            if (await refreshAccessToken()) {
                return addExpense(amount, description, categoryId);
            } else {
                return;
            }
        }
        if (!response.ok) throw new Error('Falha ao adicionar despesa');
        await loadData(); // Recarrega os dados após adicionar
    } catch (error) {
        console.error('Erro ao adicionar despesa:', error);
        alert(`Erro ao adicionar despesa: ${error.message}`);
    }
}

async function deleteExpense(id) {
    const headers = await getAuthenticatedHeaders();
    if (!headers) return;
    try {
        const response = await fetch(`${API_BASE_URL}/expenses/${id}/`, {
            method: 'DELETE',
            headers,
        });
        if (response.status === 401) {
            if (await refreshAccessToken()) {
                return deleteExpense(id);
            } else {
                return;
            }
        }
        if (!response.ok) throw new Error('Falha ao deletar despesa');
        await loadData();
    } catch (error) {
        console.error('Erro ao deletar despesa:', error);
        alert(`Erro ao deletar despesa: ${error.message}`);
    }
}

async function addCategory(name) {
    const headers = await getAuthenticatedHeaders();
    if (!headers) return;
    try {
        const response = await fetch(`${API_BASE_URL}/categories/`, {
            method: 'POST',
            headers,
            body: JSON.stringify({ name }),
        });
        if (response.status === 401) {
            if (await refreshAccessToken()) {
                return addCategory(name);
            } else {
                return;
            }
        }
        if (!response.ok) throw new Error('Falha ao adicionar categoria');
        await loadCategoriesToSelect(); // Recarrega as categorias no select
    } catch (error) {
        console.error('Erro ao adicionar categoria:', error);
        alert(`Erro ao adicionar categoria: ${error.message}`);
    }
}

async function fetchDailySummary() {
    const headers = await getAuthenticatedHeaders();
    if (!headers) return null;
    try {
        const response = await fetch(`${API_BASE_URL}/expenses/daily_summary/`, { headers });
        if (response.status === 401) {
            if (await refreshAccessToken()) {
                return fetchDailySummary();
            } else {
                return null;
            }
        }
        if (!response.ok) throw new Error('Falha ao buscar resumo diário');
        return await response.json();
    } catch (error) {
        console.error('Erro ao buscar resumo diário:', error);
        return null;
    }
}

async function fetchMonthlySummary() {
    const headers = await getAuthenticatedHeaders();
    if (!headers) return null;
    try {
        const response = await fetch(`${API_BASE_URL}/expenses/monthly_summary/`, { headers });
        if (response.status === 401) {
            if (await refreshAccessToken()) {
                return fetchMonthlySummary();
            } else {
                return null;
            }
        }
        if (!response.ok) throw new Error('Falha ao buscar resumo mensal');
        return await response.json();
    } catch (error) {
        console.error('Erro ao buscar resumo mensal:', error);
        return null;
    }
}

// --- Funções de Renderização e UI ---

function showAuthSection() {
    authSection.style.display = 'block';
    appSection.style.display = 'none';
}

function showAppSection() {
    authSection.style.display = 'none';
    appSection.style.display = 'block';
}

async function loadCategoriesToSelect() {
    const categories = await fetchCategories();
    categorySelect.innerHTML = '<option value="">Sem Categoria</option>';
    categories.forEach(category => {
        const option = document.createElement('option');
        option.value = category.id;
        option.textContent = category.name;
        categorySelect.appendChild(option);
    });
}

async function loadExpensesToList() {
    const expenses = await fetchExpenses();
    expenseList.innerHTML = ''; // Limpa a lista antes de adicionar novas despesas

    if (expenses.length === 0) {
        expenseList.innerHTML = '<li class="bg-gray-100 p-4 rounded-md text-gray-600 text-center">Nenhuma despesa registrada ainda.</li>';
        return;
    }

    expenses.forEach(expense => {
        const li = document.createElement('li');
        li.className = 'bg-white p-5 rounded-lg shadow-sm flex flex-col sm:flex-row justify-between items-start sm:items-center text-gray-700 border border-gray-200 transition duration-300 ease-in-out hover:shadow-md'; // Adiciona classes Tailwind ao LI

        li.innerHTML = `
            <div class="flex-grow mb-2 sm:mb-0">
                <span class="block text-lg font-medium">R$ ${parseFloat(expense.amount).toFixed(2)} - ${expense.description}</span>
                <span class="block text-sm text-gray-500">Categoria: ${expense.category_name || 'Sem Categoria'} - Data: ${new Date(expense.date).toLocaleDateString()}</span>
            </div>
            <button data-id="${expense.id}"
                    class="bg-red-500 hover:bg-red-600 active:bg-red-700 text-white py-2 px-4 rounded-md shadow-sm transition duration-300 ease-in-out focus:outline-none focus:ring-2 focus:ring-red-400 focus:ring-opacity-75">
                Excluir
            </button>
        `;
        // Adiciona as classes Tailwind ao botão e ao contêiner de texto

        li.querySelector('button').addEventListener('click', (e) => {
            deleteExpense(e.target.dataset.id);
        });
        expenseList.appendChild(li);
    });
}

async function updateDailySummary() {
    const summary = await fetchDailySummary();
    if (summary) {
        dailySummary.textContent = `Total de despesas hoje: R$ ${parseFloat(summary.total_expenses).toFixed(2)}`;
    } else {
        dailySummary.textContent = 'Não foi possível carregar o resumo diário.';
    }
}

async function updateMonthlyChart() {
    const monthlyData = await fetchMonthlySummary();
    if (monthlyData && monthlyData.length > 0) {
        const labels = monthlyData.map(item => item.category__name || 'Sem Categoria');
        const data = monthlyData.map(item => parseFloat(item.total).toFixed(2));

        if (monthlyChart) {
            monthlyChart.destroy(); // Destrói o gráfico anterior se existir
        }

        monthlyChart = new Chart(monthlyChartCanvas, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.7)',
                        'rgba(54, 162, 235, 0.7)',
                        'rgba(255, 206, 86, 0.7)',
                        'rgba(75, 192, 192, 0.7)',
                        'rgba(153, 102, 255, 0.7)',
                        'rgba(255, 159, 64, 0.7)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Resumo Mensal de Despesas por Categoria'
                    }
                }
            }
        });
    } else {
        if (monthlyChart) {
            monthlyChart.destroy();
        }
        // Pode exibir uma mensagem ou placeholder se não houver dados
        const ctx = monthlyChartCanvas.getContext('2d');
        ctx.clearRect(0, 0, monthlyChartCanvas.width, monthlyChartCanvas.height);
        ctx.font = '16px Arial';
        ctx.fillText('Nenhum dado para o resumo mensal.', 50, 100);
    }
}

async function loadData() {
    await loadCategoriesToSelect();
    await loadExpensesToList();
    await updateDailySummary();
    await updateMonthlyChart();
}

// --- Refresh Token Mechanism ---
async function refreshAccessToken() {
    if (!refreshToken) {
        console.log("No refresh token available. User must log in again.");
        showAuthSection();
        return false;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/token/refresh/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ refresh: refreshToken }),
        });

        if (!response.ok) {
            // If refresh token is also invalid, force re-login
            console.error("Refresh token invalid. Forcing re-login.");
            await logout();
            return false;
        }

        const data = await response.json();
        accessToken = data.access;
        localStorage.setItem('accessToken', accessToken);
        console.log('Access token refreshed!');
        return true;
    } catch (error) {
        console.error('Error refreshing token:', error);
        await logout();
        return false;
    }
}

// --- Event Listeners ---

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = e.target.username.value;
    const password = e.target.password.value;
    await login(username, password);
});

registerBtn.addEventListener('click', async () => {
    const username = prompt('Digite o nome de usuário para registro:');
    const password = prompt('Digite a senha para registro:');
    if (username && password) {
        await register(username, password);
    }
});

logoutBtn.addEventListener('click', logout);

expenseForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const amount = parseFloat(e.target.amount.value);
    const description = e.target.description.value;
    const categoryId = e.target.categorySelect.value || null; // Pode ser null se "Sem Categoria"
    if (!isNaN(amount) && description) {
        await addExpense(amount, description, categoryId);
        e.target.reset();
    } else {
        alert('Por favor, preencha o valor e a descrição da despesa.');
    }
});

categoryForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const categoryName = e.target.categoryName.value;
    if (categoryName) {
        await addCategory(categoryName);
        e.target.reset();
    } else {
        alert('Por favor, digite o nome da categoria.');
    }
});

// --- Inicialização ---

// Verifica se há tokens no localStorage ao carregar a página
// Se houver, tenta usar o refresh token para obter um novo access token e carregar a aplicação
// Caso contrário, mostra a seção de autenticação
document.addEventListener('DOMContentLoaded', async () => {
    if (accessToken) {
        if (await refreshAccessToken()) {
            showAppSection();
            await loadData();
        } else {
            showAuthSection();
        }
    } else {
        showAuthSection();
    }
});