const modalFamiliar = document.getElementById("familiaModal");
const formFamiliar = document.getElementById("formFamiliar");
const campos = formFamiliar.querySelectorAll("input, select");

const tituloModalFamiliar = document.getElementById("tituloModalFamiliar");
const subtituloModalFamiliar = document.getElementById("subtituloModalFamiliar");
const cpfFamiliar = document.querySelector("#cpf_familiar");
const telefoneFamiliar = document.querySelector("#telefone_familiar");

const btnAdicionarFamiliar = document.getElementById("btnAdicionarFamiliar");
const btnExcluirFamiliar = document.getElementById("btnExcluirFamiliar");
const btnEditarFamiliar = document.getElementById("btnEditarFamiliar");
const btnFecharFamiliar = document.getElementById("btnFecharFamiliar");
const btnSalvarFamiliar = document.getElementById("btnSalvarFamiliar");

function desabilitarCamposFamiliar() {
    campos.forEach(campo => {
        campo.disabled = true;
    });

    btnSalvarFamiliar.disabled = true;
}

function habilitarCamposFamiliar() {
    campos.forEach((campo) => {
        campo.disabled = false;
    });

    btnSalvarFamiliar.disabled = false;
}

btnEditarFamiliar.addEventListener("click", () => {
    habilitarCamposFamiliar();
    btnEditarFamiliar.disabled = true;

    tituloModalFamiliar.textContent = "Editando dados do familiar";
});

async function formNovoFamiliar() {
    const idAlunoReferencia = document.getElementById("aluno_id").value;
    if (!idAlunoReferencia) {
        const mensagem = "Para adicionar um familiar, é necessário salvar o aluno primeiro. Deseja salvá-lo agora?";
        const confirmacao = await pedirConfirmacao(mensagem);
        if (!confirmacao) return;

        const salvou = await salvarAluno();
        if (!salvou || !salvou.sucesso) return;
        exibirNotificacao(salvou.mensagem, "sucesso");

        modalTitulo.textContent = "Editando dados do aluno";
        modalSubtitulo.textContent = "Código: " + document.getElementById("aluno_id").value;
    }

    modalFamiliar.showModal();
    formFamiliar.reset();
    if (formFamiliar.classList.contains("com-erro")) {
        formFamiliar.classList.remove("com-erro");
    }

    tituloModalFamiliar.textContent = "Cadastrar novo familiar";
    subtituloModalFamiliar.textContent = "Preencha os dados abaixo";

    btnExcluirFamiliar.disabled = true;
    btnEditarFamiliar.disabled = true;
    btnSalvarFamiliar.disabled = false;

    habilitarCamposFamiliar();
}

btnAdicionarFamiliar.addEventListener("click", formNovoFamiliar)

function detalharParente(aluno_id, parente) {
    preencherFormularioFamiliar(parente);
    tituloModalFamiliar.textContent = "Dados do familiar";
    subtituloModalFamiliar.textContent = "Código: " + parente.parente_id;

    desabilitarCamposFamiliar();
    btnEditarFamiliar.disabled = false;
    btnExcluirFamiliar.disabled = false;
    btnExcluirFamiliar.dataset.parenteId = parente.parente_id;
    btnExcluirFamiliar.dataset.alunoId = aluno_id;

    modalFamiliar.showModal();
}


function preencherFormularioFamiliar(parente) {
    document.getElementById("parente_id").value = parente.parente_id || "";
    document.getElementById("cpf_familiar").value = parente.cpf || "";
    document.getElementById("nome_familiar").value = parente.nome || "";
    document.getElementById("telefone_familiar").value = parente.telefone || "";
    document.getElementById("profissao_familiar").value = parente.profissao || "";
    document.getElementById("local_trabalho_familiar").value = parente.local_trabalho || "";
    document.getElementById("escolaridade_familiar").value = parente.escolaridade || "";
    document.getElementById("parentesco_id").value = parente.parentesco_id || "";
    document.getElementById("parentesco_familiar").value = parente.parentesco || "";
    document.getElementById("familiar_vivo").checked = parente.vivo || false;
    document.getElementById("familiar_responsavel").checked = parente.responsavel || false;
    document.getElementById("familiar_emergencia").checked = parente.contato_emergencia || false;
}


async function buscarParentePorCpf() {
    const cpf = cpfFamiliar.value.trim();

    if (!cpf) {
        return;
    }

    const params = new URLSearchParams({cpf: cpf});
    const resposta = await fetch(
        `/dashboard/parentes/buscar-por-cpf/?${params}`
    );

    const dados = await resposta.json();

    if (dados.encontrado) {
        preencherFormularioFamiliar(dados.parente);
    }
}

cpfFamiliar.addEventListener("input", function (e) {
    e.target.value = formatarCampoCpf(e);
});

cpfFamiliar.addEventListener("blur", buscarParentePorCpf);

telefoneFamiliar.addEventListener("input", function (e) {
    e.target.value = formatarCampoTelefone(e);
});

function obterCSRFToken() {
    return document.querySelector(
        "[name=csrfmiddlewaretoken]"
    ).value;
}


async function excluirFamiliar() {
    const formData = new FormData();
    const parenteId = btnExcluirFamiliar.dataset.parenteId;
    const alunoId = btnExcluirFamiliar.dataset.alunoId;

    formData.append("parente_id", parenteId);
    formData.append("aluno_id", alunoId);

    const resposta = await fetch("/dashboard/parentes/excluir/", {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": obterCSRFToken()
        }
    });

    const dados = await resposta.json();

    if (!dados.sucesso) {
        exibirNotificacao(dados.mensagem, "erro");
        return;
    }
    
    modalFamiliar.close();
    exibirFamilia(alunoId, dados.familia)
    exibirNotificacao(dados.mensagem, "sucesso");
}


btnExcluirFamiliar.addEventListener("click", excluirFamiliar)

/* =========================================================
   SALVAR CADASTRO
========================================================= */

formFamiliar.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (!formFamiliar.checkValidity()) {
        formFamiliar.classList.add("com-erro");
        exibirNotificacao("Preencha todos os campos obrigatórios", "info");
        return false;
    }

    if (!validarCPF(cpfFamiliar.value)) {
        exibirNotificacao("CPF inválido. Verifique o CPF informado.", "erro")
        return false;
    }

    const formData = new FormData(formFamiliar);
    formData.append("aluno_id", document.getElementById("aluno_id").value);

    const csrfToken = document.querySelector(
        "[name=csrfmiddlewaretoken]",
    ).value;

    const response = await fetch("/dashboard/parentes/salvar/", {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": csrfToken,
        },
    });

    const dados = await response.json();

    if (!response.ok) {
        console.error(dados);
        return false;
    }

    modalFamiliar.close();
    exibirFamilia(dados.aluno_id, dados.familia)
    exibirNotificacao(dados.mensagem, "sucesso");
    return true;
});

btnFecharFamiliar.addEventListener("click", () => modalFamiliar.close());

