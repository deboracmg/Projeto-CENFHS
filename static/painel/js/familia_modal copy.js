const modalFamiliar = document.getElementById("modalFamiliar");
const formFamiliar = document.getElementById("formFamiliar");

const tituloModalFamiliar = document.getElementById("tituloModalFamiliar");

const btnBuscarParente = document.getElementById("btnBuscarParente");
const btnEditarFamiliar = document.getElementById("btnEditarFamiliar");
const btnFecharFamiliar = document.getElementById("btnFecharFamiliar");
const btnFecharModalFamiliar = document.getElementById(
    "btnFecharModalFamiliar"
);
const btnSalvarFamiliar = document.getElementById("btnSalvarFamiliar");

let modoEdicaoFamiliar = false;


/* =========================================================
   CONTROLE DO MODO DO FORMULÁRIO
========================================================= */

function alterarModoFamiliar(editando) {
    modoEdicaoFamiliar = editando;

    const campos = formFamiliar.querySelectorAll(
        "input:not([type='hidden']), select"
    );

    campos.forEach(campo => {
        campo.disabled = !editando;
    });

    btnEditarFamiliar.disabled = editando;
    btnSalvarFamiliar.disabled = !editando;

    // A busca pelo CPF também só funciona durante edição
    btnBuscarParente.disabled = !editando;
}


/* =========================================================
   LIMPAR FORMULÁRIO
========================================================= */

function limparFormularioFamiliar() {
    formFamiliar.reset();

    document.getElementById("parente-id").value = "";
    document.getElementById("parentesco-id").value = "";

    // Por padrão, consideramos que a pessoa está viva
    document.getElementById("familiar-vivo").checked = true;
}


/* =========================================================
   ABRIR MODAL PARA NOVO FAMILIAR
========================================================= */

function abrirNovoFamiliar() {
    limparFormularioFamiliar();

    tituloModalFamiliar.textContent = "Adicionar familiar";

    modalFamiliar.showModal();

    alterarModoFamiliar(true);
}


/* =========================================================
   ABRIR MODAL PARA VISUALIZAR FAMILIAR
========================================================= */

function abrirFamiliar(dados) {
    limparFormularioFamiliar();

    tituloModalFamiliar.textContent = "Dados do familiar";

    // IDs
    document.getElementById("parente-id").value =
        dados.parente_id || "";

    document.getElementById("parentesco-id").value =
        dados.parentesco_id || "";

    // Dados do Parente
    document.getElementById("cpf-familiar").value =
        dados.cpf || "";

    document.getElementById("nome-familiar").value =
        dados.nome || "";

    document.getElementById("telefone-familiar").value =
        dados.telefone || "";

    document.getElementById("profissao-familiar").value =
        dados.profissao || "";

    document.getElementById("local-trabalho-familiar").value =
        dados.local_trabalho || "";

    document.getElementById("escolaridade-familiar").value =
        dados.escolaridade || "";

    // Dados do Parentesco
    document.getElementById("parentesco-familiar").value =
        dados.parentesco || "";

    document.getElementById("familiar-vivo").checked =
        dados.vivo;

    document.getElementById("familiar-responsavel").checked =
        dados.responsavel;

    document.getElementById("familiar-emergencia").checked =
        dados.contato_emergencia;

    modalFamiliar.showModal();

    // Começa apenas como visualização
    alterarModoFamiliar(false);
}


/* =========================================================
   BUSCAR PARENTE PELO CPF
========================================================= */

async function buscarParente() {
    const cpfInput = document.getElementById("cpf-familiar");
    const cpf = cpfInput.value.trim();

    if (!cpf) {
        alert("Informe o CPF para realizar a busca.");
        cpfInput.focus();
        return;
    }

    try {
        const resposta = await fetch(
            `/parentes/buscar/?cpf=${encodeURIComponent(cpf)}`
        );

        const dados = await resposta.json();

        if (!resposta.ok) {
            // CPF não encontrado.
            // O usuário pode continuar cadastrando uma nova pessoa.
            document.getElementById("parente-id").value = "";

            alert(dados.erro);

            return;
        }

        // Guardamos o ID da pessoa encontrada
        document.getElementById("parente-id").value =
            dados.id;

        // Preenche os dados encontrados
        document.getElementById("nome-familiar").value =
            dados.nome || "";

        document.getElementById("telefone-familiar").value =
            dados.telefone || "";

        document.getElementById("profissao-familiar").value =
            dados.profissao || "";

        document.getElementById("local-trabalho-familiar").value =
            dados.local_trabalho || "";

        document.getElementById("escolaridade-familiar").value =
            dados.escolaridade || "";

        document.getElementById("familiar-vivo").checked =
            dados.vivo;

        alert("Familiar encontrado.");

    } catch (erro) {
        console.error("Erro ao buscar familiar:", erro);

        alert("Não foi possível realizar a busca.");
    }
}


/* =========================================================
   SALVAR FAMILIAR
========================================================= */

async function salvarFamiliar(event) {
    event.preventDefault();

    if (!modoEdicaoFamiliar) {
        return;
    }

    const alunoId = document.getElementById("aluno-id").value;

    if (!alunoId) {
        alert("Nenhum aluno foi selecionado.");
        return;
    }

    const formData = new FormData(formFamiliar);

    // O aluno ao qual o familiar será vinculado
    formData.append("aluno_id", alunoId);

    try {
        const resposta = await fetch(
            "/parentes/salvar/",
            {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": obterCSRFToken()
                }
            }
        );

        const dados = await resposta.json();

        if (!resposta.ok) {
            alert(dados.erro || "Não foi possível salvar o familiar.");
            return;
        }

        alert(dados.mensagem);

        modalFamiliar.close();

        // Aqui você pode atualizar a lista de familiares
        // atualizarListaFamiliares();

    } catch (erro) {
        console.error("Erro ao salvar familiar:", erro);

        alert("Ocorreu um erro ao salvar o familiar.");
    }
}


/* =========================================================
   CSRF
========================================================= */

function obterCSRFToken() {
    return document.querySelector(
        "[name=csrfmiddlewaretoken]"
    ).value;
}


/* =========================================================
   EVENTOS
========================================================= */

btnBuscarParente.addEventListener(
    "click",
    buscarParente
);

btnEditarFamiliar.addEventListener(
    "click",
    () => {
        alterarModoFamiliar(true);
    }
);

btnFecharFamiliar.addEventListener(
    "click",
    () => {
        modalFamiliar.close();
    }
);

btnFecharModalFamiliar.addEventListener(
    "click",
    () => {
        modalFamiliar.close();
    }
);

formFamiliar.addEventListener(
    "submit",
    salvarFamiliar
);

