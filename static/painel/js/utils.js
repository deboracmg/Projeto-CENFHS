/* =========================================================
   VALIDAÇÃO
========================================================= */

function checarFormulário(form) {
    if (form.checkValidity()) return;

    form.classList.add("com-erro");
    throw new Error("Preencha todos os campos obrigatórios.");
}

function checarCpf(campoCpf, form) {
    if (validarCPF(campoCpf.value)) return;

    form.classList.add("com-erro");
    campoCpf.setCustomValidity("CPF inválido");
    throw new Error("CPF inválido. Verifique o CPF informado.");
}

function checarCep(campoCep, form) {
    if (campoCep.value.length === 9) return;

    form.classList.add("com-erro");
    campoCep.setCustomValidity("CEP inválido");
    throw new Error("O CEP deve conter exatamente 8 números.");
}

function validarCPF(cpf) {
    cpf = cpf.replace(/\D/g, "");

    // CPF precisa ter 11 dígitos
    if (cpf.length !== 11) {
        return false;
    }

    // Rejeita CPFs com todos os dígitos iguais
    if (/^(\d)\1{10}$/.test(cpf)) {
        return false;
    }

    // Primeiro dígito verificador
    let soma = 0;
    for (let i = 0; i < 9; i++) {
        soma += Number(cpf[i]) * (10 - i);
    }

    let resto = (soma * 10) % 11;
    if (resto === 10) {
        resto = 0;
    }

    if (resto !== Number(cpf[9])) {
        return false;
    }

    // Segundo dígito verificador
    soma = 0;
    for (let i = 0; i < 10; i++) {
        soma += Number(cpf[i]) * (11 - i);
    }

    resto = (soma * 10) % 11;
    if (resto === 10) {
        resto = 0;
    }

    return resto === Number(cpf[10]);
}

/* =========================================================
   FORMATAÇÃO
========================================================= */
function converterDataHora(data_hora) {
    return new Intl.DateTimeFormat("pt-BR", {
        timeZone: "America/Sao_Paulo",
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        hourCycle: "h23",
    }).format(new Date(data_hora));
}

function preencherDataAtual() {
    const hoje = new Date();
    const ano = hoje.getFullYear();
    const mes = String(hoje.getMonth() + 1).padStart(2, "0");
    const dia = String(hoje.getDate()).padStart(2, "0");

    return `${ano}-${mes}-${dia}`;
}

function formatarData(data) {
    if (!data) return "-";
    const [ano, mes, dia] = data.split("-");
    return `${dia}/${mes}/${ano}`;
}

function permitirApenasNumeros(event) {
    return event.target.value.replace(/\D/g, "");
}

function formatarCampoCpf(e) {
    let valor = permitirApenasNumeros(e);

    if (valor.length > 9) {
        valor = valor.replace(/^(\d{3})(\d{3})(\d{3})(\d{0,2})/, "$1.$2.$3-$4");
    } else if (valor.length > 6) {
        valor = valor.replace(/^(\d{3})(\d{3})(\d{0,3})/, "$1.$2.$3");
    } else if (valor.length > 3) {
        valor = valor.replace(/^(\d{3})(\d{0,3})/, "$1.$2");
    }

    return valor;
}

function formatarCampoTelefone(e) {
    let valor = permitirApenasNumeros(e);

    if (valor.length > 7) {
        valor = valor.replace(/^(\d{2})(\d{5})(\d{0,4})/, "($1) $2-$3");
    } else if (valor.length > 2) {
        valor = valor.replace(/^(\d{2})(\d{0,5})/, "($1) $2");
    }

    return valor;
}

function formatarCampoCep(e) {
    let valor = permitirApenasNumeros(e);

    if (valor.length > 5) {
        valor = valor.replace(/^(\d{5})(\d{0,3})/, "$1-$2");
    }

    return valor;
}

/* =========================================================
   CONFIRMAÇÃO
========================================================= */

function pedirConfirmacao(mensagem) {
    return new Promise((resolve) => {
        document.getElementById("descriptionModal").textContent = mensagem;
        const modalConfirmacao = document.getElementById("confirmacaoModal");
        modalConfirmacao.showModal();

        document.getElementById("btnNegar").onclick = () => {
            modalConfirmacao.close();
            resolve(false);
        };

        document.getElementById("btnConfirmar").onclick = () => {
            modalConfirmacao.close();
            resolve(true);
        };
    });
}

/* =========================================================
   ENDEREÇO
========================================================= */

async function buscarEnderecoPorCEP(cep) {
    cep = cep.replace(/\D/g, "");

    if (cep.length !== 8) {
        return null;
    }

    const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);

    if (!response.ok) {
        throw new Error("Não foi possível consultar o CEP.");
    }

    const dados = await response.json();

    if (dados.erro) {
        return null;
    }

    return dados;
}

async function preencherEnderecoAutomaticamente(cepDigitado, campos) {
    try {
        campos.rua.placeholder = "Buscando endereço...";
        const dadosEndereco = await buscarEnderecoPorCEP(cepDigitado);

        if (dadosEndereco) {
            campos.rua.value = dadosEndereco.logradouro;
            campos.bairro.value = dadosEndereco.bairro;
            campos.cidade.value = dadosEndereco.localidade;
            campos.uf.value = dadosEndereco.uf;
            campos.numero.focus();
        } else {
            campos.rua.value = "";
            campos.bairro.value = "";
            campos.cidade.value = "";
            campos.uf.value = "";
        }
    } catch (erro) {
        console.error(erro);
    } finally {
        campos.rua.placeholder = "Nome da rua";
    }
}

/* =========================================================
   NOTIFICAÇÃO
========================================================= */

function obterContainerNotificacao() {
    const container = document.getElementById("notificacoes");

    if (!container) {
        return null;
    }

    const modais = document.querySelectorAll("dialog[open]");
    const modalAberto = modais[modais.length - 1];

    if (modalAberto) {
        modalAberto.appendChild(container);
    } else {
        document.body.appendChild(container);
    }

    return container;
}

function exibirNotificacao(mensagem, tipo = "info", duracao = 4000) {
    const container = obterContainerNotificacao();

    if (!container) {
        console.error("Container de notificações não encontrado.");
        return;
    }

    let lista = container.querySelector(".lista-notificacoes");

    if (!lista) {
        lista = document.createElement("div");
        lista.className = "lista-notificacoes";
        container.appendChild(lista);
    }

    const tipos = {
        sucesso: {
            icone: "fa-circle-check",
        },
        erro: {
            icone: "fa-circle-xmark",
        },
        aviso: {
            icone: "fa-triangle-exclamation",
        },
        info: {
            icone: "fa-circle-info",
        },
    };

    const configuracao = tipos[tipo] || tipos.info;
    const tipoFinal = tipos[tipo] ? tipo : "info";

    const notificacao = document.createElement("div");
    notificacao.className = `notificacao ${tipoFinal}`;

    const icone = document.createElement("i");
    icone.className = `notificacao-icone fa-solid ${configuracao.icone}`;
    icone.setAttribute("aria-hidden", "true");

    const texto = document.createElement("span");
    texto.className = "notificacao-mensagem";
    texto.textContent = mensagem;

    const botaoFechar = document.createElement("button");
    botaoFechar.type = "button";
    botaoFechar.className = "notificacao-fechar";
    botaoFechar.setAttribute("aria-label", "Fechar notificação");

    const iconeFechar = document.createElement("i");
    iconeFechar.className = "fa-solid fa-xmark";

    botaoFechar.appendChild(iconeFechar);

    notificacao.append(icone, texto, botaoFechar);

    lista.appendChild(notificacao);

    // Coloca o container na top layer
    if (!container.matches(":popover-open")) {
        container.showPopover();
    }

    let temporizador;

    function removerNotificacao() {
        if (!notificacao.isConnected) {
            return;
        }

        clearTimeout(temporizador);

        notificacao.classList.add("saindo");

        notificacao.addEventListener(
            "animationend",
            () => {
                notificacao.remove();

                if (lista.children.length === 0) {
                    container.hidePopover();
                }
            },
            { once: true },
        );
    }

    botaoFechar.addEventListener("click", removerNotificacao);

    if (duracao > 0) {
        temporizador = setTimeout(removerNotificacao, duracao);
    }
}

function exibirNotificacaoComReload(mensagem, tipo) {
    sessionStorage.setItem(
        "notificacao",
        JSON.stringify({
            mensagem: mensagem,
            tipo: tipo,
        }),
    );

    window.location.reload();
}

document.addEventListener("DOMContentLoaded", () => {
    const notificacao = sessionStorage.getItem("notificacao");

    if (!notificacao) return;

    const dados = JSON.parse(notificacao);
    sessionStorage.removeItem("notificacao");
    exibirNotificacao(dados.mensagem, dados.tipo);
});

const opcaoTiposServico = {
        CURSO: "curso",
        ATIVIDADE: "atividade",
        EVENTO: "evento",
    };