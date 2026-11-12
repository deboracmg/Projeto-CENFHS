const modalAula = document.getElementById("modalAula");
const modalBodyAula = modalAula.querySelector(".modal-body");
const formAula = modalAula.querySelector("#formAula");

const tituloModalAula = modalAula.querySelector("#tituloModal");
const subtituloModalAula = modalAula.querySelector("#subtituloModal");

const idAula = modalAula.querySelector("#aula_id");
const dataAula = modalAula.querySelector("#data_aula");
const nomeTurma = modalAula.querySelector("#nome_turma");

const alunosMatriculadosBody = document.getElementById(
    "alunosMatriculadosBody",
);
const aulaBody = document.getElementById("aulaBody");

const btnAdicionarAula = document.getElementById("btnAdicionarAula");
const btnExcluirAula = modalAula.querySelector("#btnExcluir");
const btnEditarAula = modalAula.querySelector("#btnEditar");
const btnSalvarAula = modalAula.querySelector("#btnSalvar");
const btnFecharAula = modalAula.querySelector("#btnFechar");

btnEditarAula.addEventListener("click", () => {
    tituloModalAula.textContent = "Editando dados da aula";
    habilitarEdicaoFormulario(modalAula);
});

/* =========================================================
   REGISTRA NOVA AULA
========================================================= */
btnAdicionarAula.addEventListener("click", async () => {
    const dados = await verificarESalvarCadastroRelacionado(
        "aula",
        "turma",
        salvarTurma,
        modalTurma,
    );

    if (!dados) return;
    nomeTurma.disabled = true;
    btnExcluirAula.disabled = true;

    gerarFrequencias(idTurma.value);
    formNovoCadastro(modalAula, "Registrar nova aula");
    nomeTurma.value = document.getElementById("descricao").value || "";
    dataAula.value = preencherDataAtual();
    if (dados.mensagem) exibirNotificacao(dados.mensagem, "sucesso");
});

async function gerarFrequencias(turma_id) {
    const response = await fetch(
        `/dashboard/turmas/buscar-alunos-matriculados/${turma_id}`,
    );
    if (!response.ok) {
        console.error("Erro ao buscar alunos da turma");
        return;
    }

    const alunos = await response.json();

    if (!alunos.length) {
        alunosMatriculadosBody.innerHTML = `
        <tr>
            <td colspan="5" class="empty-message">
                Nenhum aluno matriculado
            </td>
        </tr>
        `;
        return;
    }

    let contentFrequencia = "";
    alunos.forEach((a) => {
        contentFrequencia += `
            <tr data-matricula-id="${a.id}">
                <td>${a.aluno__nome}</td>
                <td>
                    <input
                        type="checkbox"
                        class="checkbox-presenca"
                    />
                </td>
            </tr>
        `;
    });

    alunosMatriculadosBody.innerHTML = contentFrequencia;
}

/* =========================================================
   DETALHAR AULA
========================================================= */
async function detalharAula(turma_id, aula) {
    nomeTurma.value = document.getElementById("descricao").value || "";
    idAula.value = aula.id || "";
    dataAula.value = aula.data || "";
    tituloModalAula.textContent = "Dados da aula";
    subtituloModalAula.textContent = "Código: " + aula.id;
    
    formAula.classList.remove("com-erro");
    await detalharFrequencias(aula.id);
    modalAula.showModal();
    
    btnExcluirAula.disabled = false;
    btnExcluirAula.dataset.aulaId = aula.id;
    btnExcluirAula.dataset.turmaId = turma_id;
    desabilitarEdicaoFormulario(modalAula);
}


async function detalharFrequencias(aula_id) {
    const response = await fetch(
        `/dashboard/aulas/buscar_frequencias/${aula_id}`,
    );
    if (!response.ok) {
        console.error("Erro ao buscar frequências");
        return;
    }

    const frequencias = await response.json();

    if (!frequencias.length) {
        alunosMatriculadosBody.innerHTML = `
        <tr>
            <td colspan="5" class="empty-message">
                Nenhum aluno matriculado
            </td>
        </tr>
        `;
        return;
    }

    let contentFrequencia = "";
    frequencias.forEach((f) => {
        contentFrequencia += `
            <tr data-frequencia-id="${f.id || ""}"
                data-aula-id="${f.aula_id || ""}"
                data-matricula-id="${f.matricula_id}">
                <td>${f.matricula__aluno__nome}</td>
                <td>
                    <input
                        type="checkbox"
                        class="checkbox-presenca"
                        ${f.presente ? "checked" : ""}
                    />
                </td>
            </tr>
        `;
    });

    alunosMatriculadosBody.innerHTML = contentFrequencia;
}

/* =========================================================
   EXCLUIR AULA
========================================================= */
btnExcluirAula.addEventListener("click", async () => {
    const aulaId = btnExcluirAula.dataset.aulaId;
    const turmaId = btnExcluirAula.dataset.turmaId;

    await excluirRegistro({
        modal: modalAula,
        mensagemConfirmacao:
            "Tem certeza que deseja excluir esta aula e todas as frequências relacionadas?",
        url: "/dashboard/aulas/excluir/",
        dados: {
            turma_id: turmaId,
            aula_id: aulaId,
        },
        aoExcluir: (dados) => {
            modalAula.close();
            exibirAulas(turmaId, dados.aulas);
        },
    });
});

/* =========================================================
   SALVAR AULA E FREQUÊNCIA
========================================================= */
function obterFrequencias() {
    const linhas = alunosMatriculadosBody.querySelectorAll(
        "tr[data-matricula-id]",
    );

    return Array.from(linhas, (linha) => ({
        matricula_id: Number(linha.dataset.matriculaId),
        presente: linha.querySelector(".checkbox-presenca").checked,
    }));
}

formAula.addEventListener("submit", async (event) => {
    try {
        event.preventDefault();
        formAula.classList.remove("com-erro");
        checarFormulario(formAula);

        const url = "/dashboard/aulas/salvar/";

        const formData = new FormData(formAula);
        formData.set("frequencias", JSON.stringify(obterFrequencias()));
        formData.set("turma_id", idTurma.value);

        const dados = await salvarCadastro(url, formData);

        modalAula.close();

        exibirAulas(idTurma.value, dados.aulas);
        exibirNotificacao(dados.mensagem, "sucesso");
    } catch (erro) {
        exibirNotificacao(erro.message, "erro");
    }
});

btnFecharAula.addEventListener("click", () => modalAula.close());
