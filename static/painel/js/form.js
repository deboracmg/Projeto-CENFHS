function habilitarEdicaoFormulario(modal) {
    const form = modal.querySelector("form");
    const campos = form.querySelectorAll("input, select, textarea");
    campos.forEach((campo) => {
        campo.disabled = false;
    });

    modal.querySelector("#btnSalvar").disabled = false;
    modal.querySelector("#btnEditar").disabled = true;

    const btnRemoverFoto = modal.querySelector("#btnRemoverFoto");
    if (btnRemoverFoto) btnRemoverFoto.disabled = false;
}

function desabilitarEdicaoFormulario(modal) {
    const form = modal.querySelector("form");
    const campos = form.querySelectorAll("input, select, textarea");
    campos.forEach((campo) => {
        campo.disabled = true;
    });

    modal.querySelector("#btnSalvar").disabled = true;
    modal.querySelector("#btnEditar").disabled = false;

    const btnRemoverFoto = modal.querySelector("#btnRemoverFoto");
    if (btnRemoverFoto) btnRemoverFoto.disabled = true;
}

async function salvarCadastro(url, formData) {
    const csrfToken =
        document.querySelector("[name=csrfmiddlewaretoken]")?.value || "";

    const response = await fetch(url, {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": csrfToken,
        },
    });

    const dados = await response.json();

    if (!response.ok) {
        throw new Error(dados.mensagem);
    }
    return dados;
}

async function verificarESalvarCadastroRelacionado(
    atual,
    relacionado,
    salvarRelacionado,
    modalRelacionado,
) {
    const idRelacionado = modalRelacionado.querySelector(
        `#${relacionado}_id`,
    ).value;
    if (idRelacionado) return true;

    const mensagem = `Para adicionar um(a) ${atual}, é necessário salvar o(a) ${relacionado} primeiro. Deseja salvá-lo agora?`;
    const confirmacao = await pedirConfirmacao(mensagem);
    if (!confirmacao) return false;

    const salvou = await salvarRelacionado();
    if (!salvou || !salvou.sucesso) return false;

    modalRelacionado.querySelector("#tituloModal").textContent =
        `Editando dados do ${relacionado}`;
    modalRelacionado.querySelector("#subtituloModal").textContent =
        "Código: " + salvou.id;

    const campoData = modalRelacionado.querySelector("#data_cadastro");
    if (campoData) campoData.textContent = formatarData(preencherDataAtual());
    desabilitarEdicaoFormulario(modalRelacionado);
    return salvou;
}

function formNovoCadastro(modalAtual, tabela) {
    const form = modalAtual.querySelector("form");
    form.reset();
    form.classList.remove("com-erro");

    modalAtual.querySelector("#tituloModal").textContent =
        `Cadastrar novo ${tabela}`;
    modalAtual.querySelector("#subtituloModal").textContent =
        "Preencha os dados abaixo";

    const camposDeId = modalAtual.querySelectorAll(
        'input[type="hidden"][id*="_id"]',
    );
    camposDeId.forEach((campo) => (campo.value = ""));

    const campoData = modalAtual.querySelector("#data_cadastro");
    if (campoData) campoData.textContent = "-- / -- / ----";
    modalAtual.showModal();

    const tabButtons = modalAtual.querySelectorAll(".tab-button");
    if (tabButtons.length) abrirAbaInicial(modalAtual);

    habilitarEdicaoFormulario(modalAtual);
}

/* =========================================================
   ABAS
========================================================= */
function gerenciarAbas(modal, button) {
    const tabButtons = modal.querySelectorAll(".tab-button");
    const tabContents = modal.querySelectorAll(".tab-content");
    const modalBody = modal.querySelector(".modal-body");

    button.addEventListener("click", () => {
        const tabId = button.dataset.tab;

        tabButtons.forEach((item) => {
            item.classList.remove("active");
        });

        tabContents.forEach((content) => {
            content.classList.remove("active");
        });

        button.classList.add("active");
        document.getElementById(tabId).classList.add("active");
        modalBody.scrollTo(0, 0);
    });
}

function abrirAbaInicial(modal) {
    const tabButtons = modal.querySelectorAll(".tab-button");
    const tabContents = modal.querySelectorAll(".tab-content");

    tabButtons.forEach((button) => {
        button.classList.remove("active");
    });

    tabContents.forEach((content) => {
        content.classList.remove("active");
    });

    modal.querySelector(".modal-body").scrollTo(0, 0);

    document
        .querySelector('[data-tab="dados-pessoais"]')
        .classList.add("active");

    document.getElementById("dados-pessoais").classList.add("active");
}
