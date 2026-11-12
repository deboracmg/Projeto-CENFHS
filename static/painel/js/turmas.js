const modalTurma = document.getElementById("modalPrimario");
const formTurma = modalTurma.querySelector("#formTurma");
const btnNovaTurma = document.getElementById("btnNovoCadastro");

const tituloModalTurma = modalTurma.querySelector("#tituloModal");
const subtituloModalTurma = modalTurma.querySelector("#subtituloModal");
const idProfessor = modalTurma.querySelector("#professor_id");
const nomeProfessor = modalTurma.querySelector("#professor");
const idCurso = modalTurma.querySelector("#curso_id");
const nomeCurso = modalTurma.querySelector("#nome_curso");
const matriculaBody = modalTurma.querySelector("#matriculaBody");

const btnEditarTurma = modalTurma.querySelector("#btnEditar");
const btnSalvarTurma = modalTurma.querySelector("#btnSalvar");
const btnFecharTurma = modalTurma.querySelector("#btnFechar");
const btnsDetalharTurma = document.querySelectorAll(".btn-abrir-turma");
const btnBuscarProfessor = modalTurma.querySelector("#btnBuscarProfessor");
const btnBuscarCurso = modalTurma.querySelector("#btnBuscarCurso");

const tabButtons = modalTurma.querySelectorAll(".tab-button");

tabButtons.forEach((button) => {
    gerenciarAbas(modalTurma, button);
});

btnsDetalharTurma.forEach((button) => {
    button.addEventListener("click", async () => {
        const turmaId = button.dataset.turmaId;
        const response = await fetch(`/dashboard/turmas/${turmaId}`);

        if (!response.ok) {
            console.error("Erro ao buscar turma.");
            return;
        }

        const turma = await response.json();
        detalharTurma(turma);
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
    exibirMatriculas(null, []);
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
    btnBuscarCurso.disabled = true;
    abrirAbaInicial(modalTurma);
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

    exibirMatriculas(turma.id, turma.matriculas);
    exibirAulas(turma.id, turma.aulas);
}

function exibirMatriculas(turma_id, matriculas) {
    if (!matriculas.length) {
        matriculaBody.innerHTML = `
        <tr>
            <td colspan="5" class="empty-message">
                Nenhuma matrícula cadastrada
            </td>
        </tr>
        `;
        return;
    }

    let contentMatricula = "";
    matriculas.forEach((m, index) => {
        const dataMatricula = converterDataHora(m.data_matricula);

        contentMatricula += `
            <tr data-matricula-id="${m.id}">
                <td>${m.aluno_nome}</td>
                <td>${m.aluno_cpf}</td>
                <td>${dataMatricula.split(", ")[0]}</td>
                <td>${m.matriculado_por}</td>
                <td class="centralize-button">    
                    <button
                        type="button"
                        class="action-button btn-abrir-matricula"
                        data-index=${index}
                        title="Mais informações">

                        <i class="fa-solid fa-circle-info"></i>
                    </button>
                </td>
            </tr>
        `;
    });

    matriculaBody.innerHTML = contentMatricula;

    document.querySelectorAll(".btn-abrir-matricula").forEach((button) => {
        button.addEventListener("click", async () => {
            const index = button.dataset.index;
            const matricula = matriculas[index];
            detalharMatricula(turma_id, matricula);
        });
    });
}

function exibirAulas(turma_id, aulas) {
    if (!aulas.length) {
        aulaBody.innerHTML = `
        <tr>
            <td colspan="5" class="empty-message">
                Nenhuma aula registrada
            </td>
        </tr>
        `;
        return;
    }

    let contentAulas = "";
    aulas.forEach((a, index) => {
        contentAulas += `
            <tr data-aula-id="${a.id}">
                <td>${formatarData(a.data)}</td>
                <td>${a.total_presentes}</td>
                <td class="centralize-button">    
                    <button
                        type="button"
                        class="action-button btn-abrir-aula"
                        data-index=${index}
                        title="Mais informações">

                        <i class="fa-solid fa-circle-info"></i>
                    </button>
                </td>
            </tr>
        `;
    });

    aulaBody.innerHTML = contentAulas;

    document.querySelectorAll(".btn-abrir-aula").forEach((button) => {
        button.addEventListener("click", async () => {
            const index = button.dataset.index;
            const aula = aulas[index];
            detalharAula(turma_id, aula);
        });
    });
}

/* =========================================================
   SALVAR CADASTRO
========================================================= */
async function salvarTurma() {
    try {
        formTurma.classList.remove("com-erro");
        checarFormulario(formTurma);

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

        document.getElementById("turma_id").value = dados.id;
        return dados;
    } catch (erro) {
        exibirNotificacao(erro.message, "erro");
        return null;
    }
}

formTurma.addEventListener("submit", async (event) => {
    event.preventDefault();
    const salvou = await salvarTurma();
    if (salvou && salvou.sucesso) {
        exibirNotificacaoComReload(salvou.mensagem, "sucesso");
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
