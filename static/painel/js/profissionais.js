const btnNovoProfissional = document.getElementById("btnNovoCadastro");
const modalProfissional = document.getElementById("profissionalModal");
const formProfissional = document.getElementById("formProfissional");
const camposProfissional = formProfissional.querySelectorAll("input, select");

const tituloModalProfissional = document.getElementById("tituloModalProfissional");
const subtituloModalProfissional = document.getElementById("subtituloModalProfissional");
const cpfProfissional = document.getElementById("cpf");
const telefoneProfissional = document.getElementById("telefone");

const btnEditarProfissional = document.getElementById("btnEditarProfissional");
const btnSalvarProfissional = document.getElementById("btnSalvarProfissional");
const btnFecharProfissional = document.getElementById("btnFecharProfissional");
const btnsDetalharProfissional = document.querySelectorAll(".btn-abrir-profissional");

btnsDetalharProfissional.forEach((button) => {
    button.addEventListener("click", async () => {
        const profissionalId = button.dataset.profissionalId;
        const response = await fetch(`/dashboard/profissionais/${profissionalId}`);

        if (!response.ok) {
            console.error("Erro ao buscar profissional.");
            return;
        }

        const profissional = await response.json();
        detalharProfissional(profissional);
    });
});

btnEditarProfissional.addEventListener("click", () => {
    habilitarCamposProfissional();
    btnEditarProfissional.disabled = true;

    tituloModalProfissional.textContent = "Editando dados do profissional";
});

function desabilitarCamposProfissional() {
    camposProfissional.forEach(campo => {
        campo.disabled = true;
    });

    btnSalvarProfissional.disabled = true;
}

function habilitarCamposProfissional() {
    camposProfissional.forEach((campo) => {
        campo.disabled = false;
    });

    btnSalvarProfissional.disabled = false;
}

function formNovoProfissional() {
    modalProfissional.showModal();
    formProfissional.reset();
    formProfissional.classList.remove("com-erro");
    document.getElementById("profissional_id").value = "";

    tituloModalProfissional.textContent = "Cadastrar novo profissional";
    subtituloModalProfissional.textContent = "Preencha os dados abaixo";

    btnEditarProfissional.disabled = true;
    btnSalvarProfissional.disabled = false;

    habilitarCamposProfissional();
}

btnNovoProfissional.addEventListener("click", formNovoProfissional)
btnFecharProfissional.addEventListener("click", () => modalProfissional.close());

function detalharProfissional(profissional) {
    preencherFormularioProfissional(profissional);
    tituloModalProfissional.textContent = "Dados do profissional";
    subtituloModalProfissional.textContent = "Código: " + profissional.profissional_id;
    formProfissional.classList.remove("com-erro");

    desabilitarCamposProfissional();
    btnEditarProfissional.disabled = false;

    modalProfissional.showModal();
}

function preencherFormularioProfissional(profissional) {
    document.getElementById("profissional_id").value = profissional.profissional_id || "";
    document.getElementById("cpf").value = profissional.cpf || "";
    document.getElementById("nome").value = profissional.nome || "";
    document.getElementById("data_nascimento").value = profissional.data_nascimento || "";
    document.getElementById("telefone").value = profissional.telefone || "";
    document.getElementById("email").value = profissional.email || "";
    document.getElementById("area_atuacao").value = profissional.area_atuacao || "";
    document.getElementById("data_cadastro").textContent = profissional.data_cadastro || "";
}

/* =========================================================
   VALIDAÇÃO DE CAMPOS
========================================================= */

cpfProfissional.addEventListener("input", function (e) {
    e.target.value = formatarCampoCpf(e);
    cpfProfissional.setCustomValidity("");
});

telefoneProfissional.addEventListener("input", function (e) {
    e.target.value = formatarCampoTelefone(e);
}); 

/* =========================================================
   SALVAR CADASTRO
========================================================= */

formProfissional.addEventListener("submit", async (event) => {
    try {
        event.preventDefault();

        cpfProfissional.setCustomValidity("");
        formProfissional.classList.remove("com-erro");
        
        checarFormulário(formProfissional);
        checarCpf(cpfProfissional, formProfissional);

        const url = "/dashboard/profissionais/salvar/";
        const formData = new FormData(formProfissional);
        const dados = await salvarCadastro(url, formData);

        modalProfissional.close();
        exibirNotificacaoComReload(dados.mensagem, "sucesso");
    } catch (erro) {
        exibirNotificacao(erro.message, "erro");
    }
});
