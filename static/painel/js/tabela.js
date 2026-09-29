const searchInput = document.getElementById("searchInput");
const itemsPerPage = document.getElementById("itemsPerPage");
const tableBody = document.getElementById("tableBody");
const pagination = document.getElementById("pagination");
const tableInfo = document.getElementById("tableInfo");

let currentPage = 1;

/* Obtém todas as linhas da tabela */
function getRows() {
    return Array.from(tableBody.querySelectorAll("tr"));
}

/* Filtra as linhas */
function getFilteredRows() {
    const search = searchInput.value.toLowerCase().trim();

    return getRows().filter((row) => {
        const text = row.textContent.toLowerCase();

        return text.includes(search);
    });
}

/* Renderiza a tabela */
function renderTable() {
    const rows = getFilteredRows();
    const perPage = Number(itemsPerPage.value);
    const totalPages = Math.max(1, Math.ceil(rows.length / perPage));

    if (currentPage > totalPages) {
        currentPage = totalPages;
    }

    const start = (currentPage - 1) * perPage;
    const end = start + perPage;
    const visibleRows = rows.slice(start, end);

    getRows().forEach((row) => {
        row.style.display = "none";
    });

    visibleRows.forEach((row) => {
        row.style.display = "";
    });

    renderPagination(totalPages);
    updateTableInfo(rows.length, start, visibleRows.length);
}

/* Atualiza informações da tabela */
function updateTableInfo(total, start, visible) {
    if (total === 0) {
        tableInfo.textContent = "Nenhum registro encontrado";

        return;
    }

    const first = start + 1;
    const last = start + visible;
    tableInfo.textContent = `Exibindo ${first}–${last} de ${total} registros`;
}

/* Cria a paginação */
function renderPagination(totalPages) {
    pagination.innerHTML = "";

    const previousButton = createPageButton(
        '<i class="fa-solid fa-chevron-left"></i>',
        currentPage > 1,
    );

    previousButton.addEventListener("click", () => {
        currentPage--;
        renderTable();
    });

    pagination.appendChild(previousButton);

    for (let page = 1; page <= totalPages; page++) {
        const button = createPageButton(page, true);

        if (page === currentPage) {
            button.classList.add("active");
        }

        button.addEventListener("click", () => {
            currentPage = page;
            renderTable();
        });

        pagination.appendChild(button);
    }

    const nextButton = createPageButton(
        '<i class="fa-solid fa-chevron-right"></i>',
        currentPage < totalPages,
    );

    nextButton.addEventListener("click", () => {
        currentPage++;
        renderTable();
    });

    pagination.appendChild(nextButton);
}

/* Cria botão */
function createPageButton(content, enabled) {
    const button = document.createElement("button");

    button.type = "button";
    button.className = "page-button";
    button.innerHTML = content;
    button.disabled = !enabled;

    return button;
}

/* Busca */
searchInput.addEventListener("input", () => {
    currentPage = 1;
    renderTable();
});

/* Quantidade por página */
itemsPerPage.addEventListener("change", () => {
    currentPage = 1;
    renderTable();
});

/* Inicialização */
renderTable();
