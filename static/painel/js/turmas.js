const modalTurma = document.getElementById("modalPrimario");
const formTurma = modalTurma.querySelector("#formTurma");
const btnNovaTurma = document.getElementById("btnNovoCadastro");

const tituloModalTurma = modalTurma.querySelector("#tituloModal");
const subtituloModalTurma = modalTurma.querySelector("#subtituloModal");
const idProfessor = modalTurma.querySelector("#professor_id");
const nomeProfessor = modalTurma.querySelector("#professor");
const idCurso = modalTurma.querySelector("#curso_id");
const nomeCurso = modalTurma.querySelector("#nome_curso");

const btnEditarTurma = modalTurma.querySelector("#btnEditar");
const btnSalvarTurma = modalTurma.querySelector("#btnSalvar");
const btnFecharTurma = modalTurma.querySelector("#btnFechar");
const btnsDetalharTurma = document.querySelectorAll(".btn-abrir-turma");
const btnBuscarProfessor = modalTurma.querySelector("#btnBuscarProfessor");
const btnBuscarCurso = modalTurma.querySelector("#btnBuscarCurso");

btnsDetalharTurma.forEach((button) => {
    button.addEventListener("click", async () => {
        const turmaId = button.dataset.turmaId;
        const response = await fetch(`/dashboard/turmas/${turmaId}`);

        if (!response.ok) {
            console.error("Erro ao buscar turma.");
            return;
        }

        const encontro = await response.json();
        detalharTurma(encontro);
    });
});

btnEditarTurma.addEventListener("click", () => {
    btnBuscarProfessor.disabled = false;
    btnBuscarCurso.disabled = false;
    tituloModalTurma.textContent = "Editando dados da turma";
    habilitarEdicaoFormulario(modalTurma);
});

btnNovaTurma.addEventListener("click", () => {
    btnBuscarProfessor.disabled = false;
    btnBuscarCurso.disabled = false;
    formNovoCadastro(modalTurma, "Cadastrar nova turma");
});

btnFecharTurma.addEventListener("click", () => modalTurma.close());

function detalharTurma(turma) {
    preencherFormularioTurma(turma);
    tituloModalTurma.textContent = "Dados da turma";
    subtituloModalTurma.textContent = "Código: " + turma.id;
    formTurma.classList.remove("com-erro");

    modalTurma.showModal();
    btnBuscarProfessor.disabled = true;
    desabilitarEdicaoFormulario(modalTurma);
}

function preencherFormularioTurma(turma) {
    document.getElementById("turma_id").value = turma.id || "";
    document.getElementById("curso_id").value = turma.curso_id || "";
    document.getElementById("nome_curso").value = turma.curso_nome || "";
    document.getElementById("professor_id").value = turma.professor_id || "";
    document.getElementById("professor").value = turma.professor_nome || "";
    document.getElementById("descricao").value = turma.descricao || "";
    document.getElementById("local").value = turma.local || "";

    document.getElementById("hora_inicio").value = turma.hora_inicio;
    document.getElementById("hora_fim").value = turma.hora_fim;

    const diasSemana = turma.dias_semana || [];
    document
        .querySelectorAll('.form-group-checkbox input[type="checkbox"]')
        .forEach((checkbox) => {
            checkbox.checked = diasSemana.includes(checkbox.value);
        });

    const data = converterDataHora(turma.data_cadastro);
    document.getElementById("data_cadastro").textContent = data
        .split(", ")
        .join(" - ");
}

/* =========================================================
   SALVAR CADASTRO
========================================================= */

formTurma.addEventListener("submit", async (event) => {
    try {
        event.preventDefault();
        formTurma.classList.remove("com-erro");
        checarFormulário(formTurma);

        const url = "/dashboard/turmas/salvar/";
        const formData = new FormData(formTurma);

        const diasSemana = Array.from(
            document.querySelectorAll(
                '.form-group-checkbox input[type="checkbox"]:checked',
            ),
            (checkbox) => checkbox.value,
        );
        formData.set("dias_semana", JSON.stringify(diasSemana));

        const dados = await salvarCadastro(url, formData);

        modalTurma.close();
        exibirNotificacaoComReload(dados.mensagem, "sucesso");
    } catch (erro) {
        exibirNotificacao(erro.message, "erro");
    }
});

/* =========================================================
   SELECIONAR CURSO
========================================================= */

btnBuscarCurso.addEventListener("click", () => {
    abrirModalBusca({
        titulo: "Buscar curso",
        placeholder: "Buscar curso por nome",
        url: "/dashboard/servicos/buscar/",
        parametros: {
            tipo: "CURSO",
        },
        rotulo: (curso) => curso.nome,
        aoConfirmar: (curso) => {
            nomeCurso.value = curso.nome;
            idCurso.value = curso.id;
        },
    });
});

/* =========================================================
   SELECIONAR PROFESSOR
========================================================= */

btnBuscarProfessor.addEventListener("click", () => {
    abrirModalBusca({
        titulo: "Buscar professor",
        placeholder: "Buscar professor por nome",
        url: "/dashboard/profissionais/buscar/",
        rotulo: (professor) => professor.nome,
        aoConfirmar: (professor) => {
            idProfessor.value = professor.id;
            nomeProfessor.value = professor.nome;
        },
    });
});
