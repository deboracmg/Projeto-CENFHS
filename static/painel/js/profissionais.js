const modalProfissional = document.getElementById("modalPrimario");
const formProfissional = modalProfissional.querySelector("#formProfissional");
const camposProfissional = formProfissional.querySelectorAll("input, select");
const btnNovoProfissional = document.getElementById("btnNovoCadastro");

const tituloModalProfissional = modalProfissional.querySelector("#tituloModal");
const subtituloModalProfissional =
    modalProfissional.querySelector("#subtituloModal");
const campoCpf = modalProfissional.querySelector("#cpf");
const campoTelefone = modalProfissional.querySelector("#telefone");

const btnEditarProfissional = modalProfissional.querySelector("#btnEditar");
const btnSalvarProfissional = modalProfissional.querySelector("#btnSalvar");
const btnFecharProfissional = modalProfissional.querySelector("#btnFechar");
const btnsDetalharProfissional = document.querySelectorAll(
    ".btn-abrir-profissional",
);

btnsDetalharProfissional.forEach((button) => {
    button.addEventListener("click", async () => {
        const profissionalId = button.dataset.profissionalId;
        const response = await fetch(
            `/dashboard/profissionais/${profissionalId}`,
        );

        if (!response.ok) {
            console.error("Erro ao buscar profissional.");
            return;
        }

        const profissional = await response.json();
        detalharProfissional(profissional);
    });
});

btnEditarProfissional.addEventListener("click", () => {
    habilitarEdicaoFormulario(modalProfissional);
    tituloModalProfissional.textContent = "Editando dados do profissional";
});

btnNovoProfissional.addEventListener("click", () =>
    formNovoCadastro(modalProfissional, "profissional"),
);
btnFecharProfissional.addEventListener("click", () =>
    modalProfissional.close(),
);

function detalharProfissional(profissional) {
    preencherFormularioProfissional(profissional);
    tituloModalProfissional.textContent = "Dados do profissional";
    subtituloModalProfissional.textContent =
        "Código: " + profissional.profissional_id;
    formProfissional.classList.remove("com-erro");

    desabilitarEdicaoFormulario(modalProfissional);
    modalProfissional.showModal();
}

function preencherFormularioProfissional(profissional) {
    document.getElementById("profissional_id").value =
        profissional.profissional_id || "";
    document.getElementById("cpf").value = profissional.cpf || "";
    document.getElementById("nome").value = profissional.nome || "";
    document.getElementById("data_nascimento").value =
        profissional.data_nascimento || "";
    document.getElementById("telefone").value = profissional.telefone || "";
    document.getElementById("email").value = profissional.email || "";
    document.getElementById("area_atuacao").value =
        profissional.area_atuacao || "";

    const data = converterDataHora(profissional.data_cadastro);
    document.getElementById("data_cadastro").textContent = data.split(", ").join(" - ");
}

/* =========================================================
   VALIDAÇÃO DE CAMPOS
========================================================= */

campoCpf.addEventListener("input", function (e) {
    e.target.value = formatarCampoCpf(e);
    campoCpf.setCustomValidity("");
});

campoTelefone.addEventListener("input", function (e) {
    e.target.value = formatarCampoTelefone(e);
});

/* =========================================================
   SALVAR CADASTRO
========================================================= */

formProfissional.addEventListener("submit", async (event) => {
    try {
        event.preventDefault();

        campoCpf.setCustomValidity("");
        formProfissional.classList.remove("com-erro");

        checarFormulário(formProfissional);
        checarCpf(campoCpf, formProfissional);

        const url = "/dashboard/profissionais/salvar/";
        const formData = new FormData(formProfissional);
        const dados = await salvarCadastro(url, formData);

        modalProfissional.close();
        exibirNotificacaoComReload(dados.mensagem, "sucesso");
    } catch (erro) {
        exibirNotificacao(erro.message, "erro");
    }
});
