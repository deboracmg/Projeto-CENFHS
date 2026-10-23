const modalServico = document.getElementById("modalPrimario");
const formServico = modalServico.querySelector("#formServico");
const btnNovoServico = document.getElementById("btnNovoCadastro");

const tituloModalServico = modalServico.querySelector("#tituloModal");
const subtituloModalServico = modalServico.querySelector("#subtituloModal");
const nomeServico = modalServico.querySelector("#nome");
const tipoServico = modalServico.querySelector("#tipo_servico");

const btnEditarServico = modalServico.querySelector("#btnEditar");
const btnSalvarServico = modalServico.querySelector("#btnSalvar");
const btnFecharServico = modalServico.querySelector("#btnFechar");
const btnsDetalharServico = document.querySelectorAll(".btn-abrir-servico");
const paginaAtual = document.querySelector(".page-header").dataset.paginaAtual;

const configuracoes = {
    atividade: {
        tipoServico: "ATIVIDADE",
        cadastro: "Cadastrar nova atividade",
        detalhe: "Dados da atividade",
        edicao: "Editando dados da atividade",
        placeholder: "Nome da atividade",
    },
    curso: {
        tipoServico: "CURSO",
        cadastro: "Cadastrar novo curso",
        detalhe: "Dados do curso",
        edicao: "Editando dados do curso",
        placeholder: "Nome do curso",
    },
    evento: {
        tipoServico: "EVENTO",
        cadastro: "Cadastrar novo evento",
        detalhe: "Dados do evento",
        edicao: "Editando dados do evento",
        placeholder: "Nome do evento",
    },
};

const configuracao = configuracoes[paginaAtual];

btnNovoServico.addEventListener("click", () => {
    nomeServico.placeholder = configuracao.placeholder;
    tipoServico.value = configuracao.tipoServico;
    formNovoCadastro(modalServico, configuracao.cadastro);
});

btnFecharServico.addEventListener("click", () => modalServico.close());

btnsDetalharServico.forEach((button) => {
    button.addEventListener("click", async () => {
        const servicoId = button.dataset.servicoId;
        const response = await fetch(`/dashboard/servicos/${servicoId}`);

        if (!response.ok) {
            console.error(`Erro ao buscar ${tipoPagina}`);
            return;
        }

        const servico = await response.json();
        detalharServico(servico);
    });
});

function detalharServico(servico) {
    preencherFormularioServico(servico);
    tituloModalServico.textContent = configuracao.detalhe;
    subtituloModalServico.textContent = "Código: " + servico.id;
    formServico.classList.remove("com-erro");

    modalServico.showModal();
    desabilitarEdicaoFormulario(modalServico);
}

function preencherFormularioServico(servico) {
    document.getElementById("servico_id").value = servico.id || "";
    document.getElementById("tipo_servico").value = servico.tipo || "";
    document.getElementById("nome").value = servico.nome || "";
    document.getElementById("ativo").checked = servico.ativo || false;

    const data = converterDataHora(servico.data_cadastro);
    document.getElementById("data_cadastro").textContent = data
        .split(", ")
        .join(" - ");
}

btnEditarServico.addEventListener("click", () => {
    tituloModalServico.textContent = configuracao.edicao;
    habilitarEdicaoFormulario(modalServico);
});

formServico.addEventListener("submit", async (event) => {
    try {
        event.preventDefault();
        formServico.classList.remove("com-erro");
        checarFormulário(formServico);

        const url = "/dashboard/servicos/salvar/";
        const formData = new FormData(formServico);
        const dados = await salvarCadastro(url, formData);

        modalServico.close();
        exibirNotificacaoComReload(dados.mensagem, "sucesso");
    } catch (erro) {
        exibirNotificacao(erro.message, "erro");
    }
});
