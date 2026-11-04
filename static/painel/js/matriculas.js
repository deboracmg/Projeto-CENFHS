const modalMatricula = document.getElementById("modalSecundario");
const modalBodyMatricula = modalMatricula.querySelector(
    ".modal-body.matricula",
);
const formMatricula = modalMatricula.querySelector("#formMatricula");
const camposMatricula = formMatricula.querySelectorAll(
    "input, select, textarea",
);

const tituloModalMatricula = modalMatricula.querySelector("#tituloModal");
const subtituloModalMatricula = modalMatricula.querySelector("#subtituloModal");
const idAluno = modalMatricula.querySelector("#aluno_id");
const nomeAluno = modalMatricula.querySelector("#aluno_nome");
const idTurma = document.getElementById("turma_id");

const btnMatricularAluno = document.getElementById("btnMatricularAluno");
const btnExcluirMatricula = modalMatricula.querySelector("#btnExcluir");
const btnEditarMatricula = modalMatricula.querySelector("#btnEditar");
const btnFecharMatricula = modalMatricula.querySelector("#btnFechar");
const btnSalvarMatricula = modalMatricula.querySelector("#btnSalvar");
const btnBuscarAluno = modalMatricula.querySelector("#btnBuscarAluno");

btnEditarMatricula.addEventListener("click", () => {
    btnBuscarAluno.disabled = false;
    tituloModalMatricula.textContent = "Editando dados da matrícula";
    habilitarEdicaoFormulario(modalMatricula);
});

btnMatricularAluno.addEventListener("click", async () => {
    const dados = await verificarESalvarCadastroRelacionado(
        "matricula",
        "turma",
        salvarTurma,
        modalTurma,
    );

    if (!dados) return;

    btnBuscarAluno.disabled = false;
    btnExcluirMatricula.disabled = true;
    formNovoCadastro(modalMatricula, "Cadastrar nova matrícula");
    modalMatricula.querySelector("#data_matricula").value =
        preencherDataAtual();
    if (dados.mensagem) exibirNotificacao(dados.mensagem, "sucesso");
});

/* =========================================================
   DETALHAR MATRICULA
========================================================= */
function detalharMatricula(turma_id, matricula) {
    preencherFormularioMatricula(matricula);
    tituloModalMatricula.textContent = "Dados da matrícula";
    subtituloModalMatricula.textContent = "Código: " + matricula.matricula_id;
    formMatricula.classList.remove("com-erro");
    btnBuscarAluno.disabled = true;

    desabilitarEdicaoFormulario(modalMatricula);
    btnExcluirMatricula.disabled = false;
    btnExcluirMatricula.dataset.matriculaId = matricula.matricula_id;
    btnExcluirMatricula.dataset.turmaId = turma_id;

    modalMatricula.showModal();
}

function preencherFormularioMatricula(matricula) {
    document.getElementById("matricula_id").value =
        matricula.matricula_id || "";

    const data = converterDataHora(matricula.data_matricula);
    document.getElementById("data_matricula").textContent = data
        .split(", ")
        .join(" - ");

    document.getElementById("matriculado_por").value =
        matricula.matriculado_por || "";

    document.getElementById("aluno_id").value = matricula.aluno_id || "";
    document.getElementById("aluno_nome").value = matricula.aluno_nome || "";
}


/* =========================================================
EXCLUIR CADASTRO
========================================================= */
btnExcluirMatricula.addEventListener("click", async () => {
    const matriculaId = btnExcluirMatricula.dataset.matriculaId;
    const turmaId = btnExcluirMatricula.dataset.turmaId;

    await excluirRegistro({
        modal: modalMatricula,
        mensagemConfirmacao: "Tem certeza que deseja excluir esta matrícula?",
        url: "/dashboard/matriculas/excluir/",
        dados: {
            turma_id: turmaId,
            matricula_id: matriculaId,
        },
        aoExcluir: (dados) => {
            modalMatricula.close();
            exibirMatriculas(turmaId, dados.matriculas);
        },
    });
});


/* =========================================================
   SALVAR CADASTRO
========================================================= */
formMatricula.addEventListener("submit", async (event) => {
    try {
        event.preventDefault();

        formMatricula.classList.remove("com-erro");
        checarFormulário(formMatricula);

        const url = "/dashboard/matriculas/salvar/";
        const formData = new FormData(formMatricula);
        
        formData.append("turma_id", idTurma.value);
        formData.append("aluno_id", idAluno.value);

        const dados = await salvarCadastro(url, formData);

        modalMatricula.close();
        exibirMatriculas(idTurma.value, dados.matriculas);
        exibirNotificacao(dados.mensagem, "sucesso");
    } catch (erro) {
        exibirNotificacao(erro.message, "erro");
    }
});

btnFecharMatricula.addEventListener("click", () => modalMatricula.close());

/* =========================================================
   SELECIONAR ALUNO
========================================================= */

btnBuscarAluno.addEventListener("click", () => {
    abrirModalBusca({
        titulo: "Buscar aluno",
        placeholder: "Buscar aluno por nome ou CPF",
        url: `/dashboard/turmas/buscar-alunos-nao-matriculados/${idTurma.value}`,
        rotulo: (aluno) => aluno.nome + " - CPF: " + aluno.cpf,
        aoConfirmar: (aluno) => {
            idAluno.value = aluno.id;
            nomeAluno.value = aluno.nome;
        },
    });
});
