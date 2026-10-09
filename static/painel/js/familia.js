const modalFamiliar = document.getElementById("modalFamiliar");
const formFamiliar = document.getElementById("formFamiliar");
const camposFamiliar = formFamiliar.querySelectorAll("input, select");

const tituloModalFamiliar = document.getElementById("tituloModalFamiliar");
const subtituloModalFamiliar = document.getElementById(
    "subtituloModalFamiliar",
);
const cpfFamiliar = document.getElementById("cpf_familiar");
const telefoneFamiliar = document.getElementById("telefone_familiar");

const btnAdicionarFamiliar = document.getElementById("btnAdicionarFamiliar");
const btnExcluirFamiliar = document.getElementById("btnExcluirFamiliar");
const btnEditarFamiliar = document.getElementById("btnEditarFamiliar");
const btnFecharFamiliar = document.getElementById("btnFecharFamiliar");
const btnSalvarFamiliar = document.getElementById("btnSalvarFamiliar");

function desabilitarCamposFamiliar() {
    camposFamiliar.forEach((campo) => {
        campo.disabled = true;
    });

    btnSalvarFamiliar.disabled = true;
}

function habilitarCamposFamiliar() {
    camposFamiliar.forEach((campo) => {
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
    let notificacao = "";
    if (!idAlunoReferencia) {
        const mensagem =
            "Para adicionar um familiar, é necessário salvar o aluno primeiro. Deseja salvá-lo agora?";
        const confirmacao = await pedirConfirmacao(mensagem);
        if (!confirmacao) return;

        const salvou = await salvarAluno();
        if (!salvou || !salvou.sucesso) return;

        tituloModalAluno.textContent = "Editando dados do aluno";
        subtituloModalAluno.textContent =
            "Código: " + document.getElementById("aluno_id").value;

        notificacao = salvou.mensagem;
    }

    modalFamiliar.showModal();
    if (notificacao) exibirNotificacao(notificacao, "sucesso");

    formFamiliar.reset();
    formFamiliar.classList.remove("com-erro");
    document.getElementById("parente_id").value = "";
    document.getElementById("parentesco_id").value = "";

    tituloModalFamiliar.textContent = "Cadastrar novo familiar";
    subtituloModalFamiliar.textContent = "Preencha os dados abaixo";

    btnExcluirFamiliar.disabled = true;
    btnEditarFamiliar.disabled = true;

    habilitarCamposFamiliar();
}

btnAdicionarFamiliar.addEventListener("click", formNovoFamiliar);

function detalharFamiliar(aluno_id, familiar) {
    preencherFormularioFamiliar(familiar);
    tituloModalFamiliar.textContent = "Dados do familiar";
    subtituloModalFamiliar.textContent = "Código: " + familiar.parente_id;

    desabilitarCamposFamiliar();
    btnEditarFamiliar.disabled = false;
    btnExcluirFamiliar.disabled = false;
    btnExcluirFamiliar.dataset.parenteId = familiar.parente_id;
    btnExcluirFamiliar.dataset.alunoId = aluno_id;

    modalFamiliar.showModal();
}

function preencherFormularioFamiliar(familiar) {
    document.getElementById("parente_id").value = familiar.parente_id || "";
    document.getElementById("cpf_familiar").value = familiar.cpf || "";
    document.getElementById("nome_familiar").value = familiar.nome || "";
    document.getElementById("telefone_familiar").value =
        familiar.telefone || "";
    document.getElementById("profissao_familiar").value =
        familiar.profissao || "";
    document.getElementById("local_trabalho_familiar").value =
        familiar.local_trabalho || "";
    document.getElementById("escolaridade_familiar").value =
        familiar.escolaridade || "";
    document.getElementById("parentesco_id").value =
        familiar.parentesco_id || "";
    document.getElementById("parentesco_familiar").value =
        familiar.parentesco || "";
    document.getElementById("familiar_vivo").checked = familiar.vivo || false;
    document.getElementById("familiar_responsavel").checked =
        familiar.responsavel || false;
    document.getElementById("familiar_emergencia").checked =
        familiar.contato_emergencia || false;
}

async function buscarFamiliarPorCpf() {
    const cpf = cpfFamiliar.value;
    if (!cpf) return;

    const params = new URLSearchParams({ cpf: cpf });
    const resposta = await fetch(
        `/dashboard/parentes/buscar-por-cpf/?${params}`,
    );

    const dados = await resposta.json();
    if (dados.encontrado) {
        preencherFormularioFamiliar(dados.parente);
    }
}

function obterCSRFToken() {
    return document.querySelector("[name=csrfmiddlewaretoken]").value;
}

async function excluirFamiliar() {
    const confirmacao = await pedirConfirmacao(
        "Tem certeza que deseja excluir este familiar?",
    );
    if (!confirmacao) return;

    const formData = new FormData();
    const parenteId = btnExcluirFamiliar.dataset.parenteId;
    const alunoId = btnExcluirFamiliar.dataset.alunoId;

    formData.append("parente_id", parenteId);
    formData.append("aluno_id", alunoId);

    const resposta = await fetch("/dashboard/parentes/excluir/", {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": obterCSRFToken(),
        },
    });

    const dados = await resposta.json();

    if (!dados.sucesso) {
        exibirNotificacao(dados.mensagem, "erro");
        return;
    }

    modalFamiliar.close();
    exibirFamilia(alunoId, dados.familia);
    exibirNotificacao(dados.mensagem, "sucesso");
}

btnExcluirFamiliar.addEventListener("click", excluirFamiliar);

/* =========================================================
   VALIDAÇÃO DE CAMPOS
========================================================= */

cpfFamiliar.addEventListener("input", function (e) {
    e.target.value = formatarCampoCpf(e);
    cpfFamiliar.setCustomValidity("");
});

cpfFamiliar.addEventListener("blur", buscarFamiliarPorCpf);

telefoneFamiliar.addEventListener("input", function (e) {
    e.target.value = formatarCampoTelefone(e);
});

/* =========================================================
   SALVAR CADASTRO
========================================================= */

formFamiliar.addEventListener("submit", async (event) => {
    try {
        event.preventDefault();

        formFamiliar.classList.remove("com-erro");
        cpfFamiliar.setCustomValidity("");

        checarFormulário(formFamiliar);
        checarCpf(cpfFamiliar);

        const url = "/dashboard/parentes/salvar/";
        const formData = new FormData(formFamiliar);
        formData.append("aluno_id", document.getElementById("aluno_id").value);

        const dados = await salvarCadastro(url, formData);

        modalFamiliar.close();
        exibirFamilia(dados.aluno_id, dados.familia);
        exibirNotificacao(dados.mensagem, "sucesso");
    } catch (erro) {
        exibirNotificacao(erro.message, "erro");
    }
});

btnFecharFamiliar.addEventListener("click", () => modalFamiliar.close());
